# Brazilian E-Commerce Data Pipeline (End-to-End Modern Data Stack)

## Meltano → BigQuery → dbt (Star Schema) → Great Expectations → Dagster → Machine Learning → GitHub Dashboard

Live interactive dashboard:  
👉 **https://pinghar.github.io/Brazilian-E-Commerce-Public-Dataset-by-Olist/**
Presentation slide
https://onedrive.live.com/?redeem=aHR0cHM6Ly8xZHJ2Lm1zL2IvYy9jZmQ3Y2U3Nzg1MmMzNDA0L0lRQUJKRjZ0cEJpYlI3UlhMOWlSRkk2bUFaS3ozMWY2UzByLVNaY0k3S3BONmNZP2U9WFVuN1VI&cid=CFD7CE77852C3404&id=CFD7CE77852C3404%21sad5e240118a4479bb4572fd891148ea6&parId=CFD7CE77852C3404%21s125e47f6609c4140ba0827ee87ac0566&o=OneUp
---

## 1. Architecture Overview

```
Kaggle → Meltano → BigQuery (raw)
           ↓
        dbt (staging → dim → fact)
           ↓
      GX validation
           ↓
      Dagster orchestration
           ↓
ML (prediction + feature store)
           ↓
Dashboard (GitHub Pages)
```

---

## 2. Meltano: Extract → Load into BigQuery

### Installation  
```bash
pip install meltano
meltano init olist_pipeline
cd olist_pipeline
```

### Add extractors and loaders  
```bash
meltano add extractor tap-kaggle
meltano add loader target-bigquery
```

### Run Pipeline  
```bash
meltano run tap-kaggle target-bigquery
```

---

## 3. dbt: Build Star Schema in BigQuery

### Star Schema Output  
- dim_customers  
- dim_products  
- dim_sellers  
- dim_dates  
- fact_order_items  

### Run dbt  
```bash
dbt deps
dbt build
```

---

## 4. Great Expectations (GX)

```bash
python GX_Validation_Report.py
```

Outputs HTML data quality reports.

---

## 5. Dagster Workflow Orchestration

```bash
dagster dev
```

Schedules Meltano → dbt → GX → ML.

---

## 6. Machine Learning  
Models included in `ml_eda.ipynb`:  
- Order value prediction  
- Customer segmentation  
- Review score modeling  

---

## 7. Dashboard (GitHub Pages)

Hosted at:  
👉 **https://pinghar.github.io/Brazilian-E-Commerce-Public-Dataset-by-Olist/**

---

## 8. CEO Summary

- Revenue trend grows YoY  
- São Paulo dominates customer base  
- Freight cost is major margin factor  
- Review score strongly predicts churn  
- Top categories generate 70% of revenue  

---

## 9. Run Entire Pipeline

```bash
meltano run tap-kaggle target-bigquery
dbt build
python GX_Validation_Report.py
dagster dev
python ml/train.py
```

---

## 10. Repository Structure

```
meltano/
dbt/
GX/
dagster_pipeline/
ml/
docs/index.html
README.md
```
# Brazilian E-Commerce Live BigQuery Dashboard

Live dashboard URL (GitHub Pages):  
**https://pinghar.github.io/Brazilian-E-Commerce-Public-Dataset-by-Olist/**

> Note: To see live data, users must sign in with a Google account that has
> read access to the BigQuery project **`durable-ripsaw-477914-g0`**.

---

## 1. Executive Summary (for CEO / COO)

This dashboard provides a **single, live view** of key performance indicators for
a Brazilian e-commerce marketplace (Olist dataset). It focuses on three
questions leadership often asks:

1. **Where are our customers and sellers located?**  
2. **Which products and sellers drive the majority of order volume?**  
3. **How is demand evolving over time?**

The data lives in **Google BigQuery**, and the dashboard reads it directly
through secure Google authentication. This means:

- No exports / manual Excel refreshes  
- Always-up-to-date data (as soon as BigQuery is refreshed)  
- Access can be controlled at the Google account level

---

## 2. What the Dashboard Shows

The home page is split into six tiles.

### 2.1 Customer Distribution per State

- **Question:** Where is our customer base concentrated?  
- **Data:** `dim_customers`  
- **What you see:** A treemap showing the number of **unique customers** in each
  Brazilian state.  
- **How to use:**
  - Quickly identify **priority regions** for marketing and logistics.
  - Compare customer concentration vs seller concentration (see next tile).

---

### 2.2 Seller Distribution per State

- **Question:** Do we have enough sellers where our customers are?  
- **Data:** `dim_sellers`  
- **What you see:** A treemap of **seller counts** per state.  
- **How to use:**
  - Spot states with **customer demand but weak seller coverage**.
  - Guide seller acquisition / onboarding strategy.
  - Support COO in **network and logistics planning**.

