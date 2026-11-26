
from pathlib import Path

import pandas as pd

Path("data/processed").mkdir(parents=True, exist_ok=True)

files = sorted(
    Path("data/processed").glob(
        "valid_trips_2025-??.parquet"
    )
)

print("Total valid files found:", len(files))

for file in files:

    month = file.stem.replace("valid_trips_", "")

    print("\nProcessing:", month)

    df = pd.read_parquet(file)

    # Apply 04:00 AM Service Day Logic
    df["service_date"] = (
        df["tpep_pickup_datetime"]
        - pd.Timedelta(hours=4)
    ).dt.date

    df["pickup_hour"] = (
        df["tpep_pickup_datetime"].dt.hour
    )

    output_file = (
        f"data/processed/service_day_trips_{month}.parquet"
    )

    df.to_parquet(output_file, index=False)

    print("Total Trips:", len(df))
    print("Service Day Processing Completed:", month)

    del df

print("\nALL 12 MONTHS SERVICE DAY PROCESSING COMPLETED!")
