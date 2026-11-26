
import os

import pandas as pd

# Load Dataset
file_path = "raw/yellow_tripdata_2025-01.parquet"

df = pd.read_parquet(file_path)

print("Dataset Loaded:", len(df))

# Validation Rules
pickup = pd.to_datetime(df["tpep_pickup_datetime"])
dropoff = pd.to_datetime(df["tpep_dropoff_datetime"])

rule1 = dropoff <= pickup
rule2 = df["fare_amount"] < 0

# Assign Reason Codes
reason = pd.Series("", index=df.index, dtype="string")

reason.loc[rule1] = "dropoff_before_pickup"

reason.loc[rule2 & (reason == "")] = "negative_fare"

reason.loc[rule1 & rule2] = (
    "dropoff_before_pickup|negative_fare"
)

# Separate Valid and Invalid Records
invalid = reason != ""

valid_data = df.loc[~invalid].copy()

quarantine = df.loc[invalid].copy()

quarantine["reason_code"] = reason.loc[invalid]

# Create Folders
os.makedirs("data/processed", exist_ok=True)
os.makedirs("data/quarantine", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Save Files
valid_data.to_parquet(
    "data/processed/valid_trips.parquet",
    index=False
)

quarantine.to_parquet(
    "data/quarantine/quarantined_trips.parquet",
    index=False
)

# Run Log
run_log = pd.DataFrame([{
    "month": "2025-01",
    "rows_in": len(df),
    "rows_loaded": len(valid_data),
    "rows_quarantined": len(quarantine)
}])

run_log.to_csv("logs/run_log.csv", index=False)

print("\n--- VALIDATION RESULT ---")
print("Total Rows:", len(df))
print("Valid Rows:", len(valid_data))
print("Quarantined Rows:", len(quarantine))

print("\nReason Code Counts:")
print(quarantine["reason_code"].value_counts())

print("\nValidation Completed Successfully!")
