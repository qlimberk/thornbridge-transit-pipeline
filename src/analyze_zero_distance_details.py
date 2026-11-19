import duckdb

con = duckdb.connect("data/processed/fleetsense.duckdb", read_only=True)

print("Zero-Distance Records Analysis")
print("--------------------------------")

queries = {
    "VendorID Distribution": """
        SELECT VendorID, COUNT(*) AS total_records
        FROM trips
        WHERE trip_distance = 0
        GROUP BY VendorID
        ORDER BY total_records DESC
    """,
    "Passenger Count Distribution": """
        SELECT passenger_count, COUNT(*) AS total_records
        FROM trips
        WHERE trip_distance = 0
        GROUP BY passenger_count
        ORDER BY passenger_count
    """,
    "Payment Type Distribution": """
        SELECT payment_type, COUNT(*) AS total_records
        FROM trips
        WHERE trip_distance = 0
        GROUP BY payment_type
        ORDER BY total_records DESC
    """,
}

for title, query in queries.items():
    print(f"\n{title}")
    print(con.execute(query).fetchdf().to_string(index=False))

con.close()
