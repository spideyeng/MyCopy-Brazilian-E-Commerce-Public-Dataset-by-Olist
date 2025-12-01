# Kaggle → CSV → Meltano → BigQuery Pipeline (Step-by-Step Guide)

This project demonstrates how to:

✅ Generate Kaggle API credentials\
✅ Download Kaggle datasets using Python\
✅ Store raw CSV safely\
✅ Load into BigQuery using Meltano\
✅ Prepare for dbt transformations

------------------------------------------------------------------------
## 1. Generate Kaggle API Key

### Step 1: Login to Kaggle

Go to: https://www.kaggle.com/settings

### Step 2: Scroll to "API" Section

Click: ✅ **Create New API Token**
```Copy the API key and safe it to a safety place```
------------------------------------------------------------------------

## 3. Setup Kaggle API in Jupyter Notebook

### Option A (Recommended): Use `.env` file

Create `.env`:

``` Right Click > create new file name as ".env"
.env
```

``` env
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key
```

### Load in Jupyter:

``` python
from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("KAGGLE_USERNAME"))
print(os.getenv("KAGGLE_KEY"))
```

------------------------------------------------------------------------

## 4. Setup `.gitignore`

``` gitignore
.env
*.json
.meltano/
data/*.csv
__pycache__/
```

✅ Prevents leaking secrets

------------------------------------------------------------------------

## 5. Download Kaggle CSVs Using Python (Jupyter Notebook)

``` python
import kagglehub
from kagglehub import KaggleDatasetAdapter
from pathlib import Path

DATASET_SLUG = "olistbr/brazilian-ecommerce"

FILES = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

for file in FILES:
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        DATASET_SLUG,
        file
    )
    output = data_dir / file
    df.to_csv(output, index=False)
    print(f"Saved {file} → {len(df)} rows")
```

------------------------------------------------------------------------

## 6. Generate BigQuery Service Account JSON

### Step 1: Google Cloud Console

https://console.cloud.google.com

### Step 2: IAM & Admin → Service Accounts

Create new account:

    Name: meltano-bq-loader
    Role: BigQuery Admin

### Step 3: Create Key → JSON

Download file and store it safely:

``` bash
/home/youruser/project/bq-key.json
```

------------------------------------------------------------------------

## 7. Setup BigQuery Credentials in Jupyter

``` python
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/youruser/project/bq-key.json"
```

------------------------------------------------------------------------

## 8. Initialize Meltano

``` bash
meltano init meltano_kaggle_csv
cd meltano_kaggle_csv
```

------------------------------------------------------------------------

## 9. Add CSV Extractor

``` bash
meltano add extractor tap-csv
```

------------------------------------------------------------------------

## 10. Add BigQuery Loader

``` bash
meltano add loader target-bigquery
```

------------------------------------------------------------------------

## 11. Configure `meltano.yml`

``` yaml
plugins:
  extractors:
  - name: tap-csv
    variant: meltanolabs
    config:
      files:
        - entity: olist_customers
          path: data/olist_customers_dataset.csv
          keys: ["customer_id"]
```

``` yaml
  loaders:
  - name: target-bigquery
    variant: z3z1ma
    config:
      project: your_project_id
      dataset: ecommerce
      location: US
      method: batch_job
      credentials_path: /full/path/bq-key.json
      denormalized: true
      flattening_enabled: true
      flattening_max_depth: 1
```

------------------------------------------------------------------------

## 12. Run the Pipeline

``` bash
meltano run tap-csv target-bigquery
```

------------------------------------------------------------------------

## 13. Verify in BigQuery

``` sql
SELECT COUNT(*) FROM ecommerce.olist_customers;
```

------------------------------------------------------------------------

✅ Pipeline Complete\
✅ dbt transformations come next\
✅ Raw data fully preserved
