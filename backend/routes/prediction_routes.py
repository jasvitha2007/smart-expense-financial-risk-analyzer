from fastapi import APIRouter
from pydantic import BaseModel

from services.prediction_service import calculate_risk


router = APIRouter()


class FinancialData(BaseModel):
    income: float
    expenses: float
    savings: float
    debt: float


@router.post("/predict")
def predict(data: FinancialData):

    result = calculate_risk(
        data.income,
        data.expenses,
        data.savings,
        data.debt
    )

    return result