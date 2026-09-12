from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.prediction_routes import router as prediction_router


app = FastAPI(
    title="Smart Expense & Financial Risk Analyzer",
    description="API for analyzing personal financial risk",
    version="1.0.0"
)


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "message": "Smart Expense & Financial Risk Analyzer API"
    }


@app.get("/health")
def health():
    return {
        "status": "API is working"
    }


app.include_router(prediction_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)