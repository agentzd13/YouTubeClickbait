import argparse
import sys

from core.parser import parse_csv_files
from reports.clickbait import ClickbaitReport
from reports.registry import ReportRegistry


def setup_registry() -> ReportRegistry:
    registry = ReportRegistry()
    registry.register("clickbait", ClickbaitReport)
    return registry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate reports from YouTube CSV metrics files."
    )
    parser.add_argument("--files", nargs="+", required=True, help="CSV file paths.")
    parser.add_argument("--report", required=True, help="Report name (clickbait).")

    args = parser.parse_args(argv)
    registry = setup_registry()

    try:
        report_instance = registry.get_report(args.report)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        data = parse_csv_files(args.files)
    except OSError as exc:
        print(f"Error reading files: {exc}", file=sys.stderr)
        return 1

    result = report_instance.generate(data)
    print(report_instance.format_output(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
