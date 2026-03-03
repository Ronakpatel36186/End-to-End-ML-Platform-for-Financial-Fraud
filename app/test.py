import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import mlflow.sklearn
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# 🚀 THIS LINE FIXES YOUR ISSUE
mlflow.set_registry_uri(MLFLOW_TRACKING_URI)

MODEL_NAME = "XGBoost"
MODEL_VERSION = "latest"
model_uri = f"models:/{MODEL_NAME}/{MODEL_VERSION}"

app = FastAPI(title="Credit Risk Prediction API")

class CreditData(BaseModel):
    features: Dict[str, float]

# Load the model once on startup
try:
    print("Loading MLflow model...")
    model = mlflow.sklearn.load_model(model_uri)
    print("Model loaded successfully!")
except Exception as e:
    print(f"[ERROR] Could not load model at startup: {e}")
    model = None  # App will still start

@app.get("/")
def read_root():
    return {"message": "Welcome to the Credit Risk Prediction API!"}

@app.post("/predict")
def predict_credit_risk(data: CreditData):
    global model
    if model is None:
        try:
            model = mlflow.sklearn.load_model(model_uri)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model not available: {e}")
    
    input_data = pd.DataFrame([data.features])
    
    # Match feature columns
    try:
        input_data = input_data[model.feature_names_in_]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid features: {e}")
    
    prediction = model.predict(input_data)
    
    return {
        "credit_risk_prediction": int(prediction[0]),
        "risk_label": "High Risk" if prediction[0] == 1 else "Low Risk"
    }
