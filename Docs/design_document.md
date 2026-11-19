Fleetsense_phase_1_Design_Document
Project: FleetSense – Data Foundation and Operations Analytics
Client: MetroCab (NYC Taxi Operator)
Phase: Phase 1
Team: Team No. 6
Status: Draft – Pending Team Review and Mentor Approval
Date: 15 November 2026
1. Project Overview
The objective of FleetSense Phase 1 is to build a reliable data foundation and operations analytics solution for MetroCab.
The project will use NYC Yellow Taxi trip data to analyse trip activity, revenue, trip duration, and hourly demand across different taxi zones.
The final solution will include a data pipeline, data validation, a DuckDB warehouse, analytical metrics, and an interactive dashboard.
2. Data Sources
The project will use the following datasets:
1.	NYC TLC Yellow Taxi Trip Records – trip-level information such as pickup time, drop-off time, pickup and drop-off zones, fares, and surcharges.
2.	NYC TLC Taxi Zone Lookup – information about taxi zone IDs and their names.
At least 12 consecutive months of Yellow Taxi data will be ingested.
Data will be stored in a suitable local project data directory. Raw datasets will not be committed to the GitHub repository.
3. Proposed Warehouse Model
The warehouse will be built using DuckDB.
Fact Table: fact_trips
Stores individual taxi trip records, including:
•	Pickup and drop-off timestamps
•	Pickup and drop-off location IDs
•	Trip distance
•	Fare amount
•	Extra charges, tolls and surcharges
•	Total amount
Dimension Table: dim_zones
Stores taxi zone information, including:
•	Location ID
•	Borough
•	Zone name
•	Service zone
Dimension Table: dim_calendar
Stores calendar information such as:
•	Date
•	Day
•	Weekday
•	Month
•	Year
Analytical Table: hourly_demand_by_zone
Stores hourly trip demand grouped by taxi zone and time.
4. Metric Definitions
The following metrics will be used consistently throughout the project:
•	Total Trips: Count of valid taxi trip records.
•	Total Revenue: Sum of the selected revenue amount. The exact treatment of tolls and surcharges will be documented.
•	Average Fare: Total fare amount divided by valid trip count.
•	Trip Duration: Difference between drop-off and pickup timestamps, measured in minutes.
•	Hourly Demand: Number of trips grouped by pickup hour and pickup zone.
•	Utilisation Proxy: A clearly documented measure based on available trip activity data. It will not be treated as actual vehicle utilisation unless supporting vehicle availability data exists.
5. Data Quality and Validation
The pipeline will check:
•	Required columns and data types.
•	Missing or invalid values.
•	Drop-off time occurring after pickup time.
•	Non-negative fare values.
•	Valid pickup and drop-off zone IDs.
•	Duplicate trip records.
Invalid records will be quarantined with reason codes. Data quality results and processing logs will be maintained.
The pipeline should be repeatable. Running it a second time should not add duplicate records.
6. Risks and Mitigation
Risk	Mitigation
Missing or corrupted monthly data	Verify downloaded files before ingestion
Duplicate records	Implement duplicate checks and repeatable loading
Invalid trip records	Apply validation rules and quarantine failures
Unknown zone IDs	Validate against the zone lookup dataset
Different metric interpretations	Document metric definitions and calculations
Large data volume	Use Parquet and DuckDB for efficient processing
7. Technology Stack
•	Python 3.11+
•	DuckDB
•	Parquet
•	Pandas or Polars
•	Pandera or Great Expectations
•	Streamlit
•	Git and GitHub
•	Pytest
•	GitHub Actions
The final tool choices will be confirmed by the team.
8. Reproducibility and Delivery
The project should support rebuilding the warehouse, features, and analytical results using a documented command.
The team will maintain:
•	Source code and documentation in GitHub.
•	Data validation and unit tests.
•	Processing logs.
•	A README and data dictionary.
•	A reproducible workflow.
•	A dashboard and findings report.
9. Pending Team and Mentor Decisions
The following items require confirmation:
•	Final data ingestion approach.
•	Final warehouse schema and SQL design.
•	Exact revenue calculation rules.
•	Utilisation proxy definition.
•	Individual team responsibilities.
•	Mentor review and approval.
Document Status: Draft – Not yet approved by mentor.

