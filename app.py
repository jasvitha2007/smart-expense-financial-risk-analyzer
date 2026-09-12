
import streamlit as st
import pandas as pd
import sys
import os

# ==========================================
# PROJECT PATH
# ==========================================

sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)

# ==========================================
# IMPORT PROJECT MODULES
# ==========================================

from src.data_processing import load_data
from src.financial_analysis import analyze_finances
from src.anomaly_detection import detect_anomalies
from src.prediction import predict_expenses
from src.financial_health import calculate_financial_health

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Smart Expense & Financial Risk Analyzer",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# HEADER
# ==========================================

st.title("📊 Smart Expense & Financial Risk Analyzer")

st.write(
    "AI-powered personal finance analysis and risk prediction"
)

# ==========================================
# SESSION STATE
# ==========================================

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# ==========================================
# RESET DASHBOARD
# ==========================================

if st.button("🔄 Reset Dashboard"):

    st.session_state.analysis_done = False

    keys_to_remove = [
        "df",
        "total_income",
        "total_expenses",
        "total_savings",
        "savings_rate",
        "anomalies",
        "anomaly_rate",
        "health",
        "best_model",
        "next_month_expense",
        "model_comparison",
        "test_results"
    ]

    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]

    st.rerun()

# ==========================================
# CSV UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "📁 Upload your Personal Finance CSV",
    type=["csv"]
)

# ==========================================
# ANALYZE CSV
# ==========================================

if uploaded_file is not None:

    if st.button(
        "🔍 Analyze CSV",
        type="primary"
    ):

        try:

            # ----------------------------------
            # SAVE UPLOADED FILE
            # ----------------------------------

            temp_path = "uploaded_finance.csv"

            with open(temp_path, "wb") as f:
                f.write(
                    uploaded_file.getbuffer()
                )

            # ----------------------------------
            # LOAD DATA
            # ----------------------------------

            df = load_data(temp_path)

            # ----------------------------------
            # FINANCIAL ANALYSIS
            # ----------------------------------

            financial_summary = analyze_finances(df)

            total_income = (
                financial_summary["total_income"]
            )

            total_expenses = (
                financial_summary["total_expense"]
            )

            total_savings = (
                total_income - total_expenses
            )

            # ----------------------------------
            # SAVINGS RATE
            # ----------------------------------

            if total_income != 0:

                savings_rate = (
                    total_savings /
                    total_income
                ) * 100

            else:

                savings_rate = 0

            # ----------------------------------
            # ANOMALY DETECTION
            # ----------------------------------

            all_data, anomalies = detect_anomalies(
                df
            )

            if len(df) != 0:

                anomaly_rate = (
                    len(anomalies) /
                    len(df)
                ) * 100

            else:

                anomaly_rate = 0

            # ----------------------------------
            # ML PREDICTION
            # ----------------------------------

            (
                test_results,
                model_comparison_data,
                best_model,
                next_month_expense
            ) = predict_expenses(
                financial_summary["expense_df"]
            )

            # ----------------------------------
            # FINANCIAL HEALTH
            # ----------------------------------

            health = calculate_financial_health(
                total_income,
                total_expenses,
                savings_rate,
                anomaly_rate
            )

            # ----------------------------------
            # STORE RESULTS
            # ----------------------------------

            st.session_state.analysis_done = True

            st.session_state.df = df

            st.session_state.total_income = (
                total_income
            )

            st.session_state.total_expenses = (
                total_expenses
            )

            st.session_state.total_savings = (
                total_savings
            )

            st.session_state.savings_rate = (
                savings_rate
            )

            st.session_state.anomalies = (
                anomalies
            )

            st.session_state.anomaly_rate = (
                anomaly_rate
            )

            st.session_state.health = health

            st.session_state.best_model = (
                best_model
            )

            st.session_state.next_month_expense = (
                next_month_expense
            )

            st.session_state.model_comparison = (
                model_comparison_data
            )

            st.session_state.test_results = (
                test_results
            )

            st.success(
                "✅ Financial analysis completed successfully!"
            )

        except Exception as e:

            st.error(
                f"❌ Error while processing the file: {e}"
            )

# ==========================================
# DASHBOARD
# ==========================================

