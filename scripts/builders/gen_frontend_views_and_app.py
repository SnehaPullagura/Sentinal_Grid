import os
import sys
sys.path.insert(0, os.getcwd())
from scripts.file_writer import write_file

def generate():
    write_file("frontend/src/components/Views.tsx", """import React from "react";

export const CampaignView: React.FC<{ onDeploy: () => void }> = ({ onDeploy }) => (
  <div className="flex-1 p-8 overflow-y-auto bg-[#0a0d14]">
    <h2 className="text-xl font-bold text-cyan-400 mb-2 font-mono">CAMPAIGN SECTORS</h2>
    <p className="text-xs text-slate-400 mb-6 font-mono">Conquer strategic sectors to unlock advanced weapons and tech tokens.</p>
    <div className="grid md:grid-cols-3 gap-6">
      {[
        { id: "s1", name: "Sector 1: Iron Frontier", diff: "Normal", stars: 3, desc: "Outer colony defense outpost" },
        { id: "s2", name: "Sector 2: Neon Grid", diff: "Hard", stars: 2, desc: "Cybernetic core energy matrix" },
        { id: "s3", name: "Sector 3: Void Abyss", diff: "Extreme", stars: 0, desc: "Titan Hive Stronghold" }
      ].map((s) => (
        <div key={s.id} className="bg-[#111726] border border-[#243254] rounded-2xl p-5 hover:border-cyan-500/50 transition">
          <div className="flex justify-between items-start mb-3">
            <h3 className="font-bold text-sm text-white">{s.name}</h3>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">{s.diff}</span>
          </div>
          <p className="text-xs text-slate-400 mb-4">{s.desc}</p>
          <div className="flex justify-between items-center">
            <span className="text-xs text-amber-400 font-mono">★ {s.stars} / 3 Stars</span>
            <button onClick={onDeploy} className="px-4 py-1.5 bg-cyan-500 text-black text-xs font-bold rounded-lg hover:bg-cyan-400">Deploy</button>
          </div>
        </div>
      ))}
    </div>
  </div>
);

export const LeaderboardView: React.FC = () => (
  <div className="flex-1 p-8 overflow-y-auto bg-[#0a0d14]">
    <h2 className="text-xl font-bold text-cyan-400 mb-4 font-mono">GLOBAL COMMANDER RANKINGS</h2>
    <div className="bg-[#111726] border border-[#243254] rounded-2xl overflow-hidden max-w-4xl">
      <table className="w-full text-left text-xs">
        <thead className="bg-[#161f36] text-slate-400 border-b border-[#243254]">
          <tr>
            <th className="p-3.5">Rank</th>
            <th className="p-3.5">Commander</th>
            <th className="p-3.5">Sector</th>
            <th className="p-3.5">Waves Cleared</th>
            <th className="p-3.5 text-right">Score</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-[#243254] font-mono">
          {[
            { r: 1, name: "Aegis_Prime", map: "Sector 7 Outpost", waves: 15, score: 45800 },
            { r: 2, name: "Commander_Alpha", map: "Sector 7 Outpost", waves: 14, score: 38200 },
            { r: 3, name: "VortexTactician", map: "Sector 7 Outpost", waves: 12, score: 31500 },
            { r: 4, name: "CyberSentinel", map: "Sector 7 Outpost", waves: 10, score: 26400 }
          ].map((row) => (
            <tr key={row.r} className="hover:bg-[#161f36]/60">
              <td className="p-3.5 text-amber-400 font-bold">#{row.r}</td>
              <td className="p-3.5 text-white font-sans font-bold">{row.name}</td>
              <td className="p-3.5 text-slate-400">{row.map}</td>
              <td className="p-3.5 text-cyan-400">{row.waves}</td>
              <td className="p-3.5 text-right text-amber-300 font-bold">{row.score.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

export const LevelEditorView: React.FC = () => (
  <div className="flex-1 p-8 overflow-y-auto bg-[#0a0d14]">
    <h2 className="text-xl font-bold text-cyan-400 mb-2 font-mono">TACTICAL LEVEL & ROUTE DESIGNER</h2>
    <p className="text-xs text-slate-400 mb-4 font-mono">Draw custom spawn routes, place barricades, balance threat wave curves and export JSON.</p>
    <div className="bg-[#111726] border border-[#243254] rounded-2xl p-6 max-w-2xl space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-xs text-slate-400 block mb-1">Sector Name</label>
          <input defaultValue="Sector X - Neon Stronghold" className="w-full bg-[#0a0d14] border border-[#243254] rounded-lg p-2 text-xs text-white" />
        </div>
        <div>
          <label className="text-xs text-slate-400 block mb-1">Wave Count</label>
          <input type="number" defaultValue="20" className="w-full bg-[#0a0d14] border border-[#243254] rounded-lg p-2 text-xs text-white" />
        </div>
      </div>
      <button onClick={() => alert("Level Definition JSON exported successfully to /data/definitions/custom_level.json")} className="px-6 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-black font-bold text-xs rounded-lg">
        Export LevelDefinition.json
      </button>
    </div>
  </div>
);
""")

    write_file("frontend/src/App.tsx", """import React, { useState, useEffect, useRef } from "react";
import { Navbar } from "./components/Navbar";
import { HUD } from "./components/HUD";
import { CampaignView, LeaderboardView, LevelEditorView } from "./components/Views";
import { Play, Pause, FastForward, AlertTriangle } from "lucide-react";

interface Tower {
  id: string;
  x: number;
  y: number;
  type: string;
  level: number;
  range: number;
  damage: number;
  cooldown: number;
  lastShot: number;
}

interface Enemy {
  id: string;
  x: number;
  y: number;
  hp: number;
  maxHp: number;
  speed: number;
  type: string;
  isFlying: boolean;
  distance: number;
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  color: string;
  size: number;
}

export default function App() {
  const [screen, setScreen] = useState<"game" | "campaign" | "editor" | "leaderboard">("game");
  const [credits, setCredits] = useState(450);
  const [energy, setEnergy] = useState(100);
  const [baseHp, setBaseHp] = useState(100);
  const [wave, setWave] = useState(1);
  const [score, setScore] = useState(0);
  const [selectedTowerType, setSelectedTowerType] = useState<string>("kinetic_gatling");
  const [selectedTower, setSelectedTower] = useState<Tower | null>(null);
  const [gameSpeed, setGameSpeed] = useState<number>(1);
  const [isPaused, setIsPaused] = useState<boolean>(false);
  const [tacticAlert, setTacticAlert] = useState<string>("Adaptive Engine: Monitoring defensive cluster patterns...");
  const [userLogged] = useState<string>("Commander_Alpha");

  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const towersRef = useRef<Tower[]>([]);
  const enemiesRef = useRef<Enemy[]>([]);
  const particlesRef = useRef<Particle[]>([]);
  const animationRef = useRef<number>(0);

  const towerCatalog: Record<string, { cost: number; range: number; damage: number; color: string }> = {
    kinetic_gatling: { cost: 100, range: 120, damage: 14, color: "#00f0ff" },
    heavy_railgun: { cost: 220, range: 190, damage: 85, color: "#3b82f6" },
    laser_prism: { cost: 150, range: 135, damage: 28, color: "#a855f7" },
    cryo_emitter: { cost: 130, range: 105, damage: 10, color: "#38bdf8" },
    plasma_mortar: { cost: 280, range: 160, damage: 65, color: "#f59e0b" }
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let lastTime = performance.now();

    const render = (time: number) => {
      const dt = Math.min(0.1, (time - lastTime) / 1000) * gameSpeed;
      lastTime = time;

      if (!isPaused) {
        enemiesRef.current.forEach((enemy) => {
          enemy.x += enemy.speed * dt;
          enemy.distance += enemy.speed * dt;
          if (enemy.x >= 920) {
            enemy.hp = 0;
            setBaseHp((prev) => Math.max(0, prev - (enemy.type === "boss" ? 30 : 5)));
          }
        });

        const dead = enemiesRef.current.filter((e) => e.hp <= 0);
        if (dead.length > 0) {
          dead.forEach((d) => {
            if (d.x < 920) {
              setCredits((c) => c + (d.type === "boss" ? 150 : 20));
              setScore((s) => s + (d.type === "boss" ? 2500 : 150));
            }
          });
          enemiesRef.current = enemiesRef.current.filter((e) => e.hp > 0);
        }

        towersRef.current.forEach((tower) => {
          tower.lastShot += dt;
          const target = enemiesRef.current.find((e) => Math.hypot(e.x - tower.x, e.y - tower.y) <= tower.range);
          if (target && tower.lastShot >= tower.cooldown) {
            tower.lastShot = 0;
            target.hp -= tower.damage;

            ctx.beginPath();
            ctx.strokeStyle = towerCatalog[tower.type]?.color || "#00f0ff";
            ctx.lineWidth = tower.type === "heavy_railgun" ? 4 : 2;
            ctx.moveTo(tower.x, tower.y);
            ctx.lineTo(target.x, target.y);
            ctx.stroke();
          }
        });

        particlesRef.current.forEach((p) => {
          p.x += p.vx * dt;
          p.y += p.vy * dt;
          p.life -= dt;
        });
        particlesRef.current = particlesRef.current.filter((p) => p.life > 0);
      }

      ctx.fillStyle = "#0a0d14";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Grid
      ctx.strokeStyle = "rgba(36, 50, 84, 0.4)";
      ctx.lineWidth = 1;
      for (let x = 0; x < canvas.width; x += 32) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
      }
      for (let y = 0; y < canvas.height; y += 32) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
      }

      // Paths
      ctx.fillStyle = "rgba(22, 31, 54, 0.8)";
      ctx.fillRect(0, 160, 920, 64);
      ctx.fillRect(0, 380, 920, 64);

      // Base
      ctx.fillStyle = "#1e293b";
      ctx.strokeStyle = "#00f0ff";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(920, 300, 45, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // Towers
      towersRef.current.forEach((t) => {
        const cat = towerCatalog[t.type];
        if (selectedTower?.id === t.id) {
          ctx.beginPath();
          ctx.strokeStyle = "rgba(0, 240, 255, 0.3)";
          ctx.arc(t.x, t.y, t.range, 0, Math.PI * 2);
          ctx.stroke();
        }
        ctx.fillStyle = cat ? cat.color : "#00f0ff";
        ctx.beginPath();
        ctx.arc(t.x, t.y, 16, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.stroke();
      });

      // Enemies
      enemiesRef.current.forEach((e) => {
        ctx.fillStyle = e.type === "boss" ? "#ef4444" : e.isFlying ? "#a855f7" : "#f59e0b";
        ctx.beginPath();
        ctx.arc(e.x, e.y, e.type === "boss" ? 22 : 12, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 1.5;
        ctx.stroke();

        const barWidth = e.type === "boss" ? 40 : 24;
        const hpPct = Math.max(0, e.hp / e.maxHp);
        ctx.fillStyle = "rgba(0,0,0,0.6)";
        ctx.fillRect(e.x - barWidth / 2, e.y - 18, barWidth, 4);
        ctx.fillStyle = hpPct > 0.5 ? "#22c55e" : "#ef4444";
        ctx.fillRect(e.x - barWidth / 2, e.y - 18, barWidth * hpPct, 4);
      });

      animationRef.current = requestAnimationFrame(render);
    };

    animationRef.current = requestAnimationFrame(render);
    return () => cancelAnimationFrame(animationRef.current);
  }, [gameSpeed, isPaused, selectedTower]);

  const startNextWave = () => {
    const count = 6 + wave * 3;
    const isBoss = wave % 5 === 0;

    if (wave >= 2) {
      const counters = ["High-Armor Vanguard detected", "Air Swarm Flank bypassing defenses", "EMP Disruptor wave"];
      setTacticAlert(`Adaptive Engine: Wave ${wave} counters -> ${counters[(wave - 1) % counters.length]}`);
    }

    for (let i = 0; i < count; i++) {
      setTimeout(() => {
        const isArmored = i % 3 === 0;
        const isFly = i % 4 === 0;
        enemiesRef.current.push({
          id: `e_${Date.now()}_${i}`,
          x: -20 - i * 40,
          y: i % 2 === 0 ? 192 : 412,
          hp: 70 + wave * 25 + (isArmored ? 120 : 0),
          maxHp: 70 + wave * 25 + (isArmored ? 120 : 0),
          speed: isFly ? 90 : isArmored ? 45 : 70,
          type: isArmored ? "armored" : isFly ? "flying" : "basic",
          isFlying: isFly,
          distance: 0
        });
      }, i * 650);
    }

    if (isBoss) {
      setTimeout(() => {
        enemiesRef.current.push({
          id: `boss_${Date.now()}`,
          x: -80,
          y: 300,
          hp: 1500 + wave * 500,
          maxHp: 1500 + wave * 500,
          speed: 35,
          type: "boss",
          isFlying: false,
          distance: 0
        });
      }, count * 650 + 1000);
    }

    setWave((w) => w + 1);
  };

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    const clicked = towersRef.current.find((t) => Math.hypot(t.x - clickX, t.y - clickY) <= 20);
    if (clicked) {
      setSelectedTower(clicked);
      return;
    }

    const cat = towerCatalog[selectedTowerType];
    if (!cat || credits < cat.cost) return;

    const newTower: Tower = {
      id: `tow_${Date.now()}`,
      x: clickX,
      y: clickY,
      type: selectedTowerType,
      level: 1,
      range: cat.range,
      damage: cat.damage,
      cooldown: 0.6,
      lastShot: 0
    };

    towersRef.current.push(newTower);
    setCredits((c) => c - cat.cost);
    setSelectedTower(newTower);
  };

  const upgradeSelected = () => {
    if (!selectedTower || credits < 120) return;
    selectedTower.level += 1;
    selectedTower.damage = Math.round(selectedTower.damage * 1.4);
    selectedTower.range += 15;
    setCredits((c) => c - 120);
    setSelectedTower({ ...selectedTower });
  };

  const sellSelected = () => {
    if (!selectedTower) return;
    const cat = towerCatalog[selectedTower.type];
    const refund = Math.round((cat?.cost || 100) * 0.75);
    setCredits((c) => c + refund);
    towersRef.current = towersRef.current.filter((t) => t.id !== selectedTower.id);
    setSelectedTower(null);
  };

  const triggerOrbitalStrike = () => {
    if (energy < 40) return;
    setEnergy((e) => e - 40);
    enemiesRef.current.forEach((enemy) => {
      enemy.hp -= 250;
    });
  };

  return (
    <div className="flex h-screen w-screen bg-[#0a0d14] text-slate-100 flex-col select-none">
      <Navbar screen={screen} setScreen={setScreen} userLogged={userLogged} />

      <div className="flex-1 flex overflow-hidden">
        {screen === "game" && (
          <>
            <HUD
              credits={credits}
              energy={energy}
              baseHp={baseHp}
              wave={wave}
              selectedTowerType={selectedTowerType}
              setSelectedTowerType={setSelectedTowerType}
              selectedTower={selectedTower}
              upgradeSelected={upgradeSelected}
              sellSelected={sellSelected}
              triggerOrbitalStrike={triggerOrbitalStrike}
            />

            <main className="flex-1 bg-[#0a0d14] relative flex flex-col items-center justify-center p-4">
              <div className="absolute top-6 left-6 right-6 bg-[#111726]/90 backdrop-blur border border-cyan-500/40 rounded-xl px-4 py-2 flex items-center justify-between text-xs font-mono text-cyan-300 z-10">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-400 animate-pulse" />
                  <span>{tacticAlert}</span>
                </div>
                <div>Score: <strong className="text-white">{score.toLocaleString()}</strong></div>
              </div>

              <div className="relative border-2 border-[#243254] rounded-2xl overflow-hidden shadow-2xl">
                <canvas
                  ref={canvasRef}
                  width={960}
                  height={576}
                  onClick={handleCanvasClick}
                  className="cursor-crosshair block"
                />
              </div>

              <div className="mt-4 flex items-center gap-3 bg-[#111726] border border-[#243254] rounded-xl px-4 py-2">
                <button
                  onClick={startNextWave}
                  className="px-6 py-2 bg-cyan-500 hover:bg-cyan-400 text-black font-extrabold text-xs rounded-lg transition flex items-center gap-2"
                >
                  <Play className="w-4 h-4 fill-current" /> INITIATE WAVE {wave}
                </button>
                <div className="h-6 w-px bg-[#243254]" />
                <button onClick={() => setIsPaused(!isPaused)} className="px-3 py-2 bg-[#161f36] text-slate-200 rounded-lg text-xs font-bold">
                  {isPaused ? <Play className="w-3.5 h-3.5" /> : <Pause className="w-3.5 h-3.5" />}
                </button>
                <button onClick={() => setGameSpeed(gameSpeed === 1 ? 2 : gameSpeed === 2 ? 4 : 1)} className="px-3 py-2 bg-[#161f36] text-cyan-400 font-mono text-xs font-bold rounded-lg flex items-center gap-1">
                  <FastForward className="w-3.5 h-3.5" /> {gameSpeed}x
                </button>
              </div>
            </main>
          </>
        )}

        {screen === "campaign" && <CampaignView onDeploy={() => setScreen("game")} />}
        {screen === "leaderboard" && <LeaderboardView />}
        {screen === "editor" && <LevelEditorView />}
      </div>
    </div>
  );
}
""")

if __name__ == "__main__":
    generate()
