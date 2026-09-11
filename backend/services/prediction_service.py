def calculate_risk(income, expenses, savings, debt):

    if income <= 0:
        return {
            "risk": "High",
            "risk_score": 100,
            "recommendations": [
                "Please enter a valid income."
            ]
        }

    expense_ratio = expenses / income
    debt_ratio = debt / income

    score = 0
    recommendations = []


    # Check expenses
    if expense_ratio > 0.8:
        score += 50
        recommendations.append(
            "Your expenses are very high compared to your income."
        )

    elif expense_ratio > 0.5:
        score += 30
        recommendations.append(
            "Try to reduce unnecessary monthly expenses."
        )

    else:
        score += 10


    # Check debt
    if debt_ratio > 0.5:
        score += 40
        recommendations.append(
            "Your debt payment is high compared to your income."
        )

    elif debt_ratio > 0.3:
        score += 20
        recommendations.append(
            "Consider reducing your debt burden."
        )

    else:
        score += 10


    # Check savings
    if savings < income * 0.1:
        score += 10
        recommendations.append(
            "Try to increase your monthly savings."
        )


    # Decide risk level
    if score >= 70:
        risk = "High"

    elif score >= 40:
        risk = "Medium"

    else:
        risk = "Low"


    # General recommendation
    if risk == "Low":
        recommendations.append(
            "Your financial situation looks relatively healthy. Continue maintaining good saving habits."
        )

    elif risk == "Medium":
        recommendations.append(
            "Review your expenses and savings regularly to improve your financial health."
        )

    else:
        recommendations.append(
            "Create a budget and prioritize reducing expenses and debt."
        )


    return {
        "risk": risk,
        "risk_score": score,
        "recommendations": recommendations
    }