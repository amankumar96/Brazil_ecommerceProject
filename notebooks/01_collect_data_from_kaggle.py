# Databricks notebook source
# MAGIC %md
# MAGIC ## Collect Brazilian E-Commerce dataset from Kaggle
# MAGIC Downloads the Olist Brazilian E-Commerce public dataset via kagglehub and saves it to a Unity Catalog Volume.

# COMMAND ----------

# Install kagglehub with pandas dataset-loading support
%pip install kagglehub[pandas-datasets]

# COMMAND ----------

# Restart Python so the newly installed package is picked up
dbutils.library.restartPython()

# COMMAND ----------

import kagglehub
from kagglehub import KaggleDatasetAdapter

# Kaggle dataset handle and destination Volume path
DATASET_HANDLE = "olistbr/brazilian-ecommerce"
VOLUME_PATH = "/Volumes/volumes/default/processing/Brazilian_E-Commerce_public_Data/"

# COMMAND ----------

# MAGIC %md
# MAGIC Kaggle credentials must be available before calling kagglehub.
# MAGIC Set `KAGGLE_USERNAME` / `KAGGLE_KEY` as a Databricks secret-backed env vars, or via `kagglehub.login()`.

# COMMAND ----------

# CSV files that make up the Olist dataset
DATASET_FILES = [
    "olist_customers_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "product_category_name_translation.csv",
]

# Load each CSV straight into a pandas DataFrame via the PANDAS adapter
dataframes = {
    file_name: kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        DATASET_HANDLE,
        file_name,
    )
    for file_name in DATASET_FILES
}

# COMMAND ----------

# Ensure the target Volume directory exists before writing
dbutils.fs.mkdirs(VOLUME_PATH)

# Persist each DataFrame back out as CSV under its original filename
for file_name, df in dataframes.items():
    df.to_csv(f"{VOLUME_PATH}{file_name}", index=False)

# COMMAND ----------

# Verify the files landed in the Volume and report row counts
display(dbutils.fs.ls(VOLUME_PATH))
for file_name, df in dataframes.items():
    print(f"{file_name}: {len(df)} rows")
