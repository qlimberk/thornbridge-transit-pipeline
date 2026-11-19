from datetime import datetime

import duckdb
import polars as pl

from src.ingest import DEFAULT_MONTHS, load_to_duckdb


def test_quarantine_logic_catches_bad_rows():
    sample = pl.DataFrame(
        {
            "tpep_pickup_datetime": [
                datetime(2025, 1, 1, 10, 0),
                datetime(2025, 1, 1, 10, 30),
            ],
            "tpep_dropoff_datetime": [
                datetime(2025, 1, 1, 10, 15),
                datetime(2025, 1, 1, 10, 10),
            ],
            "fare_amount": [15.0, -5.0],
            "trip_distance": [2.5, 1.0],
            "PULocationID": [100, 100],
            "DOLocationID": [101, 101],
        }
    )

    bad_time = sample.filter(
        pl.col("tpep_dropoff_datetime")
        <= pl.col("tpep_pickup_datetime")
    )

    assert len(bad_time) == 1


def test_twelve_month_ingestion_is_idempotent(tmp_path, capsys):
    data_dir = tmp_path / "raw"
    data_dir.mkdir()

    db_path = tmp_path / "test_fleetsense.duckdb"

    # Create a small zone lookup CSV.
    zone_file = data_dir / "taxi_zone_lookup.csv"
    zone_file.write_text(
        "LocationID,Borough,Zone,service_zone\n"
        "100,Manhattan,Test Zone,Yellow Zone\n",
        encoding="utf-8",
    )

    # Create one small Parquet file for each month.
    for index, month in enumerate(DEFAULT_MONTHS, start=1):
        parquet_file = data_dir / f"yellow_tripdata_{month}.parquet"

        con = duckdb.connect()
        try:
            con.execute(
                f"""
                COPY (
                    SELECT
                        {index}::BIGINT AS vendor_id,
                        TIMESTAMP '2024-01-01 10:00:00'
                            AS tpep_pickup_datetime,
                        TIMESTAMP '2024-01-01 10:15:00'
                            AS tpep_dropoff_datetime,
                        15.0::DOUBLE AS fare_amount,
                        2.5::DOUBLE AS trip_distance,
                        100::INTEGER AS PULocationID,
                        101::INTEGER AS DOLocationID
                )
                TO '{parquet_file.as_posix()}'
                (FORMAT PARQUET)
                """
            )
        finally:
            con.close()

    # First run: load all 12 months.
    load_to_duckdb(
        DEFAULT_MONTHS,
        data_dir=data_dir,
        db_path=db_path,
    )

    first_output = capsys.readouterr().out

    assert "New rows added: 12" in first_output

    # Second run: no new rows should be added.
    load_to_duckdb(
        DEFAULT_MONTHS,
        data_dir=data_dir,
        db_path=db_path,
    )

    second_output = capsys.readouterr().out

    assert "New rows added: 0" in second_output
    assert "Monthly row counts unchanged: True" in second_output

    # Verify all 12 monthly row counts remain unchanged.
    con = duckdb.connect(str(db_path), read_only=True)

    try:
        monthly_counts = con.execute(
            """
            SELECT source_month, COUNT(*)
            FROM raw_trips
            GROUP BY source_month
            ORDER BY source_month
            """
        ).fetchall()

        assert len(monthly_counts) == 12
        assert all(count == 1 for _, count in monthly_counts)

        logged_months = con.execute(
            "SELECT COUNT(*) FROM ingestion_log"
        ).fetchone()[0]

        assert logged_months == 12

        total_rows = con.execute(
            "SELECT COUNT(*) FROM raw_trips"
        ).fetchone()[0]

        assert total_rows == 12

    finally:
        con.close()