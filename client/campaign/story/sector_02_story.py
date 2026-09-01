"""
Campaign Sector 02 Narrative Briefing & Tactical Logbook.
World 1 - Operation Stage 2
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

class Sector02IntelLog:
    @staticmethod
    def get_intel_briefing() -> List[TacticalIntelEntry]:
        return [
            TacticalIntelEntry(
                entry_id="INTEL_02_A",
                timestamp_stardate="SD 4280.24.4",
                classification_level="RESTRICTED // COMMAND EYES ONLY",
                officer="Admiral Sonya Cross",
                transcript="Forward scouting probes detect massive cybernetic armada gathering in Sector 02. Sentinel grid grid-lock protocol authorized."
            ),
            TacticalIntelEntry(
                entry_id="INTEL_02_B",
                timestamp_stardate="SD 4280.24.6",
                classification_level="TACTICAL UPLINK",
                officer="Chief Engineer Kaelen",
                transcript="Core energy capacitors primed. Kinetic turrets and heavy railguns deployed along chokepoints. Expect heavy counter-adaptive waves."
            )
        ]
