from pathlib import Path

import duckdb

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dataset path
DATA_GLOB = (PROJECT_ROOT / "data" / "raw" / "yellow_tripdata_2024-*.parquet").as_posix()

# Database path
DB_PATH = PROJECT_ROOT / "data" / "processed" / "fleetsense.duckdb"

# Connect to persistent DuckDB database
con = duckdb.connect(str(DB_PATH))

print("FleetSense Quarantine Processing")
print("--------------------------------")

# Check invalid records and store them in quarantine table
con.execute(f"""
    CREATE OR REPLACE TABLE quarantine_trips AS

    SELECT
        *,
        CASE
            WHEN tpep_pickup_datetime IS NULL
                THEN 'Missing pickup timestamp'

            WHEN tpep_dropoff_datetime IS NULL
                THEN 'Missing dropoff timestamp'

            WHEN tpep_dropoff_datetime < tpep_pickup_datetime
                THEN 'Invalid trip timestamp'

            WHEN trip_distance < 0
                THEN 'Negative trip distance'
        END AS quarantine_reason

    FROM read_parquet('{DATA_GLOB}')

    WHERE
        tpep_pickup_datetime IS NULL
        OR tpep_dropoff_datetime IS NULL
        OR tpep_dropoff_datetime < tpep_pickup_datetime
        OR trip_distance < 0
""")

# Count quarantined records
count = con.execute("""
    SELECT COUNT(*)
    FROM quarantine_trips
""").fetchone()[0]

print("Quarantine processing completed!")
print("Total quarantined records:", count)

# Display sample records
print("\nSample Quarantined Records:")

sample = con.execute("""
    SELECT
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        trip_distance,
        quarantine_reason
    FROM quarantine_trips
    LIMIT 10
""").fetchdf()

print(sample.to_string(index=False))
# Verify quarantine reasons
print("\nQuarantine Reason Summary:")
print("--------------------------")

reason_summary = con.execute("""
    SELECT
        quarantine_reason,
        COUNT(*) AS record_count
    FROM quarantine_trips
    GROUP BY quarantine_reason
""").fetchdf()

print(reason_summary.to_string(index=False))
con.close()

print("\nDatabase connection closed.")
