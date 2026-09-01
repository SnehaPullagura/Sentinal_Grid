"""
Adaptive Engine Evaluator: ChokepointDensityEvaluator
Quantifies spatial tower clustering at narrow corridor bottlenecks
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
from client.math.vector2d import Vector2D
from client.adaptive.defense_profiler import DefenseProfile

class ChokepointDensityEvaluator:
    def __init__(self):
        self.evaluation_score: float = 0.0
        self.history: List[float] = []

    def evaluate(self, profile: DefenseProfile, telemetry_data: Dict) -> float:
        score = 0.5
        if profile.kinetic_dominance > 0.6: score += 0.2
        if profile.crowd_control_reliance > 0.4: score += 0.3
        self.evaluation_score = min(1.0, score)
        self.history.append(self.evaluation_score)
        return self.evaluation_score

    def get_counter_weight(self) -> float:
        return self.evaluation_score * 1.5
