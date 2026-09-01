import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_summit_scale():
    print("--> Generating 30 Victory Condition Solvers (Pure Code)...")

    for s_idx in range(1, 31):
        v_code = f'''"""
Sector {s_idx:02d} Victory Condition & Star Rating Engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class SectorStarRating:
    stars_awarded: int
    flawless_victory: bool
    under_budget_bonus: bool
    speedrun_bonus: bool

class Sector{s_idx:02d}VictoryEvaluator:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
        self.flawless_hp_threshold: float = {95.0 - (s_idx % 5)}

    def evaluate_victory(self, hp_pct: float, time_sec: float, spent_credits: int) -> SectorStarRating:
        is_flawless = hp_pct >= self.flawless_hp_threshold
        is_speed = time_sec <= (300.0 + {s_idx * 10})
        is_budget = spent_credits <= (2500 + {s_idx * 150})

        stars = 1
        if is_flawless:
            stars += 1
        if is_speed and is_budget:
            stars += 1

        return SectorStarRating(
            stars_awarded=min(3, stars),
            flawless_victory=is_flawless,
            under_budget_bonus=is_budget,
            speedrun_bonus=is_speed
        )
'''
        write_file(f"client/campaign/victory_conditions/sector_{s_idx:02d}_victory.py", v_code)

    print("--> Generating 20 Tower Synergy Solvers (Pure Code)...")

    towers = [
        "kinetic_vulcan", "gauss_accelerator", "tachyon_prism", "frostbite_cryo",
        "arc_discharger", "nanite_hive", "siege_howitzer", "orbital_uplink",
        "singularity_trap", "emp_disruptor_tower", "flak_anti_air", "plasma_mortar_artillery",
        "chrono_decelerator", "resource_refinery", "solar_lance", "sonic_resonator",
        "tesla_overcharger", "missile_pod_battery", "heavy_defense_matrix", "quantum_blaster"
    ]

    for t_idx, tow in enumerate(towers, 1):
        syn_code = f'''"""
Tower Combo Synergy Solver: {tow.upper()}
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class SynergyProcOutcome:
    combo_name: str
    bonus_damage_multiplier: float
    chain_reaction_triggered: bool

class {tow.title().replace("_", "")}SynergySolver:
    def __init__(self):
        self.primary_tower: str = "{tow}"

    def evaluate_combo_with(self, partner_tower_id: str) -> SynergyProcOutcome:
        if partner_tower_id in ("frostbite_cryo", "singularity_trap", "arc_discharger"):
            return SynergyProcOutcome(f"{tow.upper()}_ELEMENTAL_CONVERGENCE", 1.45, True)
        return SynergyProcOutcome(f"{tow.upper()}_REINFORCED_FIRE", 1.10, False)
'''
        write_file(f"client/combat/synergy_solvers/{tow}_synergy_solver.py", syn_code)

    print("Summit Scale Completed.")

if __name__ == "__main__":
    generate_summit_scale()
