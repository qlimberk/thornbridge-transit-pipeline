
from pathlib import Path

import pandas as pd

# Create output folders
Path("data/processed").mkdir(parents=True, exist_ok=True)
Path("data/quarantine").mkdir(parents=True, exist_ok=True)
Path("logs").mkdir(parents=True, exist_ok=True)

raw_folder = Path("raw")

files = sorted(raw_folder.glob("yellow_tripdata_2025-??.parquet"))

print("Total monthly files found:", len(files))

if len(files) != 12:
    raise ValueError("Expected 12 monthly Parquet files.")

run_logs = []

for file in files:

    month = file.stem[-7:]

    print("\nProcessing:", month)

    df = pd.read_parquet(file)

    total_rows = len(df)

    # Validation rules
    invalid_time = (
        df["tpep_dropoff_datetime"]
        <= df["tpep_pickup_datetime"]
    )

    negative_fare = df["fare_amount"] < 0

    invalid = invalid_time | negative_fare

    # Reason codes
    df["validation_reason"] = ""

    df.loc[invalid_time, "validation_reason"] = (
        "dropoff_before_pickup"
    )

    df.loc[negative_fare, "validation_reason"] = (
        df.loc[negative_fare, "validation_reason"]
        .apply(
            lambda x: (
                x + ";negative_fare"
                if x else "negative_fare"
            )
        )
    )

    # Separate valid and quarantined trips
    valid = df.loc[~invalid].drop(
        columns=["validation_reason"]
    )

    quarantined = df.loc[invalid]

    # Save monthly files
    valid.to_parquet(
        f"data/processed/valid_trips_{month}.parquet",
        index=False
    )

    quarantined.to_parquet(
        f"data/quarantine/quarantined_trips_{month}.parquet",
        index=False
    )

    # Monthly run log
    run_logs.append({
        "month": month,
        "total_rows": total_rows,
        "valid_rows": len(valid),
        "quarantined_rows": len(quarantined),
        "negative_fare_count": int(negative_fare.sum()),
        "invalid_time_count": int(invalid_time.sum()),
        "status": "Completed"
    })

    print("Total:", total_rows)
    print("Valid:", len(valid))
    print("Quarantined:", len(quarantined))

    del df, valid, quarantined

# Save complete monthly run log
log_df = pd.DataFrame(run_logs)

log_df.to_csv(
    "logs/monthly_run_log_2025.csv",
    index=False
)

print("\n--- ALL MONTHS VALIDATION SUMMARY ---")
print(log_df.to_string(index=False))

print("\n12 MONTHS VALIDATION COMPLETED!")
