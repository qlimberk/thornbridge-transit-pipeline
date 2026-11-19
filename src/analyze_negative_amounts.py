import duckdb

con = duckdb.connect("data/processed/fleetsense.duckdb", read_only=True)

print("Negative Total Amount Analysis")
print("--------------------------------")

queries = {
    "VendorID Distribution": """
        SELECT
            VendorID,
            COUNT(*) AS total_records
        FROM trips
        WHERE total_amount < 0
        GROUP BY VendorID
        ORDER BY total_records DESC
    """,
    "Payment Type Distribution": """
        SELECT
            payment_type,
            COUNT(*) AS total_records
        FROM trips
        WHERE total_amount < 0
        GROUP BY payment_type
        ORDER BY total_records DESC
    """,
    "Trip Distance Analysis": """
        SELECT
            COUNT(*) AS total_records,
            MIN(trip_distance) AS minimum_distance,
            MAX(trip_distance) AS maximum_distance,
            AVG(trip_distance) AS average_distance
        FROM trips
        WHERE total_amount < 0
    """,
    "Negative Amount Range": """
        SELECT
            MIN(total_amount) AS minimum_amount,
            MAX(total_amount) AS maximum_amount,
            AVG(total_amount) AS average_amount
        FROM trips
        WHERE total_amount < 0
    """,
}

for title, query in queries.items():
    print(f"\n{title}")
    print(con.execute(query).fetchdf().to_string(index=False))

con.close()
