# Week 3 – Data Quality Analysis

## 1. Project Overview

This document records the data quality analysis performed
on the FleetSense transit trip dataset during Week 3.

The analysis was performed using Python and DuckDB
to understand the dataset structure, identify potential
data anomalies, and validate timestamp quality.

### Analysis Objectives

- Analyze trip distribution by year.
- Investigate historical records.
- Examine trip duration statistics.
- Identify unusually long trips.
- Check for possible duplicate records.
- Validate pickup and drop-off timestamps.

### Database

Database: `data/processed/fleetsense.duckdb`

Main table: `trips`

Total records analyzed: 41,168,145

---

## 2. Year-wise Trip Analysis

The trip records were grouped by pickup year
to understand the distribution of trips across years.

| Year | Total Trips |
|------|------------:|
| 2002 | 11 |
| 2008 | 10 |
| 2009 | 18 |
| 2023 | 10 |
| 2024 | 41,168,089 |
| 2025 | 5 |
| 2026 | 2 |

### Observation

The analysis shows that the dataset contains
41,168,089 trips from 2024, while only a small
number of records belong to other years.

This unusual distribution was identified as a
potential data quality issue requiring further
investigation.

---

## 3. Historical Records Investigation

Records outside the dominant year (2024) were
investigated by examining their pickup and
drop-off timestamps.

The following historical years were identified:

| Year | Total Trips |
|------|------------:|
| 2002 | 11 |
| 2008 | 10 |
| 2009 | 18 |
| 2023 | 10 |
| 2025 | 5 |
| 2026 | 2 |

### Observations

- Records from 2002, 2008, and 2009 were found.
- Some trips had unusually long durations.
- Some trips crossed calendar-year boundaries.
- These records require further investigation
  to determine their validity.

No records were deleted or modified during
this investigation.

---

## 4. Trip Duration Analysis

Trip duration was calculated using the difference
between pickup and drop-off timestamps.

The average and maximum trip durations were
analyzed for each pickup year.

| Year | Total Trips | Average Duration (Minutes) | Maximum Duration (Minutes) |
|------|------------:|---------------------------:|---------------------------:|
| 2002 | 11 | 528.94 | 1308.30 |
| 2008 | 10 | 942.95 | 1381.70 |
| 2009 | 18 | 344.65 | 1322.82 |
| 2023 | 10 | 10.16 | 18.75 |
| 2024 | 41,168,089 | 17.47 | 9767.52 |
| 2025 | 5 | 215.31 | 443.27 |
| 2026 | 2 | 643.45 | 1265.97 |

### Observations

- The average trip duration for 2024 was 17.47 minutes.
- The maximum recorded trip duration in 2024
  was 9767.52 minutes.
- Some years with very few records showed
  unusually high average durations.
- These results indicate potential duration
  anomalies that require further investigation.

---

## 5. Unusually Long Trips Investigation

The longest trip durations in the 2024 dataset
were investigated by sorting trips in descending
order of calculated duration.

The analysis identified several trips with
extremely long durations.

The longest recorded trip lasted approximately
9767.52 minutes (around 6.78 days).

### Observations

- Several trips had durations exceeding multiple days.
- These durations are unusual for normal taxi trips.
- Such records may indicate potential data quality
  issues or unusual recording circumstances.
- Further investigation is required to determine
  the actual cause of these long durations.

No records were deleted or modified during
this investigation.

---

## 6. Duplicate Records Analysis

A preliminary duplicate check was performed
using the following fields:

- Pickup timestamp
- Drop-off timestamp
- Pickup location ID
- Drop-off location ID

The analysis produced the following results:

| Metric | Count |
|--------|------:|
| Total Trips | 41,168,145 |
| Unique Combinations | 40,617,447 |
| Possible Duplicate Combinations | 550,698 |

### Observations

- The analysis identified 550,698 records
  belonging to repeated combinations of the
  selected fields.
- These records are considered possible duplicates,
  not confirmed duplicate trips.
- Different trips may share the same timestamps
  and location IDs.
- Further investigation is required before
  classifying or removing any records.

No records were deleted or modified.

---

## 7. Timestamp Data Quality Validation

Pickup and drop-off timestamps were checked
to identify missing timestamp values and
negative trip durations.

The validation produced the following results:

| Validation Check | Count |
|------------------|------:|
| Total Trips | 41,168,145 |
| NULL Pickup Timestamps | 0 |
| NULL Drop-off Timestamps | 0 |
| Negative Trip Durations | 0 |

### Observations

- No NULL pickup timestamps were identified.
- No NULL drop-off timestamps were identified.
- No negative trip durations were found.
- However, unusually long positive trip durations
  were identified during the duration analysis.

These results indicate that the timestamp fields
passed the basic NULL and negative-duration checks.
Further investigation may still be required for
unusually long trip durations.

No records were deleted or modified.

---

## 8. Key Findings and Conclusion

### Key Findings

1. The dataset contains 41,168,145 trip records.
2. The majority of records belong to the year 2024.
3. A small number of records belong to other years,
   including 2002, 2008, 2009, 2023, 2025, and 2026.
4. The average trip duration in 2024 was 17.47 minutes.
5. The maximum recorded trip duration was 9767.52 minutes.
6. A preliminary duplicate check identified
   550,698 possible duplicate combinations.
7. No NULL pickup timestamps, NULL drop-off timestamps,
   or negative trip durations were identified.

### Conclusion

The Week 3 data quality analysis helped identify
unusual year distributions, unusually long trip
durations, and possible duplicate combinations.

Basic timestamp validation checks passed successfully.

The identified anomalies require further investigation
before any records can be classified as invalid
or removed.

No original database records were modified or deleted
during this analysis.

---

