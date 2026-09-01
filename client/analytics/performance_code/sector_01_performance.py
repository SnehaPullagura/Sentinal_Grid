"""
Sector 01 Combat Efficiency & Performance Solver.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

@dataclass
class WavePerformanceSnapshot:
    wave_id: int
    damage_dealt: float
    damage_taken: float
    credits_spent: int
    tactical_score: int

class Sector01PerformanceSolver:
    def __init__(self):
        self.sector_id: str = "sector_01"
        self.snapshots: List[WavePerformanceSnapshot] = []

    def record_wave(self, wave: int, dmg_out: float, dmg_in: float, credits: int) -> int:
        score = int(max(0.0, dmg_out * 2.0 - dmg_in * 5.0) + (100 - wave * 2))
        self.snapshots.append(WavePerformanceSnapshot(
            wave_id=wave,
            damage_dealt=dmg_out,
            damage_taken=dmg_in,
            credits_spent=credits,
            tactical_score=score
        ))
        return score

    def calculate_total_score(self) -> int:
        return sum(s.tactical_score for s in self.snapshots)
