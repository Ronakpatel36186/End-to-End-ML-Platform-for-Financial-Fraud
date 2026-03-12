# End-to-End ML Platform for Financial Fraud Detection
# Overview

This project is a production-style machine learning system for detecting fraudulent financial transactions. The goal was to simulate a real-world ML workflow — from training a model, tracking experiments, to serving predictions via an API, all in a reproducible, containerized environment.

The project demonstrates how a machine learning model can be developed, tracked, containerized, and deployed using industry-grade tools and practices

## Dataset
The model is trained on historical financial transaction data containing numerical features and anonymized variables.  

- Public dataset reference: [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- Data type: Numerical, anonymized features, and transaction amount/time.

## Model Input Features
- Transaction Amount  
- Transaction Time  
- Anonymized numerical features (V1–V28)

## What This Project Does

- Trains a fraud detection model on historical transaction data.
- Tracks experiments and model versions using **MLflow** integrated with **DagsHub**.
- Loads the **registered model directly from DagsHub** for inference.
- Serves the model through a **FastAPI REST API** for real-time predictions.
- Ensures reproducibility and environment consistency using **Docker**.
- Organized in a modular, **production-ready architecture**.

## Key Features

- End-to-end ML pipeline for fraud detection.
- Experiment tracking & model versioning with **MLflow + DagsHub**.
- Real-time predictions via **FastAPI API**.
- **Dockerized** environment for easy deployment.
- Modular project structure reflecting **production workflows**.

## Technology Stack

- Python – core language
- Pandas & NumPy – data handling & numerical computations
- Scikit-learn, XGBoost, LightGBM – machine learning models
- MLflow & DagsHub – experiment tracking & model versioning
- FastAPI – serving real-time predictions
- Docker – reproducible, containerized environment

## ML Pipeline Overview


![ML Pipeline Diagram](images/ml_pipeline.png)
<img src="images/ml_pipeline.png" alt="ML Pipeline Diagram" width="800"/>

Step-by-step:

1. Transaction data is sent to the API endpoint
2. FastAPI formats and processes the input
3. The trained model is loaded from DagsHub’s registered models
4. Model generates predictions
5. Results are returned as structured JSON
6. All experiments and metrics are tracked in MLflow

## Author

Ronak Miteshkumar Patel – Master’s in Computer Science, Lakehead University

Interested in Machine Learning Engineering, Data Science, and production ML systems