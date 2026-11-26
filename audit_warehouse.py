
import os

import duckdb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "fleetsense.duckdb")

con = duckdb.connect(DB_PATH, read_only=True)

print("========== DATA QUALITY AUDIT ==========")

# 1. Records outside 2025
outside_2025 = con.execute("""
    SELECT COUNT(*)
    FROM fact_trips
    WHERE pickup_datetime < TIMESTAMP '2025-01-01'
       OR pickup_datetime >= TIMESTAMP '2026-01-01'
""").fetchone()[0]

print("Pickup dates outside 2025:", outside_2025)

# 2. Invalid duration
invalid_duration = con.execute("""
    SELECT COUNT(*)
    FROM fact_trips
    WHERE dropoff_datetime <= pickup_datetime
       OR date_diff('second', pickup_datetime, dropoff_datetime) > 86400
""").fetchone()[0]

print("Invalid trip durations:", invalid_duration)

# 3. Negative fare or total amount
negative_amounts = con.execute("""
    SELECT COUNT(*)
    FROM fact_trips
    WHERE fare_amount < 0 OR total_amount < 0
""").fetchone()[0]

print("Negative fare/total records:", negative_amounts)

# 4. Apply the metrics.py validation criteria
metrics_eligible = con.execute("""
    SELECT COUNT(*)
    FROM fact_trips
    WHERE pickup_datetime IS NOT NULL
      AND dropoff_datetime IS NOT NULL
      AND dropoff_datetime > pickup_datetime
      AND date_diff('microsecond',
                    pickup_datetime,
                    dropoff_datetime) <= 86400000000
      AND fare_amount >= 0
      AND total_amount >= 0
""").fetchone()[0]

print("Records eligible under metrics criteria:", metrics_eligible)

# 5. Monthly eligible records
print("\nMonthly eligible trip counts:")

rows = con.execute("""
    SELECT
        STRFTIME(pickup_datetime, '%Y-%m') AS month,
        COUNT(*) AS trip_count
    FROM fact_trips
    WHERE pickup_datetime IS NOT NULL
      AND dropoff_datetime IS NOT NULL
      AND dropoff_datetime > pickup_datetime
      AND date_diff('microsecond',
                    pickup_datetime,
                    dropoff_datetime) <= 86400000000
      AND fare_amount >= 0
      AND total_amount >= 0
    GROUP BY month
    ORDER BY month
""").fetchall()

for row in rows:
    print(row)

print("\n========== AUDIT COMPLETED ==========")

con.close()
