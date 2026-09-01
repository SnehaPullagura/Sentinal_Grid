import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_ultimate_scale():
    print("--> Generating 30 Full Sector Wave Schedule Matrix Models (Pure Code)...")

    for s_idx in range(1, 31):
        w_code = f'''"""
Sector {s_idx:02d} Complete Wave Schedule & Enemy Density Matrix.
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

class Sector{s_idx:02d}WaveScheduleMatrix:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
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
'''
        write_file(f"client/campaign/wave_schedules_full/sector_{s_idx:02d}_wave_schedule.py", w_code)

    print("--> Generating 20 Enemy Mutation & Adaptation Solvers (Pure Code)...")

    enemies = [
        "scout_infiltrator", "armored_juggernaut", "phantom_infiltrator", "aero_interceptor",
        "aegis_shield_bearer", "nanite_medic", "emp_saboteur", "hydra_broodmother",
        "shadow_assassin", "siege_breaker_ram", "dreadnought_titan", "cyber_hive_carrier",
        "glider_swarmer", "heavy_colossus", "leech_parasite", "phase_shifter",
        "warp_striker", "vanguard_mech", "frost_walker", "apocalypse_overlord"
    ]

    for e_idx, ene in enumerate(enemies, 1):
        mut_code = f'''"""
Enemy Mutation & Defensive Adaptation Engine: {ene.upper()}
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class EnemyMutationState:
    mutation_id: str
    speed_factor: float
    armor_factor: float
    shield_factor: float
    special_perk: str

class {ene.title().replace("_", "")}MutationEngine:
    def __init__(self):
        self.enemy_type: str = "{ene}"
        self.base_tier: int = {((e_idx - 1) // 4) + 1}

    def generate_counter_mutation(self, player_kinetic_ratio: float, player_energy_ratio: float) -> EnemyMutationState:
        if player_kinetic_ratio > 0.6:
            return EnemyMutationState("HARDENED_CARAPACE", 0.90, 1.50, 1.0, "KINETIC_RESISTANCE_50")
        elif player_energy_ratio > 0.6:
            return EnemyMutationState("REFLECTIVE_SHIELDING", 1.0, 0.85, 1.60, "ENERGY_ABSORPTION_40")
        return EnemyMutationState("AGILITY_SERVO", 1.25, 1.0, 1.0, "EVASION_BOOST_25")
'''
        write_file(f"client/ai/mutation_solvers/{ene}_mutation_solver.py", mut_code)

    print("Ultimate Scale Completed.")

if __name__ == "__main__":
    generate_ultimate_scale()
