
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(
    "data/processed/monthly_summary_2025.csv"
)

plt.figure(figsize=(12, 6))

plt.bar(
    df["month"],
    df["total_revenue"]
)

plt.xlabel("Month")
plt.ylabel("Total Revenue ($)")
plt.title("Monthly Revenue Analysis - 2025")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "data/processed/monthly_revenue_graph.png"
)

plt.show()

print("Monthly Revenue Graph Created!")
