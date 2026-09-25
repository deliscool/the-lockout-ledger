# The Lockout Ledger

A cross-platform data brief tracking real, publicly reported complaints about
Meta disabling Facebook and Instagram accounts, 2019–2026 — built as a
Databricks foundations project.

**Live page:** _link goes here once GitHub Pages is turned on_
**Live Databricks dashboard:** _pending_

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

## Stack

- **Databricks Free Edition** — Unity Catalog, Delta Lake, SQL
- Static HTML/CSS/JS for the showcase page (no framework, no build step)

## Built by

Del · [DevMoms](https://devmoms.com)
