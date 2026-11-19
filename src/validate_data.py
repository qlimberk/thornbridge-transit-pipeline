from pathlib import Path

import duckdb

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 12-month dataset path
DATA_GLOB = (PROJECT_ROOT / "data" / "raw" / "yellow_tripdata_2024-*.parquet").as_posix()

# Persistent Database path
DB_DIR = PROJECT_ROOT / "data" / "processed"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "fleetsense.duckdb"

# Connect to persistent DuckDB database
con = duckdb.connect(str(DB_PATH))
print("FleetSense Data Validation")
print("--------------------------")

# Check whether dataset files exist
files = list((PROJECT_ROOT / "data" / "raw").glob("yellow_tripdata_2024-*.parquet"))

if not files:
    raise FileNotFoundError("No Parquet dataset files found!")

print(f"Dataset files found: {len(files)}")

# Run data validation
query = f"""
    SELECT
        COUNT(*) AS total_records,

        COUNT(*) FILTER (
            WHERE tpep_pickup_datetime IS NULL
        ) AS missing_pickup,

        COUNT(*) FILTER (
            WHERE tpep_dropoff_datetime IS NULL
        ) AS missing_dropoff,

        COUNT(*) FILTER (
            WHERE passenger_count IS NULL
        ) AS missing_passenger_count,

        COUNT(*) FILTER (
            WHERE trip_distance < 0
        ) AS negative_trip_distance,

        COUNT(*) FILTER (
            WHERE fare_amount < 0
        ) AS negative_fare_amount,

        COUNT(*) FILTER (
            WHERE tpep_dropoff_datetime < tpep_pickup_datetime
        ) AS invalid_trip_time

    FROM read_parquet('{DATA_GLOB}')
"""

result = con.execute(query).fetchdf()

print("\nValidation Results:")
print(result.to_string(index=False))
# Investigate invalid trip timestamps
print("\nSample Invalid Trip Records:")
print("-----------------------------")

invalid_records = con.execute(f"""
    SELECT
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        fare_amount
    FROM read_parquet('{DATA_GLOB}')
    WHERE tpep_dropoff_datetime < tpep_pickup_datetime
    LIMIT 20
""").fetchdf()

print(invalid_records.to_string(index=False))
# Investigate missing passenger count
print("\nSample Missing Passenger Count Records:")
print("----------------------------------------")

missing_passengers = con.execute(f"""
    SELECT
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        fare_amount
    FROM read_parquet('{DATA_GLOB}')
    WHERE passenger_count IS NULL
    LIMIT 10
""").fetchdf()

print(missing_passengers.to_string(index=False))


# Investigate negative fare amounts
print("\nSample Negative Fare Records:")
print("------------------------------")

negative_fares = con.execute(f"""
    SELECT
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        fare_amount
    FROM read_parquet('{DATA_GLOB}')
    WHERE fare_amount < 0
    LIMIT 10
""").fetchdf()

print(negative_fares.to_string(index=False))
con.close()

print("\nData Validation Completed!")
