from __future__ import annotations
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
