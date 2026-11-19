from pathlib import Path
from shutil import copyfileobj
from urllib.request import urlopen

from get_month_url import get_month_url

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Raw data directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Months: January to December 2024
MONTHS = [
    f"2024-{month:02d}"
    for month in range(1, 13)
]

# NYC Taxi Zone Lookup URL
ZONE_URL = (
    "https://d37ci6vzurychx.cloudfront.net/misc/"
    "taxi_zone_lookup.csv"
)

ZONE_FILE = RAW_DATA_DIR / "taxi_zone_lookup.csv"


def download_file(url, file_path):

    if file_path.exists() and file_path.stat().st_size > 0:
        print(f"Already exists. Skipping: {file_path.name}")
        return False

    temp_path = file_path.with_suffix(file_path.suffix + ".part")

    try:
        print(f"Downloading: {file_path.name}")

        with urlopen(url, timeout=60) as response, open(temp_path, "wb") as output:
            copyfileobj(response, output)

        if temp_path.stat().st_size == 0:
            raise ValueError("Downloaded file is empty.")

        temp_path.replace(file_path)

        print(f"Download completed: {file_path.name}")

        return True

    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise


def ingest_12_months():

    print("\nFleetSense - 12 Month Ingestion")
    print("--------------------------------")

    downloaded = 0
    skipped = 0

    # Download monthly Yellow Taxi datasets
    for month in MONTHS:

        file_name = f"yellow_tripdata_{month}.parquet"

        file_path = RAW_DATA_DIR / file_name

        file_url = get_month_url(month)

        if download_file(file_url, file_path):
            downloaded += 1
        else:
            skipped += 1

    # Download NYC Taxi Zone Lookup
    if download_file(ZONE_URL, ZONE_FILE):
        downloaded += 1
    else:
        skipped += 1

    print("\nIngestion Summary")
    print("-----------------")
    print("Total monthly datasets:", len(MONTHS))
    print("Downloaded files:", downloaded)
    print("Skipped files:", skipped)

    print("\nIngestion completed!")


if __name__ == "__main__":
    ingest_12_months()