"""
Sector 17 Complete Wave Schedule & Enemy Density Matrix.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class WaveScheduleEntry:
    wave_index: int
    enemy_composition: List[Tuple[str, int]]
    spawn_interval_sec: float
    total_wave_threat: float
    tactical_modifier: str

class Sector17WaveScheduleMatrix:
    def __init__(self):
        self.sector_id: str = "sector_17"
        self.schedules: List[WaveScheduleEntry] = [
            WaveScheduleEntry(1, [("scout_infiltrator", 5)], 1.0, 50.0, "STANDARD_PROBE"),
            WaveScheduleEntry(2, [("scout_infiltrator", 8), ("aero_interceptor", 2)], 0.8, 85.0, "AIR_RECON"),
            WaveScheduleEntry(3, [("armored_juggernaut", 3), ("scout_infiltrator", 6)], 1.2, 120.0, "ARMOR_VANGUARD"),
            WaveScheduleEntry(4, [("hydra_broodmother", 2), ("emp_saboteur", 3)], 1.5, 180.0, "SWARM_ASSAULT"),
            WaveScheduleEntry(5, [("dreadnought_titan", 1), ("nanite_medic", 3)], 2.0, 250.0, "TITAN_CRUCIBLE")
        ]

    def get_schedule(self, wave: int) -> WaveScheduleEntry:
        if 1 <= wave <= len(self.schedules):
            return self.schedules[wave - 1]
        return self.schedules[-1]
