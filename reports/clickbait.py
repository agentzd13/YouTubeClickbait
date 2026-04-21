from typing import Any, Dict, List, Tuple

from tabulate import tabulate

from .base import BaseReport


class ClickbaitReport(BaseReport):
    """List videos with high CTR and low retention."""

    CTR_THRESHOLD = 15.0
    RETENTION_THRESHOLD = 40.0

    def generate(self, data: List[Dict[str, Any]]) -> List[Tuple[str, float, float]]:
        filtered: List[Tuple[str, float, float]] = []

        for row in data:
            ctr = float(row["ctr"])
            retention_rate = float(row["retention_rate"])
            if ctr > self.CTR_THRESHOLD and retention_rate < self.RETENTION_THRESHOLD:
                filtered.append((row["title"], ctr, retention_rate))

        filtered.sort(key=lambda item: item[1], reverse=True)
        return filtered

    def format_output(self, result: List[Tuple[str, float, float]]) -> str:
        headers = ["title", "ctr", "retention_rate"]
        return tabulate(result, headers=headers, tablefmt="grid")