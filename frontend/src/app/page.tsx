"use client";
import React, { useState, useEffect } from 'react';
import { HUDCore } from '../components/hud/HolographicCore';
import { NeuralGraph } from '../components/graph/NeuralGraph';

export default function FridayHUD() {
  const [state, setState] = useState({ nodes: [], links: [] });

  useEffect(() => {
    // Connect to WebSocket for real-time updates
    const socket = new WebSocket('ws://localhost:8000/ws/hud');
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'GRAPH_UPDATE') {
        setState(data.payload);
      }
    };
    return () => socket.close();
  }, []);

  return (
    <main className="bg-black text-cyan-400 min-h-screen overflow-hidden flex flex-col relative">
      <header className="p-6 border-b border-cyan-900 flex justify-between items-center z-10">
        <h1 className="text-3xl font-bold tracking-tighter">FRIDAY OS <span className="text-sm font-mono text-cyan-700">OS-1.0-ALIVE</span></h1>
        <div className="flex gap-4">
          <div className="status-badge px-4 py-1 border border-cyan-500 rounded-full animate-pulse">SYSTEM: CONSCIOUS</div>
        </div>
      </header>

      <div className="flex-1 flex p-6 gap-6 relative">
        <section className="w-1/4 border border-cyan-900 rounded-lg p-4 bg-black/50 backdrop-blur z-10">
          <h2 className="text-lg font-mono mb-4 border-b border-cyan-900 pb-2">NEURAL UNITS</h2>
          <div className="space-y-4">
            {/* Dynamic Agent Cards */}
          </div>
        </section>

        <section className="flex-1 relative border border-cyan-900 rounded-lg bg-black/30 overflow-hidden">
          <HUDCore />
          <div className="absolute bottom-4 left-4 p-4 bg-black/60 border border-cyan-900 rounded">
             <p className="text-xs font-mono uppercase tracking-widest opacity-50">Core Neural Vitals</p>
             <div className="h-1 w-48 bg-cyan-900 mt-2"><div className="h-full bg-cyan-400 w-3/4 shadow-[0_0_10px_#00f5ff]"></div></div>
          </div>
        </section>

        <section className="w-1/4 border border-cyan-900 rounded-lg p-4 bg-black/50 backdrop-blur z-10 flex flex-col">
          <h2 className="text-lg font-mono mb-4 border-b border-cyan-900 pb-2">KNOWLEDGE GRAPH</h2>
          <div className="flex-1">
             <NeuralGraph data={state} />
          </div>
        </section>
      </div>

      <footer className="p-6 border-t border-cyan-900 z-10">
        <div className="max-w-3xl mx-auto">
          <input
            type="text"
            placeholder="GIVE COMMAND TO FRIDAY..."
            className="w-full bg-transparent border-b-2 border-cyan-700 p-4 text-2xl font-mono focus:outline-none focus:border-cyan-400 text-center"
          />
        </div>
      </footer>
    </main>
  );
}
