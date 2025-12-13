# %%
#User to install seaborn, pandas, db-dtypes, scikit-learn and xgboost if haven't already done so
#User to authenticate account with the gcloud CLI, if havent already done so

# %% [markdown]
# # Brazilian E-Commerce (Olist) – Exploratory Data Analysis (EDA)
# 
# This notebook is part of the **end-to-end data pipeline**:
# 
# - Kaggle → CSV → Meltano → BigQuery  
# - dbt → Star Schema (fact + dim tables)  
# - Great Expectations → Data Quality  
# - **Python (this notebook) → Exploratory Data Analysis**  
# - ML model notebook  
# - HTML / Plotly dashboard
# 
# **Audience:** Data engineers, analytics engineers, and data scientists.  
# **Warehouse:** BigQuery  
# **Schema:** `ecommerce` (dbt outputs)

# %% [markdown]
# ## 0. Setup & Imports
# 
# This section:
# 
# - Imports core Python libraries  
# - Creates a BigQuery client (using Application Default Credentials or a service account)  
# - Sets some display and plotting defaults

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from google.cloud import bigquery

# Display options
pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 200)
sns.set(style="whitegrid", palette="deep")

PROJECT_ID = "durable-ripsaw-477914-g0"  # <-- change if needed
DATASET = "ecommerce"                    # dbt output dataset

client = bigquery.Client(project=PROJECT_ID)
print("✅ BigQuery client initialised for project:", PROJECT_ID)

# %% [markdown]
# ## Load dbt Star-Schema Tables
# 
# We **never** run EDA directly on raw CSVs.  
# Instead we consume **cleaned, modeled tables** produced by dbt and validated by Great Expectations:
# 
# - `dim_customers`
# - `dim_products`
# - `dim_sellers`
# - `fact_orders`
# 
# These should correspond to your dbt models.
# 

# %%
def load_table(table_name: str) -> pd.DataFrame:
    """Helper to load a table from BigQuery into pandas."""
    query = f"""SELECT * FROM `{PROJECT_ID}.{DATASET}.{table_name}`"""
    print(f"\n▶ Loading {PROJECT_ID}.{DATASET}.{table_name} ...")
    df = client.query(query).to_dataframe()
    print(f"   Shape: {df.shape}")
    return df

df_customers = load_table("dim_db_customers")
df_sellers   = load_table("dim_db_sellers")
df_products  = load_table("dim_db_products")
df_orders    = load_table("fact_db_order_items")  # fact table from dbt

df_customers.head()

# %% [markdown]
# ## Basic Data Health Checks
# 
# Even though dbt + Great Expectations have already validated the data,  
# it's good practice to perform **quick sanity checks** in the notebook:
# 
# - Missing values by column  
# - Basic descriptive statistics  
# - Key date ranges

# %%
df_customers.info()
df_sellers.info()
df_products.info()
df_orders.info()

# %%
df_customers.describe()

# %%
df_sellers.describe()

# %%
df_products.describe()

# %%
df_orders.describe()

# %%
print("\n🔍 Missing values in fact_orders:")
print(df_orders.isna().sum().sort_values(ascending=False))

print("\n📊 Descriptive statistics (numeric columns):")
print(df_orders.describe())

if 'order_date_key' in df_orders.columns:
    df_orders['order_date_key'] = pd.to_datetime(df_orders['order_date_key'])
    print("\n⏱ Purchase timestamp range:")
    print(df_orders['order_date_key'].min(), "→", df_orders['order_date_key'].max())

# %% [markdown]
# ## Monthly Sales Trend
# 
# Objective for technical engineering:
# 
# - Verify that date logic is correct  
# - Confirm that **aggregation over fact_orders** works as expected  
# - Provide a high-level volume view for business stakeholders

# %%
# Create year-month column
df_orders['year_month'] = df_orders['order_date_key'].dt.to_period('M').astype(str)

