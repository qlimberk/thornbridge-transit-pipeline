@'
# Seasonality and Zone Analysis - Decision Log

**Date:** 22 November 2026

## 1. Objective

Analyze trip seasonality by hour, weekday, and month, identify the
top and bottom pickup and drop-off zones, investigate unusual
observations, and document the handling decisions.

## 2. Seasonality Findings

### Hourly Analysis

- Peak pickup hour: 18:00 (6 PM), with 2,955,724 trips.
- Lowest pickup hour: 04:00 (4 AM), with 243,796 trips.
- Trip activity generally increases during the day and reaches
  its highest level in the evening.

### Weekday Analysis

- Highest activity: Thursday, with 6,428,083 trips.
- Lowest activity: Monday, with 5,113,600 trips.
- Saturday also shows relatively high trip activity.

### Monthly Analysis

- Highest activity: October, with 3,833,741 trips.
- Lowest activity: January, with 2,964,581 trips.
- May, September, and October show relatively high activity.
- January and August show comparatively lower activity.
- Monthly totals combine all available years. They should not be
  interpreted as a year-over-year trend.

## 3. Zone Analysis

### Top Pickup Zones

| Zone ID | Trips |
|---|---:|
| 132 | 1,989,966 |
| 237 | 1,915,439 |
| 161 | 1,914,592 |
| 236 | 1,729,893 |
| 162 | 1,418,842 |
| 230 | 1,391,135 |
| 186 | 1,362,136 |
| 142 | 1,314,686 |
| 138 | 1,295,508 |
| 170 | 1,176,576 |

### Bottom Pickup Zones

| Zone ID | Trips |
|---|---:|
| 110 | 1 |
| 99 | 4 |
| 105 | 4 |
| 5 | 7 |
| 199 | 17 |
| 204 | 18 |
| 84 | 21 |
| 44 | 23 |
| 176 | 38 |
| 187 | 38 |

### Top Drop-off Zones

| Zone ID | Trips |
|---|---:|
| 236 | 1,793,144 |
| 237 | 1,723,796 |
| 161 | 1,539,894 |
| 230 | 1,310,972 |
| 170 | 1,212,845 |
| 162 | 1,183,358 |
| 142 | 1,141,623 |
| 239 | 1,131,525 |
| 68 | 1,075,680 |
| 141 | 1,061,285 |

### Bottom Drop-off Zones

| Zone ID | Trips |
|---|---:|
| 110 | 3 |
| 105 | 7 |
| 99 | 11 |
| 2 | 81 |
| 5 | 184 |
| 44 | 184 |
| 204 | 197 |
| 59 | 274 |
| 176 | 300 |
| 187 | 327 |

## 4. Anomaly Investigation

### 4.1 Zone Data Quality

The trips table contains 41,168,145 records.

| Check | Result |
|---|---:|
| NULL pickup zone IDs | 0 |
| NULL drop-off zone IDs | 0 |
| Minimum pickup zone ID | 1 |
| Maximum pickup zone ID | 265 |
| Distinct pickup zone IDs | 263 |
| Distinct drop-off zone IDs | 262 |

### 4.2 Missing Zone Activity

The following IDs from the range 1-265 had no observed activity
in the corresponding trip columns:

| Zone ID | Pickup | Drop-off |
|---|---|---|
| 103 | Missing | Missing |
| 104 | Missing | Missing |
| 199 | Present | Missing |

Lookup investigation identified:

- Zone 103: Manhattan, Governor's Island/Ellis Island/Liberty Island.
- Zone 104: Manhattan, Governor's Island/Ellis Island/Liberty Island.
- Zone 199: Bronx, Rikers Island.

Zone 199 had 17 pickup trips and no observed drop-off trips.

### 4.3 Lookup Table Validation

The taxi_zones table was checked for consistency.

| Check | Result |
|---|---:|
| Lookup records | 265 |
| Distinct Location IDs | 265 |
| Duplicate ID rows | 0 |
| NULL Location IDs | 0 |
| Unmatched pickup IDs | 0 |
| Unmatched drop-off IDs | 0 |

All observed non-NULL pickup and drop-off zone IDs matched
the taxi_zones lookup table.

## 5. Handling Decisions

| Observation | Decision | Reason |
|---|---|---|
| Very low trip counts in some zones | Retain | Low volume alone does not prove invalid data. |
| Zones 103 and 104 have no observed activity | Retain lookup records | No trips were observed, but no invalid IDs were found. |
| Zone 199 has pickup activity but no drop-off activity | Retain and document | The observation alone does not establish a data error. |
| NULL pickup zone IDs | No action required | None found. |
| NULL drop-off zone IDs | No action required | None found. |
| Duplicate lookup IDs | No action required | None found. |
| Unmatched pickup/drop-off IDs | No action required | None found. |

### Final Decision

No records were deleted or quarantined as a result of this
investigation.

Low-volume and no-activity zones are retained because the available
evidence does not establish that they are invalid records.

The analysis is observational and does not establish the cause
of differences in trip volume between zones.

## 6. Generated Charts

The following HTML charts were generated and saved in the reports
directory:

1. reports/hourly_seasonality.html
2. reports/weekday_seasonality.html
3. reports/monthly_seasonality.html
4. reports/top_pickup_zones.html
5. reports/bottom_pickup_zones.html
6. reports/top_dropoff_zones.html
7. reports/bottom_dropoff_zones.html

## 7. Data Handling and Reproducibility

- Analysis was performed using DuckDB read-only connections.
- The source trips table was not modified.
- The taxi_zones lookup table was used to validate zone IDs.
- The chart generation script is available at:
  src/create_seasonality_charts.py
- The HTML charts are stored in reports/.

## 8. Conclusion

Hourly, weekday, and monthly trip patterns were analyzed.
Top and bottom pickup and drop-off zones were identified and
visualized.

Zone data quality checks found no NULL zone IDs, duplicate
lookup IDs, or unmatched zone IDs. Low-volume and no-activity
zones were investigated and retained.

The findings and handling decisions are documented in this log.
'@ | Set-Content docs/decisions/seasonality-and-zone-analysis.md -Encoding utf8