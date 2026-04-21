import csv
from typing import List, Dict, Any


NUMERIC_COLUMNS = {
    "ctr",
    "retention_rate",
    "views",
    "likes",
    "avg_watch_time",
}


def parse_csv_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """Parse multiple CSV files and normalize known numeric fields."""
    data_rows = []

    for file_path in file_paths:
        with open(file_path, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                for column in NUMERIC_COLUMNS:
                    if column in row and row[column] not in (None, ""):
                        row[column] = float(row[column])
                data_rows.append(row)

    return data_rows
