import csv
from typing import List, Dict, Any

def parse_csv_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Parses multiple CSV files and returns a list of dictionaries with the data.
    """
    data_rows = []
    
    for file_path in file_paths:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['coffee_spent'] = float(row['coffee_spent'])
                except (ValueError, KeyError, TypeError):
                    pass
                data_rows.append(row)
                
    return data_rows
