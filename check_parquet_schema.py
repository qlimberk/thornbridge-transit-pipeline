
import os

import duckdb

file_path = os.path.join(
    "data",
    "processed",
    "valid_trips_2025-01.parquet"
)

con = duckdb.connect()

result = con.execute(
    f"DESCRIBE SELECT * FROM read_parquet('{file_path}')"
).fetchall()

print("Parquet File Columns:")
for column in result:
    print(column[0], ":", column[1])

con.close()
