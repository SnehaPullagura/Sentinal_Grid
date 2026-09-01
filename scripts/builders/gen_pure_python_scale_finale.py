import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_grand_scale_finale():
    print("--> Generating 30 Military Operational Briefing Modules (Pure Code)...")

    for s_idx in range(1, 31):
        directives = []
        for d in range(1, 6):
            directives.append(f'''
            OperationalDirective(
                directive_id="DIR_{s_idx:02d}_{d}",
                title="Perimeter Objective #{d}",
                description="Secure grid sector {s_idx:02d} sub-station {d} against hostile infiltration.",
                priority_level="HIGH" if {d} == 1 else "STANDARD",
                reward_tokens={10 + d * 5}
            )''')
        dir_joined = ",".join(directives)

        b_code = f'''"""
Sector {s_idx:02d} Operational Command Directive & Strategic Rulebook.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

@dataclass
class OperationalDirective:
    directive_id: str
    title: str
    description: str
    priority_level: str
    reward_tokens: int

class Sector{s_idx:02d}OperationalBriefing:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
        self.operational_tier: int = {((s_idx - 1) // 5) + 1}
        self.directives: List[OperationalDirective] = [{dir_joined}
        ]

    def get_primary_directive(self) -> OperationalDirective:
        return self.directives[0]
'''
        write_file(f"client/campaign/briefings_code/sector_{s_idx:02d}_briefing.py", b_code)

    print("--> Generating 20 Tower Matchup Multiplier Matrices (Pure Code)...")

    towers = [
        "kinetic_vulcan", "gauss_accelerator", "tachyon_prism", "frostbite_cryo",
        "arc_discharger", "nanite_hive", "siege_howitzer", "orbital_uplink",
        "singularity_trap", "emp_disruptor_tower", "flak_anti_air", "plasma_mortar_artillery",
        "chrono_decelerator", "resource_refinery", "solar_lance", "sonic_resonator",
        "tesla_overcharger", "missile_pod_battery", "heavy_defense_matrix", "quantum_blaster"
    ]
    enemies = [
        "scout_infiltrator", "armored_juggernaut", "phantom_infiltrator", "aero_interceptor",
        "aegis_shield_bearer", "nanite_medic", "emp_saboteur", "hydra_broodmother",
        "shadow_assassin", "siege_breaker_ram", "dreadnought_titan", "cyber_hive_carrier",
        "glider_swarmer", "heavy_colossus", "leech_parasite", "phase_shifter",
        "warp_striker", "vanguard_mech", "frost_walker", "apocalypse_overlord"
    ]

    for t_idx, tow in enumerate(towers, 1):
        matchup_entries = []
        for e_idx, ene in enumerate(enemies, 1):
            mult = 1.45 if (tow == "gauss_accelerator" and "juggernaut" in ene) or (tow == "flak_anti_air" and "interceptor" in ene) else 1.0
            matchup_entries.append(f'''
            MatchupCoeff(
                enemy_type="{ene}",
                damage_multiplier={mult},
                armor_penetration_override={0.20 + (t_idx % 4) * 0.15},
                status_application_potency={1.0 + (e_idx % 3) * 0.25}
            )''')
        m_joined = ",".join(matchup_entries)

        t_code = f'''"""
Tower Matchup Multiplier Matrix: {tow.upper()}
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class MatchupCoeff:
    enemy_type: str
    damage_multiplier: float
    armor_penetration_override: float
    status_application_potency: float

class {tow.title().replace("_", "")}MatrixTable:
    def __init__(self):
        self.tower_id: str = "{tow}"
        self.coefficients: Dict[str, MatchupCoeff] = self._init_table()

    def _init_table(self) -> Dict[str, MatchupCoeff]:
        raw_list = [{m_joined}
        ]
        return {{c.enemy_type: c for c in raw_list}}

    def get_coeff(self, enemy_type: str) -> MatchupCoeff:
        return self.coefficients.get(enemy_type, MatchupCoeff(enemy_type, 1.0, 0.20, 1.0))
'''
        write_file(f"client/combat/tables_code/{tow}_matrix_table.py", t_code)

    print("--> Generating 30 Performance Analytics Solvers (Pure Code)...")

    for s_idx in range(1, 31):
        p_code = f'''"""
Sector {s_idx:02d} Combat Efficiency & Performance Solver.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

@dataclass
class WavePerformanceSnapshot:
    wave_id: int
    damage_dealt: float
    damage_taken: float
    credits_spent: int
    tactical_score: int

class Sector{s_idx:02d}PerformanceSolver:
    def __init__(self):
        self.sector_id: str = "sector_{s_idx:02d}"
        self.snapshots: List[WavePerformanceSnapshot] = []

    def record_wave(self, wave: int, dmg_out: float, dmg_in: float, credits: int) -> int:
        score = int(max(0.0, dmg_out * 2.0 - dmg_in * 5.0) + (100 - wave * 2))
        self.snapshots.append(WavePerformanceSnapshot(
            wave_id=wave,
            damage_dealt=dmg_out,
            damage_taken=dmg_in,
            credits_spent=credits,
            tactical_score=score
        ))
        return score

    def calculate_total_score(self) -> int:
        return sum(s.tactical_score for s in self.snapshots)
'''
        write_file(f"client/analytics/performance_code/sector_{s_idx:02d}_performance.py", p_code)

    print("Grand Scale Finale Generated.")

if __name__ == "__main__":
    generate_grand_scale_finale()
