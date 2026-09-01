from __future__ import annotations
import math
from typing import Tuple, Union, List, Optional
from dataclasses import dataclass

EPSILON = 1e-6

@dataclass(slots=True)
class Vector2D:
    x: float
    y: float

    @classmethod
    def zero(cls) -> Vector2D: return cls(0.0, 0.0)
    @classmethod
    def one(cls) -> Vector2D: return cls(1.0, 1.0)
    @classmethod
    def up(cls) -> Vector2D: return cls(0.0, -1.0)
    @classmethod
    def down(cls) -> Vector2D: return cls(0.0, 1.0)
    @classmethod
    def left(cls) -> Vector2D: return cls(-1.0, 0.0)
    @classmethod
    def right(cls) -> Vector2D: return cls(1.0, 0.0)
    @classmethod
    def from_angle(cls, radians: float, magnitude: float = 1.0) -> Vector2D:
        return cls(math.cos(radians) * magnitude, math.sin(radians) * magnitude)
    @classmethod
    def from_tuple(cls, t: Tuple[float, float]) -> Vector2D:
        return cls(float(t[0]), float(t[1]))

    def to_tuple(self) -> Tuple[float, float]: return (self.x, self.y)
    def to_int_tuple(self) -> Tuple[int, int]: return (int(round(self.x)), int(round(self.y)))
    def copy(self) -> Vector2D: return Vector2D(self.x, self.y)

    def __add__(self, other: Union[Vector2D, float, Tuple[float, float]]) -> Vector2D:
        if isinstance(other, Vector2D): return Vector2D(self.x + other.x, self.y + other.y)
        if isinstance(other, (int, float)): return Vector2D(self.x + other, self.y + other)
        if isinstance(other, tuple) and len(other) == 2: return Vector2D(self.x + other[0], self.y + other[1])
        return NotImplemented

    def __radd__(self, other: Union[Vector2D, float, Tuple[float, float]]) -> Vector2D: return self.__add__(other)

    def __sub__(self, other: Union[Vector2D, float, Tuple[float, float]]) -> Vector2D:
        if isinstance(other, Vector2D): return Vector2D(self.x - other.x, self.y - other.y)
        if isinstance(other, (int, float)): return Vector2D(self.x - other, self.y - other)
        if isinstance(other, tuple) and len(other) == 2: return Vector2D(self.x - other[0], self.y - other[1])
        return NotImplemented

    def __rsub__(self, other: Union[Vector2D, float, Tuple[float, float]]) -> Vector2D:
        if isinstance(other, (int, float)): return Vector2D(other - self.x, other - self.y)
        if isinstance(other, tuple) and len(other) == 2: return Vector2D(other[0] - self.x, other[1] - self.y)
        return NotImplemented

    def __mul__(self, scalar: Union[int, float, Vector2D]) -> Vector2D:
        if isinstance(scalar, (int, float)): return Vector2D(self.x * scalar, self.y * scalar)
        if isinstance(scalar, Vector2D): return Vector2D(self.x * scalar.x, self.y * scalar.y)
        return NotImplemented

    def __rmul__(self, scalar: Union[int, float, Vector2D]) -> Vector2D: return self.__mul__(scalar)

    def __truediv__(self, scalar: Union[int, float, Vector2D]) -> Vector2D:
        if isinstance(scalar, (int, float)):
            if abs(scalar) < EPSILON: raise ZeroDivisionError("Cannot divide Vector2D by zero.")
            return Vector2D(self.x / scalar, self.y / scalar)
        if isinstance(scalar, Vector2D):
            if abs(scalar.x) < EPSILON or abs(scalar.y) < EPSILON: raise ZeroDivisionError("Cannot divide Vector2D by zero.")
            return Vector2D(self.x / scalar.x, self.y / scalar.y)
        return NotImplemented

    def __neg__(self) -> Vector2D: return Vector2D(-self.x, -self.y)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D): return False
        return abs(self.x - other.x) <= EPSILON and abs(self.y - other.y) <= EPSILON

    def magnitude_squared(self) -> float: return self.x * self.x + self.y * self.y
    def magnitude(self) -> float: return math.sqrt(self.magnitude_squared())
    def normalized(self) -> Vector2D:
        m = self.magnitude()
        return Vector2D.zero() if m <= EPSILON else Vector2D(self.x / m, self.y / m)

    def dot(self, other: Vector2D) -> float: return self.x * other.x + self.y * other.y
    def cross(self, other: Vector2D) -> float: return self.x * other.y - self.y * other.x
    def distance_to_squared(self, other: Vector2D) -> float:
        dx, dy = self.x - other.x, self.y - other.y
        return dx * dx + dy * dy
    def distance_to(self, other: Vector2D) -> float: return math.sqrt(self.distance_to_squared(other))
    def manhattan_distance_to(self, other: Vector2D) -> float: return abs(self.x - other.x) + abs(self.y - other.y)
    def angle(self) -> float: return math.atan2(self.y, self.x)
    def angle_to(self, other: Vector2D) -> float: return math.atan2(other.y - self.y, other.x - self.x)

    def rotate(self, radians: float) -> Vector2D:
        c, s = math.cos(radians), math.sin(radians)
        return Vector2D(self.x * c - self.y * s, self.x * s + self.y * c)

    def lerp(self, target: Vector2D, alpha: float) -> Vector2D:
        a = max(0.0, min(1.0, alpha))
        return Vector2D(self.x + (target.x - self.x) * a, self.y + (target.y - self.y) * a)

    def move_towards(self, target: Vector2D, max_delta: float) -> Vector2D:
        to_v = target - self
        d = to_v.magnitude()
        if d <= max_delta or d <= EPSILON: return target.copy()
        return self + (to_v / d) * max_delta

    def clamp_magnitude(self, max_length: float) -> Vector2D:
        m_sq = self.magnitude_squared()
        if m_sq > max_length * max_length and m_sq > 0:
            return self.normalized() * max_length
        return self.copy()

    def round_to(self, decimals: int = 4) -> Vector2D:
        return Vector2D(round(self.x, decimals), round(self.y, decimals))

    def as_dict(self) -> dict: return {"x": self.x, "y": self.y}

