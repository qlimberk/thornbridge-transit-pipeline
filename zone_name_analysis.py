
import pandas as pd

print("Loading Trip Dataset...")

# Load trip data
df = pd.read_parquet(
    "data/processed/service_day_trips.parquet"
)

print("Loading Zone Lookup Dataset...")

# Load zone names
zones = pd.read_csv(
    "raw/taxi_zone_lookup.csv"
)

# Rename columns
zones = zones.rename(columns={
    "LocationID": "PULocationID",
    "Zone": "Pickup_Zone_Name",
    "Borough": "Borough"
})

# Calculate zone-wise trips
zone_summary = df.groupby("PULocationID").agg(
    total_trips=("PULocationID", "count"),
    total_revenue=("total_amount", "sum"),
    average_fare=("fare_amount", "mean")
).reset_index()

# Join zone names
zone_summary = zone_summary.merge(
    zones[["PULocationID", "Pickup_Zone_Name", "Borough"]],
    on="PULocationID",
    how="left"
)

# Sort and select top 10
top_zones = zone_summary.sort_values(
    by="total_trips",
    ascending=False
).head(10)

print("\n--- TOP 10 PICKUP ZONES WITH NAMES ---")
print(top_zones.to_string(index=False))

# Save result
top_zones.to_csv(
    "data/processed/top_10_zones_with_names.csv",
    index=False
)

print("\nZone Name Analysis Completed!")
