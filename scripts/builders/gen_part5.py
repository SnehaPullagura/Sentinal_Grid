import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    print("Generating Part 5: Signature Adaptive Defense Engine...")

    # 1. client/adaptive/event_collector.py
    write_file("client/adaptive/event_collector.py", """from __future__ import annotations
from typing import Dict, List, Any
from dataclasses import dataclass, field
from client.events.event_bus import EventBus, GameEventType, GameEvent

@dataclass
class PlayerDefenseMetrics:
    towers_built_by_type: Dict[str, int] = field(default_factory=dict)
    damage_dealt_by_type: Dict[str, float] = field(default_factory=dict)
    kills_by_archetype: Dict[str, int] = field(default_factory=dict)
    cc_applications: int = 0
    abilities_used_count: int = 0
    leaked_enemies_count: int = 0
    average_kill_distance_pct: float = 0.5
    tower_density_score: float = 1.0

class AdaptiveEventCollector:
    def __init__(self, event_bus: EventBus):
        self.event_bus: EventBus = event_bus
        self.metrics: PlayerDefenseMetrics = PlayerDefenseMetrics()
        self._subscribe_events()

    def _subscribe_events(self) -> None:
        self.event_bus.subscribe(GameEventType.TOWER_PLACED, self._on_tower_placed)
        self.event_bus.subscribe(GameEventType.DAMAGE_DEALT, self._on_damage_dealt)
        self.event_bus.subscribe(GameEventType.STATUS_EFFECT_APPLIED, self._on_status_applied)
        self.event_bus.subscribe(GameEventType.ENEMY_DEATH, self._on_enemy_death)
        self.event_bus.subscribe(GameEventType.ENEMY_REACHED_GOAL, self._on_enemy_leak)
        self.event_bus.subscribe(GameEventType.ABILITY_TRIGGERED, self._on_ability)

    def _on_tower_placed(self, event: GameEvent) -> None:
        archetype = event.payload.get("archetype", "KINETIC")
        self.metrics.towers_built_by_type[archetype] = self.metrics.towers_built_by_type.get(archetype, 0) + 1

    def _on_damage_dealt(self, event: GameEvent) -> None:
        dmg_type = event.payload.get("damage_type", "kinetic")
        amount = event.payload.get("damage", 0.0)
        self.metrics.damage_dealt_by_type[dmg_type] = self.metrics.damage_dealt_by_type.get(dmg_type, 0.0) + amount

    def _on_status_applied(self, event: GameEvent) -> None:
        self.metrics.cc_applications += 1

    def _on_enemy_death(self, event: GameEvent) -> None:
        arch = event.payload.get("archetype", "BASIC")
        self.metrics.kills_by_archetype[arch] = self.metrics.kills_by_archetype.get(arch, 0) + 1

    def _on_enemy_leak(self, event: GameEvent) -> None:
        self.metrics.leaked_enemies_count += 1

    def _on_ability(self, event: GameEvent) -> None:
        self.metrics.abilities_used_count += 1
""")

    # 2. client/adaptive/defense_profiler.py
    write_file("client/adaptive/defense_profiler.py", """from __future__ import annotations
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
""")

    # 3. client/adaptive/threat_analyzer.py
    write_file("client/adaptive/threat_analyzer.py", """from __future__ import annotations
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
""")

    # 4. client/adaptive/difficulty_controller.py
    write_file("client/adaptive/difficulty_controller.py", """from __future__ import annotations
from dataclasses import dataclass

@dataclass
class DifficultyState:
    wave_number: int = 1
    base_threat_budget: float = 20.0
    threat_growth_rate: float = 1.25
    player_performance_multiplier: float = 1.0

class DifficultyController:
    def __init__(self):
        self.state: DifficultyState = DifficultyState()

    def calculate_wave_budget(self, wave: int, player_lives_pct: float, response_time_factor: float = 1.0) -> float:
        self.state.wave_number = wave
        raw_budget = self.state.base_threat_budget * (self.state.threat_growth_rate ** (wave - 1))
        
        # Bounded difficulty scaling
        perf_mult = 1.0
        if player_lives_pct > 0.9:
            perf_mult = 1.15  # Challenge high performing players
        elif player_lives_pct < 0.3:
            perf_mult = 0.85  # Mercy relief

        self.state.player_performance_multiplier = perf_mult
        return raw_budget * perf_mult
""")

    # 5. client/adaptive/wave_generator.py
    write_file("client/adaptive/wave_generator.py", """from __future__ import annotations
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
""")

    print("Part 5 Complete.")

if __name__ == "__main__":
    generate()
