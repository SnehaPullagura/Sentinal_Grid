from __future__ import annotations
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from client.math.vector2d import Vector2D
from client.core.rng import DeterministicRNG
from client.events.event_bus import EventBus, GameEventType, GameEvent
from client.entities.entity_model import Entity, TransformComponent, HealthComponent
from client.simulation.spatial_hash import SpatialHashGrid

class SimulationStatus(Enum):
    UNINITIALIZED = auto()
    READY = auto()
    RUNNING = auto()
    PAUSED = auto()
    VICTORY = auto()
    DEFEAT = auto()

@dataclass
class SimulationStats:
    total_ticks: int = 0
    elapsed_sim_time: float = 0.0
    enemies_spawned: int = 0
    enemies_killed: int = 0
    towers_built: int = 0
    towers_sold: int = 0
    total_damage_dealt: float = 0.0
    credits_earned: int = 0
    credits_spent: int = 0
    abilities_used: int = 0

class SimulationKernel:
    def __init__(self, seed: int = 1337, tick_rate: int = 60):
        self.tick_rate: int = tick_rate
        self.delta_time: float = 1.0 / float(tick_rate)
        self.current_tick: int = 0
        self.status: SimulationStatus = SimulationStatus.UNINITIALIZED
        
        self.rng: DeterministicRNG = DeterministicRNG(seed=seed)
        self.event_bus: EventBus = EventBus()
        self.spatial_grid: SpatialHashGrid = SpatialHashGrid(cell_size=64.0)
        
        self._entities: Dict[str, Entity] = {}
        self._towers: Dict[str, Entity] = {}
        self._enemies: Dict[str, Entity] = {}
        self._projectiles: Dict[str, Entity] = {}
        
        self.base_max_hp: float = 100.0
        self.base_current_hp: float = 100.0
        self.credits: int = 400
        self.energy: int = 100
        self.tech_tokens: int = 0
        
        self.stats: SimulationStats = SimulationStats()
        self._tick_listeners: List[Callable[[int, float], None]] = []

    def initialize(self, base_hp: float = 100.0, starting_credits: int = 400, starting_energy: int = 100) -> None:
        self.current_tick = 0
        self.base_max_hp = base_hp
        self.base_current_hp = base_hp
        self.credits = starting_credits
        self.energy = starting_energy
        self.tech_tokens = 0
        self.status = SimulationStatus.READY
        self.stats = SimulationStats()
        self._entities.clear()
        self._towers.clear()
        self._enemies.clear()
        self._projectiles.clear()
        self.spatial_grid.clear()
        self.event_bus.clear()
        
        self.event_bus.emit(GameEventType.SIMULATION_INITIALIZED, tick=0, base_hp=base_hp, credits=starting_credits)

    def register_entity(self, entity: Entity) -> Entity:
        self._entities[entity.id] = entity
        if entity.tag == "Tower":
            self._towers[entity.id] = entity
            self.stats.towers_built += 1
        elif entity.tag == "Enemy":
            self._enemies[entity.id] = entity
            self.stats.enemies_spawned += 1
        elif entity.tag == "Projectile":
            self._projectiles[entity.id] = entity

        tf = entity.get_component(TransformComponent)
        if tf is not None:
            self.spatial_grid.insert(entity.id, tf.position, tf.bounding_radius)
        return entity

    def unregister_entity(self, entity_id: str) -> Optional[Entity]:
        entity = self._entities.pop(entity_id, None)
        if entity:
            self._towers.pop(entity_id, None)
            self._enemies.pop(entity_id, None)
            self._projectiles.pop(entity_id, None)
            self.spatial_grid.remove(entity_id)
            entity.destroy()
        return entity

    def get_entity(self, entity_id: str) -> Optional[Entity]: return self._entities.get(entity_id)
    def get_all_enemies(self) -> List[Entity]: return list(self._enemies.values())
    def get_all_towers(self) -> List[Entity]: return list(self._towers.values())

    def add_tick_listener(self, listener: Callable[[int, float], None]) -> None:
        self._tick_listeners.append(listener)

    def step_tick(self) -> None:
        if self.status not in (SimulationStatus.RUNNING, SimulationStatus.READY): return
        self.status = SimulationStatus.RUNNING
        self.current_tick += 1
        self.stats.total_ticks += 1
        self.stats.elapsed_sim_time += self.delta_time

        for enemy in list(self._enemies.values()):
            tf = enemy.get_component(TransformComponent)
            if tf and enemy.is_active:
                self.spatial_grid.update(enemy.id, tf.position, tf.bounding_radius)

        for listener in self._tick_listeners:
            listener(self.current_tick, self.delta_time)

        dead_entities = [e for e in self._entities.values() if e.is_destroyed or not e.is_active]
        for e in dead_entities:
            self.unregister_entity(e.id)

        if self.base_current_hp <= 0.0 and self.status == SimulationStatus.RUNNING:
            self.status = SimulationStatus.DEFEAT
            self.event_bus.emit(GameEventType.GAME_LOST, tick=self.current_tick, stats=self.stats)

    def damage_base(self, amount: float) -> None:
        old_hp = self.base_current_hp
        self.base_current_hp = max(0.0, self.base_current_hp - amount)
        self.event_bus.emit(GameEventType.BASE_HEALTH_CHANGED, tick=self.current_tick, old_hp=old_hp, new_hp=self.base_current_hp, max_hp=self.base_max_hp)
        if self.base_current_hp <= 0.0:
            self.status = SimulationStatus.DEFEAT
            self.event_bus.emit(GameEventType.GAME_LOST, tick=self.current_tick)

    def add_credits(self, amount: int) -> None:
        if amount <= 0: return
        self.credits += amount
        self.stats.credits_earned += amount
        self.event_bus.emit(GameEventType.CREDITS_CHANGED, tick=self.current_tick, delta=amount, total=self.credits)

    def spend_credits(self, amount: int) -> bool:
        if amount < 0 or self.credits < amount: return False
        self.credits -= amount
        self.stats.credits_spent += amount
        self.event_bus.emit(GameEventType.CREDITS_CHANGED, tick=self.current_tick, delta=-amount, total=self.credits)
        return True

    def pause(self) -> None:
        if self.status == SimulationStatus.RUNNING:
            self.status = SimulationStatus.PAUSED
            self.event_bus.emit(GameEventType.SIMULATION_PAUSED, tick=self.current_tick)

    def resume(self) -> None:
        if self.status == SimulationStatus.PAUSED:
            self.status = SimulationStatus.RUNNING
            self.event_bus.emit(GameEventType.SIMULATION_RESUMED, tick=self.current_tick)
