import React from "react";

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
