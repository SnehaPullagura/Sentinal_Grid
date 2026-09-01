import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    print("Generating Part 7: Replay Engine, Save System & Visual Level Editor...")

    # 1. client/replay/command_recorder.py
    write_file("client/replay/command_recorder.py", """from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json

class PlayerCommandType(Enum):
    PLACE_TOWER = auto()
    UPGRADE_TOWER = auto()
    SELL_TOWER = auto()
    TRIGGER_ABILITY = auto()
    CHANGE_TARGETING = auto()
    START_WAVE = auto()
    SPEED_CHANGE = auto()

@dataclass
class PlayerCommand:
    tick: int
    command_type: PlayerCommandType
    params: Dict[str, Any]

@dataclass
class ReplayHeader:
    version: str = "1.0.0"
    map_id: str = "map_alpha_outpost"
    random_seed: int = 1337
    total_ticks: int = 0
    final_score: int = 0
    player_name: str = "Commander"

class ReplayRecorder:
    def __init__(self, map_id: str, random_seed: int):
        self.header: ReplayHeader = ReplayHeader(map_id=map_id, random_seed=random_seed)
        self.commands: List[PlayerCommand] = []

    def record_command(self, tick: int, command_type: PlayerCommandType, **params) -> None:
        self.commands.append(PlayerCommand(tick=tick, command_type=command_type, params=params))

    def serialize(self) -> str:
        return json.dumps({
            "header": {
                "version": self.header.version,
                "map_id": self.header.map_id,
                "random_seed": self.header.random_seed,
                "total_ticks": self.header.total_ticks,
                "final_score": self.header.final_score
            },
            "commands": [
                {
                    "tick": cmd.tick,
                    "type": cmd.command_type.name,
                    "params": cmd.params
                }
                for cmd in self.commands
            ]
        }, indent=2)
""")

    # 2. client/replay/replay_playback.py
    write_file("client/replay/replay_playback.py", """from __future__ import annotations
from typing import List, Dict, Optional, Callable
import json
from client.replay.command_recorder import PlayerCommand, PlayerCommandType, ReplayHeader

class ReplayPlaybackController:
    def __init__(self, replay_json: str):
        data = json.loads(replay_json)
        h = data.get("header", {})
        self.header: ReplayHeader = ReplayHeader(
            version=h.get("version", "1.0.0"),
            map_id=h.get("map_id", ""),
            random_seed=int(h.get("random_seed", 1337)),
            total_ticks=int(h.get("total_ticks", 0)),
            final_score=int(h.get("final_score", 0))
        )
        self.commands: List[PlayerCommand] = [
            PlayerCommand(
                tick=int(c["tick"]),
                command_type=PlayerCommandType[c["type"]],
                params=c.get("params", {})
            )
            for c in data.get("commands", [])
        ]
        self._command_index: int = 0

    def get_commands_for_tick(self, tick: int) -> List[PlayerCommand]:
        active_cmds = []
        while self._command_index < len(self.commands):
            cmd = self.commands[self._command_index]
            if cmd.tick == tick:
                active_cmds.append(cmd)
                self._command_index += 1
            elif cmd.tick < tick:
                self._command_index += 1
            else:
                break
        return active_cmds

    def is_finished(self) -> bool:
        return self._command_index >= len(self.commands)
""")

    # 3. client/save/save_manager.py
    write_file("client/save/save_manager.py", """from __future__ import annotations
import json
import hashlib
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class PlayerSaveProfile:
    version: int = 1
    player_id: str = "player_001"
    player_name: str = "Sentinel One"
    tech_tokens: int = 150
    unlocked_towers: list = None
    campaign_progress: dict = None
    settings: dict = None

    def __post_init__(self):
        if self.unlocked_towers is None:
            self.unlocked_towers = ["kinetic_gatling", "heavy_railgun", "cryo_emitter"]
        if self.campaign_progress is None:
            self.campaign_progress = {"level_1_1": {"stars": 3, "score": 12500}}
        if self.settings is None:
            self.settings = {"master_volume": 0.8, "sfx_volume": 1.0, "music_volume": 0.7, "fast_forward": 2}

class SaveManager:
    @staticmethod
    def calculate_checksum(data_str: str) -> str:
        return hashlib.sha256(data_str.encode("utf-8")).hexdigest()

    @staticmethod
    def export_save(profile: PlayerSaveProfile) -> str:
        raw_json = json.dumps(asdict(profile), indent=2)
        checksum = SaveManager.calculate_checksum(raw_json)
        return json.dumps({"payload": raw_json, "checksum": checksum})

    @staticmethod
    def import_save(save_string: str) -> Optional[PlayerSaveProfile]:
        try:
            container = json.loads(save_string)
            raw_payload = container["payload"]
            expected_chk = container["checksum"]
            if SaveManager.calculate_checksum(raw_payload) != expected_chk:
                print("Save data corrupted! Checksum mismatch.")
                return None
            data = json.loads(raw_payload)
            return PlayerSaveProfile(**data)
        except Exception as ex:
            print(f"Failed to load save: {ex}")
            return None
""")

    # 4. client/editor/level_editor_core.py
    write_file("client/editor/level_editor_core.py", """from __future__ import annotations
from typing import List, Dict, Tuple, Optional
import json
from client.math.vector2d import Vector2D
from client.maps.map_definition import MapDefinition

class LevelEditorCore:
    def __init__(self, width: int = 32, height: int = 24):
        self.map_def: MapDefinition = MapDefinition(
            map_id="custom_map_01",
            name="Custom Battleground",
            width=width,
            height=height
        )

    def set_cell_blocked(self, gx: int, gy: int, blocked: bool = True) -> None:
        pt = (gx, gy)
        if blocked and pt not in self.map_def.blocked_cells:
            self.map_def.blocked_cells.append(pt)
        elif not blocked and pt in self.map_def.blocked_cells:
            self.map_def.blocked_cells.remove(pt)

    def add_spawn_point(self, world_x: float, world_y: float) -> None:
        self.map_def.spawn_points.append(Vector2D(world_x, world_y))

    def set_base_objective(self, world_x: float, world_y: float) -> None:
        self.map_def.base_objective_pos = Vector2D(world_x, world_y)

    def export_json(self) -> str:
        return json.dumps({
            "map_id": self.map_def.map_id,
            "name": self.map_def.name,
            "width": self.map_def.width,
            "height": self.map_def.height,
            "cell_size": self.map_def.cell_size,
            "spawn_points": [p.to_tuple() for p in self.map_def.spawn_points],
            "base_objective": self.map_def.base_objective_pos.to_tuple(),
            "blocked_cells": self.map_def.blocked_cells,
            "starting_credits": self.map_def.starting_credits,
            "total_waves": self.map_def.total_waves
        }, indent=2)
""")

    print("Part 7 Complete.")

if __name__ == "__main__":
    generate()
