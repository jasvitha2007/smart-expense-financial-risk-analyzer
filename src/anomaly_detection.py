from sklearn.ensemble import IsolationForest


def detect_anomalies(expense_df):

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    expense_df = expense_df.copy()

    expense_df["Anomaly"] = model.fit_predict(
        expense_df[["Amount"]]
    )

    anomalies = expense_df[
        expense_df["Anomaly"] == -1
    ].copy()

    return expense_df, anomalies