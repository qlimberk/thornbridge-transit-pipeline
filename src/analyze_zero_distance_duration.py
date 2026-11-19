import duckdb

con = duckdb.connect(
    "data/processed/fleetsense.duckdb",
    read_only=True
)

query = """
SELECT
    COUNT(*) AS zero_distance_records,
    COUNT(*) FILTER (
        WHERE tpep_dropoff_datetime > tpep_pickup_datetime
    ) AS positive_duration,
    COUNT(*) FILTER (
        WHERE tpep_dropoff_datetime = tpep_pickup_datetime
    ) AS zero_duration,
    COUNT(*) FILTER (
        WHERE tpep_dropoff_datetime < tpep_pickup_datetime
    ) AS negative_duration
FROM trips
WHERE trip_distance = 0
"""

result = con.execute(query).fetchdf()
print(result.to_string(index=False))

con.close()