
import duckdb
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR, "data", "fleetsense.duckdb"
)

CSV_PATH = os.path.join(
    BASE_DIR, "raw", "taxi_zone_lookup.csv"
)

con = duckdb.connect(DB_PATH)

# Clear old zone records to make loading repeatable
con.execute("DELETE FROM dim_zones")

# Load Taxi Zone Lookup data
con.execute("""
    INSERT INTO dim_zones (
        location_id,
        borough,
        zone,
        service_zone
    )
    SELECT
        LocationID,
        Borough,
        Zone,
        service_zone
    FROM read_csv_auto(?)
""", [CSV_PATH])

# Verify loaded records
total = con.execute(
    "SELECT COUNT(*) FROM dim_zones"
).fetchone()[0]

print("Taxi Zone Data Loaded Successfully!")
print("Total Zone Records:", total)

print("\nFirst 10 Zones:")

rows = con.execute("""
    SELECT * FROM dim_zones
    ORDER BY location_id
    LIMIT 10
""").fetchall()

for row in rows:
    print(row)

con.close()
