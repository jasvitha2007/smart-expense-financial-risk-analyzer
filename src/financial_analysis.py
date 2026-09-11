def analyze_finances(df):

    income_df = df[
        df["Type"].str.lower() == "income"
    ].copy()

    expense_df = df[
        df["Type"].str.lower() == "expense"
    ].copy()

    total_income = income_df["Amount"].sum()
    total_expense = expense_df["Amount"].sum()
    total_savings = total_income - total_expense

    if total_income > 0:
        expense_ratio = (
            total_expense / total_income
        ) * 100

        savings_rate = (
            total_savings / total_income
        ) * 100
    else:
        expense_ratio = 100
        savings_rate = 0

    category_expenses = (
        expense_df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "income_df": income_df,
        "expense_df": expense_df,
        "total_income": total_income,
        "total_expense": total_expense,
        "total_savings": total_savings,
        "expense_ratio": expense_ratio,
        "savings_rate": savings_rate,
        "category_expenses": category_expenses
    }