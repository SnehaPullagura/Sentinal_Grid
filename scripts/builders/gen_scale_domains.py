import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate_missions():
    print("--> Generating 15 Campaign Mission Controllers...")
    for i in range(1, 16):
        world_idx = ((i - 1) // 5) + 1
        level_idx = ((i - 1) % 5) + 1
        is_boss = (level_idx == 5)
        
        m_code = f'''"""
Campaign Mission {i:02d}: World {world_idx} - Level {level_idx}
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from client.math.vector2d import Vector2D
from client.maps.map_definition import MapDefinition

@dataclass
class MissionObjective:
    objective_id: str
    description: str
    is_mandatory: bool = True
    is_completed: bool = False
    reward_tokens: int = 10

@dataclass
class ScriptedWaveEvent:
    wave_number: int
    trigger_delay: float
    enemy_types: List[str]
    count: int
    dialogue_cue: str

class Mission{i:02d}Controller:
    def __init__(self):
        self.mission_id: str = "mission_{i:02d}"
        self.world_number: int = {world_idx}
        self.level_number: int = {level_idx}
        self.is_boss_mission: bool = {is_boss}
        self.starting_credits: int = {400 + i * 25}
        self.starting_energy: int = {100 + i * 5}
        self.target_waves: int = {10 + i}
        self.objectives: List[MissionObjective] = self._build_objectives()
        self.scripted_events: List[ScriptedWaveEvent] = self._build_events()

    def _build_objectives(self) -> List[MissionObjective]:
        return [
            MissionObjective("obj_survive", "Survive all waves", is_mandatory=True, reward_tokens=15),
            MissionObjective("obj_base_hp", "Maintain base integrity above 75%", is_mandatory=False, reward_tokens=25),
            MissionObjective("obj_speed_clear", "Complete mission in record time", is_mandatory=False, reward_tokens=20)
        ]

    def _build_events(self) -> List[ScriptedWaveEvent]:
        events = []
        for w in range(1, {11 + i}):
            events.append(ScriptedWaveEvent(
                wave_number=w,
                trigger_delay=2.0,
                enemy_types=["scout_infiltrator", "armored_juggernaut"] if w % 2 == 0 else ["aero_interceptor", "shield_bearer"],
                count=5 + w * 2,
                dialogue_cue="Tactical HQ: Hostiles inbound!"
            ))
        return events

    def get_map_definition(self) -> MapDefinition:
        return MapDefinition(
            map_id="map_sector_{i:02d}",
            name="Sector {i:02d}",
            width=32,
            height=24,
            spawn_points=[Vector2D(16.0, 16.0), Vector2D(16.0, 680.0)],
            base_objective_pos=Vector2D(960.0, 350.0),
            starting_credits=self.starting_credits,
            starting_energy=self.starting_energy,
            total_waves=self.target_waves
        )
'''
        write_file(f"client/campaign/missions/mission_{i:02d}.py", m_code)

if __name__ == "__main__":
    generate_missions()
