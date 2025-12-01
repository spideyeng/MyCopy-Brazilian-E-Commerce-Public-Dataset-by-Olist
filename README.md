# Kaggle → CSV → Meltano → BigQuery Pipeline (Step-by-Step Guide)

This project demonstrates how to:

✅ Generate Kaggle API credentials\
✅ Download Kaggle datasets using Python\
✅ Store raw CSV safely\
✅ Load into BigQuery using Meltano\
✅ Prepare for dbt transformations

------------------------------------------------------------------------
## 2. Generate Kaggle API Key

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
# Kaggle
KAGGLE_USERNAME=xxxx
KAGGLE_KEY=xxxx

# GitHub (for tap-github / Dagster)
GITHUB_TOKEN=xxxxx

# BigQuery
GCP_PROJECT_ID=xxxx
GOOGLE_APPLICATION_CREDENTIALS=xxxxxx json file path
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
    pip_url: git+https://github.com/MeltanoLabs/tap-csv.git
    config:
      files:
      - entity: olist_customers
        path: data/olist_customers_dataset.csv
        keys: [customer_id]

      - entity: olist_order_items
        path: data/olist_order_items_dataset.csv
        keys: [order_id, order_item_id]

      - entity: olist_order_payments
        path: data/olist_order_payments_dataset.csv
        keys: [order_id, payment_sequential]

      - entity: olist_order_reviews
        path: data/olist_order_reviews_dataset.csv
        keys: [review_id]

      - entity: olist_orders
        path: data/olist_orders_dataset.csv
        keys: [order_id]

      - entity: olist_products
        path: data/olist_products_dataset.csv
        keys: [product_id]

      - entity: olist_sellers
        path: data/olist_sellers_dataset.csv
        keys: [seller_id]

      - entity: olist_geolocation
        path: data/olist_geolocation_dataset.csv
        keys: [geolocation_zip_code_prefix]

      - entity: product_category_name_translation
        path: data/product_category_name_translation.csv
        keys: [product_category_name]

    select:
    - '*.*'
```

``` yaml
 loaders:
  - name: target-bigquery
    variant: z3z1ma
    pip_url: git+https://github.com/z3z1ma/target-bigquery.git
    config:
      project: durable-ripsaw-477914-g0
      dataset: ecommerce
      location: US
      method: batch_job
      credentials_path: /home/pingh/project 
        2/durable-ripsaw-477914-g0-206ef3866e00.json
      denormalized: true
      flattening_enabled: true
      flattening_max_depth: 1
      upsert: false
      overwrite: false
      dedupe_before_upsert: false
```

------------------------------------------------------------------------

## 12. Run the Pipeline

``` bash
meltano run tap-csv target-bigquery
```

------------------------------------------------------------------------

## 13. Verify in BigQuery

``` sql
SELECT 
  'olist_customers' AS table_name, COUNT(*) AS total_rows FROM ecommerce.olist_customers
UNION ALL
SELECT 
  'olist_geolocation', COUNT(*) FROM ecommerce.olist_geolocation
UNION ALL
SELECT 
  'olist_order_items', COUNT(*) FROM ecommerce.olist_order_items
UNION ALL
SELECT 
  'olist_order_payments', COUNT(*) FROM ecommerce.olist_order_payments
UNION ALL
SELECT 
  'olist_order_reviews', COUNT(*) FROM ecommerce.olist_order_reviews
UNION ALL
SELECT 
  'olist_orders', COUNT(*) FROM ecommerce.olist_orders
UNION ALL
SELECT 
  'olist_products', COUNT(*) FROM ecommerce.olist_products
UNION ALL
SELECT 
  'olist_sellers', COUNT(*) FROM ecommerce.olist_sellers
UNION ALL
SELECT 
  'product_category_name_translation', COUNT(*) FROM ecommerce.product_category_name_translation;
```

------------------------------------------------------------------------

✅ Pipeline Complete\
✅ dbt transformations come next\
✅ Raw data fully preserved
