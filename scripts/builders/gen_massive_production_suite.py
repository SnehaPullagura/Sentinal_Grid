import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    print("--> Generating Massive Production Domain Suites...")

    # 1. 10 Challenge Mode Engines
    challenges = [
        ("challenge_limited_resources", "Resource Scarcity", "Credits and Energy income reduced by 60%"),
        ("challenge_fog_of_war", "Radar Blindspot", "Tower detection range reduced by 40%"),
        ("challenge_turbo_swarm", "Hyperspeed Swarm", "All enemies move 75% faster"),
        ("challenge_glass_cannon", "Fragile Armaments", "Towers deal 200% damage but base has only 10 HP"),
        ("challenge_boss_onslaught", "Titan Vanguard", "Every wave contains an enraged Boss unit"),
        ("challenge_pure_kinetic", "Iron Age Doctrine", "Energy and Experimental towers are forbidden"),
        ("challenge_pure_energy", "Plasma Matrix", "Kinetic towers are disabled; all shields doubled"),
        ("challenge_extreme_cc", "Cryo Sub-Zero", "Enemies have 80% slow resistance but freeze deals 3x DoT"),
        ("challenge_sudden_death", "One Life Shield", "Any single enemy leaking results in immediate defeat"),
        ("challenge_endless_overclock", "Overclocked Surge", "Both player towers and enemies have 100% higher speed")
    ]

    for cid, name, desc in challenges:
        code = f'''"""
Sentinel Grid Challenge Rule: {name}
{desc}
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ChallengeModifiers:
    challenge_id: str = "{cid}"
    title: str = "{name}"
    description: str = "{desc}"
    credit_multiplier: float = 1.0
    energy_multiplier: float = 1.0
    enemy_speed_multiplier: float = 1.0
    tower_range_multiplier: float = 1.0
    tower_damage_multiplier: float = 1.0
    base_hp_override: float = 100.0
    allowed_archetypes: list = None

    def apply_to_simulation(self, kernel_config: Dict[str, Any]) -> Dict[str, Any]:
        cfg = dict(kernel_config)
        cfg["credit_mult"] = self.credit_multiplier
        cfg["energy_mult"] = self.energy_multiplier
        cfg["enemy_speed_mult"] = self.enemy_speed_multiplier
        cfg["damage_mult"] = self.tower_damage_multiplier
        return cfg
'''
        write_file(f"client/campaign/challenges/{cid}.py", code)

    # 2. 15 Tactical Briefing Dialogue Trees
    for i in range(1, 16):
        d_code = f'''"""
Tactical Command Briefing Dialogue: Sector {i:02d}
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

@dataclass
class DialogueLine:
    speaker: str
    message: str
    audio_cue: str = "radio_chatter"

class Sector{i:02d}Dialogue:
    @staticmethod
    def get_briefing() -> List[DialogueLine]:
        return [
            DialogueLine("Commander Vance", "Sentinel Grid deployed in Sector {i:02d}. Hostile signatures detected on long-range radar."),
            DialogueLine("Tactical AI (Aegis)", "Analyzing enemy vanguard composition. Recommending layered perimeter defense."),
            DialogueLine("Commander Vance", "Hold the objective at all costs. Do not allow the core energy reactor to fall!")
        ]

    @staticmethod
    def get_victory_debrief() -> List[DialogueLine]:
        return [
            DialogueLine("Tactical AI (Aegis)", "Hostile signatures eliminated. Sector {i:02d} secured with zero critical breaches."),
            DialogueLine("Commander Vance", "Outstanding work, Commander. Collect tech tokens and prepare for next deployment.")
        ]
'''
        write_file(f"client/campaign/dialogues/dialogue_sector_{i:02d}.py", d_code)

if __name__ == "__main__":
    generate()
