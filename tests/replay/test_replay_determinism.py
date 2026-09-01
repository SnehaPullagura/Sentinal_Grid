import pytest
from client.core.rng import DeterministicRNG
from client.replay.command_recorder import ReplayRecorder, PlayerCommandType
from client.replay.replay_playback import ReplayPlaybackController

def test_replay_recorder_and_playback():
    rec = ReplayRecorder(map_id="map_alpha", random_seed=777)
    rec.record_command(tick=10, command_type=PlayerCommandType.PLACE_TOWER, tower_type="kinetic_gatling", x=120, y=180)
    rec.record_command(tick=60, command_type=PlayerCommandType.START_WAVE, wave=1)
    
    serialized = rec.serialize()
    controller = ReplayPlaybackController(serialized)
    assert controller.header.random_seed == 777
    assert len(controller.commands) == 2

    cmds_tick_10 = controller.get_commands_for_tick(10)
    assert len(cmds_tick_10) == 1
    assert cmds_tick_10[0].params["tower_type"] == "kinetic_gatling"
