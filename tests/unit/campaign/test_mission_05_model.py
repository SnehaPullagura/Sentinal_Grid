import pytest
from client.campaign.mission_models.mission_05_model import Mission05DataModel

def test_mission_05_data_model_waves():
    model = Mission05DataModel()
    assert model.mission_index == 5
    assert len(model.waves_data) > 0
    w1 = model.get_wave_config(1)
    assert w1 is not None
    assert w1.threat_cap > 0.0
