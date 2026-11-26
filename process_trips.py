
import os

import pandas as pd

print("Loading Valid Dataset...")

# Load validated dataset
file_path = "data/processed/valid_trips.parquet"

df = pd.read_parquet(file_path)

print("Dataset Loaded Successfully!")
print("Total Records:", len(df))

# Convert pickup datetime
df["tpep_pickup_datetime"] = pd.to_datetime(
    df["tpep_pickup_datetime"]
)

# Service Day Logic (4:00 AM)
df["service_date"] = (
    df["tpep_pickup_datetime"] -
    pd.Timedelta(hours=4)
).dt.date

# Extract pickup hour
df["pickup_hour"] = (
    df["tpep_pickup_datetime"].dt.hour
)

# Create output folder
os.makedirs("data/processed", exist_ok=True)

# Save processed dataset
output_path = "data/processed/service_day_trips.parquet"

df.to_parquet(output_path, index=False)

print("\nSERVICE DAY PROCESSING COMPLETED!")
print("Total Records:", len(df))
print("\nFirst 5 Records:")
print(df[[
    "tpep_pickup_datetime",
    "service_date",
    "pickup_hour"
]].head())

print("\nSaved Successfully:", output_path)
