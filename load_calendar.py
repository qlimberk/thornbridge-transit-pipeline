
import duckdb
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR, "data", "fleetsense.duckdb"
)

con = duckdb.connect(DB_PATH)

# Clear existing calendar records
con.execute("DELETE FROM dim_calendar")

# Generate calendar dates for 2025
con.execute("""
    INSERT INTO dim_calendar (
        date,
        day,
        weekday,
        month,
        year
    )
    SELECT
        calendar_date,
        EXTRACT(DAY FROM calendar_date)::INTEGER,
        STRFTIME(calendar_date, '%A'),
        EXTRACT(MONTH FROM calendar_date)::INTEGER,
        EXTRACT(YEAR FROM calendar_date)::INTEGER
    FROM generate_series(
        DATE '2025-01-01',
        DATE '2025-12-31',
        INTERVAL 1 DAY
    ) AS dates(calendar_date)
""")

# Verify calendar records
total = con.execute(
    "SELECT COUNT(*) FROM dim_calendar"
).fetchone()[0]

print("Calendar Data Created Successfully!")
print("Total Calendar Days:", total)

print("\nFirst 5 Calendar Records:")

rows = con.execute("""
    SELECT * FROM dim_calendar
    ORDER BY date
    LIMIT 5
""").fetchall()

for row in rows:
    print(row)

con.close()
