import csv

from core.parser import parse_csv_files


def _write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["title", "ctr", "retention_rate", "views", "likes", "avg_watch_time"]
        )
        writer.writerows(rows)


def test_parse_csv_files_converts_numeric_fields(tmp_path):
    file_path = tmp_path / "stats.csv"
    _write_csv(
        file_path,
        [
            ["Video A", "18.2", "35", "45200", "1240", "4.2"],
            ["Video B", "9.5", "82", "31500", "890", "8.9"],
        ],
    )

    data = parse_csv_files([str(file_path)])

    assert len(data) == 2
    assert data[0]["title"] == "Video A"
    assert data[0]["ctr"] == 18.2
    assert data[0]["retention_rate"] == 35.0
    assert data[0]["views"] == 45200.0
    assert data[0]["likes"] == 1240.0
    assert data[0]["avg_watch_time"] == 4.2


def test_parse_multiple_files_combines_data(tmp_path):
    file_path_1 = tmp_path / "stats1.csv"
    file_path_2 = tmp_path / "stats2.csv"
    _write_csv(file_path_1, [["Video A", "18", "35", "100", "10", "4.2"]])
    _write_csv(file_path_2, [["Video B", "22", "20", "300", "30", "3.1"]])

    data = parse_csv_files([str(file_path_1), str(file_path_2)])

    assert len(data) == 2
    assert [row["title"] for row in data] == ["Video A", "Video B"]
