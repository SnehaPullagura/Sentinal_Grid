from __future__ import annotations
import math
from typing import List, Sequence, TypeVar, Any

T = TypeVar("T")

class DeterministicRNG:
    __slots__ = ("_state", "_inc", "_initial_seed", "_call_count")

    def __init__(self, seed: int = 42, sequence: int = 54):
        self._initial_seed = seed & 0xFFFFFFFFFFFFFFFF
        self._state: int = 0
        self._inc: int = (sequence << 1) | 1
        self._call_count: int = 0
        self.reseed(seed, sequence)

    def reseed(self, seed: int, sequence: int = 54) -> None:
        self._initial_seed = seed & 0xFFFFFFFFFFFFFFFF
        self._state = 0
        self._inc = (sequence << 1) | 1
        self._step()
        self._state = (self._state + self._initial_seed) & 0xFFFFFFFFFFFFFFFF
        self._step()
        self._call_count = 0

    def _step(self) -> None:
        self._state = (self._state * 6364136223846793005 + self._inc) & 0xFFFFFFFFFFFFFFFF

    def next_u32(self) -> int:
        self._call_count += 1
        old_state = self._state
        self._step()
        xorshifted = (((old_state >> 18) ^ old_state) >> 27) & 0xFFFFFFFF
        rot = (old_state >> 59) & 0x1F
        result = ((xorshifted >> rot) | (xorshifted << ((-rot) & 31))) & 0xFFFFFFFF
        return result

    def next_float(self) -> float:
        return self.next_u32() / 4294967296.0

    def random(self) -> float: return self.next_float()

    def uniform(self, a: float, b: float) -> float:
        return a + (b - a) * self.next_float()

    def randint(self, a: int, b: int) -> int:
        if a > b: raise ValueError(f"Lower bound {a} cannot exceed upper bound {b}")
        span = (b - a) + 1
        return a + (self.next_u32() % span)

    def choice(self, seq: Sequence[T]) -> T:
        if not seq: raise IndexError("Cannot choose from an empty sequence")
        idx = self.next_u32() % len(seq)
        return seq[idx]

    def shuffle(self, lst: List[Any]) -> None:
        n = len(lst)
        for i in range(n - 1, 0, -1):
            j = self.randint(0, i)
            lst[i], lst[j] = lst[j], lst[i]

    def chance(self, probability: float) -> bool:
        return self.next_float() < probability

    def gaussian(self, mean: float = 0.0, std_dev: float = 1.0) -> float:
        u1 = max(1e-15, self.next_float())
        u2 = self.next_float()
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        return mean + z0 * std_dev

    @property
    def call_count(self) -> int: return self._call_count

    def serialize_state(self) -> dict:
        return {
            "initial_seed": self._initial_seed,
            "state": self._state,
            "inc": self._inc,
            "call_count": self._call_count
        }

    def deserialize_state(self, data: dict) -> None:
        self._initial_seed = int(data["initial_seed"])
        self._state = int(data["state"])
        self._inc = int(data["inc"])
        self._call_count = int(data.get("call_count", 0))