# Compute monthly distinct orders
monthly_sales = (
    df_orders
    .groupby('year_month')['order_id']
    .nunique()
    .reset_index(name='num_orders')
)

# Plot
plt.figure(figsize=(15,5))
sns.lineplot(data=monthly_sales, x='year_month', y='num_orders', marker="o")
plt.title("Monthly Sales Trend (Number of Orders)")
plt.xlabel("Year-Month")
plt.ylabel("Distinct Orders")
plt.xticks(rotation=45)
plt.tight_layout()
#plt.show()

# Show last few rows
monthly_sales.tail()

# %% [markdown]
# ## Top Product Categories
# 
# We now combine the **fact_orders** table with **dim_products** to get  
# the top-selling product categories by order item count.
# 

# %%
# Ensure we only keep relevant product columns
product_cols = ['product_id', 'product_category_name', 'product_category_name_english']
product_cols = [c for c in product_cols if c in df_products.columns]

df_orders_products = df_orders.merge(
    df_products[product_cols],
    on='product_id',
    how='left'
)

top_categories = (
    df_orders_products
    .groupby('product_category_name_english', dropna=False)['order_item_id']
    .count()
    .sort_values(ascending=False)
    .head(20)
)

plt.figure(figsize=(12,8))
sns.barplot(x=top_categories.values, y=top_categories.index)
plt.title("Top 20 Product Categories by Items Sold")
plt.xlabel("Order Items Count")
plt.ylabel("Category (English)")
plt.tight_layout()
#plt.show()

top_categories.to_frame(name='order_items').reset_index().head(10)

# %% [markdown]
# ## Customer Segmentation – RFM (Recency, Frequency, Monetary)
# 
# We create **RFM features** from fact_orders:
# 
# - **Recency**: Days since last purchase  
# - **Frequency**: Number of distinct orders  
# - **Monetary**: Total gross order value
# 
# These RFM features are also good **inputs for ML models** later.
# 

# %%
df_orders['order_purchase_timestamp'] = df_orders['order_date_key']

df_orders['order_date'] = df_orders['order_purchase_timestamp'].dt.date
df_orders['gross_order_item_value'] = (
    df_orders['gross_order_item_value']
    .astype(str)
    .str.replace(',', '', regex=False)
    .astype(float)
)

snapshot_date = df_orders['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

# %%
rfm = (
    df_orders
    .groupby('customer_id')
    .agg({
        'order_date': lambda x: (snapshot_date.date() - max(x)).days,
        'order_id': 'nunique',
        'gross_order_item_value': 'sum'
    })
    .rename(columns={
        'order_date': 'Recency',
        'order_id': 'Frequency',
        'gross_order_item_value': 'Monetary'
    })
)


# %%
print("RFM shape:", rfm.shape)
print(rfm.describe())

sns.pairplot(rfm.reset_index()[['Recency', 'Frequency', 'Monetary']])
plt.suptitle("RFM Feature Relationships", y=1.02)
#plt.show()


# %% [markdown]
# ## Freight vs Price Relationship
# 
# This checks whether freight cost is proportional to product price,  
# which may indicate **pricing policy or carrier rules**.

# %%
sample_df = df_orders[['price', 'freight_value']].dropna().copy()
if len(sample_df) > 10000:
    sample_df = sample_df.sample(10000, random_state=42)

plt.figure(figsize=(7,7))
sns.scatterplot(data=sample_df, x='price', y='freight_value', alpha=0.4)
plt.title("Price vs Freight Value (Sample)")
plt.xlabel("Item Price")
plt.ylabel("Freight Cost")
plt.tight_layout()
#plt.show()

sample_df.corr()

# %% [markdown]
# ## Seller Regional Activity
# 
# Use **dim_sellers** joined with **fact_orders** to identify high-activity regions.
# 
# This is useful for:
# 
# - Network planning  
# - Capacity planning  
# - Regional campaigns

# %%
# Clean deduped dim table
df_sellers_unique = (
    df_sellers.groupby('seller_id')['seller_state']
    .agg(lambda x: x.mode()[0])
    .reset_index()
)

df_sellers_unique['seller_state'] = (
    df_sellers_unique['seller_state']
    .astype(str)
    .str.upper()
    .str.strip()
)

# Merge to fact
df_orders_sellers = df_orders.merge(
    df_sellers_unique,
    on='seller_id',
    how='left',
    validate='many_to_one'
)

# Compute seller activity
seller_activity = (
    df_orders_sellers
    .groupby('seller_state')['order_item_id']
    .count()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10,6))
