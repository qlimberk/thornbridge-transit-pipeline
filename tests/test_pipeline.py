from datetime import datetime

import polars as pl


def test_quarantine_logic_catches_bad_rows():
    sample = pl.DataFrame({
        "tpep_pickup_datetime": [datetime(2025, 1, 1, 10, 0), datetime(2025, 1, 1, 10, 30)],
        "tpep_dropoff_datetime": [datetime(2025, 1, 1, 10, 15), datetime(2025, 1, 1, 10, 10)],
        "fare_amount": [15.0, -5.0],
        "trip_distance": [2.5, 1.0],
        "PULocationID": [100, 100],
        "DOLocationID": [101, 101],
    })
    bad_time = sample.filter(pl.col("tpep_dropoff_datetime") <= pl.col("tpep_pickup_datetime"))
    assert len(bad_time) == 1