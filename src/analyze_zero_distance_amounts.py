import duckdb

con = duckdb.connect(
    "data/processed/fleetsense.duckdb",
    read_only=True
)

print("Zero-Distance Records - Total Amount Analysis")
print("----------------------------------------------")

query = """
SELECT
    COUNT(*) AS total_zero_distance_records,

    COUNT(*) FILTER (
        WHERE total_amount < 0
    ) AS negative_amount_records,

    COUNT(*) FILTER (
        WHERE total_amount = 0
    ) AS zero_amount_records,

    COUNT(*) FILTER (
        WHERE total_amount > 0
    ) AS positive_amount_records,

    COUNT(*) FILTER (
        WHERE total_amount IS NULL
    ) AS null_amount_records

FROM trips
WHERE trip_distance = 0
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()