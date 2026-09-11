import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def predict_expenses(expense_df):

    # --------------------------------
    # 1. Monthly expense aggregation
    # --------------------------------
    monthly_expense = (
        expense_df.groupby(["Year", "Month"])["Amount"]
        .sum()
        .reset_index()
    )

    monthly_expense = monthly_expense.sort_values(
        ["Year", "Month"]
    ).reset_index(drop=True)

    # --------------------------------
    # 2. Create features
    # --------------------------------
    monthly_expense["Time_Index"] = range(
        len(monthly_expense)
    )

    monthly_expense["Previous_Expense"] = (
        monthly_expense["Amount"].shift(1)
    )

    monthly_expense["Rolling_Average"] = (
        monthly_expense["Amount"]
        .shift(1)
        .rolling(window=2)
        .mean()
    )

    # Remove unavailable previous-month values
    model_data = monthly_expense.dropna().copy()

    # --------------------------------
    # 3. Features and target
    # --------------------------------
    features = [
        "Time_Index",
        "Previous_Expense",
        "Rolling_Average"
    ]

    X = model_data[features]
    y = model_data["Amount"]

    # --------------------------------
    # 4. Chronological train/test split
    # --------------------------------
    split_index = int(len(model_data) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    # --------------------------------
    # 5. Define models
    # --------------------------------
    models = {
        "Linear Regression": LinearRegression(),

        "Random Forest": RandomForestRegressor(
            n_estimators=200,
            random_state=42
        ),

        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=2,
            random_state=42
        )
    }

    results = []

    best_model = None
    best_model_name = None
    best_mae = float("inf")

    # --------------------------------
    # 6. Train and evaluate models
    # --------------------------------
    for name, model in models.items():

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                predictions
            )
        )

        if len(y_test) >= 2:
            r2 = r2_score(
                y_test,
                predictions
            )
        else:
            r2 = np.nan

        results.append({
            "Model": name,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        })

        # Select model with lowest MAE
        if mae < best_mae:
            best_mae = mae
            best_model = model
            best_model_name = name

    # --------------------------------
    # 7. Model comparison table
    # --------------------------------
    model_comparison = pd.DataFrame(results)

    # --------------------------------
    # 8. Get best model predictions
    # --------------------------------
    best_predictions = best_model.predict(X_test)

    test_results = model_data.iloc[
        split_index:
    ].copy()

    test_results["Predicted_Expense"] = (
        best_predictions
    )

    # --------------------------------
    # 9. Final model using all data
    # --------------------------------
    final_model = models[best_model_name]

    final_model.fit(X, y)

    # --------------------------------
    # 10. Next month prediction
    # --------------------------------
    last_expense = monthly_expense[
        "Amount"
    ].iloc[-1]

    previous_two_expenses = monthly_expense[
        "Amount"
    ].iloc[-2:]

    rolling_average = (
        previous_two_expenses.mean()
    )

    next_month_index = len(
        monthly_expense
    )

    next_month_features = pd.DataFrame({
        "Time_Index": [next_month_index],
        "Previous_Expense": [last_expense],
        "Rolling_Average": [rolling_average]
    })

    next_month_prediction = final_model.predict(
        next_month_features
    )[0]

    # --------------------------------
    # 11. Return results
    # --------------------------------
    return (
        test_results,
        model_comparison,
        best_model_name,
        next_month_prediction
    )