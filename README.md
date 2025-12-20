
# Brazilian E-Commerce (Olist) End-to-End Data Pipeline  
### Meltano → BigQuery → dbt (Staging + Star Schema) → Great Expectations → ML → HTML Dashboard → Dagster Orchestration

![Dashboard Flowchart](https://github.com/pinghar/Brazilian-E-Commerce-Public-Dataset-by-Olist/blob/main/images/FlowChart.png)

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
Clone repo:<br>
```git clone https://github.com/pinghar/Brazilian-E-Commerce-Public-Dataset-by-Olist.git```<br>
```cd Brazilian-E-Commerce-Public-Dataset-by-Olist```

Create environment:<br>
```conda env create -f eltn_environment.yml```<br>
```conda activate eltn```

## 4. Create .env
KAGGLE_USERNAME="your_kaggle_username"<br>
KAGGLE_KEY="your_kaggle_api_key"<br>
GCP_PROJECT_ID="your_gcp_project_id"<br>
GOOGLE_APPLICATION_CREDENTIALS="/full/path/to/your-service-account.json"<br>
WEB_CLIENT_ID="your_google_client_id"<br>

## 5. .gitignore
.env<br>
*.json<br>
data/<br>
.meltano/<br>
__pycache__/<br>
.ipynb_checkpoints/<br>
GX/uncommitted/<br>

## 6. Meltano – Extract & Load Into BigQuery
```python download_kaggle.py```<br>
```meltano run tap-csv target-bigquery```<br>

## 7. dbt – Staging, Star Schema & Tests
```cd ./Dbt_Final/```

### 1. Connection Check
```dbt debug```

### 2. Install Packages (First Time only)
```dbt deps```

### 3. Staging Layer
```dbt run  --select stg_db_*```<br>
```dbt test --select stg_db_*```

### 4. Dimension Layer
```dbt run  --select dim_db_*```<br>
```dbt test --select dim_db_*```

### 5. Fact Layer
```dbt run  --select fact_db_*```<br>
```dbt test --select fact_db_*```

### 6. Or ALL-IN-ONE
```dbt build --full-refresh```

## 8. Great Expectations
```python GX/GX_Validation_Report.py```

## 9. EDA & Machine Learning
```python EDA_ML/EDA_ML.py```

## 10. Dashboard

🔗 **Live Dashboard (Restricted Access)**  
[View Live Dashboard](https://pinghar.github.io/Brazilian-E-Commerce-Public-Dataset-by-Olist/)

> ⚠️ **Access Notice**  
> The live dashboard is restricted and only accessible to authorized team members.  
> External users may not be able to view it due to bigquery warehouse data access controls.

🎥 **Dashboard Walkthrough Video**  
To ensure visibility for everyone, a recorded dashboard walkthrough is provided below:  
[View Dashboard Video](https://github.com/pinghar/Brazilian-E-Commerce-Public-Dataset-by-Olist/blob/main/Dashboard%20Video.mp4)


## 11. Dagster Orchestration
### For who execute Dagster for the first time

### 1. go to your project root folder
```cd ~/Brazilian-E-Commerce-Public-Dataset-by-Olist```

### 2. install dagster into your existing eltn env
```conda activate eltn```<br>
```conda env update -f eltn_environment.yml```

### 3. ensure all *.py files executable
```chmod 755 Dbt_Final/*.py GX/*.py EDA_ML/*.py```

### 4. launch dagster dashboard under your project root folder
```dagster dev -m dagster_proj.definitions```

## 12. Executive & Technical Presentation

This project includes a complete executive-ready presentation deck covering:
- Business value
- Technical architecture
- Data quality & governance
- Key insights and recommendations

📎 **Full Slide Deck (PDF):**  
[Full_Presentation_Slide.pdf](https://github.com/pinghar/Brazilian-E-Commerce-Public-Dataset-by-Olist/blob/main/group_presentation/Olist_Data_Platform_Building_Strategic_Assets.pdf)
