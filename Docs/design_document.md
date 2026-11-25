# FleetSense – Design Document

## 1. Project Overview

FleetSense is a data analytics project based on NYC TLC Yellow Taxi trip records. The project aims to build a reliable data pipeline and analytical warehouse to understand taxi trip activity, revenue, demand patterns and operational trends.

The project will process at least 12 consecutive months of Yellow Taxi data for January to December 2025.

## 2. Data Sources and Ingestion

The project uses the following datasets:

1. **NYC TLC Yellow Taxi Trip Records:** Contains trip-level information such as pickup time, drop-off time, pickup and drop-off zones, trip distance, fares, surcharges and total amounts.
2. **NYC TLC Taxi Zone Lookup:** Contains taxi zone IDs, boroughs, zone names and service zones.

### Data Storage

- Raw datasets are stored in the local project `raw/` directory.
- Processed and validated datasets are stored in `data/processed/`.
- Raw datasets will not be committed to the GitHub repository.
- The pipeline processes 12 monthly Yellow Taxi Parquet files for January–December 2025.
- Processing is designed to be repeatable.

## 3. Proposed Warehouse Model

The analytical warehouse is planned to be built using DuckDB.

### Fact Table: fact_trips

Stores individual taxi trip records, including:

- Pickup and drop-off timestamps.
- Pickup and drop-off location IDs.
- Trip distance.
- Fare amount.
- Extra charges, tolls and surcharges.
- Total amount.

### Dimension Table: dim_zones

Stores taxi zone information, including:

- Location ID.
- Borough.
- Zone name.
- Service zone.

### Dimension Table: dim_calendar

Stores calendar information, including:

- Date.
- Day.
- Weekday.
- Month.
- Year.

### Analytical Table: hourly_demand_by_zone

Stores hourly trip demand grouped by pickup zone and pickup time.

**Note:** This is the proposed warehouse design. Tables will be marked as implemented only after their creation and validation.

## 4. Metric Definitions

The following metrics are used consistently throughout the project. Monthly metrics are calculated using valid taxi trip records from January to December 2025.

- **Total Trips:** Count of valid taxi trip records after applying data validation rules.
- **Total Revenue:** Sum of `total_amount` for all valid trips. This includes the fare and additional charges recorded in the total amount.
- **Average Fare:** Mean of `fare_amount` across all valid trips.
- **Average Trip Duration:** Mean difference between drop-off and pickup timestamps, measured in minutes.
- **Hourly Demand:** Number of valid trips grouped by pickup hour and pickup zone.
- **Aggregate Trip Activity Proxy:** Total valid trip-duration minutes divided by the total calendar minutes in the month, multiplied by 100.

### Utilisation Proxy Limitation

The aggregate trip activity proxy measures total trip activity relative to the calendar time in a month. It can exceed 100% because multiple taxis can operate simultaneously.

This metric does not represent actual fleet utilisation. Actual fleet utilisation requires information about the number of available vehicles and their available operating time.

Monthly metric results are saved in `reports/metrics_2025.csv`. An annual summary is also generated.

## 5. Data Quality and Validation

The pipeline performs the following validation checks:

- Required columns and data types.
- Missing or invalid values.
- Drop-off timestamp must be after pickup timestamp.
- Trip duration must be greater than zero and no more than 24 hours.
- Fare and total amounts must be non-negative.
- Duplicate trip records.
- Valid pickup and drop-off zone IDs, where zone lookup validation is implemented.

Invalid records are separated into quarantine files with appropriate reason codes.

Processing logs and data quality results are maintained.

The pipeline supports repeatable processing to avoid duplicate records when executed again.

## 6. Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Missing or corrupted monthly data | Verify downloaded files before ingestion |
| Duplicate records | Implement duplicate checks and repeatable loading |
| Invalid trip records | Apply validation rules and quarantine failures |
| Unknown zone IDs | Validate against the zone lookup dataset |
| Different metric interpretations | Document metric definitions and calculations |
| Large data volume | Use Parquet and DuckDB for efficient processing |
| Misleading utilisation results | Document the proxy calculation and its limitations |

## 7. Technology Stack

The project uses or plans to use the following technologies:

- Python 3.11+
- DuckDB
- Parquet
- Pandas or Polars
- Pandera or Great Expectations
- Streamlit
- Git and GitHub
- Pytest
- GitHub Actions

Final tool choices will be confirmed by the team.

## 8. Reproducibility and Delivery

The project aims to support rebuilding the warehouse, features and analytical results using documented commands.

The team will maintain:

- Source code and documentation in GitHub.
- Data validation and unit tests.
- Processing logs.
- README and data dictionary.
- Reproducible workflow.
- Dashboard and findings report.
- Monthly metrics output in `reports/metrics_2025.csv`.

Raw datasets will remain outside the GitHub repository.

## 9. Pending Team and Mentor Decisions

The following items require confirmation:

- Final data ingestion approach.
- Final warehouse schema and SQL design.
- Exact revenue calculation rules.
- Final utilisation proxy definition.
- Individual team responsibilities.
- Mentor review and approval.

**Document Status:** Draft – Not yet approved by mentor.
## 10. Results and Analysis

### 10.1 Data Processing Results

The FleetSense project successfully processed NYC TLC Yellow Taxi trip data for all 12 months of 2025.

- Total monthly files processed: 12
- Total records loaded into the warehouse: 45,327,896
- Dimension zones: 265
- Calendar records: 365
- Hourly demand records: 1,400,032

### 10.2 Yearly Summary – 2025

The monthly summary files contain 45,327,896 trip records.

| Metric | Result |
|---|---:|
| Total Trip Records | 45,327,896 |
| Total Revenue | $1,313,420,509.64 |
| Mean of Monthly Average Fare | $20.15 |
| Mean of Monthly Average Distance | 6.40 miles |
| Total Distance | 291,089,750.32 miles |

**Data Quality Note:** The warehouse audit identified 45,322,551 eligible records for 2025. The warehouse contains 45,327,896 records in total, including 29 pickup dates outside 2025 and records that failed certain quality checks.

### 10.3 Monthly Analysis

Based on the generated monthly summary:

- December recorded the highest monthly revenue of $132,913,650.02.
- February recorded the lowest monthly revenue of $90,392,497.83.
- December had the highest average fare of approximately $22.84.
- May recorded the highest average trip distance of approximately 7.11 miles.

### 10.4 Zone Analysis

The Top 10 Pickup Zones report and graph were generated using the January 2025 service-day trip dataset. The analysis includes trip counts, revenue and average fare for the top pickup zones.

This analysis represents January data only and should not be interpreted as a full-year zone ranking.