from pathlib import Path

import altair as alt
import duckdb


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "fleetsense.duckdb"
REPORTS_DIR = PROJECT_ROOT / "reports"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def run_query(connection, query):
    result = connection.execute(query)
    columns = [item[0] for item in result.description]
    return [
        dict(zip(columns, row))
        for row in result.fetchall()
    ]


def save_chart(chart, filename):
    output_path = REPORTS_DIR / filename
    chart.save(str(output_path))
    print(f"Created: {output_path}")


def create_bar_chart(data, x_field, y_field, title, x_title):
    chart = (
        alt.Chart(alt.Data(values=data))
        .mark_bar()
        .encode(
            x=alt.X(
                f"{x_field}:O",
                title=x_title,
                sort=None,
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y(
                f"{y_field}:Q",
                title="Total Trips",
            ),
            tooltip=[
                alt.Tooltip(f"{x_field}:O", title=x_title),
                alt.Tooltip(f"{y_field}:Q", title="Total Trips", format=","),
            ],
        )
        .properties(
            title=title,
            width=700,
            height=400,
        )
    )
    return chart


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    print("Connecting to DuckDB in read-only mode...")

    connection = duckdb.connect(
        str(DATABASE_PATH),
        read_only=True,
    )

    try:
        print("\nGenerating hourly seasonality chart...")

        hourly_data = run_query(
            connection,
            """
            SELECT
                EXTRACT(HOUR FROM tpep_pickup_datetime)::INTEGER
                    AS pickup_hour,
                COUNT(*) AS total_trips
            FROM trips
            WHERE tpep_pickup_datetime IS NOT NULL
            GROUP BY pickup_hour
            ORDER BY pickup_hour
            """,
        )

        save_chart(
            create_bar_chart(
                hourly_data,
                "pickup_hour",
                "total_trips",
                "Pickup Trips by Hour",
                "Pickup Hour",
            ),
            "hourly_seasonality.html",
        )

        print("\nGenerating weekday seasonality chart...")

        weekday_data = run_query(
            connection,
            """
            SELECT
                DAYNAME(tpep_pickup_datetime) AS weekday,
                DAYOFWEEK(tpep_pickup_datetime) AS weekday_number,
                COUNT(*) AS total_trips
            FROM trips
            WHERE tpep_pickup_datetime IS NOT NULL
            GROUP BY weekday, weekday_number
            ORDER BY weekday_number
            """,
        )

        save_chart(
            create_bar_chart(
                weekday_data,
                "weekday",
                "total_trips",
                "Pickup Trips by Weekday",
                "Weekday",
            ),
            "weekday_seasonality.html",
        )

        print("\nGenerating monthly seasonality chart...")

        monthly_data = run_query(
            connection,
            """
            SELECT
                MONTH(tpep_pickup_datetime) AS month_number,
                MONTHNAME(tpep_pickup_datetime) AS month_name,
                COUNT(*) AS total_trips
            FROM trips
            WHERE tpep_pickup_datetime IS NOT NULL
            GROUP BY month_number, month_name
            ORDER BY month_number
            """,
        )

        save_chart(
            create_bar_chart(
                monthly_data,
                "month_name",
                "total_trips",
                "Pickup Trips by Month (All Years Combined)",
                "Month",
            ),
            "monthly_seasonality.html",
        )

        print("\nGenerating pickup zone charts...")

        pickup_top = run_query(
            connection,
            """
            SELECT
                PULocationID,
                COUNT(*) AS total_trips
            FROM trips
            WHERE PULocationID IS NOT NULL
            GROUP BY PULocationID
            ORDER BY total_trips DESC
            LIMIT 10
            """,
        )

        pickup_bottom = run_query(
            connection,
            """
            SELECT
                PULocationID,
                COUNT(*) AS total_trips
            FROM trips
            WHERE PULocationID IS NOT NULL
            GROUP BY PULocationID
            ORDER BY total_trips ASC, PULocationID ASC
            LIMIT 10
            """,
        )

        save_chart(
            create_bar_chart(
                pickup_top,
                "PULocationID",
                "total_trips",
                "Top 10 Pickup Zones",
                "Pickup Location ID",
            ),
            "top_pickup_zones.html",
        )

        save_chart(
            create_bar_chart(
                pickup_bottom,
                "PULocationID",
                "total_trips",
                "Bottom 10 Pickup Zones",
                "Pickup Location ID",
            ),
            "bottom_pickup_zones.html",
        )

        print("\nGenerating drop-off zone charts...")

        dropoff_top = run_query(
            connection,
            """
            SELECT
                DOLocationID,
                COUNT(*) AS total_trips
            FROM trips
            WHERE DOLocationID IS NOT NULL
            GROUP BY DOLocationID
            ORDER BY total_trips DESC
            LIMIT 10
            """,
        )

        dropoff_bottom = run_query(
            connection,
            """
            SELECT
                DOLocationID,
                COUNT(*) AS total_trips
            FROM trips
            WHERE DOLocationID IS NOT NULL
            GROUP BY DOLocationID
            ORDER BY total_trips ASC, DOLocationID ASC
            LIMIT 10
            """,
        )

        save_chart(
            create_bar_chart(
                dropoff_top,
                "DOLocationID",
                "total_trips",
                "Top 10 Drop-off Zones",
                "Drop-off Location ID",
            ),
            "top_dropoff_zones.html",
        )

        save_chart(
            create_bar_chart(
                dropoff_bottom,
                "DOLocationID",
                "total_trips",
                "Bottom 10 Drop-off Zones",
                "Drop-off Location ID",
            ),
            "bottom_dropoff_zones.html",
        )

        print("\nAll 7 charts generated successfully.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
