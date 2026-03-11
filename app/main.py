import os
import uvicorn
os.environ["XGBOOST_VERBOSITY"] = "0"
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import mlflow
import mlflow.sklearn
from dotenv import load_dotenv
from typing import Dict
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="xgboost")

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# 🚀 THIS LINE FIXES YOUR ISSUE
mlflow.set_registry_uri(MLFLOW_TRACKING_URI)

MODEL_NAME = "XGBoost"
MODEL_VERSION = "latest"
MODEL_URI = f"models:/{MODEL_NAME}/{MODEL_VERSION}"

model = mlflow.sklearn.load_model(MODEL_URI)

# Get feature names (important!)
features = model.feature_names_in_.tolist()

app = FastAPI(title="End-to-End ML Platform for Financial Fraud Detection")

class CreditData(BaseModel):
    features: Dict[str, float]

@app.get("/")
def root():
    return {"Welcome to the Credit Risk Prediction API!"}

@app.post("/predict")
def predict(data: CreditData):
    """ TITLE: Predict credit risk based on input features.
        Input: Expected input feature_names = [
             "V1",-,"V28","Amount"]
        Example: "features": {
                "V1": -2.303349568,
                "V2": 1.75924746,
                "V3": -0.359744743,
                 .
                 .
                 .
                 "V26": -0.542627889,
                "V27": 0.039565989,
                "V28": -0.153028797,
                "Amount": 239.93
            }
        }
   """
    try:
        input_data = np.array(
            [data.features[f] for f in features]
        ).reshape(1, -1)

        prediction = model.predict(input_data)

        return {
            "prediction": int(prediction[0]),
            "risk": "High Risk" if prediction[0] == 1 else "Low Risk"
        }

    except KeyError as e:
        return {"error": f"Missing feature: {e}"}
    
print("features:", features)

PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False") == "True"

if __name__ == "__main__":
   uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=False)
