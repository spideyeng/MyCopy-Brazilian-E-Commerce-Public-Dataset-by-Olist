
# Brazilian E-Commerce (Olist) End-to-End Data Pipeline  
### Meltano → BigQuery → dbt (Staging + Star Schema) → Great Expectations → ML → HTML Dashboard → Dagster Orchestration

![Dashboard Flowchart](https://github.com/pinghar/Brazilian-E-Commerce-Public-Dataset-by-Olist/blob/main/FlowChart.png)

## 1. Project Overview
This repository implements a full modern data pipeline for the Brazilian E-Commerce Public Dataset (Olist):

Pipeline: Kaggle → CSV → Meltano → BigQuery → dbt (Staging/Dim/Fact) → Tests → Great Expectations → EDA/ML → HTML Dashboard → Dagster

## 2. Repository Structure
project_root/
- meltano_kaggle_csv/
- Dbt_Final/
- GX/
- dagster_proj/
- EDA_ML/
- index.html
- README.md

## 3. Environment Setup
Clone repo:
```git clone https://github.com/pinghar/Brazilian-E-Commerce-Public-Dataset-by-Olist.git```
```cd Brazilian-E-Commerce-Public-Dataset-by-Olist```

Create environment:
```conda env create -f eltn_environment.yml```
```conda activate eltn```

## 4. Configure .env
KAGGLE_USERNAME="your_kaggle_username"
KAGGLE_KEY="your_kaggle_api_key"
GITHUB_TOKEN="ghp-xxxx"
GCP_PROJECT_ID="your_gcp_project_id"
GOOGLE_APPLICATION_CREDENTIALS="/full/path/to/your-service-account.json"
WEB_CLIENT_ID="your_google_client_id"

## 5. .gitignore
.env
*.json
data/
.meltano/
__pycache__/
.ipynb_checkpoints/
GX/uncommitted/

## 6. Meltano – Extract & Load Into BigQuery
python download_kaggle.py
meltano run tap-csv target-bigquery

## 7. dbt – Staging, Star Schema & Tests
cd ./Dbt_Final/

### 1. Connection Check
dbt debug

### 2. Install Packages (First Time only)
dbt deps

### 3. Staging Layer
dbt run  --select stg_db_*
dbt test --select stg_db_*

### 4. Dimension Layer
dbt run  --select dim_db_*
dbt test --select dim_db_*

### 5. Fact Layer
dbt run  --select fact_db_*
dbt test --select fact_db_*

### 6. Or ALL-IN-ONE
dbt build --full-refresh

## 8. Great Expectations
python GX/GX_Validation_Report.py

## 9. EDA & Machine Learning
python EDA_ML/EDA_ML.py

## 10. Dashboard
[View Live Dashboard](https://pinghar.github.io/Brazilian-E-Commerce-Public-Dataset-by-Olist/).

## 11. Dagster Orchestration
### For who execute Dagster for the first time

### 1. go to your project root folder
cd ~/Brazilian-E-Commerce-Public-Dataset-by-Olist

### 2. install dagster into your existing eltn env
conda env update -f eltn_environment.yml

### 3. ensure all *.py files executable
chmod 755 Dbt_Final/*.py GX/*.py EDA_ML/*.py

### 4. launch dagster dashboard under your project root folder
dagster dev -m dagster_proj.definitions

## 12. Architecture Overview
Kaggle → Meltano → BigQuery → dbt → GX → ML → Dashboard → Dagster

## 13. Executive Slides
[slides/Executive_Presentation.pdf](https://onedrive.live.com/?id=CFD7CE77852C3404%21sad5e240118a4479bb4572fd891148ea6&cid=CFD7CE77852C3404&redeem=aHR0cHM6Ly8xZHJ2Lm1zL2IvYy9jZmQ3Y2U3Nzg1MmMzNDA0L0lRQUJKRjZ0cEJpYlI3UlhMOWlSRkk2bUFaS3ozMWY2UzByLVNaY0k3S3BONmNZP2U9WFVuN1VI&parId=CFD7CE77852C3404%21s125e47f6609c4140ba0827ee87ac0566&o=OneUp).
