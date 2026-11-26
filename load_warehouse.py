
import glob
import os

import duckdb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "fleetsense.duckdb")
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

con = duckdb.connect(DB_PATH)

# Add CBD congestion fee column if it does not exist
con.execute("""
ALTER TABLE fact_trips
ADD COLUMN IF NOT EXISTS cbd_congestion_fee DOUBLE
""")

# Get all 12 monthly valid Parquet files
files = sorted(
    glob.glob(os.path.join(DATA_DIR, "valid_trips_2025-*.parquet"))
)

if len(files) != 12:
    raise ValueError(f"Expected 12 files, found {len(files)}")

# Clear existing records to make loading repeatable
con.execute("DELETE FROM fact_trips")

trip_id_offset = 0

for file_path in files:

    print("Loading:", os.path.basename(file_path))

    file_path_sql = file_path.replace("\\", "/").replace("'", "''")

    # Count records in current file
    count = con.execute(
        "SELECT COUNT(*) FROM read_parquet(?)",
        [file_path]
    ).fetchone()[0]

    # Insert records into fact_trips
    con.execute(f"""
        INSERT INTO fact_trips (
            trip_id,
            pickup_datetime,
            dropoff_datetime,
            pickup_location_id,
            dropoff_location_id,
            trip_distance,
            fare_amount,
            extra,
            mta_tax,
            tip_amount,
            tolls_amount,
            improvement_surcharge,
            total_amount,
            congestion_surcharge,
            airport_fee,
            cbd_congestion_fee
        )
        SELECT
            {trip_id_offset} + ROW_NUMBER() OVER (),
            tpep_pickup_datetime,
            tpep_dropoff_datetime,
            PULocationID,
            DOLocationID,
            trip_distance,
            fare_amount,
            extra,
            mta_tax,
            tip_amount,
            tolls_amount,
            improvement_surcharge,
            total_amount,
            congestion_surcharge,
            Airport_fee,
            cbd_congestion_fee
        FROM read_parquet('{file_path_sql}')
    """)

    trip_id_offset += count

    print("Records loaded:", count)

# Final record count
total = con.execute(
    "SELECT COUNT(*) FROM fact_trips"
).fetchone()[0]

print("\nDATA LOADING COMPLETED!")
print("Total records in fact_trips:", total)

con.close()
