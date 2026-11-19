from pathlib import Path
import duckdb

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 12-month dataset path
DATA_GLOB = (
    PROJECT_ROOT / "data" / "raw" / "yellow_tripdata_2024-*.parquet"
).as_posix()

# Database path
DB_PATH = PROJECT_ROOT / "data" / "processed" / "fleetsense.duckdb"

# Check dataset files
files = list(
    (PROJECT_ROOT / "data" / "raw").glob(
        "yellow_tripdata_2024-*.parquet"
    )
)

if len(files) != 12:
    raise FileNotFoundError(
        f"Expected 12 Parquet files, found {len(files)}"
    )

# Connect to persistent DuckDB database
con = duckdb.connect(str(DB_PATH))

try:

    print("FleetSense Trip Processing")
    print("--------------------------")

    # Verify quarantine table exists
    tables = [
        row[0] for row in con.execute("SHOW TABLES").fetchall()
    ]

    if "quarantine_trips" not in tables:
        raise RuntimeError("quarantine_trips table not found!")

    # Count original records
    total_records = con.execute(f"""
        SELECT COUNT(*)
        FROM read_parquet('{DATA_GLOB}')
    """).fetchone()[0]

    # Count quarantined records
    quarantine_count = con.execute("""
        SELECT COUNT(*)
        FROM quarantine_trips
    """).fetchone()[0]

    print("Total source records:", total_records)
    print("Quarantined records:", quarantine_count)

    # Create main trips table with valid records
    print("\nCreating main trips table...")

    con.execute(f"""
        CREATE OR REPLACE TABLE trips AS

        SELECT *
        FROM read_parquet('{DATA_GLOB}')

        WHERE
            tpep_pickup_datetime IS NOT NULL

            AND tpep_dropoff_datetime IS NOT NULL

            AND tpep_dropoff_datetime >= tpep_pickup_datetime

            AND (
                trip_distance >= 0
                OR trip_distance IS NULL
            )
    """)

    # Count valid records
    valid_count = con.execute("""
        SELECT COUNT(*)
        FROM trips
    """).fetchone()[0]

    # Verify quarantine table remains unchanged
    quarantine_after = con.execute("""
        SELECT COUNT(*)
        FROM quarantine_trips
    """).fetchone()[0]

    print("\nTrip Processing Summary")
    print("-----------------------")
    print("Total source records:", total_records)
    print("Valid trip records:", valid_count)
    print("Quarantined records:", quarantine_after)

    print(
        "Total processed records:",
        valid_count + quarantine_after
    )

    # Final verification
    if total_records == valid_count + quarantine_after:
        print("\nData verification successful!")
    else:
        print("\nWARNING: Record counts do not match!")

    print("\nMain trips table created successfully!")

finally:
    con.close()

print("Database connection closed.")