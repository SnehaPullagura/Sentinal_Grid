import pytest
from client.math.vector2d import Vector2D
from client.combat.solvers.plasma_mortar_artillery_solver import PlasmaMortarArtilleryCombatSolver

def test_plasma_mortar_artillery_combat_solver_intercept():
    solver = PlasmaMortarArtilleryCombatSolver()
    origin = Vector2D(50.0, 50.0)
    target_pos = Vector2D(100.0, 50.0)
    target_vel = Vector2D(10.0, 0.0)

    solution = solver.calculate_intercept(origin, target_pos, target_vel)
    assert solution.time_to_target_sec >= 0.0
    assert solution.effective_damage > 0.0
    assert solution.hit_probability > 0.0
