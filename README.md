# Kaggle → CSV → Meltano → BigQuery Pipeline (Step-by-Step Guide)

This project demonstrates how to:

✅ Generate Kaggle API credentials  
✅ Download Kaggle datasets using Python  
✅ Store raw CSV safely  
✅ Load into BigQuery using Meltano  
✅ Verify that CSV row counts match BigQuery  
✅ Prepare for dbt transformations

---

## 1. Conda Environment

```bash
# From the folder where your environment YAML file is
conda env create -f eltn_environment.yml   # or your file path
conda activate eltn                        

```
------------------------------------------------------------------------
## 2. Generate Kaggle API Key

### Step 1: Login to Kaggle

Go to: https://www.kaggle.com/settings

### Step 2: Scroll to "API" Section

Click: ✅ **Create New API Token**
```Copy the API key and safe it to a safety place```
------------------------------------------------------------------------

## 3. Setup Kaggle API in Jupyter Notebook

### Use `.env` file

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

## 5. Download Kaggle CSVs Using Python into data/
Use the helper script [download_kaggle.py](https://github.com/pinghar/Brazilian-E-Commerce-Public-Dataset-by-Olist/blob/main/download_kaggle.py) to pull all 9 Olist CSVs and save them to the data/ folder.

You can run it either from terminal:


``` bash
python download_kaggle.py
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

## 7. Initialize Meltano

``` bash
meltano init meltano_kaggle_csv
cd meltano_kaggle_csv
```

------------------------------------------------------------------------

## 8. Add CSV Extractor

``` bash
meltano add extractor tap-csv
```

------------------------------------------------------------------------

## 9. Add BigQuery Loader

``` bash
meltano add loader target-bigquery
```

------------------------------------------------------------------------

## 10. Configure `meltano.yml`
# find meltano.yml then paste below plugins & loaders into it and save
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

## 11. Run the Pipeline

``` bash
meltano run tap-csv target-bigquery
```

------------------------------------------------------------------------

## 12. Verify in BigQuery match with CSV
Verify CSV Files Locally (Row & Column Counts) with [check_all_csvs.py](https://github.com/pinghar/Brazilian-E-Commerce-Public-Dataset-by-Olist/blob/main/check_all_csvs.py). 

Run from terminal:
``` bash
python download_kaggle.py
```

Then go to google console > big query run below sql

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
After that, match the csv file rows and columns vs bigquery rows and columns all should be same.
------------------------------------------------------------------------

✅ Pipeline Complete\
✅ dbt transformations come next\
✅ Raw data fully preserved

Run Dashboard

cd /home/pingh/Brazilian-E-Commerce-Public-Dataset-by-Olist/dashboard
explorer.exe olist_ml_business_dashboard.html


