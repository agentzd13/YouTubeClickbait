import pytest
import os
import csv
from core.parser import parse_csv_files

@pytest.fixture
def sample_csv(tmp_path):
    file_path = tmp_path / "test.csv"
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["student", "date", "coffee_spent", "sleep_hours", "study_hours", "mood", "exam"])
        writer.writerow(["Иван", "2024-06-01", "600", "3.0", "15", "зомби", "Математика"])
        writer.writerow(["Иван", "2024-06-02", "bad_data", "2.5", "17", "зомби", "Математика"])
    return str(file_path)

@pytest.fixture
def empty_csv(tmp_path):
    file_path = tmp_path / "empty.csv"
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["student", "date", "coffee_spent", "sleep_hours", "study_hours", "mood", "exam"])
    return str(file_path)

def test_parse_csv_files(sample_csv):
    data = parse_csv_files([sample_csv])
    assert len(data) == 2
    assert data[0]['student'] == "Иван"
    assert data[0]['coffee_spent'] == 600.0  # properly converted
    assert data[1]['coffee_spent'] == "bad_data"  # kept as str since it couldn't be converted

def test_parse_empty_csv(empty_csv):
    data = parse_csv_files([empty_csv])
    assert len(data) == 0

def test_multiple_files(sample_csv, empty_csv):
    data = parse_csv_files([sample_csv, empty_csv])
    assert len(data) == 2
