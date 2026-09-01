import pytest
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity, TransformComponent, HealthComponent
from client.towers.targeting_system import TargetingStrategy, TargetingPipeline
from client.combat.status_effects import StatusEffectComponent, StatusEffectType
from client.combat.attack_pipeline import AttackPipeline, AttackDefinition
from client.events.event_bus import EventBus
from client.simulation.spatial_hash import SpatialHashGrid

def test_targeting_and_attack_pipeline():
    grid = SpatialHashGrid()
    bus = EventBus()
    entities = {}

    e1 = Entity(name="E1", tag="Enemy")
    e1.add_component(TransformComponent(position=Vector2D(100, 100)))
    e1.add_component(HealthComponent(max_health=100.0, current_health=80.0))
    grid.insert(e1.id, Vector2D(100, 100))
    entities[e1.id] = e1

    e2 = Entity(name="E2", tag="Enemy")
    e2.add_component(TransformComponent(position=Vector2D(120, 100)))
    e2.add_component(HealthComponent(max_health=150.0, current_health=150.0))
    grid.insert(e2.id, Vector2D(120, 100))
    entities[e2.id] = e2

    tower = Entity(name="Tower", tag="Tower")
    tower_pos = Vector2D(90, 100)

    target = TargetingPipeline.select_target(tower_pos, 50.0, TargetingStrategy.STRONGEST, grid, lambda eid: entities.get(eid))
    assert target is not None
    assert target.id == e2.id

    attack_def = AttackDefinition(base_damage=30.0, damage_type="kinetic")
    dealt = AttackPipeline.execute_attack(tower, target, attack_def, bus, lambda eid: entities.get(eid))
    assert dealt == 30.0
    assert e2.get_component(HealthComponent).current_health == 120.0
