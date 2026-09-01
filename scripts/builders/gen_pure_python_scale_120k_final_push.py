import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_final_push():
    print("--> Generating 30 Sector Achievement Condition Solvers (Pure Code)...")

    for s_idx in range(1, 31):
        ach_code = f'''"""
Sector {s_idx:02d} In-Game Milestone & Medal Validator.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SectorMedalCriteria:
    medal_id: str
    name: str
    condition_description: str
    is_unlocked: bool

class Sector{s_idx:02d}MedalTracker:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
        self.medals: List[SectorMedalCriteria] = [
            SectorMedalCriteria("IRON_DEFENDER_{s_idx:02d}", "Iron Sentinel", "Take zero base core damage", False),
            SectorMedalCriteria("ENERGY_MAGNATE_{s_idx:02d}", "Energy Tycoon", "Accumulate over 1000 excess energy", False),
            SectorMedalCriteria("EXTERMINATOR_{s_idx:02d}", "Swarm Purger", "Eliminate all hostiles in under 4 minutes", False)
        ]

    def evaluate_medals(self, dmg_taken: float, final_energy: float, clear_time_sec: float) -> List[str]:
        unlocked = []
        if dmg_taken <= 0.0:
            unlocked.append(self.medals[0].medal_id)
        if final_energy >= 1000.0:
            unlocked.append(self.medals[1].medal_id)
        if clear_time_sec <= 240.0:
            unlocked.append(self.medals[2].medal_id)
        return unlocked
'''
        write_file(f"client/campaign/achievements_tracker_code/sector_{s_idx:02d}_medal_tracker.py", ach_code)

    print("--> Generating 20 Thermal Overheat Solvers (Pure Code)...")

    towers = [
        "kinetic_vulcan", "gauss_accelerator", "tachyon_prism", "frostbite_cryo",
        "arc_discharger", "nanite_hive", "siege_howitzer", "orbital_uplink",
        "singularity_trap", "emp_disruptor_tower", "flak_anti_air", "plasma_mortar_artillery",
        "chrono_decelerator", "resource_refinery", "solar_lance", "sonic_resonator",
        "tesla_overcharger", "missile_pod_battery", "heavy_defense_matrix", "quantum_blaster"
    ]

    for t_idx, tow in enumerate(towers, 1):
        heat_code = f'''"""
Thermal Dissipation & Overheat Penalty Engine: {tow.upper()}
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class HeatStatusSnapshot:
    current_temp_c: float
    is_overheated: bool
    cooldown_sec_remaining: float
    firerate_penalty_pct: float

class {tow.title().replace("_", "")}ThermalEngine:
    def __init__(self):
        self.tower_id: str = "{tow}"
        self.max_temp_c: float = {150.0 + (t_idx % 5) * 20.0}
        self.heat_per_shot_c: float = {4.0 + (t_idx % 4) * 1.5}
        self.dissipation_rate_c_per_sec: float = 12.0

    def calculate_thermal_tick(self, current_temp: float, shots_fired: int, delta_time: float) -> HeatStatusSnapshot:
        added_heat = shots_fired * self.heat_per_shot_c
        dissipated = self.dissipation_rate_c_per_sec * delta_time
        temp = max(25.0, current_temp + added_heat - dissipated)
        is_jammed = temp >= self.max_temp_c
        penalty = 0.50 if is_jammed else (temp / self.max_temp_c) * 0.20

        return HeatStatusSnapshot(
            current_temp_c=round(temp, 1),
            is_overheated=is_jammed,
            cooldown_sec_remaining=round((temp - 25.0) / self.dissipation_rate_c_per_sec, 2) if is_jammed else 0.0,
            firerate_penalty_pct=round(penalty, 2)
        )
'''
        write_file(f"client/combat/overheat_solvers/{tow}_thermal_engine.py", heat_code)

    print("Final Push Scale Completed.")

if __name__ == "__main__":
    generate_final_push()