sns.barplot(x=seller_activity.index, y=seller_activity.values)
plt.title("Seller Activity by State (Order Items)")
plt.xlabel("State")
plt.ylabel("Items Sold")
plt.tight_layout()
#plt.show()

# %%
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# %%
# Ensure numeric types for aggregation
df_orders['gross_order_item_value'] = pd.to_numeric(df_orders['gross_order_item_value'], errors='coerce')
df_orders['freight_value'] = pd.to_numeric(df_orders['freight_value'], errors='coerce')
df_orders['price'] = pd.to_numeric(df_orders['price'], errors='coerce')

# Aggregate orders per customer
orders_agg = (
    df_orders
    .groupby('customer_id')
    .agg(
        total_revenue=('gross_order_item_value', 'sum'),
        total_freight=('freight_value', 'sum')
    )
    .reset_index()
)

# Merge with customer info
df_features = df_customers.merge(
    orders_agg,
    on='customer_id',
    how='left'
)

# Select only required columns
df_features = df_features[[
    'customer_id',
    'customer_state',
    'customer_zip_code_prefix',  # maps to customer_zip
    'total_revenue',
    'total_freight',
]]

df_features.head()


# %%
df_features.info()

# %%
df_features_cleaned = df_features.dropna()

# %%
df_features_cleaned.info()

# %%
y = df_features_cleaned['total_freight']
X = df_features_cleaned.drop(columns=['total_freight','customer_id'])

# %%
num_features = ['customer_zip_code_prefix','total_revenue']
cat_features = ['customer_state']

# %%
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples: {X_test.shape[0]}")

# %%
# Numeric transformer: fill missing values, then scale
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),  # fill NaN with mean
    ('scaler', StandardScaler())
])

# Categorical transformer: fill missing values, then one-hot encode
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),  # fill NaN with most frequent
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Column transformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, num_features),
        ('cat', categorical_transformer, cat_features)
    ],
    remainder='drop'  # drop other columns
)

# %%
def evaluate_model(model_name, y_true, y_pred):
    """Calculates and prints key regression performance metrics."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    print(f"--- {model_name} Performance ---")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"R-squared (R2): {r2:.4f}")
    print("-" * 40)
    return {'RMSE': rmse, 'MAE': mae, 'R2': r2}

# %%
print("Starting Linear Regression (Baseline) Training...")

# Create the full pipeline for Linear Regression
lr_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Train the model
lr_model.fit(X_train, y_train)

# Predict on the test set
y_pred_lr = lr_model.predict(X_test)

# Evaluate performance
lr_metrics = evaluate_model("Linear Regression (Baseline)", y_test, y_pred_lr)

# %%
from xgboost import XGBRegressor

print("Starting XGBoost Training...")

# Create the full pipeline for XGBoost
xgb_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor(
         objective='reg:squarederror',
    n_estimators=500,  # Number of boosting rounds
    learning_rate=0.05,
    random_state=42,
    n_jobs=-1, # Use all available cores
    tree_method='hist' # Faster tree cons
    ))
])


# Train the model
xgb_model.fit(X_train, y_train)

# Predict on the test set
y_pred_xgb = xgb_model.predict(X_test)

# Evaluate performance
xgb_metrics = evaluate_model("XGBoost Regressor", y_test, y_pred_xgb)

# %%



