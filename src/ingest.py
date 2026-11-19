import argparse
from pathlib import Path

import duckdb
import httpx

DATA_DIR = Path("data/raw")
DB_PATH = Path("data/fleetsense.duckdb")
TLC_BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
ZONE_LOOKUP_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"


def download_file(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[SKIP] Already downloaded: {dest.name}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"[DOWNLOAD] Fetching {url}...")
    with httpx.stream("GET", url, follow_redirects=True, timeout=60.0) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            f.writelines(r.iter_bytes(chunk_size=8192))


def load_to_duckdb(months: list[str]) -> None:
    con = duckdb.connect(str(DB_PATH))
    con.execute("""
        CREATE TABLE IF NOT EXISTS ingestion_log (
            month VARCHAR PRIMARY KEY,
            rows_ingested BIGINT,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Load Zone Lookup (idempotent replace)
    zone_file = DATA_DIR / "taxi_zone_lookup.csv"
    download_file(ZONE_LOOKUP_URL, zone_file)
    con.execute(f"""
        CREATE OR REPLACE TABLE dim_zones AS
        SELECT * FROM read_csv_auto('{zone_file.as_posix()}');
    """)

    # Load Trips incrementally (AC-1.1: second run adds no rows)
    for month in months:
        already_loaded = con.execute(
            "SELECT 1 FROM ingestion_log WHERE month = ?", [month]
        ).fetchone()
        if already_loaded:
            print(f"[SKIP] Month {month} already loaded in DuckDB.")
            continue

        parquet_file = DATA_DIR / f"yellow_tripdata_{month}.parquet"
        download_file(f"{TLC_BASE_URL}/yellow_tripdata_{month}.parquet", parquet_file)

        con.execute(f"""
            CREATE TABLE IF NOT EXISTS raw_trips AS
            SELECT *, '{month}' AS source_month
            FROM read_parquet('{parquet_file.as_posix()}') LIMIT 0;
        """)
        con.execute(f"""
            INSERT INTO raw_trips
            SELECT *, '{month}' AS source_month
            FROM read_parquet('{parquet_file.as_posix()}');
        """)
        row_count = con.execute(
            "SELECT COUNT(*) FROM raw_trips WHERE source_month = ?", [month]
        ).fetchone()[0]
        con.execute(
            "INSERT INTO ingestion_log (month, rows_ingested) VALUES (?, ?)",
            [month, row_count],
        )
        print(f"[LOADED] {month}: {row_count:,} rows.")
    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--months", nargs="+", required=True, help="e.g. 2025-01")
    args = parser.parse_args()
    load_to_duckdb(args.months)
