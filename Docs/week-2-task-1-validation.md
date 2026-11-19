# Week 2 - Task 1: Data Quality Validation Report

## 1. Project Information

- Project: FleetSense
- Dataset: NYC TLC Yellow Taxi Trip Records
- Processing Database: `data/processed/fleetsense.duckdb`
- Source Format: Parquet
- Validation Date: 19 November 2026

## 2. Source and Database Reconciliation

The 12 monthly source Parquet files were compared with the processed database.

| Metric | Records |
|---|---:|
| Total source records | 41,169,720 |
| Valid records in `trips` | 41,168,145 |
| Records in `quarantine_trips` | 1,575 |
| Total processed and quarantined | 41,169,720 |

The sum of valid and quarantined records matches the total source record count.

For 2024 pickup-year records:

| Metric | Records |
|---|---:|
| Source records | 41,169,664 |
| Database records | 41,168,089 |
| Difference | 1,575 |

The monthly source-to-database differences matched the monthly quarantine counts.

**Result: PASS**

## 3. Quarantine Validation

A total of 1,575 records were present in `quarantine_trips`.

| Check | Result |
|---|---:|
| Total quarantined records | 1,575 |
| Records with reason `Invalid trip timestamp` | 1,575 |
| Records with drop-off before pickup | 1,575 |
| NULL pickup timestamps | 0 |
| NULL drop-off timestamps | 0 |
| Equal pickup and drop-off timestamps | 0 |

All quarantined records were associated with invalid trip timestamps.

**Result: PASS**

## 4. Processing Idempotency

The processing script `src/process_trips.py` was executed again to test repeatability.

| Table | Before | After |
|---|---:|---:|
| `trips` | 41,168,145 | 41,168,145 |
| `quarantine_trips` | 1,575 | 1,575 |
| `taxi_zones` | 265 | 265 |

The row counts remained unchanged after the second processing run.

This confirms row-count idempotency for the tested execution. It does not independently prove byte-for-byte or row-by-row equality.

**Result: PASS (row-count idempotency)**

## 5. Duplicate Record Validation

Exact full-row duplicate checks were performed on both the source Parquet files and the processed `trips` table.

| Metric | Source | Processed Database |
|---|---:|---:|
| Duplicate groups | 4 | 4 |
| Extra duplicate rows | 4 | 4 |

The same number of exact duplicate groups and extra duplicate rows were found in the source and processed data.

No evidence of additional exact duplicates introduced by processing was identified from these aggregate checks.

The four duplicate groups each contained two identical rows.

**Result: PASS (source and database duplicate counts match)**

## 6. NULL Value Validation

The following fields were checked in the `trips` table.

| Column | NULL Records |
|---|---:|
| `tpep_pickup_datetime` | 0 |
| `tpep_dropoff_datetime` | 0 |
| `VendorID` | 0 |
| `trip_distance` | 0 |
| `fare_amount` | 0 |
| `total_amount` | 0 |

No NULL values were found in the selected fields.

Pickup and drop-off location IDs were also checked separately during zone validation.

**Result: PASS**

## 7. Timestamp and Distance Validation

The processed `trips` table was checked for invalid timestamps and negative trip distances.

| Check | Invalid Records |
|---|---:|
| Drop-off earlier than pickup | 0 |
| Negative trip distance | 0 |

No records violating these two conditions were found in the processed trips table.

**Result: PASS**

## 8. Negative Fare and Total Amount Analysis

Negative financial values were found in the processed data.

Full `trips` table results:

| Metric | Records |
|---|---:|
| Negative fare | 731,007 |
| Negative total amount | 609,330 |
| Both fare and total negative | 606,469 |
| Negative fare only | 124,538 |
| Negative total only | 2,861 |

The same aggregate counts were found when the source Parquet files were queried using the processing filters.

These records were not deleted or quarantined during this validation.

Negative amounts may represent reversals, refunds, adjustments, or anomalies. Their exact business meaning has not yet been confirmed.

**Result: REVIEW REQUIRED**

The design document specifies non-negative fare values. This requirement needs a documented business decision before negative fare records can be accepted, excluded, or quarantined.

## 9. Negative Charge Component Analysis

The following counts were found among 2024 pickup-year records.

| Component | Negative Records |
|---|---:|
| `fare_amount` | 731,006 |
| `extra` | 304,556 |
| `mta_tax` | 583,149 |
| `tip_amount` | 1,331 |
| `tolls_amount` | 49,268 |
| `improvement_surcharge` | 606,097 |
| `congestion_surcharge` | 495,730 |
| `Airport_fee` | 99,252 |
| `total_amount` | 609,329 |

These counts overlap. They must not be added together to calculate the number of distinct trips with negative values.

Negative financial components were retained pending clarification of their business meaning.

**Result: REVIEW REQUIRED**

## 10. Pickup and Drop-off Zone Validation

The `PULocationID` and `DOLocationID` columns were checked against `taxi_zones.LocationID` using LEFT JOIN validation.

| Check | Result |
|---|---:|
| Total trips | 41,168,145 |
| NULL pickup IDs | 0 |
| NULL drop-off IDs | 0 |
| Unmatched pickup IDs | 0 |
| Unmatched drop-off IDs | 0 |
| Trips with unmatched zones | 0 |

Every pickup and drop-off location ID matched an entry in the taxi zone lookup table.

**Result: PASS**

## 11. Additional Source Records Outside 2024

The source Parquet files contained 56 records whose pickup year was not 2024.

| Pickup Year | Records |
|---|---:|
| 2002 | 11 |
| 2008 | 10 |
| 2009 | 18 |
| 2023 | 10 |
| 2025 | 5 |
| 2026 | 2 |
| **Total** | **56** |

These records were retained in the processed `trips` table. They were not removed solely because their pickup year was outside 2024.

Their treatment should be confirmed against the project's intended reporting period.

**Result: REVIEW REQUIRED**

## 12. Validation Summary

| Validation Area | Status |
|---|---|
| Source/database reconciliation | PASS |
| Quarantine validation | PASS |
| Processing row-count idempotency | PASS |
| Duplicate count comparison | PASS |
| Selected NULL checks | PASS |
| Timestamp validation | PASS |
| Negative distance validation | PASS |
| Zone ID validation | PASS |
| Negative financial values | REVIEW REQUIRED |
| Non-2024 pickup-year records | REVIEW REQUIRED |

## 13. Pending Actions

1. Confirm the business treatment of negative fare and total amounts.
2. Confirm whether records outside the 2024 reporting period should be retained.
3. Review the four exact duplicate groups and decide whether deduplication is required.
4. Confirm the final validation and quarantine rules with the team or mentor.
5. Extend validation to other required fields and business rules where applicable.

## 14. Conclusion

The source-to-database record counts reconcile when valid and quarantined records are considered together.

The processed dataset passed the tested timestamp, negative distance, selected NULL, and pickup/drop-off zone checks.

The repeated processing run preserved table row counts. Source and processed data also had matching aggregate counts of exact duplicate groups.

Negative financial values and records outside the 2024 pickup-year period remain documented review items. No additional deletion or quarantine action was taken for these records during this validation.

This report documents the checks performed and their observed results. It does not imply that every requirement in the draft design document or the complete Week 2 Task 1 acceptance checklist has been satisfied.
