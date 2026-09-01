import React from "react";
import { Crosshair, Award, Wrench, BarChart3, UserCheck } from "lucide-react";

interface Props {
  screen: string;
  setScreen: (s: any) => void;
  userLogged: string;
}

export const Navbar: React.FC<Props> = ({ screen, setScreen, userLogged }) => (
  <header className="h-14 bg-[#111726] border-b border-[#243254] px-6 flex items-center justify-between shrink-0">
    <div className="flex items-center gap-3">
      <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center font-bold text-black text-lg">
        S
      </div>
      <div>
        <h1 className="font-extrabold text-sm tracking-widest text-cyan-400">
          SENTINEL <span className="text-white">GRID</span>
        </h1>
        <p className="text-[10px] text-slate-400 font-mono leading-none">2D Adaptive Defense Engine v1.0</p>
      </div>
    </div>

    <div className="flex items-center gap-2">
      <button onClick={() => setScreen("game")} className={`px-4 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${screen === "game" ? "bg-cyan-500 text-black" : "text-slate-300 hover:bg-[#161f36]"}`}>
        <Crosshair className="w-3.5 h-3.5" /> Battlefield
      </button>
      <button onClick={() => setScreen("campaign")} className={`px-4 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${screen === "campaign" ? "bg-cyan-500 text-black" : "text-slate-300 hover:bg-[#161f36]"}`}>
        <Award className="w-3.5 h-3.5" /> Campaign
      </button>
      <button onClick={() => setScreen("editor")} className={`px-4 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${screen === "editor" ? "bg-cyan-500 text-black" : "text-slate-300 hover:bg-[#161f36]"}`}>
        <Wrench className="w-3.5 h-3.5" /> Level Editor
      </button>
      <button onClick={() => setScreen("leaderboard")} className={`px-4 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${screen === "leaderboard" ? "bg-cyan-500 text-black" : "text-slate-300 hover:bg-[#161f36]"}`}>
        <BarChart3 className="w-3.5 h-3.5" /> Leaderboards
      </button>
    </div>

    <div className="flex items-center gap-3">
      <span className="text-xs font-mono text-emerald-400 bg-emerald-950/40 border border-emerald-800/60 px-2.5 py-1 rounded-full flex items-center gap-1">
        <UserCheck className="w-3.5 h-3.5" /> {userLogged}
      </span>
    </div>
  </header>
);
