from typing import Type, Dict
from .base import BaseReport

class ReportRegistry:
    """Registry for managing available reports."""
    
    def __init__(self):
        self._reports: Dict[str, Type[BaseReport]] = {}
        
    def register(self, name: str, report_class: Type[BaseReport]) -> None:
        self._reports[name] = report_class
        
    def get_report(self, name: str) -> BaseReport:
        if name not in self._reports:
            raise ValueError(f"Report '{name}' is not registered. Available: {', '.join(self._reports.keys())}")
        return self._reports[name]()
