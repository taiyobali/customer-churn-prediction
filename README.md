# Telco Churn – End-to-End Machine Learning Project


An end-to-end machine learning system for predicting customer churn in a telecom environment, covering data validation, feature engineering, model training, experiment tracking, API serving, web UI, containerization, CI/CD, and cloud deployment.


---


## 🎯 Project Purpose


Build and ship a production-oriented machine learning solution that predicts whether a telecom customer is likely to churn.


### Benefits


- **Faster decisions:** Identify customers likely to churn so retention teams can take action.
- **Operationalized ML:** The trained model is accessible through a REST API and Gradio web interface.
- **Repeatable delivery:** Docker and GitHub Actions provide consistent builds and delivery.
- **Traceable experiments:** MLflow tracks experiments, parameters, metrics, and model artifacts.
- **Production-oriented architecture:** The application is designed to run on AWS ECS Fargate behind an Application Load Balancer.


---


## 🏗️ What I Built


### Data & Modeling


- Data validation using Great Expectations
- Data preprocessing
- Feature engineering
- XGBoost classification
- Class-imbalance handling
- Model evaluation using:
  - Precision
  - Recall
  - F1-score
  - ROC-AUC


### Experiment Tracking


MLflow is used to track:


- Experiments
- Parameters
- Metrics
- Model artifacts
- Training information


### Inference Service


FastAPI provides:


- `GET /` — health check
- `POST /predict` — customer churn prediction


### Web UI


A Gradio interface is mounted at:


