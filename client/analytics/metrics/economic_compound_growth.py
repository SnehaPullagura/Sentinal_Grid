"""
Telemetry Metric Engine: EconomicCompoundGrowthMetric
Evaluates credit bank growth from interest and refineries
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class MetricSnapshot:
    tick: int
    metric_value: float
    confidence_score: float

class EconomicCompoundGrowthMetric:
    def __init__(self):
        self.metric_name: str = "EconomicCompoundGrowthMetric"
        self.description: str = "Evaluates credit bank growth from interest and refineries"
        self.history: List[MetricSnapshot] = []

    def record_sample(self, tick: int, raw_value: float, confidence: float = 1.0) -> None:
        self.history.append(MetricSnapshot(tick=tick, metric_value=raw_value, confidence_score=confidence))

    def get_average(self) -> float:
        if not self.history: return 0.0
        return sum(s.metric_value for s in self.history) / len(self.history)

    def get_latest(self) -> float:
        return self.history[-1].metric_value if self.history else 0.0
