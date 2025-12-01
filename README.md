# Olist Kaggle → BigQuery with Meltano (plus Jupyter validation)

This project demonstrates a full EL pipeline:

Kaggle → Local CSV → Meltano → BigQuery → dbt (later)

------------------------------------------------------------------------

## 1. Project Structure

    meltano_kaggle_olist/
    ├── data/
    ├── notebooks/
    ├── .env
    ├── .gitignore
    ├── meltano.yml
    ├── README.md

------------------------------------------------------------------------

## 2. Environment Setup

``` bash
conda create -n eltn python=3.10 -y
conda activate eltn
pip install meltano pandas python-dotenv jupyter kaggle
```

------------------------------------------------------------------------

## 3. Kaggle API Setup

Download kaggle.json from Kaggle → Account → API.

``` bash
mkdir -p ~/.kaggle
mv kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

------------------------------------------------------------------------

## 4. .env File

``` env
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key

GCP_PROJECT_ID=durable-ripsaw-477914-g0
BIGQUERY_DATASET=ecommerce
GOOGLE_APPLICATION_CREDENTIALS=/full/path/to/service_account.json
```

------------------------------------------------------------------------

## 5. .gitignore

``` gitignore
.env
*.json
__pycache__/
.ipynb_checkpoints/
.meltano/
logs/
state.*
```

------------------------------------------------------------------------

## 6. Jupyter Notebook 01 -- Download Kaggle Dataset

``` python
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path

api = KaggleApi()
api.authenticate()

data_dir = Path("../data")
data_dir.mkdir(exist_ok=True)

api.dataset_download_files(
  "olistbr/brazilian-ecommerce",
  path=str(data_dir),
  unzip=True
)
```

------------------------------------------------------------------------

## 7. Jupyter Notebook 02 -- CSV Row Count Validation

``` python
import pandas as pd
from pathlib import Path

data_dir = Path("../data")

for f in data_dir.glob("*.csv"):
    df = pd.read_csv(f)
    print(f.name, len(df))
```

------------------------------------------------------------------------

## 8. Meltano Setup

``` bash
meltano init .
meltano add extractor tap-csv
meltano add loader target-bigquery
```

------------------------------------------------------------------------

## 9. meltano.yml

``` yaml
version: 1
default_environment: dev

plugins:
  extractors:
    - name: tap-csv
      variant: meltanolabs
      pip_url: git+https://github.com/MeltanoLabs/tap-csv.git
      config:
        files:
          - entity: olist_customers
            path: data/olist_customers_dataset.csv
            keys: ["customer_id"]

  loaders:
    - name: target-bigquery
      variant: z3z1ma
      pip_url: git+https://github.com/z3z1ma/target-bigquery.git
      config:
        project: ${GCP_PROJECT_ID}
        dataset: ${BIGQUERY_DATASET}
        location: US
        credentials_path: ${GOOGLE_APPLICATION_CREDENTIALS}
        denormalized: true
        flattening_enabled: true
        flattening_max_depth: 1
        upsert: false
        overwrite: false
```

------------------------------------------------------------------------

## 10. Run the Pipeline

``` bash
rm -f .meltano/state*
meltano run tap-csv target-bigquery --force
```

------------------------------------------------------------------------

## 11. Jupyter Notebook 03 -- CSV vs BigQuery Validation

``` python
from google.cloud import bigquery
client = bigquery.Client()

query = "SELECT COUNT(*) FROM `durable-ripsaw-477914-g0.ecommerce.olist_customers`"
print(client.query(query).to_dataframe())
```

------------------------------------------------------------------------

## ✅ Result

All Kaggle CSV data is now safely loaded into BigQuery without
deduplication. dbt transformations can be built on top.
