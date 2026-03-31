# model_loader.py
import os
import mlflow
import mlflow.sklearn
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="xgboost")

load_dotenv()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_registry_uri(MLFLOW_TRACKING_URI)

MODEL_NAME = "XGBoost"
MODEL_VERSION = "latest"
MODEL_URI = f"models:/{MODEL_NAME}/{MODEL_VERSION}"

model = None
features = None

def get_model():
    """ Lazy-load the model from MLflow/DagsHub """
    global model, features
    if model is None:
        print("Loading model from DagsHub MLflow...")
        model = mlflow.sklearn.load_model(MODEL_URI)
        features = model.feature_names_in_.tolist()
        print("Model loaded successfully!")
    return model, features