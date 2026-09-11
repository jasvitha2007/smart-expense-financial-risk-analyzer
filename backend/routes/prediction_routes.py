import os
import tempfile

from fastapi import APIRouter, UploadFile, File

from services.prediction_service import analyze_csv


router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Create temporary file OUTSIDE the project folder
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".csv"
    )

    try:

        # Save uploaded CSV
        contents = await file.read()

        temp_file.write(contents)
        temp_file.close()

        # Run ML analysis
        result = analyze_csv(
            temp_file.name
        )

        return result

    finally:

        # Delete temporary CSV
        if os.path.exists(
            temp_file.name
        ):
            os.remove(
                temp_file.name
            )