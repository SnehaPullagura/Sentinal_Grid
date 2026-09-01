import pytest
from client.math.vector2d import Vector2D
from client.navigation.grid_graph import GridGraph, TerrainType
from client.navigation.advanced.flow_field_generator import FlowFieldGenerator

def test_flow_field_generation():
    graph = GridGraph(width=16, height=16, cell_size=32.0)
    flow = FlowFieldGenerator(graph)
    goal = Vector2D(400.0, 400.0)
    flow.generate_field(goal)
    
    vec = flow.get_flow_vector(Vector2D(50.0, 50.0))
    assert vec.magnitude() > 0.0
