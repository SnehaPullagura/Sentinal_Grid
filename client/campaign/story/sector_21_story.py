"""
Campaign Sector 21 Narrative Briefing & Tactical Logbook.
World 5 - Operation Stage 1
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class TacticalIntelEntry:
    entry_id: str
    timestamp_stardate: str
    classification_level: str
    officer: str
    transcript: str

class Sector21IntelLog:
    @staticmethod
    def get_intel_briefing() -> List[TacticalIntelEntry]:
        return [
            TacticalIntelEntry(
                entry_id="INTEL_21_A",
                timestamp_stardate="SD 4280.252.4",
                classification_level="RESTRICTED // COMMAND EYES ONLY",
                officer="Admiral Sonya Cross",
                transcript="Forward scouting probes detect massive cybernetic armada gathering in Sector 21. Sentinel grid grid-lock protocol authorized."
            ),
            TacticalIntelEntry(
                entry_id="INTEL_21_B",
                timestamp_stardate="SD 4280.252.6",
                classification_level="TACTICAL UPLINK",
                officer="Chief Engineer Kaelen",
                transcript="Core energy capacitors primed. Kinetic turrets and heavy railguns deployed along chokepoints. Expect heavy counter-adaptive waves."
            )
        ]
