
import pandas as pd

print("Loading Dataset...")

df = pd.read_parquet(
    "data/processed/service_day_trips.parquet"
)

print("Dataset Loaded:", len(df))

# Zone-wise pickup analysis
zone_summary = df.groupby("PULocationID").agg(
    total_trips=("PULocationID", "count"),
    total_revenue=("total_amount", "sum"),
    average_fare=("fare_amount", "mean")
).reset_index()

# Sort by total trips
zone_summary = zone_summary.sort_values(
    by="total_trips",
    ascending=False
)

# Top 10 pickup zones
top_zones = zone_summary.head(10)

print("\n--- TOP 10 PICKUP ZONES ---")
print(top_zones)

# Save output
top_zones.to_csv(
    "data/processed/top_10_zones.csv",
    index=False
)

print("\nZone Analysis Completed!")
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.bar(
    top_zones["PULocationID"].astype(str),
    top_zones["total_trips"]
)

plt.xlabel("Pickup Zone ID")
plt.ylabel("Total Trips")
plt.title("Top 10 Pickup Zones by Trip Count")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("data/processed/top_10_zones.png")

plt.show()