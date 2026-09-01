"""
Sector 21 Complete Wave Spawn Schedule & Dynamic Timing Configuration.
Contains fixed wave templates, adaptive scaling thresholds, and boss trigger points.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class SpawnEntry:
    spawn_time_offset: float
    enemy_type: str
    count: int
    interval: float
    lane_index: int

@dataclass
class SectorWave:
    wave_number: int
    threat_budget: float
    spawns: List[SpawnEntry]
    bonus_credits: int

class Sector21WaveSchedule:
    def __init__(self):
        self.sector_id: str = "sector_21"
        self.total_waves: int = 33
        self.waves: List[SectorWave] = self._build_waves()

    def _build_waves(self) -> List[SectorWave]:
        waves = []
        for w in range(1, 34):
            is_boss_wave = (w % 5 == 0)
            threat = 20.0 + w * 12.0
            spawns = [
                SpawnEntry(0.0, "scout_infiltrator" if w < 5 else "armored_juggernaut", 4 + w, 1.2, 0),
                SpawnEntry(5.0, "aero_interceptor" if w % 2 == 0 else "emp_saboteur", 3 + (w // 2), 1.5, 1)
            ]
            if is_boss_wave:
                spawns.append(SpawnEntry(12.0, "dreadnought_titan" if w == 10 else "apocalypse_overlord", 1, 0.0, 0))

            waves.append(SectorWave(
                wave_number=w,
                threat_budget=threat,
                spawns=spawns,
                bonus_credits=50 + w * 15
            ))
        return waves

    def get_wave(self, wave_number: int) -> SectorWave:
        if 1 <= wave_number <= len(self.waves):
            return self.waves[wave_number - 1]
        return self.waves[-1]
