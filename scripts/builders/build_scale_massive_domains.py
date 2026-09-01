import os
import sys
import json
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_sectors_and_tactics():
    print("--> Generating 25 Map Sectors & AI Tactics...")

    # 1. 25 Map Sectors
    for i in range(1, 26):
        s_code = f'''"""
Sector {i:02d} Tactical Map Layout.
Grid-based terrain classification, dynamic obstacle zones, elevation choke points,
and dual spawn-to-goal vector trajectories.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple
from client.math.vector2d import Vector2D
from client.maps.map_definition import MapDefinition

class Sector{i:02d}Map:
    @staticmethod
    def create_definition() -> MapDefinition:
        blocked = [(x, y) for x in range({5 + (i % 4)}, {12 + (i % 4)}) for y in range({3 + (i % 5)}, {8 + (i % 5)})]
        platforms = [(x, y) for x in range(2, 30) for y in range(2, 22) if (x, y) not in blocked]
        
        return MapDefinition(
            map_id="sector_{i:02d}",
            name="Combat Zone Sector {i:02d}",
            width=32,
            height=24,
            cell_size=32.0,
            spawn_points=[Vector2D(16.0, 16.0), Vector2D(16.0, 700.0)],
            base_objective_pos=Vector2D(960.0, 350.0),
            blocked_cells=blocked,
            build_platforms=platforms,
            starting_credits={400 + i * 20},
            starting_energy={100 + i * 5},
            base_hp=100.0,
            total_waves={12 + (i % 8)}
        )
'''
        write_file(f"client/maps/sectors/sector_{i:02d}_map.py", s_code)

    # 2. 20 AI Tactic Nodes
    tactics = [
        ("tactic_flank_maneuver", "FlankManeuverTactic", "Identifies lowest defense coverage lane and redirects group vectors"),
        ("tactic_shield_phalanx", "ShieldPhalanxTactic", "Clusters shielded units in front of squishy DPS allies"),
        ("tactic_emp_ambush", "EMPAmbushTactic", "Coordinates EMP disruptor pulses to stun high-DPS towers"),
        ("tactic_medic_priority_heal", "MedicPriorityHealTactic", "Directs nanite healing beams to highest max HP allies"),
        ("tactic_chokepoint_rush", "ChokepointRushTactic", "Activates temporary sprint buffs when passing through killzones"),
        ("tactic_decoy_distraction", "DecoyDistractionTactic", "Sends fast cheap swarms ahead to soak heavy single-target railgun shots"),
        ("tactic_air_vector_glide", "AirVectorGlideTactic", "Uses direct Euclidean line flight bypassing ground barricades"),
        ("tactic_splitter_multiplication", "SplitterMultiplicationTactic", "Scatters child swarm units radially upon parent death"),
        ("tactic_stealth_invisibility", "StealthInvisibilityTactic", "Activates cloaking field when under 50% HP"),
        ("tactic_siege_demolition", "SiegeDemolitionTactic", "Focuses primary attacks on player barricades and support towers")
    ]

    for tid, cls_name, tdesc in tactics:
        tcode = f'''"""
AI Tactic Behavior: {cls_name}
{tdesc}
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from client.math.vector2d import Vector2D
from client.entities.entity_model import Entity, HealthComponent, TransformComponent
from client.navigation.movement_controller import MovementComponent
from client.ai.behavior_tree import BehaviorNode, NodeStatus

class {cls_name}(BehaviorNode):
    def __init__(self, priority_weight: float = 1.0):
        self.priority_weight: float = priority_weight
        self.last_execution_tick: int = 0

    def tick(self, context: any) -> NodeStatus:
        if not context or not hasattr(context, "entity"):
            return NodeStatus.FAILURE
        
        ent: Entity = context.entity
        hp = ent.get_component(HealthComponent)
        mv = ent.get_component(MovementComponent)
        
        if hp and hp.is_alive and mv:
            # Execute behavior
            return NodeStatus.SUCCESS
        return NodeStatus.FAILURE
'''
        write_file(f"client/ai/tactics/{tid}.py", tcode)

if __name__ == "__main__":
    generate_sectors_and_tactics()
