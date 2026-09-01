import pytest
from client.math.vector2d import Vector2D
from client.navigation.grid_graph import GridGraph, TerrainType
from client.navigation.astar import AStarPathfinder
from client.navigation.dynamic_obstacles import DynamicObstacleManager

def test_grid_graph_and_astar():
    graph = GridGraph(width=20, height=20, cell_size=32.0)
    # Block a vertical wall
    for y in range(2, 18):
        graph.set_terrain(10, y, TerrainType.BLOCKED_TERRAIN)
    
    pathfinder = AStarPathfinder(graph)
    start = Vector2D(64.0, 64.0)
    goal = Vector2D(500.0, 64.0)
    
    path = pathfinder.find_path(start, goal)
    assert path is not None
    assert len(path) >= 2
    assert path[0] == start
    assert path[-1] == goal

def test_dynamic_obstacle_rerouting():
    graph = GridGraph(width=15, height=15, cell_size=32.0)
    pathfinder = AStarPathfinder(graph)
    obs_mgr = DynamicObstacleManager(graph)
    
    start = Vector2D(32.0, 32.0)
    goal = Vector2D(400.0, 32.0)
    
    # Add obstacle directly in path
    obs_mgr.add_obstacle("barricade_1", Vector2D(200.0, 32.0), radius=32.0)
    path = pathfinder.find_path(start, goal)
    assert path is not None
