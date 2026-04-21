import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _run_main(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "main.py", *args],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )


def test_main_help():
    result = _run_main(["--help"])

    assert result.returncode == 0
    assert "--files" in result.stdout
    assert "--report" in result.stdout


def test_main_generates_clickbait_report_for_multiple_files():
    result = _run_main(
        ["--files", "stats1.csv", "stats2.csv", "--report", "clickbait"]
    )

    assert result.returncode == 0
    assert "Секрет который скрывают тимлиды" in result.stdout
    assert "Почему продакшн упал в пятницу вечером" in result.stdout
    assert "Почему сеньоры не носят галстуки" not in result.stdout

    top_1 = result.stdout.find("Секрет который скрывают тимлиды")
    top_2 = result.stdout.find("Почему продакшн упал в пятницу вечером")
    assert top_1 < top_2


def test_main_invalid_report_returns_error():
    result = _run_main(["--files", "stats1.csv", "--report", "unknown-report"])

    assert result.returncode != 0
    assert "not registered" in result.stderr


def test_main_missing_file_returns_error():
    result = _run_main(["--files", "missing.csv", "--report", "clickbait"])

    assert result.returncode != 0
    assert "Error reading files" in result.stderr
