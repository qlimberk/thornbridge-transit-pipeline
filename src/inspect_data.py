from pathlib import Path

import duckdb

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dataset path
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "yellow_tripdata_2024-01.parquet"

# Connect to DuckDB
con = duckdb.connect()

# Read dataset
df = con.execute(f"""
    SELECT *
    FROM read_parquet('{DATA_FILE.as_posix()}')
    LIMIT 5
""").df()

print("First 5 Records:")
print(df)

# Total rows
row_count = con.execute(f"""
    SELECT COUNT(*)
    FROM read_parquet('{DATA_FILE.as_posix()}')
""").fetchone()[0]

print("\nTotal Rows:", row_count)

# Column names
print("\nColumn Names:")
print(df.columns.tolist())

con.close()