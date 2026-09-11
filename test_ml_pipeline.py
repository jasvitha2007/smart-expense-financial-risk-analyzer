from src.data_processing import load_data
from src.financial_analysis import analyze_finances
from src.anomaly_detection import detect_anomalies
from src.prediction import predict_expenses
from src.financial_health import calculate_financial_health

# 1. Load and clean dataset
file_path = "data/Personal_Finance_Dataset.csv"

df = load_data(file_path)

print("\nDataset loaded successfully!")
print("Rows:", len(df))


# 2. Financial analysis
results = analyze_finances(df)

expense_df = results["expense_df"]

print("\n===== FINANCIAL ANALYSIS =====")
print("Total Income:", round(results["total_income"], 2))
print("Total Expense:", round(results["total_expense"], 2))
print("Total Savings:", round(results["total_savings"], 2))
print("Expense Ratio:", round(results["expense_ratio"], 2), "%")
print("Savings Rate:", round(results["savings_rate"], 2), "%")


# 3. Anomaly detection
expense_df, anomalies = detect_anomalies(expense_df)

print("\n===== ANOMALY DETECTION =====")
print("Anomalies Detected:", len(anomalies))


# 4. Expense prediction
test_results, model_comparison, best_model_name, next_month_prediction = (
    predict_expenses(expense_df)
)

print("\n===== EXPENSE PREDICTION =====")

print("\nModel Comparison:")
print(model_comparison.round(2))

print("\nBest Model:", best_model_name)

print(
    "Next Month Predicted Expense:",
    round(next_month_prediction, 2)
)
# --------------------------------
# FINANCIAL HEALTH ANALYSIS
# --------------------------------

anomaly_rate = (
    len(anomalies) / len(expense_df)
) * 100

health_results = calculate_financial_health(
    total_income=results["total_income"],
    total_expense=results["total_expense"],
    savings_rate=results["savings_rate"],
    anomaly_rate=anomaly_rate
)

print("\n===== FINANCIAL HEALTH =====")

print(
    "Financial Health Score:",
    health_results["financial_health_score"],
    "/ 100"
)

print(
    "Health Status:",
    health_results["health_status"]
)

print(
    "Risk Level:",
    health_results["risk_level"]
)

print(
    "Anomaly Rate:",
    round(health_results["anomaly_rate"], 2),
    "%"
)

print("\nRecommendations:")

for recommendation in health_results["recommendations"]:
    print("-", recommendation)

print("\n================================")
print("ML PIPELINE TEST COMPLETED!")
print("================================")