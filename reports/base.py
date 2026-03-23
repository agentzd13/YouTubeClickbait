import abc
from typing import List, Dict, Any

class BaseReport(abc.ABC):
    """
    Base class for all reports.
    """
    @abc.abstractmethod
    def generate(self, data: List[Dict[str, Any]]) -> Any:
        pass
        
    @abc.abstractmethod
    def format_output(self, result: Any) -> str:
        pass
