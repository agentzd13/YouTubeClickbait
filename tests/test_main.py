import pytest
import subprocess
import os

def test_main_script_help():
    result = subprocess.run(["python3", "main.py", "--help"], capture_output=True, text=True)
    # Could be python or python3 on windows, let's just check if it exits ok or use sys.executable
    import sys
    result = subprocess.run([sys.executable, "main.py", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "--files" in result.stdout
    assert "--report" in result.stdout

def test_main_script_execution(tmp_path):
    import sys
    import csv
    
    file_path = tmp_path / "test.csv"
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["student", "coffee_spent"])
        writer.writerow(["Иван", "600"])
        
    result = subprocess.run(
        [sys.executable, "main.py", "--files", str(file_path), "--report", "median-coffee"],
        capture_output=True, text=True
    )
    
    assert result.returncode == 0
    assert "Иван" in result.stdout
    assert "600" in result.stdout

def test_main_script_invalid_report(tmp_path):
    import sys
    import csv
    
    file_path = tmp_path / "test.csv"
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["student", "coffee_spent"])
        writer.writerow(["Иван", "600"])
        
    result = subprocess.run(
        [sys.executable, "main.py", "--files", str(file_path), "--report", "invalid-report"],
        capture_output=True, text=True
    )
    
    assert result.returncode != 0
    assert "Error: Report 'invalid-report' is not registered" in result.stderr
