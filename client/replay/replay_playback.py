from __future__ import annotations
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
