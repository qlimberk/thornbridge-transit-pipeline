from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "yellow_tripdata_2024-*.parquet"

con = duckdb.connect()

query = f"""
    DESCRIBE
    SELECT *
    FROM read_parquet('{DATA_PATH.as_posix()}')
"""

result = con.execute(query).df()

print("12-Month Dataset Schema")
print("-----------------------")
print(result.to_string(index=False))

con.close()