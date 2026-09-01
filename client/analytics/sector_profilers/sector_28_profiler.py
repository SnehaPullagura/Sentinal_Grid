"""
Sector 28 Real-Time Telemetry Profiler & Defense Gap Evaluator.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from client.math.vector2d import Vector2D

@dataclass
class SectorMetricLog:
    tick_stamp: int
    active_towers_count: int
    active_hostiles_count: int
    cumulative_damage_dealt: float
    cumulative_damage_taken: float
    current_threat_budget: float
    cluster_entropy: float

class Sector28TelemetryProfiler:
    def __init__(self):
        self.sector_id: str = "sector_28"
        self.sampling_rate_hz: int = 10
        self.logs: List[SectorMetricLog] = []

    def record_tick_telemetry(
        self,
        tick: int,
        towers: int,
        hostiles: int,
        dmg_out: float,
        dmg_in: float,
        threat: float
    ) -> None:
        entropy = (towers * 1.5) / max(1, hostiles)
        self.logs.append(SectorMetricLog(
            tick_stamp=tick,
            active_towers_count=towers,
            active_hostiles_count=hostiles,
            cumulative_damage_dealt=dmg_out,
            cumulative_damage_taken=dmg_in,
            current_threat_budget=threat,
            cluster_entropy=round(entropy, 3)
        ))

    def get_peak_dps(self) -> float:
        if len(self.logs) < 2:
            return 0.0
        return max(l.cumulative_damage_dealt for l in self.logs)

    def get_survival_score(self) -> float:
        if not self.logs:
            return 1.0
        last = self.logs[-1]
        return max(0.0, 1.0 - (last.cumulative_damage_taken / 1000.0))
