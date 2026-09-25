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

## Top 4 things I learned — for PMs, product owners, and program managers

I came into this as a platform admin, not a data engineer. Here's what
stood out as genuinely useful for anyone who scopes, ships, or governs
products with data behind them — not just people who write the SQL.

1. **It replaces "who has the master CSV?" with one governed source of
   truth.** Every team I've worked on has a version of this pain point: a
   spreadsheet gets emailed around, someone edits a copy, and nobody's sure
   which one is current. Unity Catalog gives every table and column one
   real address (`catalog.schema.table`) with its own access controls, so
   "where's the current data" stops being a Slack question. For a PM, that's
   fewer status-check pings and fewer decisions made on stale numbers.
2. **It shortens the gap between "raw data" and "something stakeholders can
   see."** This whole project went from a messy CSV to a working dashboard
   without a data engineer, a BI license, or a deploy pipeline — load the
   file, write SQL, pin a chart. That's the prototyping win: you can hand a
   product decision a real visual instead of a slide built from a manual
   pivot table, and iterate on it live instead of re-exporting a new chart
   every time the ask changes.
3. **Data cleaning is still the real bottleneck — Databricks doesn't remove
   it, it just gives you a place to see it.** My biggest time sink wasn't
   the platform, it was the CSV itself: inconsistent date formats, one
   partial-year data point sitting next to full-year ones, categories that
   needed merging before they'd chart cleanly. The lesson for a PM scoping
   a data project: budget real time for data cleanup before analysis,
   because "we have the data" and "the data is usable" are different
   milestones — and a bad assumption there produced a genuinely misleading
   chart in this project (see the SQL notebook's query 4b for the fix).
4. **A "streamlined" pipeline still has a chain of custody worth mapping.**
   CSV → Delta table → SQL → dashboard is simple to describe but each hop
   is a place scope, permissions, or definitions can drift — exactly what
   happened when a chart's "most recent year" logic didn't match what the
   underlying data actually supported. For a program manager, the takeaway
   isn't "trust the pipeline," it's that each stage deserves its own
   sign-off, the same way you'd checkpoint any multi-stage deliverable.

## Stack

- **Databricks Free Edition** — Unity Catalog, Delta Lake, SQL
- Static HTML/CSS/JS for the showcase page (no framework, no build step)

## Built by

Del · [https://deliscool.github.io/portfolio-site-delguerra/](https://deliscool.github.io/portfolio-site-delguerra/)
