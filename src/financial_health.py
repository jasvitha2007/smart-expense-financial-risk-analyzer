def calculate_financial_health(
    total_income,
    total_expense,
    savings_rate,
    anomaly_rate
):

    # --------------------------------
    # 1. Expense-to-Income Ratio
    # --------------------------------
    if total_income > 0:
        expense_ratio = (
            total_expense / total_income
        ) * 100
    else:
        expense_ratio = 100

    # --------------------------------
    # 2. Savings Score
    # Maximum = 40
    # --------------------------------
    if savings_rate >= 30:
        savings_score = 40
    elif savings_rate >= 20:
        savings_score = 30
    elif savings_rate >= 10:
        savings_score = 20
    elif savings_rate > 0:
        savings_score = 10
    else:
        savings_score = 0

    # --------------------------------
    # 3. Expense Score
    # Maximum = 40
    # --------------------------------
    if expense_ratio <= 50:
        expense_score = 40
    elif expense_ratio <= 70:
        expense_score = 30
    elif expense_ratio <= 90:
        expense_score = 20
    elif expense_ratio <= 100:
        expense_score = 10
    else:
        expense_score = 0

    # --------------------------------
    # 4. Anomaly Score
    # Maximum = 20
    # --------------------------------
    if anomaly_rate <= 2:
        anomaly_score = 20
    elif anomaly_rate <= 5:
        anomaly_score = 15
    elif anomaly_rate <= 10:
        anomaly_score = 10
    elif anomaly_rate <= 20:
        anomaly_score = 5
    else:
        anomaly_score = 0

    # --------------------------------
    # 5. Financial Health Score
    # --------------------------------
    financial_health_score = (
        savings_score
        + expense_score
        + anomaly_score
    )

    # --------------------------------
    # 6. Health Status
    # --------------------------------
    if financial_health_score >= 80:
        health_status = "Excellent"
    elif financial_health_score >= 60:
        health_status = "Good"
    elif financial_health_score >= 40:
        health_status = "Moderate"
    else:
        health_status = "High Risk"

    # --------------------------------
    # 7. Risk Level
    # --------------------------------
    if expense_ratio > 100:
        risk_level = "High Risk"
    elif expense_ratio > 80:
        risk_level = "Moderate Risk"
    elif savings_rate < 10:
        risk_level = "Moderate Risk"
    else:
        risk_level = "Low Risk"

    # --------------------------------
    # 8. Recommendations
    # --------------------------------
    recommendations = []

    if savings_rate < 10:
        recommendations.append(
            "Increase savings by reducing unnecessary expenses."
        )

    if expense_ratio > 100:
        recommendations.append(
            "Expenses are higher than income. Focus on reducing major expenses."
        )

    if anomaly_rate > 5:
        recommendations.append(
            "Review unusual transactions detected by the anomaly detection model."
        )

    if not recommendations:
        recommendations.append(
            "Maintain your current spending and saving habits."
        )

    # --------------------------------
    # 9. Return Results
    # --------------------------------
    return {
        "expense_ratio": expense_ratio,
        "savings_rate": savings_rate,
        "anomaly_rate": anomaly_rate,
        "savings_score": savings_score,
        "expense_score": expense_score,
        "anomaly_score": anomaly_score,
        "financial_health_score": financial_health_score,
        "health_status": health_status,
        "risk_level": risk_level,
        "recommendations": recommendations
    }