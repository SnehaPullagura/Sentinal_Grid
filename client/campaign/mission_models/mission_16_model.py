"""
Campaign Mission Model 16: Tactical Scenario Data & Execution Pipeline.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from client.math.vector2d import Vector2D

@dataclass
class SectorWaveConfig:
    wave_id: int
    threat_cap: float
    credit_reward: int
    energy_reward: int
    enemy_spawn_list: List[Tuple[str, int, float, float]]  # type, count, delay, interval
    special_hazard_active: bool = False

class Mission16DataModel:
    def __init__(self):
        self.mission_index: int = 16
        self.sector_name: str = "Tactical Sector 16 - Iron Outpost"
        self.world_tier: int = 4
        self.base_starting_credits: int = 720
        self.base_starting_energy: int = 180
        self.waves_data: Dict[int, SectorWaveConfig] = self._compile_waves()

    def _compile_waves(self) -> Dict[int, SectorWaveConfig]:
        waves = {}
        for w in range(1, 27):
            threat = round(20.0 + w * 12.5 + 16 * 3.5, 1)
            spawns = [
                ("scout_infiltrator" if w < 4 else "armored_juggernaut", 4 + w, 0.0, 1.2),
                ("aero_interceptor" if w % 2 == 0 else "emp_saboteur", 3 + (w // 2), 6.0, 1.5),
                ("hydra_broodmother" if w % 3 == 0 else "phantom_infiltrator", 2 + (w // 4), 12.0, 2.0)
            ]
            if w % 5 == 0:
                spawns.append(("dreadnought_titan" if w == 10 else "apocalypse_overlord", 1, 18.0, 0.0))

            waves[w] = SectorWaveConfig(
                wave_id=w,
                threat_cap=threat,
                credit_reward=60 + w * 15,
                energy_reward=15 + w * 2,
                enemy_spawn_list=spawns,
                special_hazard_active=(w % 4 == 0)
            )
        return waves

    def get_wave_config(self, wave_number: int) -> Optional[SectorWaveConfig]:
        return self.waves_data.get(wave_number)
