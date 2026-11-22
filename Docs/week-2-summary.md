# Week 2 – Project Summary

## Project Information

- Project: FleetSense – Data Foundation and Operations Analytics
- Client: MetroCab
- Dataset: NYC TLC Yellow Taxi Trip Records
- Processing Database: DuckDB
- Reporting Period: January–December 2024
- Week: 2

## 1. Objective

The objective of Week 2 was to build and validate a reliable data pipeline for processing 12 consecutive months of NYC Yellow Taxi trip records.

The work focused on monthly data ingestion, DuckDB storage, data quality validation, quarantine handling, and repeatable processing.

## 2. Core Pipeline Implementation

Implemented the 12-month ingestion pipeline in `src/ingest.py`.

Key achievements:

- Downloaded 12 monthly Yellow Taxi Parquet datasets.
- Downloaded the NYC Taxi Zone Lookup CSV.
- Loaded zone information into DuckDB.
- Loaded monthly trip records into the database.
- Implemented ingestion tracking using the `ingestion_log` table.
- Added transaction-based monthly ingestion.
- Implemented checks to prevent reloading completed months.

**Total source records loaded: 41,169,720**

## 3. Idempotency Verification

The ingestion pipeline was executed a second time to verify repeatability.

Results:
- Months processed: 12
- New rows added: 0
- Monthly row counts remained unchanged.
- All previously loaded months were skipped.

The processing pipeline was also executed again, and the row counts of the `trips`, `quarantine_trips`, and `taxi_zones` tables remained unchanged.

## 4. Data Quality Validation

The 12 monthly source Parquet files were reconciled against the processed DuckDB database.

| Metric | Records |
|---|---:|
| Total source records | 41,169,720 |
| Valid records in trips | 41,168,145 |
| Quarantined records | 1,575 |

All 1,575 quarantined records were associated with invalid trip timestamps, specifically drop-off timestamps occurring before pickup timestamps.

Additional validation covered:

- NULL values in selected important columns.
- Invalid timestamps.
- Negative trip distances.
- Pickup and drop-off zone ID matching.
- Exact duplicate record comparisons.
- Negative financial values.
- Records outside the 2024 pickup-year period.

All pickup and drop-off location IDs matched the taxi zone lookup table.

## 5. Duplicate and Financial Data Investigation

Exact duplicate checks identified four duplicate groups in both the source data and processed database, with four extra duplicate rows in each.

Negative financial values were also identified and documented. These records were retained pending clarification of their business meaning.

Records outside the 2024 pickup-year period were also retained for further review.

## 6. Automated Testing and Code Quality

Automated tests were executed using Pytest.

Results:
- 2 tests passed.
- Ruff lint checks passed.
- GitHub Actions CI checks passed after resolving an import formatting issue.

## 7. Documentation and Deliverables

The following documentation was maintained:

- `Docs/week-2-core-pipeline-12-months.md`
- `Docs/week-2-task-1-validation.md`

The implementation and documentation were committed and pushed to the GitHub repository.

## 8. Pending Review Items

The following items remain documented for team or mentor review:

1. Confirm the business treatment of negative fare and total amounts.
2. Confirm the reporting treatment of records outside the 2024 pickup-year period.
3. Review the four exact duplicate groups.
4. Confirm final validation and quarantine rules.
5. Extend validation to additional required fields and business rules where applicable.

## 9. Conclusion

Week 2 established a repeatable 12-month NYC Yellow Taxi data ingestion pipeline using Python and DuckDB.

The source-to-database record counts reconciled when valid and quarantined records were considered together. The tested validation checks, row-count idempotency checks, automated tests, and code quality checks were completed successfully.

The remaining review items have been documented for further discussion with the team and mentor.

**Week 2 implementation and validation documentation are available in the FleetSense GitHub repository.**