---

### 2.3 Top 100 Sellers

- **Question:** Who drives most of our orders? How concentrated is our risk?  
- **Data:** `fact_orders` (joined to `dim_sellers`)  
- **Metric:** Number of **order items** per seller.  
- **What you see:**
  - A ranked bar chart (1 = top seller) showing each seller’s order volume.
  - Hover tooltip displays **seller city** and item count.  
- **How to use:**
  - Identify top strategic sellers for **priority support and negotiations**.
  - Assess **concentration risk** if too much volume depends on a few sellers.
  - Support promotional or partnership decisions.

---

### 2.4 Top 50 Product Categories Sold

- **Question:** Which categories dominate our business? Are we diversified?  
- **Data:**  
  - `fact_orders`  
  - `olist_products`  
  - `product_category_name_translation` (for English category names)  
- **Metric:** Count of order items per product category.  
- **What you see:**
  - A horizontal bar chart of the **top 50 categories** by order volume.
- **How to use:**
  - Understand **core categories** that drive demand.
  - Decide where to invest in:
    - assortment expansion,
    - campaigns,
    - or improving service levels.
  - Identify **long-tail categories** that might require a different strategy.

---

### 2.5 Sales per Month

- **Question:** Are we growing? Where is seasonality?  
- **Data:** `fact_orders`  
- **Metric:** Number of **distinct orders** per month.  
- **What you see:**
  - Line chart with monthly order counts (YYYY-MM).
- **How to use:**
  - Track **growth trends** and **seasonal peaks**.
  - Support discussions on:
    - inventory,
    - staffing,
    - marketing timing.
  - Compare with external events (holidays, campaigns, etc.).

---

### 2.6 About / Notes

- Explains the purpose of the dashboard for leadership.
- Suggests additional analyses that can be added later (e.g. revenue, reviews,
  payment types).

---

## 3. How to Use the Dashboard

1. Open the live URL:  
   **https://pinghar.github.io/Brazilian-E-Commerce-Public-Dataset-by-Olist/**
2. Click **“Sign in with Google”** in the top-right corner.
3. Sign in with a Google account that has read access to the BigQuery project.
4. After login, the tiles will load automatically:
   - You can **hover, zoom, and pan** any chart.
   - Use the legend / treemap hierarchy to focus on specific states or
     categories.

For external stakeholders, access can be limited by controlling **who has
BigQuery permissions**; the HTML site itself contains no raw data, only the
visuals generated after secure login.

---

## 4. Data Model (for COO / Technical Audience)

The dashboard is powered by a simple **star schema** in BigQuery:

- **Fact table**
  - `fact_orders`  
    - Grain: one row per order item  
    - Key fields: `order_id`, `customer_id`, `seller_id`, `product_id`,
      `order_purchase_timestamp`  

- **Dimension tables**
  - `dim_customers`  
    - Customer attributes including `customer_state`
  - `dim_sellers`  
    - Seller attributes including `seller_state`, `seller_city`
  - Raw product tables used for categorisation:
    - `olist_products`
    - `product_category_name_translation`

This structure allows fast aggregation **by customer**, **seller**, **category**
and **time** without repeatedly joining the raw Olist tables.

---

## 5. Technical Architecture (High Level)

Pipeline (current or intended):

1. **Source**: Olist Brazilian E-Commerce dataset (Kaggle).
2. **Storage**: Data landed in **Google BigQuery** under dataset `ecommerce`.
3. **Transformations**:
   - Dim/fact tables materialised in BigQuery (`dim_*`, `fact_*`).
4. **Validation (optional next step)**:
   - Add Great Expectations or dbt tests to validate row counts, nulls, etc.
5. **Presentation**:
   - Static HTML dashboard (`index.html`) hosted on **GitHub Pages**.
   - JavaScript front-end uses:
     - **Google API Client (gapi)** for OAuth and BigQuery queries.
     - **Plotly.js** for interactive charts.

No server-side code is required; everything runs in the browser, connecting
directly (and securely) to BigQuery.

---

## 6. Possible Future Enhancements

For roadmap discussions with leadership:

- Add **revenue and margin** metrics, not just order counts.
- Add **delivery performance** KPIs (on-time vs delayed orders).
- Add **customer review scores** by seller / category.
- Create **drill-through** pages for individual states or top sellers.
- Automate data ingestion from production systems instead of Kaggle.

---

## 7. Ownership

This dashboard and pipeline were designed and implemented by **LIM PING HAR
(Pinky)** as part of the NTU PACE Data Science & AI programme.

For questions, enhancements, or access requests, please contact the owner.

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
