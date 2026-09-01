from __future__ import annotations
from typing import List, Dict
from client.adaptive.defense_profiler import DefenseProfile

class ThreatAnalyzer:
    @staticmethod
    def determine_counter_strategies(profile: DefenseProfile) -> List[str]:
        counters: List[str] = []

        # 1. High CC reliance -> Fast rushers + EMP Disruptors
        if profile.crowd_control_reliance > 0.4:
            counters.append("DISRUPTOR_SWARM")
            counters.append("SPEED_SURGE")

        # 2. Kinetic dominance -> Heavy Armored Brutes
        if profile.kinetic_dominance > 0.6:
            counters.append("HEAVY_ARMOR_WALL")

        # 3. Energy dominance -> High Shield Bearers
        if profile.energy_dominance > 0.6:
            counters.append("SHIELD_FORMATION")

        # 4. Dense cluster defense -> Splitters + Air Bypass
        if profile.cluster_density > 0.6:
            counters.append("AIR_FLANK")
            counters.append("SPLITTER_CHAOS")

        if not counters:
            counters.append("BALANCED_ESCORT")

        return counters
