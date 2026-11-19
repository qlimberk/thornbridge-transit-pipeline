import sys
from datetime import datetime


def get_month_url(month):

    try:
        parsed_month = datetime.strptime(month, "%Y-%m")

        if parsed_month.strftime("%Y-%m") != month:
            raise ValueError

    except ValueError:
        raise ValueError(
            "Invalid month format. Use YYYY-MM (example: 2024-01)."
        )

    file_name = f"yellow_tripdata_{month}.parquet"

    file_url = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/"
        f"{file_name}"
    )

    return file_url


if __name__ == "__main__":

    month = sys.argv[1] if len(sys.argv) > 1 else "2024-01"

    url = get_month_url(month)

    print("Month:", month)
    print("File Name:", f"yellow_tripdata_{month}.parquet")
    print("File URL:", url)