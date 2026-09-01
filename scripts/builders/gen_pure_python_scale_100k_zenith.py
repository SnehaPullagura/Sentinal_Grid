import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_zenith_scale():
    print("--> Generating 30 Planetary Defense Protocols (Pure Code)...")

    for s_idx in range(1, 31):
        prot_code = f'''"""
Sector {s_idx:02d} Planetary Defense Tactical Protocol Engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class DefenseProtocolDirective:
    code: str
    priority_level: int
    reinforcement_threshold_hp: float
    tactical_behavior: str

class Sector{s_idx:02d}DefenseProtocol:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
        self.directives: List[DefenseProtocolDirective] = [
            DefenseProtocolDirective("ALPHA_LOCKDOWN", 1, 0.25, "CONVERGE_DEFENSIVE_FIRE"),
            DefenseProtocolDirective("BETA_OVERDRIVE", 2, 0.50, "ACTIVATE_SURGE_BATTERIES"),
            DefenseProtocolDirective("GAMMA_EVAC", 3, 0.10, "PRIORITIZE_CORE_SURVIVAL")
        ]

    def get_directive_for_integrity(self, hp_ratio: float) -> DefenseProtocolDirective:
        for d in sorted(self.directives, key=lambda x: x.reinforcement_threshold_hp):
            if hp_ratio <= d.reinforcement_threshold_hp:
                return d
        return self.directives[1]
'''
        write_file(f"client/campaign/tactical_protocols/sector_{s_idx:02d}_protocol.py", prot_code)

    print("--> Generating 20 Commander Aura Solvers (Pure Code)...")

    towers = [
        "kinetic_vulcan", "gauss_accelerator", "tachyon_prism", "frostbite_cryo",
        "arc_discharger", "nanite_hive", "siege_howitzer", "orbital_uplink",
        "singularity_trap", "emp_disruptor_tower", "flak_anti_air", "plasma_mortar_artillery",
        "chrono_decelerator", "resource_refinery", "solar_lance", "sonic_resonator",
        "tesla_overcharger", "missile_pod_battery", "heavy_defense_matrix", "quantum_blaster"
    ]

    for t_idx, tow in enumerate(towers, 1):
        aura_code = f'''"""
Commander Tactical Aura & Spatial Resonance Solver: {tow.upper()}
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class AuraResonanceState:
    tower_id: str
    aura_radius: float
    efficiency_bonus_pct: float
    energy_regeneration_buff: float
    max_stacked_allies: int

class {tow.title().replace("_", "")}AuraSolver:
    def __init__(self):
        self.tower_id: str = "{tow}"
        self.base_radius: float = {120.0 + (t_idx % 6) * 15.0}

    def compute_aura_effect(self, ally_count_in_range: int) -> AuraResonanceState:
        eff = min(35.0, ally_count_in_range * {2.5 + (t_idx % 3)})
        return AuraResonanceState(
            tower_id=self.tower_id,
            aura_radius=self.base_radius,
            efficiency_bonus_pct=round(eff, 1),
            energy_regeneration_buff=round(ally_count_in_range * 0.4, 2),
            max_stacked_allies=8
        )
'''
        write_file(f"client/combat/aura_solvers/{tow}_aura_solver.py", aura_code)

    print("Zenith Scale Completed.")

if __name__ == "__main__":
    generate_zenith_scale()
