import argparse
from pathlib import Path

import duckdb
import polars as pl

DB_PATH = Path("data/fleetsense.duckdb")


def validate_month(month: str) -> dict[str, int]:
    con = duckdb.connect(str(DB_PATH))
    df = con.execute(
        "SELECT * FROM raw_trips WHERE source_month = ?", [month]
    ).pl()

    valid_zones = set(
        con.execute("SELECT LocationID FROM dim_zones").pl()["LocationID"].to_list()
    )

    # Flag invalid conditions (NFR-02: quarantine with reason code)
    df = df.with_columns(
        pl.when(pl.col("tpep_dropoff_datetime") <= pl.col("tpep_pickup_datetime"))
        .then(pl.lit("INVALID_TIMESTAMPS"))
        .when(pl.col("fare_amount") < 0)
        .then(pl.lit("NEGATIVE_FARE"))
        .when(pl.col("trip_distance") <= 0)
        .then(pl.lit("NON_POSITIVE_DISTANCE"))
        .when(~pl.col("PULocationID").is_in(valid_zones) | ~pl.col("DOLocationID").is_in(valid_zones))
        .then(pl.lit("UNKNOWN_ZONE_ID"))
        .otherwise(pl.lit(None))
        .alias("quarantine_reason")
    )

    clean_df = df.filter(pl.col("quarantine_reason").is_null()).drop("quarantine_reason")
    quarantine_df = df.filter(pl.col("quarantine_reason").is_not_null())

    # Replace month partition cleanly so re-runs are idempotent
    con.execute("CREATE TABLE IF NOT EXISTS clean_trips AS SELECT * FROM clean_df LIMIT 0")
    con.execute("DELETE FROM clean_trips WHERE source_month = ?", [month])
    con.execute("INSERT INTO clean_trips SELECT * FROM clean_df")

    con.execute("CREATE TABLE IF NOT EXISTS quarantined_trips AS SELECT * FROM quarantine_df LIMIT 0")
    con.execute("DELETE FROM quarantined_trips WHERE source_month = ?", [month])
    con.execute("INSERT INTO quarantined_trips SELECT * FROM quarantine_df")

    con.close()
    stats = {
        "rows_in": len(df),
        "rows_clean": len(clean_df),
        "rows_quarantined": len(quarantine_df),
    }
    print(f"[QUALITY {month}] In: {stats['rows_in']:,} | Clean: {stats['rows_clean']:,} | Quarantined: {stats['rows_quarantined']:,}")
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--months", nargs="+", required=True)
    args = parser.parse_args()
    for m in args.months:
        validate_month(m)