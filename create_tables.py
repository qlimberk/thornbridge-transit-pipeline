
import duckdb
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "fleetsense.duckdb")

con = duckdb.connect(DB_PATH)

# Fact Table
con.execute("""
CREATE TABLE IF NOT EXISTS fact_trips (
    trip_id BIGINT,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    pickup_location_id INTEGER,
    dropoff_location_id INTEGER,
    trip_distance DOUBLE,
    fare_amount DOUBLE,
    extra DOUBLE,
    mta_tax DOUBLE,
    tip_amount DOUBLE,
    tolls_amount DOUBLE,
    improvement_surcharge DOUBLE,
    total_amount DOUBLE,
    congestion_surcharge DOUBLE,
    airport_fee DOUBLE
)
""")

# Zone Dimension Table
con.execute("""
CREATE TABLE IF NOT EXISTS dim_zones (
    location_id INTEGER,
    borough VARCHAR,
    zone VARCHAR,
    service_zone VARCHAR
)
""")

# Calendar Dimension Table
con.execute("""
CREATE TABLE IF NOT EXISTS dim_calendar (
    date DATE,
    day INTEGER,
    weekday VARCHAR,
    month INTEGER,
    year INTEGER
)
""")

# Hourly Demand Table
con.execute("""
CREATE TABLE IF NOT EXISTS hourly_demand_by_zone (
    pickup_hour TIMESTAMP,
    pickup_location_id INTEGER,
    trip_count BIGINT
)
""")

print("All Warehouse Tables Created Successfully!")

tables = con.execute("SHOW TABLES").fetchall()

print("\nAvailable Tables:")
for table in tables:
    print(table[0])

con.close()
