
import os

import duckdb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "raw", "taxi_zone_lookup.csv")

con = duckdb.connect()

result = con.execute(
    "DESCRIBE SELECT * FROM read_csv_auto(?)",
    [CSV_PATH]
).fetchall()

print("Taxi Zone CSV Columns:")

for column in result:
    print(column[0], ":", column[1])

print("\nFirst 5 Records:")

rows = con.execute(
    "SELECT * FROM read_csv_auto(?) LIMIT 5",
    [CSV_PATH]
).fetchall()

for row in rows:
    print(row)

con.close()
