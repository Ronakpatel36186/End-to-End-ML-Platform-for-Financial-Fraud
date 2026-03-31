# app/main.py
import os
import uvicorn
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from .model_loader import get_model
import warnings

os.environ["XGBOOST_VERBOSITY"] = "0"
warnings.filterwarnings("ignore", category=UserWarning)

app = FastAPI(title="End-to-End ML Platform for Financial Fraud Detection")

class CreditData(BaseModel):
    features: Dict[str, float]

@app.get("/")
def root():
    return {"message": "Welcome to the Credit Risk Prediction API!"}

@app.post("/predict")
def predict(data: CreditData):
    try:
        # Lazy-load the model on first request
        model, features = get_model()

        # Convert input features to array
        input_data = np.array([data.features[f] for f in features]).reshape(1, -1)
        prediction = model.predict(input_data)

        return {
            "prediction": int(prediction[0]),
            "risk": "High Risk" if prediction[0] == 1 else "Low Risk"
        }

    except KeyError as e:
        return {"error": f"Missing feature: {e}"}

# Use PORT from env if set; default 8000
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False") == "True"

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, workers=1)