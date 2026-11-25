
import pandas as pd
import os

file_path = r"C:\Users\hp pavillion\fleetsense\raw\yellow_tripdata_2025-01.parquet"

print("Loading Dataset...")

if os.path.exists(file_path):
    df = pd.read_parquet(file_path)

    print("Dataset Loaded Successfully!")
    print("Rows and Columns:", df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nFirst 5 Records:")
    print(df.head())

else:
    print("Dataset file not found. Check the file path.")

# Dataset Information
print("\n--- DATASET INFORMATION ---")

print("\nDataset Shape:")
print(df.shape)

print("\nDataset Information:")
df.info()

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nStatistical Summary:")
print(df.describe())