if st.session_state.analysis_done:

    df = st.session_state.df

    total_income = (
        st.session_state.total_income
    )

    total_expenses = (
        st.session_state.total_expenses
    )

    total_savings = (
        st.session_state.total_savings
    )

    savings_rate = (
        st.session_state.savings_rate
    )

    anomalies = (
        st.session_state.anomalies
    )

    anomaly_rate = (
        st.session_state.anomaly_rate
    )

    health = (
        st.session_state.health
    )

    best_model = (
        st.session_state.best_model
    )

    next_month_expense = (
        st.session_state.next_month_expense
    )

    model_comparison_data = (
        st.session_state.model_comparison
    )

    # ==========================================
    # FINANCIAL SUMMARY
    # ==========================================

    st.header("💰 Financial Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💵 Total Income",
        f"₹{total_income:,.2f}"
    )

    col2.metric(
        "💸 Total Expenses",
        f"₹{total_expenses:,.2f}"
    )

    col3.metric(
        "💰 Total Savings",
        f"₹{total_savings:,.2f}"
    )

    # ==========================================
    # FINANCIAL HEALTH
    # ==========================================

    st.header("❤️ Financial Health")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Health Score",
        f"{health['financial_health_score']}/100"
    )

    col2.metric(
        "Risk Level",
        health["risk_level"]
    )

    col3.metric(
        "Expense Ratio",
        f"{health['expense_ratio']:.2f}%"
    )

    col4.metric(
        "Savings Rate",
        f"{savings_rate:.2f}%"
    )

    # ==========================================
    # SPENDING BY CATEGORY
    # ==========================================

    st.header("🛒 Spending by Category")

    category_expenses = (
        df[
            df["Type"].str.lower() == "expense"
        ]
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        category_expenses
    )

    if len(category_expenses) > 0:

        top_category = (
            category_expenses.index[0]
        )

        top_amount = (
            category_expenses.iloc[0]
        )

        st.warning(
            f"⚠️ Highest spending category: "
            f"{top_category} — "
            f"₹{top_amount:,.2f}"
        )

    # ==========================================
    # MONTHLY SPENDING TREND
    # ==========================================

    st.header("📈 Monthly Spending Trend")

    expense_df = df[
        df["Type"].str.lower() == "expense"
    ].copy()

    expense_df["Date"] = pd.to_datetime(
        expense_df["Date"]
    )

    monthly_expenses = (
        expense_df
        .groupby(
            expense_df["Date"].dt.to_period("M")
        )["Amount"]
        .sum()
        .reset_index()
    )

    monthly_expenses["Date"] = (
        monthly_expenses["Date"]
        .astype(str)
    )

    monthly_expenses = (
        monthly_expenses
        .rename(
            columns={
                "Date": "Month",
                "Amount": "Monthly Expense"
            }
        )
    )

    monthly_expenses = (
        monthly_expenses
        .set_index("Month")
    )

    st.line_chart(
        monthly_expenses["Monthly Expense"]
    )

    # ==========================================
    # NEXT MONTH EXPENSE PREDICTION
    # ==========================================

    st.header(
        "🔮 Next Month Expense Prediction"
    )

    st.metric(
        "Estimated Expense",
        f"₹{next_month_expense:,.2f}"
    )

    st.write(
        "📊 Estimated expense for the next month "
        "based on historical spending patterns."
    )

    st.write(
        f"Best performing model: "
        f"**{best_model}**"
    )

    # ==========================================
    # UNUSUAL TRANSACTIONS
    # ==========================================

    st.header("⚠️ Unusual Transactions")

    st.write(
        f"Detected **{len(anomalies)}** "
        f"unusual transactions."
    )

    if len(anomalies) > 0:

        st.dataframe(
            anomalies,
            use_container_width=True,
            height=400
        )

    # ==========================================
    # SMART RECOMMENDATIONS
    # ==========================================

    st.header("💡 Smart Recommendations")

    for recommendation in (
        health["recommendations"]
    ):

        st.write(
            f"• {recommendation}"
        )

    # ==========================================
    # ML MODEL COMPARISON
    # ==========================================

    st.header("🤖 ML Model Comparison")

    model_df = (
        model_comparison_data.copy()
    )

    st.dataframe(
        model_df,
        use_container_width=True
    )

    st.success(
        f"🏆 Best Model: {best_model}"
    )

    # ==========================================
    # DOWNLOAD REPORT
    # ==========================================

    st.header("📥 Download Report")

    report = f"""
SMART EXPENSE & FINANCIAL RISK ANALYZER
========================================

FINANCIAL SUMMARY
-----------------
Total Income: ₹{total_income:,.2f}
Total Expenses: ₹{total_expenses:,.2f}
Total Savings: ₹{total_savings:,.2f}

FINANCIAL HEALTH
----------------
Health Score: {health['financial_health_score']}/100
Risk Level: {health['risk_level']}
Expense Ratio: {health['expense_ratio']:.2f}%
Savings Rate: {savings_rate:.2f}%
Anomaly Rate: {anomaly_rate:.2f}%

SPENDING ANALYSIS
-----------------
Highest Spending Category: {top_category}
Highest Category Amount: ₹{top_amount:,.2f}

PREDICTION
----------
Next Month Expense Prediction: ₹{next_month_expense:,.2f}
Best Performing Model: {best_model}

ANOMALY DETECTION
-----------------
Unusual Transactions Detected: {len(anomalies)}

RECOMMENDATIONS
---------------
"""

    for recommendation in (
        health["recommendations"]
    ):

        report += (
            f"- {recommendation}\n"
        )

    report += """

ML MODEL COMPARISON
-------------------
"""

    report += (
        model_df.to_string(
            index=False
        )
    )

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="financial_analysis_report.txt",
        mime="text/plain"
    )

    # ==========================================
    # FOOTER
    # ==========================================

    st.divider()

    st.caption(
        "Smart Expense & Financial Risk Analyzer | "
        "AI/ML Financial Analysis Project"
    )
