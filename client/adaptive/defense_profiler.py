from __future__ import annotations
from typing import Dict
from dataclasses import dataclass
from client.adaptive.event_collector import PlayerDefenseMetrics

@dataclass
class DefenseProfile:
    kinetic_dominance: float  # [0.0, 1.0]
    energy_dominance: float   # [0.0, 1.0]
    crowd_control_reliance: float  # [0.0, 1.0]
    single_target_bias: float  # [0.0, 1.0] vs AoE
    cluster_density: float     # [0.0, 1.0]
    leak_vulnerability: float  # [0.0, 1.0]
    ability_burst_frequency: float

class DefenseProfiler:
    @staticmethod
    def analyze_profile(metrics: PlayerDefenseMetrics) -> DefenseProfile:
        tot_dmg = sum(metrics.damage_dealt_by_type.values()) or 1.0
        kinetic_dmg = metrics.damage_dealt_by_type.get("kinetic", 0.0)
        energy_dmg = metrics.damage_dealt_by_type.get("energy", 0.0)

        tot_towers = sum(metrics.towers_built_by_type.values()) or 1
        cc_count = metrics.cc_applications

        return DefenseProfile(
            kinetic_dominance=kinetic_dmg / tot_dmg,
            energy_dominance=energy_dmg / tot_dmg,
            crowd_control_reliance=min(1.0, cc_count / max(10.0, tot_dmg / 100.0)),
            single_target_bias=0.7,
            cluster_density=metrics.tower_density_score,
            leak_vulnerability=min(1.0, metrics.leaked_enemies_count * 0.1),
            ability_burst_frequency=min(1.0, metrics.abilities_used_count / 5.0)
        )
