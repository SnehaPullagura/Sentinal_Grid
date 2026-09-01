import pytest
from client.math.vector2d import Vector2D
from client.combat.solvers.emp_disruptor_tower_solver import EmpDisruptorTowerCombatSolver

def test_emp_disruptor_tower_combat_solver_intercept():
    solver = EmpDisruptorTowerCombatSolver()
    origin = Vector2D(50.0, 50.0)
    target_pos = Vector2D(100.0, 50.0)
    target_vel = Vector2D(10.0, 0.0)

    solution = solver.calculate_intercept(origin, target_pos, target_vel)
    assert solution.time_to_target_sec >= 0.0
    assert solution.effective_damage > 0.0
    assert solution.hit_probability > 0.0
