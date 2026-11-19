# Week 2 – Task 2: Core Pipeline for 12 Months

## Objective

Build an idempotent ingestion pipeline to load 12 consecutive months of NYC Yellow Taxi trip data and the taxi zone lookup CSV into DuckDB.

## Implementation

Implemented in `src/ingest.py`.

Key features:
- Downloads monthly Yellow Taxi Parquet files if they are not already available.
- Downloads the taxi zone lookup CSV.
- Loads zone data into the `dim_zones` table.
- Loads monthly trip records into the `raw_trips` table.
- Tracks completed months using the `ingestion_log` table.
- Uses database transactions for monthly ingestion.
- Skips months that have already been loaded.
- Verifies monthly row counts before and after ingestion.

## Initial Ingestion

Command:

`python src/ingest.py`

Successfully loaded 12 months of 2024 Yellow Taxi data.

**Total records loaded: 41,169,720**

| Month | Records |
|---|---:|
| 2024-01 | 2,964,624 |
| 2024-02 | 3,007,526 |
| 2024-03 | 3,582,628 |
| 2024-04 | 3,514,289 |
| 2024-05 | 3,723,833 |
| 2024-06 | 3,539,193 |
| 2024-07 | 3,076,903 |
| 2024-08 | 2,979,183 |
| 2024-09 | 3,633,030 |
| 2024-10 | 3,833,771 |
| 2024-11 | 3,646,369 |
| 2024-12 | 3,668,371 |
| **Total** | **41,169,720** |

## Idempotency Verification

The same ingestion command was executed a second time.

Results:

- Months processed: 12
- New rows added: 0
- Monthly row counts unchanged: True
- All 12 months were skipped because they were already loaded.

### Monthly Row Count Comparison

| Month | Before | After |
|---|---:|---:|
| 2024-01 | 2,964,624 | 2,964,624 |
| 2024-02 | 3,007,526 | 3,007,526 |
| 2024-03 | 3,582,628 | 3,582,628 |
| 2024-04 | 3,514,289 | 3,514,289 |
| 2024-05 | 3,723,833 | 3,723,833 |
| 2024-06 | 3,539,193 | 3,539,193 |
| 2024-07 | 3,076,903 | 3,076,903 |
| 2024-08 | 2,979,183 | 2,979,183 |
| 2024-09 | 3,633,030 | 3,633,030 |
| 2024-10 | 3,833,771 | 3,833,771 |
| 2024-11 | 3,646,369 | 3,646,369 |
| 2024-12 | 3,668,371 | 3,668,371 |

## Automated Tests

Added an idempotency test in `tests/test_pipeline.py`.

The test:
- Creates sample Parquet files for all 12 months.
- Runs the ingestion process twice.
- Verifies that the first run inserts 12 records.
- Verifies that the second run inserts zero records.
- Confirms that monthly row counts remain unchanged.
- Verifies the ingestion log and total record count.

Test command:

`python -m pytest -v`

Result: 2 tests passed.

## Lint Check

Command:

`python -m ruff check src/ingest.py tests/test_pipeline.py`

Result: All checks passed.

## Acceptance Criteria

| Requirement | Status |
|---|---|
| Load 12 consecutive months into DuckDB | PASS |
| Load taxi zone lookup data | PASS |
| Second run adds zero new rows | PASS |
| Monthly row counts remain unchanged | PASS |
| Automated idempotency test | PASS |

## Conclusion

The 12-month ingestion pipeline was implemented and successfully verified. The second execution confirmed that the pipeline is idempotent and does not insert duplicate monthly records.
