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

# dbt Pipeline Guide — Brazilian E-Commerce (Olist)

This README explains **only the dbt process step by step** for building a **star schema** in BigQuery using the Olist Brazilian E‑Commerce dataset.

All transformations happen inside the **`ecommerce`** BigQuery dataset.

---

## 1. Prerequisites

- Python environment with `dbt-bigquery` installed (you use `eltn`):
  
```bash
conda activate eltn
pip install dbt-bigquery
```

- Raw Olist tables already in BigQuery (loaded by Meltano or other EL tool):

Typical tables in dataset **`ecommerce`**:

- `olist_orders`
- `olist_order_items`
- `olist_customers`
- `olist_order_payments`
- `olist_order_reviews`
- `olist_products`
- `olist_sellers`
- `olist_geolocation`
- `product_category_name_translation`

---

## 2. dbt Project Location & Structure

The dbt project folder is:

```bash
~/Brazilian-E-Commerce-Public-Dataset-by-Olist/dbt_edits_star_db_fixed
```

Inside it you should see:

```text
dbt_edits_star_db_fixed/
├── dbt_project.yml
├── profiles.yml            # project-specific dbt profile
├── staging/                # staging models: stg_db_*.sql
│   └── sources.yml         # BigQuery sources
└── marts/
    ├── dim/                # dimension models: dim_db_*.sql
    └── fact/               # fact models: fact_db_*.sql
```

All dbt commands must be run **inside this folder**.

---

## 3. Configure dbt to Use BigQuery `ecommerce` Dataset

### 3.1. `profiles.yml`

In `dbt_edits_star_db_fixed/profiles.yml`:

```yaml
dbt_olist:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: "durable-ripsaw-477914-g0"
      dataset: "ecommerce"       # ⭐ all models go to this dataset
      location: US
      threads: 4
      priority: interactive
      retries: 1
```

### 3.2. `dbt_project.yml`

In `dbt_edits_star_db_fixed/dbt_project.yml`:

```yaml
name: dbt_edits_star_db
version: 1.0.0
config-version: 2

profile: dbt_olist

model-paths: ["staging", "marts"]

target-path: "target"
clean-targets: ["target", "dbt_packages"]

models:
  dbt_edits_star_db:

    # Uses dataset = ecommerce from profiles.yml

    staging:
      +materialized: view      # stg_db_* are views

    marts:
      dim:
        +materialized: table   # dim_db_* are tables
      fact:
        +materialized: table   # fact_db_* are tables
```

This setup gives you a **classic star schema**:

```text
          dim_db_customers
                 ↑
                 |
dim_db_products ← fact_db_order_items → dim_db_sellers
                 |
                 ↓
            dim_db_dates
```

All of these live in **BigQuery dataset: `ecommerce`**.

---

## 4. Step-by-Step: Running dbt

### 4.1. Step 1 — Activate Environment & Go to dbt Folder

```bash
conda activate eltn

cd ~/Brazilian-E-Commerce-Public-Dataset-by-Olist/dbt_edits_star_db_fixed
```

### 4.2. Step 2 — Check Configuration

```bash
dbt debug
```

You should see:

- `profiles.yml file [OK found and valid]`
- `dbt_project.yml file [OK found and valid]`
- `Connection test: [OK connection ok]`

> ⚠ If you see  
> `No dbt_project.yml found at expected path /home/.../Brazilian-E-Commerce-Public-Dataset-by-Olist/dbt_project.yml`  
> you are in the **wrong folder**. Make sure you are inside `dbt_edits_star_db_fixed/`.

### 4.3. Step 3 — Install dbt Packages (If Any)

```bash
dbt deps
```

### 4.4. Step 4 — List All dbt Nodes (Models & Sources)

```bash
dbt ls
```

You should see entries like:

```text
dbt_edits_star_db.stg_db_customers
dbt_edits_star_db.stg_db_orders
dbt_edits_star_db.stg_db_order_items
dbt_edits_star_db.dim.dim_db_customers
dbt_edits_star_db.dim.dim_db_products
dbt_edits_star_db.dim.dim_db_sellers
dbt_edits_star_db.dim.dim_db_dates
dbt_edits_star_db.fact.fact_db_order_items
source:dbt_edits_star_db.olist_raw.olist_orders
...
```

This confirms dbt can see all models and sources correctly.

---

## 5. Running Staging Models Only (Optional)

If you want to materialize only the **staging views** first:

```bash
dbt run --select stg_db_*
```

This will create views in BigQuery:

- `ecommerce.stg_db_customers`
- `ecommerce.stg_db_orders`
- `ecommerce.stg_db_order_items`
- `ecommerce.stg_db_order_payments`
- `ecommerce.stg_db_products`
- `ecommerce.stg_db_sellers`
- `ecommerce.stg_db_product_category_name_translation`

These staging models usually:

- Clean column names  
- Cast data types  
- Standardize timestamps, currencies, etc.

---

## 6. Running Dimension & Fact Models

### 6.1. Run Only Dimension Tables

```bash
dbt run --select dim_db_*
```

Creates dimension tables in `ecommerce`:

- `dim_db_customers`
- `dim_db_products`
- `dim_db_sellers`
- `dim_db_dates`

### 6.2. Run Only Fact Tables

```bash
dbt run --select fact_db_*
```

Creates fact tables such as:

- `fact_db_order_items`

### 6.3. Run Everything (Staging + Dim + Fact)

```bash
dbt run
```

or better:

```bash
dbt build
```

`dbt build` will:

- Run all models (staging, dim, fact)  
- Run all configured tests for those models

---

## 7. Running dbt Tests

Tests are usually defined in `schema.yml` files next to your models and include:

- `not_null` tests on primary keys and foreign keys  
- `unique` tests on natural keys (e.g., `order_id`, `customer_id`)  

### 7.1. Run Tests for All Models

```bash
dbt test
```

### 7.2. Run Tests Only for Dim & Fact Models

```bash
dbt test --select dim_db_* fact_db_*
```

You should see a summary such as:

```text
PASS=XX WARN=0 ERROR=0 SKIP=0
```

If there are failures, dbt will show which column/model failed which test.

---

## 8. Typical One-Command Workflow

From a fresh shell:

```bash
conda activate eltn
cd ~/Brazilian-E-Commerce-Public-Dataset-by-Olist/dbt_edits_star_db_fixed

dbt debug       # check profile & connection
dbt deps        # install dependencies
dbt build       # run models + tests (staging + dim + fact)
```

After `dbt build` finishes successfully, you will have:

- A validated **star schema** in BigQuery dataset `ecommerce`  
- Ready-to-use tables for BI dashboards, ML, and further analysis.

---

## 9. What to Expect in BigQuery After dbt

Final curated tables (all in dataset **`ecommerce`**):

- **Dimensions**
  - `dim_db_customers`
  - `dim_db_products`
  - `dim_db_sellers`
  - `dim_db_dates`

- **Fact**
  - `fact_db_order_items`

These tables form the backbone of your analytics and machine learning workflows.



