"""
Tower Matchup Multiplier Matrix: SINGULARITY_TRAP
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

class SingularityTrapMatrixTable:
    def __init__(self):
        self.tower_id: str = "singularity_trap"
        self.coefficients: Dict[str, MatchupCoeff] = self._init_table()

    def _init_table(self) -> Dict[str, MatchupCoeff]:
        raw_list = [
            MatchupCoeff(
                enemy_type="scout_infiltrator",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.25
            ),
            MatchupCoeff(
                enemy_type="armored_juggernaut",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.5
            ),
            MatchupCoeff(
                enemy_type="phantom_infiltrator",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.0
            ),
            MatchupCoeff(
                enemy_type="aero_interceptor",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.25
            ),
            MatchupCoeff(
                enemy_type="aegis_shield_bearer",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.5
            ),
            MatchupCoeff(
                enemy_type="nanite_medic",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.0
            ),
            MatchupCoeff(
                enemy_type="emp_saboteur",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.25
            ),
            MatchupCoeff(
                enemy_type="hydra_broodmother",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.5
            ),
            MatchupCoeff(
                enemy_type="shadow_assassin",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.0
            ),
            MatchupCoeff(
                enemy_type="siege_breaker_ram",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.25
            ),
            MatchupCoeff(
                enemy_type="dreadnought_titan",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.5
            ),
            MatchupCoeff(
                enemy_type="cyber_hive_carrier",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.0
            ),
            MatchupCoeff(
                enemy_type="glider_swarmer",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.25
            ),
            MatchupCoeff(
                enemy_type="heavy_colossus",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.5
            ),
            MatchupCoeff(
                enemy_type="leech_parasite",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.0
            ),
            MatchupCoeff(
                enemy_type="phase_shifter",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.25
            ),
            MatchupCoeff(
                enemy_type="warp_striker",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.5
            ),
            MatchupCoeff(
                enemy_type="vanguard_mech",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.0
            ),
            MatchupCoeff(
                enemy_type="frost_walker",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.25
            ),
            MatchupCoeff(
                enemy_type="apocalypse_overlord",
                damage_multiplier=1.0,
                armor_penetration_override=0.35,
                status_application_potency=1.5
            )
        ]
        return {c.enemy_type: c for c in raw_list}

    def get_coeff(self, enemy_type: str) -> MatchupCoeff:
        return self.coefficients.get(enemy_type, MatchupCoeff(enemy_type, 1.0, 0.20, 1.0))
