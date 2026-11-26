
from pathlib import Path

import pandas as pd

files = sorted(
    Path("data/processed").glob(
        "service_day_trips_2025-??.parquet"
    )
)

print("Monthly files found:", len(files))

monthly_results = []

for file in files:

    month = file.stem.replace(
        "service_day_trips_", ""
    )

    print("Analyzing:", month)

    df = pd.read_parquet(file)

    summary = {
        "month": month,
        "total_trips": len(df),
        "total_revenue": df["total_amount"].sum(),
        "average_fare": df["fare_amount"].mean(),
        "average_distance": df["trip_distance"].mean(),
        "total_distance": df["trip_distance"].sum()
    }

    monthly_results.append(summary)

    del df

result = pd.DataFrame(monthly_results)

result.to_csv(
    "data/processed/monthly_summary_2025.csv",
    index=False
)

print("\n--- 2025 MONTHLY SUMMARY ---")
print(result.to_string(index=False))

print("\nMonthly Summary Completed!")
