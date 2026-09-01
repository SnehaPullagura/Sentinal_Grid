import pytest
from client.math.vector2d import Vector2D
from client.ai.solvers.emp_saboteur_solver import EmpSaboteurStrategySolver

def test_emp_saboteur_strategy_solver_evasion():
    solver = EmpSaboteurStrategySolver()
    cur = Vector2D(10.0, 10.0)
    goal = Vector2D(200.0, 10.0)
    hazards = [Vector2D(50.0, 10.0)]

    decision = solver.evaluate_threats(cur, goal, hazards, current_hp_pct=0.8)
    assert decision.recommended_velocity.magnitude() > 0.0
    assert decision.threat_urgency >= 0.0
