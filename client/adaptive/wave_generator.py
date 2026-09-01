from __future__ import annotations
from typing import List, Dict
from dataclasses import dataclass
from client.enemies.enemy_definitions import EnemyStats
from client.enemies.enemy_catalog import get_enemy_catalog
from client.adaptive.defense_profiler import DefenseProfile
from client.adaptive.threat_analyzer import ThreatAnalyzer
from client.adaptive.difficulty_controller import DifficultyController
from client.core.rng import DeterministicRNG

@dataclass
class SpawnEntry:
    enemy_id: str
    spawn_time: float  # In seconds from wave start
    lane_id: int = 0

@dataclass
class AdaptiveWaveDefinition:
    wave_index: int
    threat_budget: float
    counters_applied: List[str]
    spawn_schedule: List[SpawnEntry]
    estimated_duration: float

class AdaptiveWaveGenerator:
    def __init__(self, rng: DeterministicRNG):
        self.rng: DeterministicRNG = rng
        self.catalog: Dict[str, EnemyStats] = get_enemy_catalog()
        self.difficulty_ctrl: DifficultyController = DifficultyController()

    def generate_wave(
        self,
        wave_index: int,
        profile: DefenseProfile,
        player_lives_pct: float = 1.0
    ) -> AdaptiveWaveDefinition:
        budget = self.difficulty_ctrl.calculate_wave_budget(wave_index, player_lives_pct)
        counters = ThreatAnalyzer.determine_counter_strategies(profile)

        schedule: List[SpawnEntry] = []
        remaining_budget = budget
        current_time = 1.0

        # Select composition based on counters
        priority_enemies = []
        if "DISRUPTOR_SWARM" in counters:
            priority_enemies.extend(["emp_disruptor", "swarm_cluster"])
        if "HEAVY_ARMOR_WALL" in counters:
            priority_enemies.append("heavy_brute")
        if "SHIELD_FORMATION" in counters:
            priority_enemies.append("shield_bearer")
        if "AIR_FLANK" in counters:
            priority_enemies.append("aero_drone")

        if not priority_enemies:
            priority_enemies = ["scout_runner", "heavy_brute", "aero_drone"]

        # Fill budget
        while remaining_budget > 0.5:
            e_id = self.rng.choice(priority_enemies)
            stats = self.catalog[e_id]
            if stats.threat_cost <= remaining_budget or len(schedule) == 0:
                schedule.append(SpawnEntry(enemy_id=e_id, spawn_time=current_time))
                remaining_budget -= stats.threat_cost
                current_time += self.rng.uniform(0.6, 1.8)
            else:
                break

        # Boss every 5 waves
        if wave_index % 5 == 0:
            schedule.append(SpawnEntry(enemy_id="dreadnought_boss", spawn_time=current_time + 2.0))

        return AdaptiveWaveDefinition(
            wave_index=wave_index,
            threat_budget=budget,
            counters_applied=counters,
            spawn_schedule=schedule,
            estimated_duration=current_time + 10.0
        )
