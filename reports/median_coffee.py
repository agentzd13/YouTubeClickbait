import statistics
from collections import defaultdict
from typing import List, Dict, Any, Tuple
from tabulate import tabulate
from .base import BaseReport

class MedianCoffeeReport(BaseReport):
    """
    Calculates the median coffee spent per student.
    Returns sorted list (descending) by median amount.
    """
    
    def generate(self, data: List[Dict[str, Any]]) -> List[Tuple[str, float]]:
        student_expenses = defaultdict(list)
        
        for row in data:
            student_name = row.get('student')
            expenses = row.get('coffee_spent')
            if student_name and expenses is not None:
                student_expenses[student_name].append(float(expenses))
                
        results = []
        for student, expenses in student_expenses.items():
            median_val = statistics.median(expenses)
            
            if median_val.is_integer():
                median_val = int(median_val)
                
            results.append((student, median_val))
            
        results.sort(key=lambda x: x[1], reverse=True)
        return results
        
    def format_output(self, result: List[Tuple[str, float]]) -> str:
        headers = ["student", "median_coffee"]
        return tabulate(result, headers=headers, tablefmt="grid")
