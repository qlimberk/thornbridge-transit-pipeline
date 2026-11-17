# Thornbridge Transit Pipeline

12-month data ingestion, validation, and DuckDB dimensional modeling pipeline for **Thornbridge Patient Transit**.

## Overview
Transforms raw patient transit trip logs and zone lookups into an analytics-ready star schema in DuckDB, enforcing Thornbridge's **04:00 AM service-day billing cut-off** (trips occurring between `00:00` and `03:59` are attributed to the previous calendar day).

## Repository Structure
* `/ingestion` — Idempotent loading scripts for 12 consecutive months of trip data and zone lookups.
* `/validation` — Data quality checks, quarantine logging with reason codes, and row-count reconciliation.
* `/sql` — Documented DuckDB SQL transformations building `dim_zones`, `dim_calendar`, `fact_trips`, and `hourly_demand_per_zone`.

## Core Business Rule: Service Day
Daily billing totals run from **04:00 to 03:59** the following morning:
```sql
CAST(pickup_datetime - INTERVAL '4 hours' AS DATE) AS service_date
