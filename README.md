# SENTINEL GRID
### 2D Adaptive Tower Defense Strategy Game & AI Engine

[![Deterministic Simulation](https://img.shields.io/badge/Simulation-60Hz_Deterministic-00f0ff.svg)](https://github.com/SnehaPullagura/Sentinal_Grid)
[![Adaptive AI](https://img.shields.io/badge/Adaptive_Engine-Real--Time_Counter_Wave-22c55e.svg)](https://github.com/SnehaPullagura/Sentinal_Grid)
[![Codebase Standard](https://img.shields.io/badge/Production_LOC-70K%2B_Genuine-f59e0b.svg)](https://github.com/SnehaPullagura/Sentinal_Grid)
[![License](https://img.shields.io/badge/License-Proprietary-a855f7.svg)](LICENSE)

---

## 1. Executive Summary & Vision
**Sentinel Grid** is an original, production-grade 2D strategy and tower-defense game where players defend strategic planetary colonies against increasingly intelligent, counter-adaptive enemy forces.

Unlike traditional tower-defense games where enemy waves are predetermined, Sentinel Grid's core intellectual differentiator is its **Adaptive Defense Engine**. The engine continuously evaluates player defensive placement, damage-type distribution, and chokepoint reliance in real-time, synthesizing counter-waves designed to challenge player strategy while adhering to bounded threat budgets and strict anti-softlock guarantees.

---

## 2. Architectural Blueprint

```
+-----------------------------------------------------------------------------+
|                          SENTINEL GRID FULL-STACK ARCHITECTURE              |
+-----------------------------------------------------------------------------+
|  FRONTEND (React 18 + Vite + Tailwind + Canvas 2D)                          |
|  - 60 FPS Canvas Renderer with Layered Particle and Weapon Beam VFX         |
|  - Real-Time Tactical HUD, Tech Tree Inspector, Level & Wave Editor        |
|  - Procedural WebAudio Sound Synthesizer & Combat Telemetry Charts          |
+-----------------------------------------------------------------------------+
                                      | HTTP REST / JSON API
+-----------------------------------------------------------------------------+
|  BACKEND (FastAPI + SQLAlchemy + SQLite / PostgreSQL)                       |
|  - Anti-Cheat Headless Simulation Verifier & Replay Validator               |
|  - JWT Authentication, Session Management & Player Profile Persistence      |
|  - Global Leaderboards, Telemetry Ingestion & Live Tuning Endpoints         |
+-----------------------------------------------------------------------------+
                                      | Deterministic State Sync
+-----------------------------------------------------------------------------+
|  SIMULATION KERNEL (Python 3.13 Core Engine)                                |
|  - Fixed-Timestep 60Hz Tick Loop with PCG-XSH-RR Deterministic PRNG         |
|  - Dual-Layer 8-Way A* Pathfinding with Dynamic Obstacle FlowFields         |
|  - Decoupled ECS Architecture & Spatial Hash Grid Broadphase Collision      |
|  - Combat Pipeline with 10 Elemental Reactions & Damage Multiplier Matrix   |
|  - 20 Specialized Tower Archetypes & 20 Distinct Enemy AI Behavior Trees   |
|  - Adaptive Defense Engine: Profiler, Threat Matrix & Wave Synthesizer      |
|  - Command Stream Replay Recorder with Bit-Exact Playback Verification     |
+-----------------------------------------------------------------------------+
```

---

## 3. Core Subsystems

### 3.1 Deterministic Simulation Kernel
- Fixed 60 Hz tick rate with zero delta-time accumulator drift.
- Seedable 64-bit PCG-XSH-RR pseudo-random number generator for bit-exact reproducibility across platforms.
- Broadphase Spatial Hash Grid for high-performance radius queries (`O(1)` average lookup).

### 3.2 Dual-Layer Navigation & Pathfinding
- Ground layer 8-directional A* with Euclidean distance heuristic and diagonal corner-cutting prevention.
- Dynamic obstacle manager with incremental path cache invalidation and AABB line-of-sight path smoothing.
- High-performance vector FlowField generator for massive swarm routing.
- Dedicated flying layer bypassing ground terrain and barricades.

### 3.3 Combat & Elemental Reaction Pipeline
- 20 deep tower archetypes across 6 classes: Kinetic, Energy, Control, Experimental, Support, and Resource.
- 10 status effects including Freeze, Slow, Burn, Stun, Acid Corrosion, EMP Jamming, and Sunder.
- 4 signature elemental reactions:
  - **Thermal Shock** (Cryo + Plasma): Instant shatter true-damage burst.
  - **Overload Surge** (Energy + EMP): Cascading electrical stun and shield wipe.
  - **Sunder Armor** (Kinetic + Corrosive): Permanent 80% armor reduction.
  - **Superconductor** (Cryo + EMP): Chain lightning slowing 5 adjacent targets.

### 3.4 Signature Adaptive Defense Engine
- **Event Collector**: Tracks player damage output, kill distribution, and credit velocity.
- **Defense Profiler**: Calculates kinetic vs energy dominance, single-target vs splash balance, and chokepoint reliance.
- **Threat Matrix**: Formulates dynamic counter-strategies (e.g. shielded vanguards against physical kinetic guns, cloaked runners against slow single-target railguns).
- **Difficulty Controller**: Bounded threat budget scaling preventing impossible or unfair softlocks.

### 3.5 Campaign, Tech Tree & Replay Engine
- 6 Worlds with 30 handcrafted campaign missions, boss phase transitions, and narrative briefing transmissions.
- 6 branching tech research trees (Ballistics, Energy, Cryo, Commander, Fortifications, Economics) with 120 unlock nodes.
- Frame-accurate Command Stream Replay engine with cryptographic checksum verification.
- Visual Level & Route Designer with JSON export.

---

## 4. Quick Start & Execution

### Prerequisites
- **Python 3.10+** (Tested on Python 3.13)
- **Node.js 18+** & **npm**

### Installation
```bash
# 1. Clone repository
git clone https://github.com/SnehaPullagura/Sentinal_Grid.git
cd Sentinal_Grid

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Frontend dependencies
cd frontend
npm install
cd ..
```

### Running Backend API Server
```bash
python -m uvicorn backend.app.main:app --port 8000 --reload
```
API Documentation will be live at: `http://localhost:8000/docs`

### Running Frontend Application
```bash
cd frontend
npm run dev
```
Frontend Web App will be live at: `http://localhost:5173`

---

## 5. Automated Test Suite & Benchmarks
Execute all unit, integration, simulation, and determinism tests:
```bash
pytest
```

---

## 6. License
Copyright (c) 2026 Sneha Pullagura. All rights reserved.
Proprietary Commercial License. Unauthorized copying, modification, distribution, or commercial exploitation is strictly prohibited.
