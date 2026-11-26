
import os

import duckdb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR, "data", "fleetsense.duckdb"
)

con = duckdb.connect(DB_PATH)

# Clear previous results
con.execute("DELETE FROM hourly_demand_by_zone")

# Calculate hourly demand by pickup zone
con.execute("""
    INSERT INTO hourly_demand_by_zone (
        pickup_hour,
        pickup_location_id,
        trip_count
    )
    SELECT
        DATE_TRUNC('hour', pickup_datetime),
        pickup_location_id,
        COUNT(*)
    FROM fact_trips
    WHERE pickup_datetime IS NOT NULL
      AND pickup_location_id IS NOT NULL
    GROUP BY
        DATE_TRUNC('hour', pickup_datetime),
        pickup_location_id
""")

# Verify results
total = con.execute(
    "SELECT COUNT(*) FROM hourly_demand_by_zone"
).fetchone()[0]

print("Hourly Demand Table Created Successfully!")
print("Total Hourly Demand Records:", total)

print("\nTop 10 Busy Zone-Hours:")

rows = con.execute("""
    SELECT
        pickup_hour,
        pickup_location_id,
        trip_count
    FROM hourly_demand_by_zone
    ORDER BY trip_count DESC
    LIMIT 10
""").fetchall()

for row in rows:
    print(row)

con.close()
