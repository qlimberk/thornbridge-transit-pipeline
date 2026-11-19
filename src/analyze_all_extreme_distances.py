import duckdb

DB_PATH = "data/processed/fleetsense.duckdb"

con = duckdb.connect(DB_PATH, read_only=True)

print("\nALL EXTREME DISTANCE ANALYSIS")
print("=" * 60)

# 1. Overall Summary
print("\n1. Overall Summary")

query = """
SELECT
    COUNT(*) AS total_records,
    ROUND(MIN(trip_distance), 2) AS minimum_distance,
    ROUND(MAX(trip_distance), 2) AS maximum_distance,
    ROUND(AVG(trip_distance), 2) AS average_distance
FROM trips
WHERE trip_distance > 100
"""

print(con.execute(query).fetchdf().to_string(index=False))


# 2. VendorID Distribution
print("\n2. VendorID Distribution")

query = """
SELECT
    VendorID,
    COUNT(*) AS total_records,
    ROUND(AVG(trip_distance), 2) AS average_distance,
    ROUND(MAX(trip_distance), 2) AS maximum_distance
FROM trips
WHERE trip_distance > 100
GROUP BY VendorID
ORDER BY total_records DESC
"""

print(con.execute(query).fetchdf().to_string(index=False))


# 3. Payment Type Distribution
print("\n3. Payment Type Distribution")

query = """
SELECT
    payment_type,
    COUNT(*) AS total_records,
    ROUND(AVG(trip_distance), 2) AS average_distance,
    ROUND(MAX(trip_distance), 2) AS maximum_distance
FROM trips
WHERE trip_distance > 100
GROUP BY payment_type
ORDER BY total_records DESC
"""

print(con.execute(query).fetchdf().to_string(index=False))


# 4. Top 20 Extreme Distance Records
print("\n4. Top 20 Extreme Distance Records")

query = """
SELECT
    VendorID,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    trip_distance,
    total_amount,
    payment_type
FROM trips
WHERE trip_distance > 100
ORDER BY trip_distance DESC
LIMIT 20
"""

print(con.execute(query).fetchdf().to_string(index=False))

con.close()

print("\nAnalysis completed successfully!")