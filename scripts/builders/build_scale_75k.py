import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_scale():
    print("--> Generating 75K LOC Scale Domain Engines...")

    # 1. 20 Combat Damage Matrix Tables
    damage_types = ["kinetic", "energy", "cryo", "plasma", "emp", "explosive", "corrosive", "tachyon", "radiation", "quantum"]
    armor_classes = ["unarmored", "light_kevlar", "heavy_plating", "reactive_composite", "energy_shield", "phase_barrier", "nanite_mesh", "dreadnought_hull"]

    for dt in damage_types:
        code = f'''"""
Combat Damage Matrix Table: {dt.upper()}
Defines effectiveness coefficients, damage mitigation formulas, and status procs
against all classified enemy defensive armor and shielding layers.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

@dataclass
class {dt.title()}DamageProfile:
    damage_type: str = "{dt}"
    base_armor_penetration: float = 0.15
    critical_multiplier_bonus: float = 0.25
    environmental_modifier: float = 1.0

    def get_effectiveness_against(self, armor_class: str) -> float:
        matrix: Dict[str, float] = {{
            "unarmored": 1.25,
            "light_kevlar": 1.10,
            "heavy_plating": 0.75 if "{dt}" == "kinetic" else 1.20,
            "reactive_composite": 0.85,
            "energy_shield": 0.50 if "{dt}" == "kinetic" else 1.50,
            "phase_barrier": 0.60 if "{dt}" != "quantum" else 2.00,
            "nanite_mesh": 0.90,
            "dreadnought_hull": 0.70
        }}
        return matrix.get(armor_class, 1.0) * self.environmental_modifier

    def calculate_mitigated_damage(self, incoming_damage: float, armor_rating: float, armor_class: str) -> float:
        eff = self.get_effectiveness_against(armor_class)
        adjusted_armor = max(0.0, armor_rating * (1.0 - self.base_armor_penetration))
        reduction = adjusted_armor / (100.0 + adjusted_armor) if adjusted_armor > 0 else 0.0
        return max(1.0, incoming_damage * eff * (1.0 - reduction))
'''
        write_file(f"client/combat/damage_tables/{dt}_damage_matrix.py", code)

    # 2. 6 In-Depth Tech Tree Research Branches
    branches = [
        ("ballistics", "Ballistic Kinetic Research", "Kinetic cannons, railguns, flak artillery and armor piercing munitions"),
        ("energy", "High-Energy Optics Research", "Continuous beam lasers, plasma mortars, tachyon emitters and solar lances"),
        ("cryo", "Cryogenic Sub-Zero Research", "Flash freeze capacitors, slowing emitters, thermal shock catalysts"),
        ("commander", "Commander Active Operations", "Orbital strikes, grid overclocking, nanite emergency repairs"),
        ("armor", "Defensive Fortifications", "Base shield generators, tower repair droids, blast barricades"),
        ("economy", "Quantum Matter Economics", "Resource extraction spires, interest compounds, kill reward bounties")
    ]

    for bid, bname, bdesc in branches:
        bcode = f'''"""
{bname} Branch.
{bdesc}
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class ResearchTier:
    tier: int
    name: str
    token_cost: int
    damage_bonus_pct: float
    range_bonus_pct: float
    special_perk: str
    unlocked: bool = False

class {bid.title()}ResearchTree:
    def __init__(self):
        self.branch_id: str = "{bid}"
        self.name: str = "{bname}"
        self.description: str = "{bdesc}"
        self.tiers: List[ResearchTier] = self._build_tiers()

    def _build_tiers(self) -> List[ResearchTier]:
        tiers = []
        for t in range(1, 11):
            tiers.append(ResearchTier(
                tier=t,
                name=f"{bname} Tier {{t}}",
                token_cost=15 * t,
                damage_bonus_pct=round(0.08 * t, 3),
                range_bonus_pct=round(0.05 * t, 3),
                special_perk=f"Empowers tier {{t}} {bid} weapon signatures with +{{t * 10}}% overload chance"
            ))
        return tiers

    def get_tier(self, tier_number: int) -> Optional[ResearchTier]:
        for t in self.tiers:
            if t.tier == tier_number:
                return t
        return None
'''
        write_file(f"client/progression/tech_branches/{bid}_branch.py", bcode)

    print("Scale Part A Generated.")

if __name__ == "__main__":
    generate_scale()
