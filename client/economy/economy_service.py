from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional
from client.events.event_bus import EventBus, GameEventType

@dataclass
class Wallet:
    credits: int = 400
    energy: int = 100
    strategic_tokens: int = 0

class EconomyService:
    def __init__(self, event_bus: EventBus, starting_credits: int = 400, starting_energy: int = 100):
        self.event_bus: EventBus = event_bus
        self.wallet: Wallet = Wallet(credits=starting_credits, energy=starting_energy)
        self.total_earned: int = 0
        self.total_spent: int = 0

    def can_afford(self, credits: int = 0, energy: int = 0, tokens: int = 0) -> bool:
        return (self.wallet.credits >= credits and
                self.wallet.energy >= energy and
                self.wallet.strategic_tokens >= tokens)

    def spend(self, credits: int = 0, energy: int = 0, tokens: int = 0, reason: str = "general") -> bool:
        if not self.can_afford(credits, energy, tokens):
            return False
        self.wallet.credits -= credits
        self.wallet.energy -= energy
        self.wallet.strategic_tokens -= tokens
        self.total_spent += credits
        self.event_bus.emit(GameEventType.CREDITS_CHANGED, delta=-credits, total=self.wallet.credits, reason=reason)
        return True

    def earn(self, credits: int = 0, energy: int = 0, tokens: int = 0, reason: str = "reward") -> None:
        self.wallet.credits += credits
        self.wallet.energy += energy
        self.wallet.strategic_tokens += tokens
        self.total_earned += credits
        self.event_bus.emit(GameEventType.CREDITS_CHANGED, delta=credits, total=self.wallet.credits, reason=reason)

    def refund_tower(self, original_cost: int, sell_ratio: float = 0.75) -> int:
        refund_amount = int(original_cost * sell_ratio)
        self.earn(credits=refund_amount, reason="tower_sold")
        return refund_amount
