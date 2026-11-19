from pathlib import Path
import duckdb

# Project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Database folder and file
DB_DIR = PROJECT_ROOT / "data" / "processed"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "fleetsense.duckdb"

# Create or connect to the database
con = duckdb.connect(str(DB_PATH))

print("FleetSense Database Initialized Successfully!")
print("Database Location:", DB_PATH)

con.close()