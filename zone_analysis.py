from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "service_day_trips.parquet"
ZONE_FILE = PROJECT_ROOT / "raw" / "taxi_zone_lookup.csv"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"

print("Dataset Path:", DATA_FILE)
print("Zone File Path:", ZONE_FILE)

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

if not ZONE_FILE.exists():
    raise FileNotFoundError(f"Zone lookup not found: {ZONE_FILE}")