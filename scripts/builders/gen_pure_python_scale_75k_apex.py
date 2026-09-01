import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_apex_scale():
    print("--> Generating 30 Full Mission Orchestration Engines (Pure Code)...")

    for s_idx in range(1, 31):
        m_code = f'''"""
Sector {s_idx:02d} Complete Mission Orchestrator & Live Combat Director.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from client.math.vector2d import Vector2D

@dataclass
class SectorEncounterState:
    wave_current: int = 1
    total_waves: int = {12 + s_idx}
    active_threat: float = 0.0
    casualties_total: int = 0
    commander_abilities_used: int = 0
    is_completed: bool = False

class Sector{s_idx:02d}MissionOrchestrator:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
        self.state: SectorEncounterState = SectorEncounterState()
        self.base_defense_rating: float = {100.0 + s_idx * 5.0}

    def evaluate_wave_progression(self, wave: int, remaining_hostiles: int) -> bool:
        self.state.wave_current = wave
        if remaining_hostiles == 0 and wave >= self.state.total_waves:
            self.state.is_completed = True
            return True
        return False

    def get_mission_report(self) -> dict:
        return {{
            "sector": self.sector_id,
            "wave": self.state.wave_current,
            "completed": self.state.is_completed,
            "rating": self.base_defense_rating
        }}
'''
        write_file(f"client/campaign/missions_full_code/sector_{s_idx:02d}_orchestrator.py", m_code)

    print("--> Generating 20 Advanced Combat Resolvers (Pure Code)...")

    towers = [
        "kinetic_vulcan", "gauss_accelerator", "tachyon_prism", "frostbite_cryo",
        "arc_discharger", "nanite_hive", "siege_howitzer", "orbital_uplink",
        "singularity_trap", "emp_disruptor_tower", "flak_anti_air", "plasma_mortar_artillery",
        "chrono_decelerator", "resource_refinery", "solar_lance", "sonic_resonator",
        "tesla_overcharger", "missile_pod_battery", "heavy_defense_matrix", "quantum_blaster"
    ]

    for t_idx, tow in enumerate(towers, 1):
        r_code = f'''"""
Advanced Combat Resolver & Status Matrix: {tow.upper()}
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class AdvancedCombatResolution:
    final_damage: float
    armor_shred: float
    shield_pierced: bool
    proc_effect: str
    combat_efficiency: float

class {tow.title().replace("_", "")}AdvancedResolver:
    def __init__(self):
        self.tower_id: str = "{tow}"
        self.base_power: float = {25.0 + t_idx * 4.0}
        self.pierce_ratio: float = {0.15 + (t_idx % 4) * 0.10}

    def resolve_combat_strike(
        self,
        target_hp: float,
        target_armor: float,
        target_shield: float,
        distance: float
    ) -> AdvancedCombatResolution:
        shred = target_armor * self.pierce_ratio
        eff_armor = max(0.0, target_armor - shred)
        dmg = self.base_power * max(0.5, 1.0 - (distance / 400.0) * 0.2)
        final = max(1.0, dmg - (eff_armor * 0.4))

        return AdvancedCombatResolution(
            final_damage=round(final, 2),
            armor_shred=round(shred, 2),
            shield_pierced=(target_shield <= 0.0 or "{tow}" == "quantum_blaster"),
            proc_effect="OVERCLOCK_CRIT" if final > self.base_power else "STANDARD_HIT",
            combat_efficiency=round(final / max(1.0, self.base_power), 3)
        )
'''
        write_file(f"client/combat/calculators_advanced/{tow}_advanced_resolver.py", r_code)

    print("--> Generating 30 Adaptive Sector Defense Profilers (Pure Code)...")

    for s_idx in range(1, 31):
        prof_code = f'''"""
Sector {s_idx:02d} Adaptive Defense Profiler & Counter-Wave Engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class DefensePostureProfile:
    kinetic_weight: float
    energy_weight: float
    control_weight: float
    recommended_threat_counter: str
    target_budget_mult: float

class Sector{s_idx:02d}AdaptiveProfiler:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
        self.historical_postures: List[DefensePostureProfile] = []

    def evaluate_defense_posture(self, kinetic_dmg: float, energy_dmg: float, control_count: int) -> DefensePostureProfile:
        total = max(1.0, kinetic_dmg + energy_dmg)
        k_ratio = kinetic_dmg / total
        e_ratio = energy_dmg / total
        c_weight = min(1.0, control_count * 0.1)

        counter = "ARMORED_VANGUARD" if k_ratio > 0.6 else "PHASE_DISRUPTOR" if e_ratio > 0.6 else "AERO_SWARM"
        profile = DefensePostureProfile(
            kinetic_weight=round(k_ratio, 2),
            energy_weight=round(e_ratio, 2),
            control_weight=round(c_weight, 2),
            recommended_threat_counter=counter,
            target_budget_mult=1.15 if total > 2000.0 else 1.0
        )
        self.historical_postures.append(profile)
        return profile
'''
        write_file(f"client/adaptive/profilers_code/sector_{s_idx:02d}_adaptive_profiler.py", prof_code)

    print("Apex Scale Generated.")

if __name__ == "__main__":
    generate_apex_scale()