```text
/ui

This provides a simple interface for manually testing customer churn predictions.

Containerization

The application is packaged as a Docker image and served using Uvicorn on port 8000.

CI/CD

GitHub Actions:

Checks out the repository
Builds the Docker image
Logs into Docker Hub
Pushes the Docker image to Docker Hub
Cloud Deployment

The application is designed to run using:

AWS ECS Fargate
Application Load Balancer
ECS Target Group
Security Groups
CloudWatch Logs
🔄 Architecture
                    ┌─────────────────────┐
                    │   Raw Customer Data │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Data Validation   │
                    │ Great Expectations  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Preprocessing &     │
                    │ Feature Engineering │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   XGBoost Model     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       MLflow        │
                    │ Experiments / Model │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI + Gradio  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Docker        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Docker Hub      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   AWS ECS Fargate   │
                    │       + ALB         │
                    └─────────────────────┘
🚀 Deployment Flow
Developer
    │
    ▼
git push origin main
    │
    ▼
GitHub Actions
    │
    ├── Checkout repository
    ├── Build Docker image
    ├── Run checks
    └── Push image to Docker Hub
              │
              ▼
         Docker Hub
              │
              ▼
       AWS ECS Fargate
              │
              ▼
   Application Load Balancer
              │
         ┌────┴────┐
         ▼         ▼
      /predict     /ui
      
🧪 Local Development
1. Create and activate a virtual environment
Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Linux / WSL
python3 -m venv .venv
source .venv/bin/activate
2. Install dependencies
pip install -r requirements.txt
3. Run the training pipeline
python scripts/run_pipeline.py --input data/raw/Telco-Customer-Churn.csv --target Churn
4. Run FastAPI locally
python -m uvicorn src.app.main:app --host 0.0.0.0 --port 8000

Application:

http://localhost:8000

Swagger API documentation:

http://localhost:8000/docs

Gradio UI:

http://localhost:8000/ui
🐳 Docker
Build the image
docker build -t customer-churn-prediction .
Run the container
docker run -p 8000:8000 customer-churn-prediction

Then open:

http://localhost:8000

Swagger:

http://localhost:8000/docs

Gradio:

http://localhost:8000/ui
🐳 Docker Hub

The production Docker image is published as:

taiyobali/customer-churn-prediction:latest

Pull the image:

docker pull taiyobali/customer-churn-prediction:latest

Run it:

docker run -p 8000:8000 taiyobali/customer-churn-prediction:latest
📊 MLflow

The project uses file-based MLflow tracking.

Start the MLflow UI:

mlflow ui --backend-store-uri file:./mlruns

Open:

http://127.0.0.1:5000
Experiment
Telco Churn
Tracked Metrics
Precision
Recall
F1-score
ROC-AUC
Training time
Prediction time
Data quality status
Tracked Parameters
Model type
Classification threshold
Test size
Model hyperparameters
Tracked Artifacts
Trained model
Feature columns
Preprocessing artifacts
🧠 Feature Engineering

Training and inference use the same feature transformation logic.

Binary Features

Examples:

Yes / No
Male / Female

These are converted deterministically to numeric values.

Categorical Features

One-hot encoding is applied using:

pd.get_dummies()

with the same training configuration.

Feature Alignment

The serving pipeline uses the feature columns generated during training to ensure the model receives features in exactly the correct order.

This helps prevent training-serving skew.

🛡️ Data Validation

Great Expectations is used to validate the input dataset.

Validation includes checks such as:

Required columns exist
Customer ID is present
Valid gender values
Valid tenure values
Valid numerical ranges
Valid monthly charges

The data-quality result is also tracked in MLflow.

🤖 Model

The primary model is:

XGBoost Classifier

The project uses optimized hyperparameters and dynamically handles class imbalance using:

scale_pos_weight

The prediction threshold defaults to:

0.35
🔌 API
Health Check
GET /

Example response:

{
  "status": "ok"
}
Prediction
POST /predict

The endpoint accepts customer information using a Pydantic request model and returns a churn prediction.

Possible prediction results:

Likely to churn

or:

Not likely to churn
🖥️ Gradio UI

The Gradio application is mounted under:

/ui

It provides a simple interface for manually entering customer information and testing the model.

The UI uses the same inference logic as the FastAPI prediction endpoint.

☁️ AWS Architecture

The production architecture can use:

Internet
   │
   ▼
Application Load Balancer
   │
   ▼
Target Group
   │
   ▼
AWS ECS Fargate
   │
   ▼
Docker Container
   │
   ▼
FastAPI + Gradio
Networking
ALB accepts HTTP traffic on port 80
ALB forwards traffic to ECS tasks on port 8000
ECS task security group allows port 8000 from the ALB security group
ALB security group allows inbound HTTP traffic
Health Check

The ALB health check uses:

GET /
🔁 CI/CD

GitHub Actions is triggered when code is pushed to the main branch.

Pipeline:

Push to main
     │
     ▼
GitHub Actions
     │
     ├── Checkout repository
     ├── Login to Docker Hub
     ├── Build Docker image
     └── Push Docker image
Required GitHub Repository Secrets
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
🧩 Roadblocks & Solutions
1. Unhealthy ECS Targets

Problem

The application was not responding correctly to the ALB health check.

Solution

Added:

GET /

health endpoint and configured the target group health check to use / on port 8000.

2. ModuleNotFoundError: serving

Problem

Python could not find modules inside the src directory when running inside Docker.

Solution

Configured the Docker environment so the project source directory is available to Python and corrected the Uvicorn application path.

3. ALB Connection Timeout

Problem

Security group rules were not allowing traffic through the complete ALB → ECS path.

Solution

Configured:

Internet
   ↓
ALB :80
   ↓
ECS :8000

with the ECS security group allowing port 8000 from the ALB security group.

4. ECS Running an Old Image

Problem

Pushing a new Docker image did not automatically replace the currently running ECS task.

Solution

A new ECS deployment must be triggered after updating the image.

This can be done manually or through CI/CD.

5. MLflow Model Path Differences

Problem

MLflow artifact paths can differ between local development and the Docker environment.

Solution

For local development, MLflow artifacts can be loaded from the project's local tracking directory.

For containerized inference, the required serving model artifacts are packaged into the Docker image and loaded from the container path.

📁 Project Structure
customer-churn-prediction/
│
├── .github/
│   └── workflows/
│       └── docker.yml
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│   ├── run_pipeline.py
│   ├── prepare_processed_data.py
│   ├── test_pipeline_phase1_data_features.py
│   ├── test_pipeline_phase2_modeling.py
│   └── test_fastapi.py
│
├── src/
│   ├── app/
│   │   └── main.py
│   │
│   ├── features/
│   │   └── build_features.py
│   │
│   ├── serving/
│   │   ├── inference.py
│   │   └── model/
│   │
│   └── utils/
│       └── validate_data.py
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
🧪 Testing

Manual test scripts are provided under:

scripts/
Data and feature tests
python scripts/test_pipeline_phase1_data_features.py
Model tests
python scripts/test_pipeline_phase2_modeling.py
FastAPI tests
python scripts/test_fastapi.py
🔐 Security

Secrets and environment variables are not committed to the repository.

The following are ignored:

.env
.venv/
mlruns/
data/raw/
data/processed/
*.pkl
*.joblib

Docker Hub credentials are stored securely using GitHub Actions repository secrets.

📌 Current Status

The project includes:

Data preprocessing
Feature engineering
Data validation
XGBoost model
Model evaluation
MLflow experiment tracking
FastAPI inference API
Gradio web UI
Docker containerization
Docker Hub image
GitHub repository
GitHub Actions CI/CD
AWS ECS/Fargate deployment architecture
ALB health checks
CloudWatch logging configuration
🎯 Future Improvements
Automated ECS deployment from GitHub Actions
Automated integration tests
Model monitoring
Data drift detection
Model performance monitoring
MLflow Tracking Server
Infrastructure as Code using Terraform
HTTPS using AWS Certificate Manager
Authentication and authorization for the API
👨‍💻 Author

Taiyob Ali

Machine Learning / AI Engineering Portfolio Project