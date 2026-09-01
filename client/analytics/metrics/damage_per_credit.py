"""
Telemetry Metric Engine: DamagePerCreditMetric
Evaluates economic ROI for each placed tower
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class MetricSnapshot:
    tick: int
    metric_value: float
    confidence_score: float

class DamagePerCreditMetric:
    def __init__(self):
        self.metric_name: str = "DamagePerCreditMetric"
        self.description: str = "Evaluates economic ROI for each placed tower"
        self.history: List[MetricSnapshot] = []

    def record_sample(self, tick: int, raw_value: float, confidence: float = 1.0) -> None:
        self.history.append(MetricSnapshot(tick=tick, metric_value=raw_value, confidence_score=confidence))

    def get_average(self) -> float:
        if not self.history: return 0.0
        return sum(s.metric_value for s in self.history) / len(self.history)

    def get_latest(self) -> float:
        return self.history[-1].metric_value if self.history else 0.0
