import sys
import os
import time

# Get the main project folder
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# Add project folder to Python path
sys.path.append(PROJECT_ROOT)

# Import Member 1's ML functions
from src.data_processing import load_data
from src.financial_analysis import analyze_finances
from src.anomaly_detection import detect_anomalies
from src.prediction import predict_expenses
from src.financial_health import calculate_financial_health


def analyze_csv(file_path):

    # Start timer
    start_time = time.time()

    # --------------------------------
    # 1. LOAD AND CLEAN DATA
    # --------------------------------

    df = load_data(file_path)


    # --------------------------------
    # 2. FINANCIAL ANALYSIS
    # --------------------------------

    financial_data = analyze_finances(df)


    # --------------------------------
    # 3. GET EXPENSE TRANSACTIONS
    # --------------------------------

    expense_df = df[
        df["Type"].str.lower() == "expense"
    ].copy()


    # --------------------------------
    # 4. ANOMALY DETECTION
    # --------------------------------

    expense_df, anomalies = detect_anomalies(
        expense_df
    )


    # --------------------------------
    # 5. EXPENSE PREDICTION
    # --------------------------------

    (
        test_results,
        model_comparison,
        best_model_name,
        next_month_prediction
    ) = predict_expenses(
        expense_df
    )


    # --------------------------------
    # 6. ANOMALY RATE
    # --------------------------------

    total_expenses = len(expense_df)

    if total_expenses > 0:

        anomaly_rate = (
            len(anomalies)
            / total_expenses
        ) * 100

    else:

        anomaly_rate = 0


    # --------------------------------
    # 7. FINANCIAL HEALTH
    # --------------------------------

    health_data = calculate_financial_health(

        financial_data["total_income"],

        financial_data["total_expense"],

        financial_data["savings_rate"],

        anomaly_rate

    )


    # --------------------------------
    # 8. CATEGORY EXPENSES
    # --------------------------------

    category_expenses = {

        str(category): float(amount)

        for category, amount
        in financial_data[
            "category_expenses"
        ].items()

    }


    # --------------------------------
    # 9. MONTHLY EXPENSE TREND
    # --------------------------------

    monthly_expenses = (

        expense_df

        .groupby(
            [
                "Year",
                "Month",
                "Month_Name"
            ]
        )["Amount"]

        .sum()

        .reset_index()

        .sort_values(
            [
                "Year",
                "Month"
            ]
        )

    )


    monthly_expenses_data = [

        {
            "month":
                f"{row['Month_Name']} "
                f"{int(row['Year'])}",

            "amount":
                float(row["Amount"])

        }

        for _, row
        in monthly_expenses.iterrows()

    ]


    # --------------------------------
    # 10. ANOMALY TRANSACTIONS
    # --------------------------------

    anomalies_data = anomalies[
        [
            "Date",
            "Transaction Description",
            "Category",
            "Amount"
        ]
    ].copy()


    anomalies_data["Date"] = (

        anomalies_data["Date"]

        .dt.strftime("%Y-%m-%d")

    )


    anomalies_data = (

        anomalies_data

        .to_dict(
            orient="records"
        )

    )


    # --------------------------------
    # 11. MODEL COMPARISON
    # --------------------------------

    model_results = (

        model_comparison

        .replace({
            float("nan"): None
        })

        .to_dict(
            orient="records"
        )

    )


    # --------------------------------
    # 12. PRINT PROCESSING TIME
    # --------------------------------

    processing_time = (
        time.time() - start_time
    )

    print(
        f"Analysis completed in "
        f"{processing_time:.2f} seconds"
    )


    # --------------------------------
    # 13. SEND RESULT TO FRONTEND
    # --------------------------------

    return {

        "financial_summary": {

            "total_income":
                float(
                    financial_data[
                        "total_income"
                    ]
                ),

            "total_expense":
                float(
                    financial_data[
                        "total_expense"
                    ]
                ),

            "total_savings":
                float(
                    financial_data[
                        "total_savings"
                    ]
                ),

            "expense_ratio":
                float(
                    financial_data[
                        "expense_ratio"
                    ]
                ),

            "savings_rate":
                float(
                    financial_data[
                        "savings_rate"
                    ]
                )

        },


        "category_expenses":
            category_expenses,


        "monthly_expenses":
            monthly_expenses_data,


        "anomalies":
            anomalies_data,


        "prediction": {

            "next_month_expense":
                float(
                    next_month_prediction
                ),

            "best_model":
                best_model_name,

            "model_comparison":
                model_results

        },


        "financial_health":
            health_data

    }