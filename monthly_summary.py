
import pandas as pd

print("Loading Processed Dataset...")

# Load processed dataset
df = pd.read_parquet(
    "data/processed/service_day_trips.parquet"
)

print("Dataset Loaded Successfully!")
print("Total Records:", len(df))

# Create month column
df["month"] = pd.to_datetime(
    df["service_date"]
).dt.to_period("M").astype(str)

# Monthly summary
monthly_summary = df.groupby("month").agg(
    total_trips=("VendorID", "count"),
    total_revenue=("total_amount", "sum"),
    average_fare=("fare_amount", "mean"),
    average_distance=("trip_distance", "mean"),
    total_distance=("trip_distance", "sum")
).reset_index()

# Round decimal values
monthly_summary = monthly_summary.round(2)

# Display results
print("\n--- MONTHLY SUMMARY ---")
print(monthly_summary)

# Save results
monthly_summary.to_csv(
    "data/processed/monthly_summary.csv",
    index=False
)

print("\nMonthly Summary Saved Successfully!")
