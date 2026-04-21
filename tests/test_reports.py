import pytest

from reports.clickbait import ClickbaitReport
from reports.registry import ReportRegistry


def test_registry_registration():
    registry = ReportRegistry()
    registry.register("clickbait", ClickbaitReport)

    report = registry.get_report("clickbait")
    assert isinstance(report, ClickbaitReport)


def test_registry_invalid_report():
    registry = ReportRegistry()
    with pytest.raises(ValueError, match="not registered"):
        registry.get_report("non-existent")


def test_clickbait_report_filters_and_sorts_by_ctr():
    data = [
        {"title": "Video 1", "ctr": 18.2, "retention_rate": 35.0},
        {"title": "Video 2", "ctr": 25.0, "retention_rate": 22.0},
        {"title": "Video 3", "ctr": 16.5, "retention_rate": 42.0},
        {"title": "Video 4", "ctr": 14.2, "retention_rate": 30.0},
        {"title": "Video 5", "ctr": 21.0, "retention_rate": 35.0},
    ]
    report = ClickbaitReport()

    result = report.generate(data)

    assert result == [
        ("Video 2", 25.0, 22.0),
        ("Video 5", 21.0, 35.0),
        ("Video 1", 18.2, 35.0),
    ]


def test_clickbait_report_format_output():
    report = ClickbaitReport()
    result = [("Video X", 22.0, 28.0)]
    output = report.format_output(result)

    assert "Video X" in output
    assert "22" in output
    assert "28" in output
    assert "title" in output
    assert "retention_rate" in output
