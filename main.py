import argparse
import sys
from core.parser import parse_csv_files
from reports.registry import ReportRegistry
from reports.median_coffee import MedianCoffeeReport

def setup_registry() -> ReportRegistry:
    registry = ReportRegistry()
    registry.register('median-coffee', MedianCoffeeReport)
    return registry

def main():
    parser = argparse.ArgumentParser(description="Generate reports from student data.")
    parser.add_argument('--files', nargs='+', required=True, help="List of CSV files to process.")
    parser.add_argument('--report', required=True, help="Name of the report to generate.")
    
    args = parser.parse_args()
    registry = setup_registry()
    
    try:
        report_instance = registry.get_report(args.report)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    try:
        data = parse_csv_files(args.files)
    except Exception as e:
        print(f"Error reading files: {e}", file=sys.stderr)
        sys.exit(1)
        
    result = report_instance.generate(data)
    print(report_instance.format_output(result))

if __name__ == '__main__':
    main()
