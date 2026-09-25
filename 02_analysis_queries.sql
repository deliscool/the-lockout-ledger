-- Databricks notebook source
-- Facebook Account-Disabling Complaints — Analysis Queries
-- Run 01_setup_and_load.py first. These queries assume
-- catalog = main, schema = fb_complaints (edit the USE line if different).

USE main.fb_complaints;

-- COMMAND ----------

-- 1. Complaints/events by source platform
-- The core "categorize by source" view — one row per platform, ranked by
-- how many entries we have logged for it.
SELECT
  source_platform,
  COUNT(*)                       AS entry_count,
  SUM(CASE WHEN metric_type = 'ag_complaints' THEN value ELSE 0 END) AS total_ag_complaints,
  MIN(date)                      AS earliest_entry,
  MAX(date)                      AS latest_entry
FROM complaints
GROUP BY source_platform
ORDER BY entry_count DESC;

-- COMMAND ----------

-- 2. Complaint volume trend by year (official AG counts only —
--    the most apples-to-apples comparable numbers we have)
SELECT
  year,
  region,
  source_name,
  value AS complaint_count
FROM complaints
WHERE metric_type = 'ag_complaints'
ORDER BY year, region;

-- COMMAND ----------

-- 3. Category breakdown — what kind of complaint is most common
--    across all sources (account takeover vs. wrongful disable vs. mass purge)
SELECT
  category,
  COUNT(*) AS mentions,
  COUNT(DISTINCT source_platform) AS distinct_platforms
FROM complaints
GROUP BY category
ORDER BY mentions DESC;

-- COMMAND ----------

-- 4. Year-over-year % change for regions with both a prior and current
--    year AG complaint count (mirrors how the AGs themselves reported it)
WITH yearly AS (
  SELECT region, year, value AS complaint_count
  FROM complaints
  WHERE metric_type = 'ag_complaints'
)
SELECT
  curr.region,
  curr.year        AS year,
  curr.complaint_count,
  prev.complaint_count AS prior_year_count,
  ROUND(100.0 * (curr.complaint_count - prev.complaint_count) / prev.complaint_count, 1) AS pct_change
FROM yearly curr
JOIN yearly prev
  ON curr.region = prev.region
 AND curr.year = prev.year + 1
ORDER BY pct_change DESC;

-- COMMAND ----------

-- 5. Petition signature growth over time (a rough proxy for public
--    complaint momentum where no hard agency number exists)
SELECT
  date,
  source_name,
  value AS signatures
FROM complaints
WHERE metric_type = 'petition_signatures'
ORDER BY date;

-- COMMAND ----------

-- 6. "Portfolio rollup" style summary — one row per platform type,
--    with the newest available signal from each. This is the shape
--    you'd feed into a dashboard's summary tiles.
SELECT
  source_platform,
  category,
  metric_type,
  value,
  unit,
  date,
  notes
FROM complaints
QUALIFY ROW_NUMBER() OVER (PARTITION BY source_platform ORDER BY date DESC) = 1
ORDER BY source_platform;

-- COMMAND ----------

-- 7. Once complaints_social is populated (Reddit/LinkedIn stretch goal):
--    monthly post volume by platform, unioned with the main dataset's
--    "anecdotal_report" rows for a combined social-sentiment view.
SELECT
  date_trunc('month', date) AS month,
  platform,
  COUNT(*) AS post_count,
  SUM(score_or_reactions) AS total_engagement
FROM complaints_social
GROUP BY date_trunc('month', date), platform
ORDER BY month, platform;
