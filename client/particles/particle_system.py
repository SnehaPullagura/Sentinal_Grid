from __future__ import annotations
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import random
from client.math.vector2d import Vector2D

@dataclass
class ParticleInstance:
    position: Vector2D
    velocity: Vector2D
    life_remaining: float
    max_life: float
    color_hex: str
    size: float
    fade_out: bool = True
    gravity: float = 0.0

class ParticleSystem:
    def __init__(self, max_particles: int = 2000):
        self.max_particles: int = max_particles
        self.particles: List[ParticleInstance] = []

    def emit_burst(
        self,
        origin: Vector2D,
        count: int = 15,
        color_hex: str = "#00f0ff",
        min_speed: float = 30.0,
        max_speed: float = 120.0,
        lifetime: float = 0.5,
        particle_size: float = 3.0
    ) -> None:
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
            angle = random.uniform(0.0, 6.28318)
            speed = random.uniform(min_speed, max_speed)
            vel = Vector2D.from_angle(angle, speed)
            p = ParticleInstance(
                position=origin.copy(),
                velocity=vel,
                life_remaining=lifetime,
                max_life=lifetime,
                color_hex=color_hex,
                size=particle_size
            )
            self.particles.append(p)

    def emit_trail(self, start_pos: Vector2D, end_pos: Vector2D, steps: int = 8, color_hex: str = "#38bdf8") -> None:
        for s in range(steps):
            t = s / max(1, steps)
            pos = start_pos.lerp(end_pos, t)
            p = ParticleInstance(
                position=pos,
                velocity=Vector2D((random.random() - 0.5) * 10.0, (random.random() - 0.5) * 10.0),
                life_remaining=0.3,
                max_life=0.3,
                color_hex=color_hex,
                size=2.0
            )
            self.particles.append(p)

    def update(self, delta_time: float) -> None:
        surviving = []
        for p in self.particles:
            p.life_remaining -= delta_time
            if p.life_remaining > 0.0:
                p.position.x += p.velocity.x * delta_time
                p.position.y += (p.velocity.y + p.gravity) * delta_time
                surviving.append(p)
        self.particles = surviving

    def clear(self) -> None:
        self.particles.clear()
