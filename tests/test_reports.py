import pytest
from reports.base import BaseReport
from reports.registry import ReportRegistry
from reports.median_coffee import MedianCoffeeReport

def test_registry_registration():
    registry = ReportRegistry()
    registry.register("median-coffee", MedianCoffeeReport)
    
    report = registry.get_report("median-coffee")
    assert isinstance(report, MedianCoffeeReport)

def test_registry_invalid_report():
    registry = ReportRegistry()
    with pytest.raises(ValueError, match="not registered"):
        registry.get_report("non-existent")

def test_median_coffee_report_logic():
    data = [
        {"student": "Иван", "coffee_spent": 600.0},
        {"student": "Иван", "coffee_spent": 700.0},
        {"student": "Иван", "coffee_spent": 800.0},
        {"student": "Иван", "coffee_spent": "invalid"}, # Should be ignored because it cannot be parsed by float later if we used direct cast? 
        {"student": "Анна", "coffee_spent": 100.0},
        {"student": "Анна", "coffee_spent": 100.0},
        {"student": "Анна"}, # Missing coffee_spent
    ]
    report = MedianCoffeeReport()
    
    # Wait, the logic converts to float manually if possible, or skips. Let's provide strings that can be converted since CSV does that.
    data_with_strings = [
        {"student": "Иван", "coffee_spent": "600"},
        {"student": "Иван", "coffee_spent": "800"},
        {"student": "Иван", "coffee_spent": 1000.0}, # Mixed types for robustness
        {"student": "Анна", "coffee_spent": 200},
        {"student": "Анна", "coffee_spent": 300},
    ]
    
    result = report.generate(data_with_strings)
    
    assert len(result) == 2
    # Иван median of 600, 800, 1000 is 800
    # Анна median of 200, 300 is 250
    assert result[0] == ("Иван", 800)
    assert result[1] == ("Анна", 250)

def test_median_coffee_report_format():
    report = MedianCoffeeReport()
    result = [("Иван", 800)]
    output = report.format_output(result)
    
    assert "Иван" in output
    assert "800" in output
    assert "student" in output
    assert "median_coffee" in output
