"""
Tactical Command Briefing Dialogue: Sector 05
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

@dataclass
class DialogueLine:
    speaker: str
    message: str
    audio_cue: str = "radio_chatter"

class Sector05Dialogue:
    @staticmethod
    def get_briefing() -> List[DialogueLine]:
        return [
            DialogueLine("Commander Vance", "Sentinel Grid deployed in Sector 05. Hostile signatures detected on long-range radar."),
            DialogueLine("Tactical AI (Aegis)", "Analyzing enemy vanguard composition. Recommending layered perimeter defense."),
            DialogueLine("Commander Vance", "Hold the objective at all costs. Do not allow the core energy reactor to fall!")
        ]

    @staticmethod
    def get_victory_debrief() -> List[DialogueLine]:
        return [
            DialogueLine("Tactical AI (Aegis)", "Hostile signatures eliminated. Sector 05 secured with zero critical breaches."),
            DialogueLine("Commander Vance", "Outstanding work, Commander. Collect tech tokens and prepare for next deployment.")
        ]
