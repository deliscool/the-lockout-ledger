# Databricks notebook source
# MAGIC %md
# MAGIC # Facebook Account-Disabling Complaints — Setup & Load
# MAGIC
# MAGIC This notebook creates a catalog/schema and loads the complaints CSV into a
# MAGIC Delta table. Run this first, then move to `02_analysis_queries.sql`.
# MAGIC
# MAGIC **Before running:** upload `facebook_complaints_2024_2026.csv` to a Databricks
# MAGIC Volume or DBFS path (Catalog > Create > Volume, then "Upload to this volume"
# MAGIC is the easiest click-path in the UI). Update `csv_path` below to match.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Config — edit these two lines for your workspace

# COMMAND ----------

catalog_name = "main"                 # change if you use a different catalog
schema_name  = "fb_complaints"        # this notebook will create it if missing
csv_path     = "/Volumes/main/default/uploads/facebook_complaints_2024_2026.csv"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Create catalog/schema (Unity Catalog)

# COMMAND ----------

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}")
spark.sql(f"USE {catalog_name}.{schema_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Load the CSV and inspect it before committing to a schema

# COMMAND ----------

raw_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(csv_path)
)

display(raw_df)
raw_df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Clean types and write as a managed Delta table
# MAGIC
# MAGIC `date` is left nullable — a few rows (LinkedIn/forum anecdotes) have no
# MAGIC reliable date, which is realistic: real-world complaint data is messy.

# COMMAND ----------

from pyspark.sql.functions import col, to_date

clean_df = (
    raw_df
    .withColumn("date", to_date(col("date")))
    .withColumn("year", col("year").cast("int"))
    .withColumn("value", col("value").cast("double"))
)

(
    clean_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{catalog_name}.{schema_name}.complaints")
)

print(f"Loaded {clean_df.count()} rows into {catalog_name}.{schema_name}.complaints")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Placeholder table for live Reddit / LinkedIn pulls (stretch goal)
# MAGIC
# MAGIC Real-time social volume wasn't pullable from outside Databricks (Reddit
# MAGIC blocks unauthenticated scraping). This table is scaffolded so you can
# MAGIC populate it later from inside a Databricks notebook using the Reddit API
# MAGIC (PRAW) with your own app credentials — Databricks' outbound network access
# MAGIC isn't restricted the way this session's was.

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, DateType, IntegerType

social_schema = StructType([
    StructField("date", DateType(), True),
    StructField("platform", StringType(), True),      # 'reddit' | 'linkedin'
    StructField("subreddit_or_group", StringType(), True),
    StructField("post_title", StringType(), True),
    StructField("score_or_reactions", IntegerType(), True),
    StructField("num_comments", IntegerType(), True),
    StructField("category", StringType(), True),       # account_takeover | wrongful_disable | mass_purge
    StructField("url", StringType(), True),
])

empty_social_df = spark.createDataFrame([], social_schema)

(
    empty_social_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(f"{catalog_name}.{schema_name}.complaints_social")
)

print(f"Created empty placeholder table {catalog_name}.{schema_name}.complaints_social")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Done
# MAGIC
# MAGIC Two tables now exist:
# MAGIC - `complaints` — the real dataset (AG offices, news, petitions, Meta disclosures)
# MAGIC - `complaints_social` — empty, ready for Reddit/LinkedIn data later
# MAGIC
# MAGIC Next: open `02_analysis_queries.sql` and run the queries as a SQL notebook,
# MAGIC or paste them into a Databricks SQL dashboard.
