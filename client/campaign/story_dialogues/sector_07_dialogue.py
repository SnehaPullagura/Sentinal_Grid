"""
Sector 07 Branching Narrative Dialogue Tree & Tactical Radio Protocol.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional

@dataclass
class DialogueNode:
    node_id: str
    speaker: str
    message: str
    audio_frequency: float
    branch_options: List[Tuple[str, str]]

class Sector07DialogueEngine:
    def __init__(self):
        self.sector_id: str = "sector_07"
        self.nodes: Dict[str, DialogueNode] = self._build_tree()

    def _build_tree(self) -> Dict[str, DialogueNode]:
        node_list = [
            DialogueNode(
                node_id="node_07_01",
                speaker="Admiral Vance" if 1 % 2 == 1 else "Tactical AI (Aegis)",
                message="Sector 07 combat transmission phase 1. Hostile signature density elevated.",
                audio_frequency=340.0,
                branch_options=[
                    ("Affirmative, reinforcing perimeter", "node_07_2"),
                    ("Request orbital kinetic support", "node_07_3")
                ]
            ),
            DialogueNode(
                node_id="node_07_02",
                speaker="Admiral Vance" if 2 % 2 == 1 else "Tactical AI (Aegis)",
                message="Sector 07 combat transmission phase 2. Hostile signature density elevated.",
                audio_frequency=380.0,
                branch_options=[
                    ("Affirmative, reinforcing perimeter", "node_07_3"),
                    ("Request orbital kinetic support", "node_07_4")
                ]
            ),
            DialogueNode(
                node_id="node_07_03",
                speaker="Admiral Vance" if 3 % 2 == 1 else "Tactical AI (Aegis)",
                message="Sector 07 combat transmission phase 3. Hostile signature density elevated.",
                audio_frequency=420.0,
                branch_options=[
                    ("Affirmative, reinforcing perimeter", "node_07_4"),
                    ("Request orbital kinetic support", "node_07_5")
                ]
            ),
            DialogueNode(
                node_id="node_07_04",
                speaker="Admiral Vance" if 4 % 2 == 1 else "Tactical AI (Aegis)",
                message="Sector 07 combat transmission phase 4. Hostile signature density elevated.",
                audio_frequency=460.0,
                branch_options=[
                    ("Affirmative, reinforcing perimeter", "node_07_5"),
                    ("Request orbital kinetic support", "node_07_6")
                ]
            ),
            DialogueNode(
                node_id="node_07_05",
                speaker="Admiral Vance" if 5 % 2 == 1 else "Tactical AI (Aegis)",
                message="Sector 07 combat transmission phase 5. Hostile signature density elevated.",
                audio_frequency=500.0,
                branch_options=[
                    ("Affirmative, reinforcing perimeter", "node_07_6"),
                    ("Request orbital kinetic support", "node_07_7")
                ]
            ),
            DialogueNode(
                node_id="node_07_06",
                speaker="Admiral Vance" if 6 % 2 == 1 else "Tactical AI (Aegis)",
                message="Sector 07 combat transmission phase 6. Hostile signature density elevated.",
                audio_frequency=540.0,
                branch_options=[
                    ("Affirmative, reinforcing perimeter", "node_07_7"),
                    ("Request orbital kinetic support", "node_07_8")
                ]
            ),
            DialogueNode(
                node_id="node_07_07",
                speaker="Admiral Vance" if 7 % 2 == 1 else "Tactical AI (Aegis)",
                message="Sector 07 combat transmission phase 7. Hostile signature density elevated.",
                audio_frequency=580.0,
                branch_options=[
                    ("Affirmative, reinforcing perimeter", "node_07_8"),
                    ("Request orbital kinetic support", "node_07_9")
                ]
            ),
            DialogueNode(
                node_id="node_07_08",
                speaker="Admiral Vance" if 8 % 2 == 1 else "Tactical AI (Aegis)",
                message="Sector 07 combat transmission phase 8. Hostile signature density elevated.",
                audio_frequency=620.0,
                branch_options=[
                    ("Affirmative, reinforcing perimeter", "node_07_9"),
                    ("Request orbital kinetic support", "node_07_10")
                ]
            ),
            DialogueNode(
                node_id="node_07_09",
                speaker="Admiral Vance" if 9 % 2 == 1 else "Tactical AI (Aegis)",
                message="Sector 07 combat transmission phase 9. Hostile signature density elevated.",
                audio_frequency=660.0,
                branch_options=[
                    ("Affirmative, reinforcing perimeter", "node_07_10"),
                    ("Request orbital kinetic support", "node_07_10")
                ]
            ),
            DialogueNode(
                node_id="node_07_10",
                speaker="Admiral Vance" if 10 % 2 == 1 else "Tactical AI (Aegis)",
                message="Sector 07 combat transmission phase 10. Hostile signature density elevated.",
                audio_frequency=700.0,
                branch_options=[
                    ("Affirmative, reinforcing perimeter", "node_07_10"),
                    ("Request orbital kinetic support", "node_07_10")
                ]
            )
        ]
        return {n.node_id: n for n in node_list}

    def get_node(self, node_id: str) -> Optional[DialogueNode]:
        return self.nodes.get(node_id)