@dataclass(slots=True)
class Rect2D:
    x: float
    y: float
    width: float
    height: float

    @property
    def left(self) -> float: return self.x
    @property
    def right(self) -> float: return self.x + self.width
    @property
    def top(self) -> float: return self.y
    @property
    def bottom(self) -> float: return self.y + self.height
    @property
    def center(self) -> Vector2D: return Vector2D(self.x + self.width * 0.5, self.y + self.height * 0.5)

    def contains_point(self, point: Vector2D) -> bool:
        return self.left <= point.x <= self.right and self.top <= point.y <= self.bottom

    def intersects(self, other: Rect2D) -> bool:
        return not (self.right < other.left or self.left > other.right or self.bottom < other.top or self.top > other.bottom)

    def intersects_circle(self, center: Vector2D, radius: float) -> bool:
        cx = max(self.left, min(center.x, self.right))
        cy = max(self.top, min(center.y, self.bottom))
        dx, dy = center.x - cx, center.y - cy
        return (dx * dx + dy * dy) <= (radius * radius)

    def expand(self, amount: float) -> Rect2D:
        return Rect2D(self.x - amount, self.y - amount, self.width + amount * 2.0, self.height + amount * 2.0)

@dataclass(slots=True)
class Circle2D:
    center: Vector2D
    radius: float

    def contains_point(self, point: Vector2D) -> bool:
        return self.center.distance_to_squared(point) <= (self.radius * self.radius)

    def intersects_circle(self, other: Circle2D) -> bool:
        tot = self.radius + other.radius
        return self.center.distance_to_squared(other.center) <= (tot * tot)

    def get_bounding_box(self) -> Rect2D:
        return Rect2D(self.center.x - self.radius, self.center.y - self.radius, self.radius * 2.0, self.radius * 2.0)
