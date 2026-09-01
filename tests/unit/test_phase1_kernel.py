import pytest
from client.math.vector2d import Vector2D, Rect2D, Circle2D
from client.core.rng import DeterministicRNG
from client.events.event_bus import EventBus, GameEventType, GameEvent
from client.simulation.spatial_hash import SpatialHashGrid
from client.entities.entity_model import Entity, TransformComponent, HealthComponent
from client.simulation.game_state import SimulationKernel, SimulationStatus

def test_vector2d_algebra():
    v1 = Vector2D(3.0, 4.0)
    assert v1.magnitude() == 5.0
    norm = v1.normalized()
    assert abs(norm.magnitude() - 1.0) < 1e-5
    v2 = Vector2D(1.0, 2.0)
    assert (v1 + v2).x == 4.0
    assert v1.dot(v2) == 11.0

def test_rng_determinism():
    rng1 = DeterministicRNG(seed=9999)
    rng2 = DeterministicRNG(seed=9999)
    seq1 = [rng1.next_float() for _ in range(50)]
    seq2 = [rng2.next_float() for _ in range(50)]
    assert seq1 == seq2

def test_spatial_hash_query():
    grid = SpatialHashGrid(cell_size=50.0)
    grid.insert("e1", Vector2D(10.0, 10.0), radius=5.0)
    grid.insert("e2", Vector2D(30.0, 30.0), radius=5.0)
    grid.insert("e3", Vector2D(200.0, 200.0), radius=5.0)
    
    nearby = grid.query_radius(Vector2D(20.0, 20.0), radius=25.0)
    assert "e1" in nearby
    assert "e2" in nearby
    assert "e3" not in nearby

def test_ecs_entity_damage():
    entity = Entity(name="TestEnemy", tag="Enemy")
    tf = entity.add_component(TransformComponent(position=Vector2D(10, 20)))
    hp = entity.add_component(HealthComponent(max_health=100.0, current_health=100.0, armor=5.0))
    dmg = hp.take_damage(25.0, damage_type="kinetic")
    assert dmg == 20.0
    assert hp.current_health == 80.0

def test_simulation_kernel_lifecycle():
    kernel = SimulationKernel(seed=123)
    kernel.initialize(base_hp=100.0, starting_credits=500)
    t = Entity(name="Turret", tag="Tower")
    t.add_component(TransformComponent(position=Vector2D(50, 50)))
    kernel.register_entity(t)
    assert len(kernel.get_all_towers()) == 1
    assert kernel.spend_credits(200)
    for _ in range(10):
        kernel.step_tick()
    assert kernel.current_tick == 10
