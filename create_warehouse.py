
import duckdb
import os

# Project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database directory
DB_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)

# Database file path
DB_PATH = os.path.join(DB_DIR, "fleetsense.duckdb")

# Create database
con = duckdb.connect(DB_PATH)

print("DuckDB Warehouse Created Successfully!")
print("Database Location:", DB_PATH)

con.close()
