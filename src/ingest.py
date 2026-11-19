import argparse
from pathlib import Path

import duckdb
import httpx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"
DB_PATH = PROJECT_ROOT / "data" / "fleetsense.duckdb"

TLC_BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
ZONE_LOOKUP_URL = (
    "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
)

DEFAULT_MONTHS = [f"2024-{month:02d}" for month in range(1, 13)]


def download_file(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    temp_path = dest.with_suffix(dest.suffix + ".part")

    try:
        print(f"[DOWNLOAD] {dest.name}")

        with httpx.stream(
            "GET", url, follow_redirects=True, timeout=120.0
        ) as response:
            response.raise_for_status()

            with open(temp_path, "wb") as output:
                output.writelines(response.iter_bytes(chunk_size=1024 * 1024))

        if temp_path.stat().st_size == 0:
            raise ValueError(f"Downloaded file is empty: {dest.name}")

        temp_path.replace(dest)

    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise


def sql_path(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def get_month_count(con, month: str) -> int:
    tables = {row[0] for row in con.execute("SHOW TABLES").fetchall()}

    if "raw_trips" not in tables:
        return 0

    return con.execute(
        "SELECT COUNT(*) FROM raw_trips WHERE source_month = ?",
        [month],
    ).fetchone()[0]


def load_to_duckdb(
    months: list[str],
    data_dir: Path = DATA_DIR,
    db_path: Path = DB_PATH,
) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    zone_file = data_dir / "taxi_zone_lookup.csv"
    download_file(ZONE_LOOKUP_URL, zone_file)

    con = duckdb.connect(str(db_path))

    try:
        con.execute("""
            CREATE TABLE IF NOT EXISTS ingestion_log (
                month VARCHAR PRIMARY KEY,
                rows_ingested BIGINT,
                ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        zone_path = sql_path(zone_file)

        con.execute(f"""
            CREATE OR REPLACE TABLE dim_zones AS
            SELECT *
            FROM read_csv_auto('{zone_path}')
        """)

        before_counts = {
            month: get_month_count(con, month)
            for month in months
        }

        new_rows = 0

        for month in months:
            logged = con.execute(
                "SELECT rows_ingested FROM ingestion_log WHERE month = ?",
                [month],
            ).fetchone()

            if logged:
                actual_count = get_month_count(con, month)

                if actual_count != logged[0]:
                    raise RuntimeError(
                        f"Row-count mismatch for {month}: "
                        f"log={logged[0]}, actual={actual_count}"
                    )

                print(f"[SKIP] {month}: already loaded ({actual_count:,} rows)")
                continue

            parquet_file = data_dir / f"yellow_tripdata_{month}.parquet"
            url = f"{TLC_BASE_URL}/{parquet_file.name}"

            download_file(url, parquet_file)
            parquet_path = sql_path(parquet_file)

            try:
                con.execute("BEGIN TRANSACTION")

                con.execute(f"""
                    CREATE TABLE IF NOT EXISTS raw_trips AS
                    SELECT *, '{month}' AS source_month
                    FROM read_parquet('{parquet_path}')
                    LIMIT 0
                """)

                existing_count = get_month_count(con, month)

                if existing_count != 0:
                    raise RuntimeError(
                        f"{month} has existing rows but no ingestion log. "
                        "Manual inspection is required."
                    )

                con.execute(f"""
                    INSERT INTO raw_trips
                    SELECT *, '{month}' AS source_month
                    FROM read_parquet('{parquet_path}')
                """)

                row_count = get_month_count(con, month)

                con.execute(
                    """
                    INSERT INTO ingestion_log (month, rows_ingested)
                    VALUES (?, ?)
                    """,
                    [month, row_count],
                )

                con.execute("COMMIT")

                new_rows += row_count
                print(f"[LOADED] {month}: {row_count:,} rows")

            except Exception:
                con.execute("ROLLBACK")
                raise

        after_counts = {
            month: get_month_count(con, month)
            for month in months
        }

        unchanged = all(
            before_counts[month] == after_counts[month]
            for month in months
        )

        print("\nIngestion Summary")
        print("-----------------")
        print("Months processed:", len(months))
        print("New rows added:", f"{new_rows:,}")
        print("Monthly row counts unchanged:", unchanged)

        print("\nMonthly Row Count Verification")
        print("------------------------------")

        for month in months:
            print(
                f"{month}: "
                f"{before_counts[month]:,} -> "
                f"{after_counts[month]:,}"
            )

    finally:
        con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load Yellow Taxi monthly data into DuckDB."
    )

    parser.add_argument(
        "--months",
        nargs="+",
        default=DEFAULT_MONTHS,
        help="Months to ingest. Defaults to all 12 months of 2024.",
    )

    args = parser.parse_args()
    load_to_duckdb(args.months)