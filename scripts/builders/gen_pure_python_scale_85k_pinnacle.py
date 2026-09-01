import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_pinnacle_scale():
    print("--> Generating 30 World Lore & Intel Codex Modules (Pure Code)...")

    for s_idx in range(1, 31):
        lore_code = f'''"""
Sector {s_idx:02d} Archive Lore, Threat Intelligence & Planetary Codex.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class CodexIntelEntry:
    entry_id: str
    classification: str
    historical_notes: str
    geological_composition: str
    strategic_value_score: int

class Sector{s_idx:02d}CodexArchive:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
        self.entries: List[CodexIntelEntry] = [
            CodexIntelEntry(
                entry_id="INTEL_{s_idx:02d}_A",
                classification="RESTRICTED_TACTICAL",
                historical_notes="Primary energy conduits established during the first expansion war.",
                geological_composition="Dense silicate crust with enriched plasma veins.",
                strategic_value_score={80 + s_idx}
            ),
            CodexIntelEntry(
                entry_id="INTEL_{s_idx:02d}_B",
                classification="BIOLOGICAL_HAZARD",
                historical_notes="Observed swarmer nest formations beneath abandoned research installations.",
                geological_composition="Chitin-infused subterranean tunnels.",
                strategic_value_score={65 + s_idx}
            )
        ]

    def get_highest_priority_intel(self) -> CodexIntelEntry:
        return self.entries[0]
'''
        write_file(f"client/campaign/codex_lore/sector_{s_idx:02d}_codex.py", lore_code)

    print("--> Generating 20 Overdrive Capability Solvers (Pure Code)...")

    towers = [
        "kinetic_vulcan", "gauss_accelerator", "tachyon_prism", "frostbite_cryo",
        "arc_discharger", "nanite_hive", "siege_howitzer", "orbital_uplink",
        "singularity_trap", "emp_disruptor_tower", "flak_anti_air", "plasma_mortar_artillery",
        "chrono_decelerator", "resource_refinery", "solar_lance", "sonic_resonator",
        "tesla_overcharger", "missile_pod_battery", "heavy_defense_matrix", "quantum_blaster"
    ]

    for t_idx, tow in enumerate(towers, 1):
        over_code = f'''"""
Overdrive Supercharge Solver: {tow.upper()}
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class OverdriveDischargeState:
    is_overdriven: bool
    damage_boost_mult: float
    firerate_boost_mult: float
    energy_consumption_per_sec: float
    heat_dissipation_factor: float

class {tow.title().replace("_", "")}OverdriveSolver:
    def __init__(self):
        self.tower_id: str = "{tow}"
        self.nominal_power_mw: float = {4.5 + t_idx * 1.2}

    def activate_overdrive(self, current_energy: float) -> OverdriveDischargeState:
        can_boost = current_energy >= 25.0
        return OverdriveDischargeState(
            is_overdriven=can_boost,
            damage_boost_mult=1.65 if can_boost else 1.0,
            firerate_boost_mult=1.40 if can_boost else 1.0,
            energy_consumption_per_sec=5.0 if can_boost else 0.0,
            heat_dissipation_factor=0.85
        )
'''
        write_file(f"client/combat/overdrive_matrices/{tow}_overdrive_solver.py", over_code)

    print("Pinnacle Scale Completed.")

if __name__ == "__main__":
    generate_pinnacle_scale()
