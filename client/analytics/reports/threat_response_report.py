"""
Tactical Report Generator: ThreatResponseReport
Audits adaptive counter-wave efficiency and player reaction time
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class ReportDataPoint:
    label: str
    value: float
    category: str

class ThreatResponseReport:
    def __init__(self, mission_id: str):
        self.mission_id: str = mission_id
        self.report_name: str = "ThreatResponseReport"
        self.data_points: List[ReportDataPoint] = []

    def add_metric(self, label: str, val: float, cat: str = "General") -> None:
        self.data_points.append(ReportDataPoint(label=label, value=val, category=cat))

    def generate_json_summary(self) -> dict:
        return {
            "mission": self.mission_id,
            "report": self.report_name,
            "metrics_count": len(self.data_points),
            "data": [{ "label": d.label, "val": d.value, "category": d.category } for d in self.data_points]
        }
