# The Lockout Ledger

A cross-platform data brief tracking real, publicly reported complaints about
Meta disabling Facebook and Instagram accounts, 2019–2026 — built to put my
[Databricks Fundamentals certification](https://www.databricks.com/try-databricks?utm_source=course_completion&utm_medium=linkedin&utm_campaign=fe_learning_completion&utm_content=fundamentals-v2)
to work on a real, messy dataset instead of a course exercise.

**Live page:** _link goes here once GitHub Pages is turned on_
**Databricks dashboard:** static export below (Free Edition has no public, no-login share link)

## What this is

44 records pulled from state attorney general filings, news investigations,
a public Change.org petition, Meta's own disclosures, and 21 individually
cited LinkedIn posts — categorized by source platform and complaint type,
then loaded into Databricks for analysis.

The goal was to practice the full Databricks pipeline end to end (Unity
Catalog → Delta Lake → SQL → dashboard) using a real, messy, non-synthetic
dataset instead of a toy tutorial dataset.

## What's in this repo

| File | What it is |
|---|---|
| `index.html` | The published showcase page — static, no live credentials |
| `dashboard-export.png` | Static export of the live Databricks dashboard |
| `facebook_complaints_2024_2026.csv` | The source dataset |
| `01_setup_and_load.py` | Databricks notebook — loads the CSV into a Delta table |
| `02_analysis_queries.sql` | SQL notebook — the analysis queries behind the dashboard |

## Data sources

- State Attorney General complaint filings (NY, PA, MI, MA)
- ABC7 Los Angeles, CBS News Philadelphia
- The Register
- Change.org ("Hold Meta Accountable" petition)
- Meta's Oversight Board
- 21 individually cited LinkedIn posts from small business owners, agencies, and creators

Figures are as publicly reported and not independently audited. Some entries
are undated or approximate where the original source gave no exact date.

## Top 4 things I learned

1. **Unity Catalog's permission hierarchy stacks.** `SELECT` on a table isn't
   enough — you also need `USE CATALOG` and `USE SCHEMA` on everything above
   it, or the grant does nothing.
2. **Delta tables aren't just "CSV but managed."** Loading the same CSV as a
   managed Delta table vs. reading it directly changes how Unity Catalog
   governs and versions it — worth the extra setup step even for a small
   dataset.
3. **A dashboard's SQL can quietly lie to you.** My "most recent year"
   region chart was pulling a global `MAX(year)` across every region, so one
   partial-year data point (Michigan) silently overwrote a real, complete
   year. The chart rendered fine — it was just wrong. Always check what a
   `MAX()` or `ORDER BY ... LIMIT 1` is actually scoped to.
4. **"Public" has more than one meaning in Databricks.** Free Edition's
   dashboard "sharing" still requires viewers to sign in — the query runs
   under the creator's credentials, not anonymous access. A truly public,
   no-login view means exporting a static PDF/image, which is why the
   dashboard below is a picture and not a live link.

## Stack

- **Databricks Free Edition** — Unity Catalog, Delta Lake, SQL
- Static HTML/CSS/JS for the showcase page (no framework, no build step)

## Built by

Del · [https://deliscool.github.io/portfolio-site-delguerra/](https://deliscool.github.io/portfolio-site-delguerra/)
