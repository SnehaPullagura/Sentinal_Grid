"""
Sector 18 Operational Command Directive & Strategic Rulebook.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

@dataclass
class OperationalDirective:
    directive_id: str
    title: str
    description: str
    priority_level: str
    reward_tokens: int

class Sector18OperationalBriefing:
    def __init__(self):
        self.sector_id: str = "sector_18"
        self.operational_tier: int = 4
        self.directives: List[OperationalDirective] = [
            OperationalDirective(
                directive_id="DIR_18_1",
                title="Perimeter Objective #1",
                description="Secure grid sector 18 sub-station 1 against hostile infiltration.",
                priority_level="HIGH" if 1 == 1 else "STANDARD",
                reward_tokens=15
            ),
            OperationalDirective(
                directive_id="DIR_18_2",
                title="Perimeter Objective #2",
                description="Secure grid sector 18 sub-station 2 against hostile infiltration.",
                priority_level="HIGH" if 2 == 1 else "STANDARD",
                reward_tokens=20
            ),
            OperationalDirective(
                directive_id="DIR_18_3",
                title="Perimeter Objective #3",
                description="Secure grid sector 18 sub-station 3 against hostile infiltration.",
                priority_level="HIGH" if 3 == 1 else "STANDARD",
                reward_tokens=25
            ),
            OperationalDirective(
                directive_id="DIR_18_4",
                title="Perimeter Objective #4",
                description="Secure grid sector 18 sub-station 4 against hostile infiltration.",
                priority_level="HIGH" if 4 == 1 else "STANDARD",
                reward_tokens=30
            ),
            OperationalDirective(
                directive_id="DIR_18_5",
                title="Perimeter Objective #5",
                description="Secure grid sector 18 sub-station 5 against hostile infiltration.",
                priority_level="HIGH" if 5 == 1 else "STANDARD",
                reward_tokens=35
            )
        ]

    def get_primary_directive(self) -> OperationalDirective:
        return self.directives[0]
