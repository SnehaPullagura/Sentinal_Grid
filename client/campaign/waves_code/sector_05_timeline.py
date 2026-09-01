"""
Sector 05 Complete Wave Timeline & Threat Matrix.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Dict

@dataclass
class WaveTimeline:
    wave_number: int
    threat_cost: float
    credit_reward: int
    energy_reward: int
    spawn_events: List[Tuple[str, int, float, float]]

class Sector05WaveCompiler:
    def __init__(self):
        self.sector_id: str = "sector_05"
        self.timelines: List[WaveTimeline] = [
            WaveTimeline(
                wave_number=1,
                threat_cost=52.0,
                credit_reward=65,
                energy_reward=12,
                spawn_events=[
                    ("scout_infiltrator" if 1 < 4 else "armored_juggernaut", 5, 0.0, 1.2),
                    ("aero_interceptor" if 1 % 2 == 0 else "emp_saboteur", 3, 5.0, 1.5),
                    ("hydra_broodmother" if 1 % 3 == 0 else "phantom_infiltrator", 2, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=2,
                threat_cost=64.0,
                credit_reward=80,
                energy_reward=14,
                spawn_events=[
                    ("scout_infiltrator" if 2 < 4 else "armored_juggernaut", 6, 0.0, 1.2),
                    ("aero_interceptor" if 2 % 2 == 0 else "emp_saboteur", 4, 5.0, 1.5),
                    ("hydra_broodmother" if 2 % 3 == 0 else "phantom_infiltrator", 2, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=3,
                threat_cost=76.0,
                credit_reward=95,
                energy_reward=16,
                spawn_events=[
                    ("scout_infiltrator" if 3 < 4 else "armored_juggernaut", 7, 0.0, 1.2),
                    ("aero_interceptor" if 3 % 2 == 0 else "emp_saboteur", 4, 5.0, 1.5),
                    ("hydra_broodmother" if 3 % 3 == 0 else "phantom_infiltrator", 2, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=4,
                threat_cost=88.0,
                credit_reward=110,
                energy_reward=18,
                spawn_events=[
                    ("scout_infiltrator" if 4 < 4 else "armored_juggernaut", 8, 0.0, 1.2),
                    ("aero_interceptor" if 4 % 2 == 0 else "emp_saboteur", 5, 5.0, 1.5),
                    ("hydra_broodmother" if 4 % 3 == 0 else "phantom_infiltrator", 3, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=5,
                threat_cost=100.0,
                credit_reward=125,
                energy_reward=20,
                spawn_events=[
                    ("scout_infiltrator" if 5 < 4 else "armored_juggernaut", 9, 0.0, 1.2),
                    ("aero_interceptor" if 5 % 2 == 0 else "emp_saboteur", 5, 5.0, 1.5),
                    ("hydra_broodmother" if 5 % 3 == 0 else "phantom_infiltrator", 3, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=6,
                threat_cost=112.0,
                credit_reward=140,
                energy_reward=22,
                spawn_events=[
                    ("scout_infiltrator" if 6 < 4 else "armored_juggernaut", 10, 0.0, 1.2),
                    ("aero_interceptor" if 6 % 2 == 0 else "emp_saboteur", 6, 5.0, 1.5),
                    ("hydra_broodmother" if 6 % 3 == 0 else "phantom_infiltrator", 3, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=7,
                threat_cost=124.0,
                credit_reward=155,
                energy_reward=24,
                spawn_events=[
                    ("scout_infiltrator" if 7 < 4 else "armored_juggernaut", 11, 0.0, 1.2),
                    ("aero_interceptor" if 7 % 2 == 0 else "emp_saboteur", 6, 5.0, 1.5),
                    ("hydra_broodmother" if 7 % 3 == 0 else "phantom_infiltrator", 3, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=8,
                threat_cost=136.0,
                credit_reward=170,
                energy_reward=26,
                spawn_events=[
                    ("scout_infiltrator" if 8 < 4 else "armored_juggernaut", 12, 0.0, 1.2),
                    ("aero_interceptor" if 8 % 2 == 0 else "emp_saboteur", 7, 5.0, 1.5),
                    ("hydra_broodmother" if 8 % 3 == 0 else "phantom_infiltrator", 4, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=9,
                threat_cost=148.0,
                credit_reward=185,
                energy_reward=28,
                spawn_events=[
                    ("scout_infiltrator" if 9 < 4 else "armored_juggernaut", 13, 0.0, 1.2),
                    ("aero_interceptor" if 9 % 2 == 0 else "emp_saboteur", 7, 5.0, 1.5),
                    ("hydra_broodmother" if 9 % 3 == 0 else "phantom_infiltrator", 4, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=10,
                threat_cost=160.0,
                credit_reward=200,
                energy_reward=30,
                spawn_events=[
                    ("scout_infiltrator" if 10 < 4 else "armored_juggernaut", 14, 0.0, 1.2),
                    ("aero_interceptor" if 10 % 2 == 0 else "emp_saboteur", 8, 5.0, 1.5),
                    ("hydra_broodmother" if 10 % 3 == 0 else "phantom_infiltrator", 4, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=11,
                threat_cost=172.0,
                credit_reward=215,
                energy_reward=32,
                spawn_events=[
                    ("scout_infiltrator" if 11 < 4 else "armored_juggernaut", 15, 0.0, 1.2),
                    ("aero_interceptor" if 11 % 2 == 0 else "emp_saboteur", 8, 5.0, 1.5),
                    ("hydra_broodmother" if 11 % 3 == 0 else "phantom_infiltrator", 4, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=12,
                threat_cost=184.0,
                credit_reward=230,
                energy_reward=34,
                spawn_events=[
                    ("scout_infiltrator" if 12 < 4 else "armored_juggernaut", 16, 0.0, 1.2),
                    ("aero_interceptor" if 12 % 2 == 0 else "emp_saboteur", 9, 5.0, 1.5),
                    ("hydra_broodmother" if 12 % 3 == 0 else "phantom_infiltrator", 5, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=13,
                threat_cost=196.0,
                credit_reward=245,
                energy_reward=36,
                spawn_events=[
                    ("scout_infiltrator" if 13 < 4 else "armored_juggernaut", 17, 0.0, 1.2),
                    ("aero_interceptor" if 13 % 2 == 0 else "emp_saboteur", 9, 5.0, 1.5),
                    ("hydra_broodmother" if 13 % 3 == 0 else "phantom_infiltrator", 5, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=14,
                threat_cost=208.0,
                credit_reward=260,
                energy_reward=38,
                spawn_events=[
                    ("scout_infiltrator" if 14 < 4 else "armored_juggernaut", 18, 0.0, 1.2),
                    ("aero_interceptor" if 14 % 2 == 0 else "emp_saboteur", 10, 5.0, 1.5),
                    ("hydra_broodmother" if 14 % 3 == 0 else "phantom_infiltrator", 5, 10.0, 2.0)
                ]
            ),
            WaveTimeline(
                wave_number=15,
                threat_cost=220.0,
                credit_reward=275,
                energy_reward=40,
                spawn_events=[
                    ("scout_infiltrator" if 15 < 4 else "armored_juggernaut", 19, 0.0, 1.2),
                    ("aero_interceptor" if 15 % 2 == 0 else "emp_saboteur", 10, 5.0, 1.5),
                    ("hydra_broodmother" if 15 % 3 == 0 else "phantom_infiltrator", 5, 10.0, 2.0)
                ]
            )
        ]

    def get_timeline(self, wave: int) -> WaveTimeline:
        if 1 <= wave <= len(self.timelines):
            return self.timelines[wave - 1]
        return self.timelines[-1]
