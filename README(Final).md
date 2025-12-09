
# Brazilian E-Commerce (Olist) End-to-End Data Platform  
### Meltano → BigQuery → dbt (Staging + Star Schema) → Great Expectations → ML → HTML Dashboard → Dagster Orchestration

## 1. Project Overview
This repository implements a full modern data pipeline for the Brazilian E-Commerce Public Dataset (Olist):

Pipeline: Kaggle → CSV → Meltano → BigQuery → dbt (Staging/Dim/Fact) → Tests → Great Expectations → EDA/ML → HTML Dashboard → Dagster

## 2. Repository Structure
project_root/
- data/
- meltano/
- dbt_edits_star_db_fixed/
- GX/
- dagster_pipeline/
- ml/
- index.html
- README.md

## 3. Environment Setup
Clone repo:
git clone https://github.com/pinghar/Brazilian-E-Commerce-Public-Dataset-by-Olist.git
cd Brazilian-E-Commerce-Public-Dataset-by-Olist

Create environment:
conda create -n eltn python=3.10 -y
conda activate eltn
pip install -r requirements.txt

## 4. Configure .env
KAGGLE_USERNAME=xxxx
KAGGLE_KEY=xxxx
GCP_PROJECT_ID=durable-ripsaw-477914-g0
GOOGLE_APPLICATION_CREDENTIALS=/ABSOLUTE/PATH/bq-key.json
BQ_DATASET=ecommerce
BQ_LOCATION=US
GOOGLE_CLIENT_ID=xxxx
GOOGLE_API_KEY=xxxx

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
dbt run --select staging --project-dir dbt_edits_star_db_fixed
dbt test --select staging --project-dir dbt_edits_star_db_fixed
dbt run --select marts --project-dir dbt_edits_star_db_fixed
dbt test --select marts --project-dir dbt_edits_star_db_fixed

## 8. Great Expectations
python GX/GX_Validation_Report.py

## 9. EDA & Machine Learning
python ml/EDA_ML_Analysis.py

## 10. Dashboard
Open index.html

## 11. Dagster Orchestration
dagster dev → open http://localhost:3000 to run full pipeline.

## 12. Architecture Overview
Kaggle → Meltano → BigQuery → dbt → GX → ML → Dashboard → Dagster

## 13. Executive Slides
slides/Executive_Presentation.pdf
