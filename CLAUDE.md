# CLAUDE.md


This file provides guidance to Claude Code when working with this repository.



# Project Overview


This repository contains an end-to-end telecom customer churn prediction system.


The project includes:


- Data validation
- Data preprocessing
- Feature engineering
- XGBoost model training
- MLflow experiment tracking
- FastAPI inference API
- Gradio web UI
- Docker containerization
- GitHub Actions CI/CD
- Docker Hub image publishing
- AWS ECS/Fargate deployment architecture


---


# Environment


Primary Docker base image:


python:3.12-slim

The local development environment may use a different Python version, but Docker is the reference environment for containerized deployment.

Commands
Training Pipeline

Run the complete ML training pipeline:

python scripts/run_pipeline.py --input data/raw/Telco-Customer-Churn.csv --target Churn

Prepare processed data:

python scripts/prepare_processed_data.py
Testing

Test data processing and feature engineering:

python scripts/test_pipeline_phase1_data_features.py

Test model training and evaluation:

python scripts/test_pipeline_phase2_modeling.py

Test FastAPI endpoints:

python scripts/test_fastapi.py
Local Development

Run FastAPI + Gradio:

python -m uvicorn src.app.main:app --host 0.0.0.0 --port 8000

Application:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs

Gradio:

http://localhost:8000/ui
Docker

Build:

docker build -t customer-churn-prediction .

Run:

docker run -p 8000:8000 customer-churn-prediction

Docker Hub image:

taiyobali/customer-churn-prediction:latest

Pull:

docker pull taiyobali/customer-churn-prediction:latest

Run:

docker run -p 8000:8000 taiyobali/customer-churn-prediction:latest
Architecture
Training Pipeline
Raw Data
   ↓
Data Validation
   ↓
Preprocessing
   ↓
Feature Engineering
   ↓
XGBoost Training
   ↓
Evaluation
   ↓
MLflow Logging

Main training entry point:

scripts/run_pipeline.py
Serving Pipeline
Customer Request
      ↓
FastAPI
      ↓
Inference
      ↓
Feature Transformation
      ↓
Trained XGBoost Model
      ↓
Prediction

FastAPI application:

src/app/main.py

Inference logic:

src/serving/inference.py
MLflow

Experiment name:

Telco Churn

Default tracking location:

./mlruns

Start MLflow:

mlflow ui --backend-store-uri file:./mlruns

MLflow tracks:

Metrics
precision
recall
f1
roc_auc
train_time
pred_time
data_quality_pass
Parameters
model type
threshold
test_size
model hyperparameters
Artifacts
trained model
feature columns
preprocessing artifacts
Feature Engineering

Training and serving MUST use the same feature transformation logic.

Training feature engineering:

src/features/build_features.py

Serving feature transformation:

src/serving/inference.py

Binary categorical features must use deterministic mappings.

Examples:

Yes / No
Male / Female

Categorical variables use one-hot encoding.

Feature alignment must be performed using the feature columns generated during training.

The model must receive features in exactly the same order used during training.

Do not change feature preprocessing independently in the serving pipeline without checking the training pipeline.

Model

Primary model:

XGBoost Classifier

Class imbalance is handled using:

scale_pos_weight

The prediction threshold defaults to:

0.35
Data Validation

Validation implementation:

src/utils/validate_data.py

Great Expectations is used to validate:

Required columns
CustomerID
Gender values
Tenure ranges
Charge ranges
Other expected data constraints

Data quality results are logged to MLflow.

API
Health Check
GET /

Expected response:

{
  "status": "ok"
}
Prediction
POST /predict

The endpoint accepts customer data using the Pydantic request model.

Prediction output:

Likely to churn

or:

Not likely to churn
Gradio

The Gradio application is mounted under:

/ui

It uses the same inference logic as the FastAPI prediction endpoint.

Do not create separate prediction logic for the UI.

The inference function in:

src/serving/inference.py

should remain the single source of truth for predictions.

Docker Configuration

Docker uses:

python:3.12-slim

The application runs on:

0.0.0.0:8000

The container exposes:

8000

Python module imports must correctly resolve the project's source code.

CI/CD

GitHub Actions is triggered by pushes to:

main

The workflow:

Checks out the repository
Logs into Docker Hub
Builds the Docker image
Pushes the image to Docker Hub

GitHub Actions secrets:

DOCKERHUB_USERNAME
DOCKERHUB_TOKEN

Docker Hub repository:

taiyobali/customer-churn-prediction
AWS Deployment

Target architecture:

Internet
   ↓
Application Load Balancer :80
   ↓
Target Group :8000
   ↓
ECS Fargate Task
   ↓
FastAPI Container

Health check:

GET /

The ECS task security group should allow port 8000 from the ALB security group.

The ALB security group should allow inbound HTTP traffic on port 80.

Important Deployment Rules

When a new Docker image is pushed:

Push the image to Docker Hub.
Update or redeploy the ECS service.
Confirm the new ECS task is running.
Confirm the ALB target becomes healthy.
Test /.
Test /predict.
Test /ui.

Pushing a new Docker image alone does not necessarily replace an already-running ECS task.

Project Structure
customer-churn-prediction/
│
├── .github/
│   └── workflows/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│
├── src/
│   ├── app/
│   ├── features/
│   ├── serving/
│   │   └── model/
│   └── utils/
│
├── artifacts/
│   ├── feature_columns.json
│   ├── feature_columns.txt
│   └── preprocessing.pkl
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── README.md
└── CLAUDE.md
Development Rules
Do Not Commit
.venv/
.env
mlruns/
data/raw/
data/processed/
*.pkl
*.joblib
Keep Serving Artifacts

The bundled serving model under:

src/serving/model/

must remain available if it is required by the Docker build or inference system.

Feature Consistency

Never change training-time preprocessing without checking the serving pipeline.

The following must remain synchronized:

Training Features
       ↕
Serving Features
       ↕
Model Feature Order
Single Source of Truth

Inference logic should remain centralized in:

src/serving/inference.py

FastAPI and Gradio should use the same inference function.

Do not duplicate model prediction logic.

Troubleshooting
ModuleNotFoundError

Check:

src/

package structure and Python import paths.

Verify that the Docker environment correctly exposes the project source code.

ALB Unhealthy

First check:

GET /

inside the container.

Then verify:

ALB :80
   ↓
Target Group :8000
   ↓
ECS :8000
Old ECS Image

Force a new ECS deployment after publishing a new image.

MLflow Model Not Found

For local development, check:

mlruns/

For Docker production, verify that the required model artifacts are packaged into the image and that the inference code uses the correct container path.

Important Principle

This repository demonstrates an end-to-end ML engineering workflow:

Data
  ↓
Validation
  ↓
Features
  ↓
Model
  ↓
MLflow
  ↓
Inference
  ↓
API / UI
  ↓
Docker
  ↓
CI/CD
  ↓
Cloud Deployment

Any change to one stage should be checked against downstream stages.