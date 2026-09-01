import React from "react";
import { Zap } from "lucide-react";

interface Props {
  credits: number;
  energy: number;
  baseHp: number;
  wave: number;
  selectedTowerType: string;
  setSelectedTowerType: (t: string) => void;
  selectedTower: any;
  upgradeSelected: () => void;
  sellSelected: () => void;
  triggerOrbitalStrike: () => void;
}

export const HUD: React.FC<Props> = ({
  credits, energy, baseHp, wave, selectedTowerType, setSelectedTowerType,
  selectedTower, upgradeSelected, sellSelected, triggerOrbitalStrike
}) => {
  const towerCatalog: Record<string, { name: string; cost: number; desc: string }> = {
    kinetic_gatling: { name: "Gatling Turret", cost: 100, desc: "High fire rate kinetic" },
    heavy_railgun: { name: "Heavy Railgun", cost: 220, desc: "Long-range anti-armor slug" },
    laser_prism: { name: "Laser Prism", cost: 150, desc: "Continuous energy beam" },
    cryo_emitter: { name: "Cryo Emitter", cost: 130, desc: "Chills & slows enemy groups" },
    plasma_mortar: { name: "Plasma Mortar", cost: 280, desc: "Area ballistic splash" }
  };

  return (
    <aside className="w-80 bg-[#111726] border-r border-[#243254] p-4 flex flex-col gap-4 overflow-y-auto">
      <div className="bg-[#161f36] border border-[#243254] rounded-xl p-3.5 space-y-2.5">
        <div className="text-xs font-bold text-slate-400 uppercase tracking-wider flex justify-between">
          <span>Sector Vitals</span>
          <span className="text-cyan-400 font-mono">Wave {wave}</span>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div className="bg-[#0a0d14] rounded-lg p-2 border border-[#243254]">
            <div className="text-[10px] text-slate-400">CREDITS</div>
            <div className="text-lg font-mono font-bold text-amber-400">§ {credits}</div>
          </div>
          <div className="bg-[#0a0d14] rounded-lg p-2 border border-[#243254]">
            <div className="text-[10px] text-slate-400">ENERGY</div>
            <div className="text-lg font-mono font-bold text-cyan-400">{energy} / 100</div>
          </div>
        </div>
        <div>
          <div className="flex justify-between text-xs font-semibold mb-1">
            <span>Base Integrity</span>
            <span className={baseHp > 40 ? "text-emerald-400 font-mono" : "text-red-400 font-mono"}>{baseHp}%</span>
          </div>
          <div className="w-full bg-[#0a0d14] h-2 rounded-full overflow-hidden border border-[#243254]">
            <div className={`h-full transition-all duration-300 ${baseHp > 40 ? "bg-cyan-500" : "bg-red-500"}`} style={{ width: `${baseHp}%` }}></div>
          </div>
        </div>
      </div>

      <div className="bg-[#161f36] border border-[#243254] rounded-xl p-3.5 space-y-2">
        <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Defensive Network</div>
        <div className="space-y-2">
          {Object.entries(towerCatalog).map(([key, t]) => (
            <button
              key={key}
              onClick={() => setSelectedTowerType(key)}
              className={`w-full p-2.5 rounded-lg border text-left transition flex items-center justify-between ${
                selectedTowerType === key ? "bg-cyan-950/40 border-cyan-400 text-white" : "bg-[#0a0d14] border-[#243254] text-slate-300 hover:border-slate-500"
              }`}
            >
              <div>
                <div className="text-xs font-bold">{t.name}</div>
                <div className="text-[10px] text-slate-400">{t.desc}</div>
              </div>
              <div className="text-xs font-mono font-bold text-amber-400">§ {t.cost}</div>
            </button>
          ))}
        </div>
      </div>

      <div className="bg-[#161f36] border border-[#243254] rounded-xl p-3.5 space-y-2">
        <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Commander Grid</div>
        <button
          onClick={triggerOrbitalStrike}
          disabled={energy < 40}
          className="w-full py-2.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 text-black font-extrabold text-xs rounded-lg transition disabled:opacity-40 flex items-center justify-center gap-2"
        >
          <Zap className="w-4 h-4 fill-current" /> Orbital Kinetic Strike (40 NRG)
        </button>
      </div>

      {selectedTower && (
        <div className="bg-[#161f36] border border-cyan-500/50 rounded-xl p-3.5 space-y-2">
          <div className="text-xs font-bold text-cyan-400 uppercase tracking-wider">Tower Node Inspector</div>
          <div className="text-xs space-y-1 text-slate-300">
            <div className="flex justify-between"><span>Level:</span> <span className="font-mono text-cyan-400">{selectedTower.level}</span></div>
            <div className="flex justify-between"><span>Damage:</span> <span className="font-mono text-amber-400">{selectedTower.damage}</span></div>
            <div className="flex justify-between"><span>Range:</span> <span className="font-mono">{selectedTower.range}m</span></div>
          </div>
          <div className="grid grid-cols-2 gap-2 pt-2">
            <button onClick={upgradeSelected} className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold">
              Upgrade (§ 120)
            </button>
            <button onClick={sellSelected} className="px-3 py-1.5 bg-red-950/60 border border-red-800 text-red-300 rounded-lg text-xs font-bold">
              Recycle (§ 75)
            </button>
          </div>
        </div>
      )}
    </aside>
  );
};
