import React from 'react';
import { Camera, Server, Database, Wifi, Activity, Box, Network } from 'lucide-react';

export default function ArchitectureDiagram() {
  return (
    <div className="w-full h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8 overflow-auto">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">EDGE-QI System Architecture</h2>
        
        {/* Frontend Layer */}
        <div className="mb-8 p-6 bg-blue-900/30 rounded-lg border-2 border-blue-500">
          <div className="flex items-center gap-3 mb-4">
            <Activity className="w-8 h-8 text-blue-400" />
            <h3 className="text-xl font-bold text-blue-300">Frontend Layer (Next.js)</h3>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div className="p-4 bg-blue-800/40 rounded border border-blue-400">
              <p className="text-sm font-semibold text-blue-200">Map Dashboard</p>
              <p className="text-xs text-blue-300 mt-1">Mapbox GL JS</p>
            </div>
            <div className="p-4 bg-blue-800/40 rounded border border-blue-400">
              <p className="text-sm font-semibold text-blue-200">Node Monitors</p>
              <p className="text-xs text-blue-300 mt-1">Real-time Metrics</p>
            </div>
            <div className="p-4 bg-blue-800/40 rounded border border-blue-400">
              <p className="text-sm font-semibold text-blue-200">Sim Controls</p>
              <p className="text-xs text-blue-300 mt-1">Event Triggers</p>
            </div>
          </div>
        </div>

        {/* Communication Layer */}
        <div className="flex justify-center mb-8">
          <div className="flex items-center gap-4">
            <div className="h-12 w-1 bg-green-500"></div>
            <Wifi className="w-8 h-8 text-green-400 animate-pulse" />
            <span className="text-sm text-green-300">Socket.IO WebSocket</span>
          </div>
        </div>

        {/* Backend Layer */}
        <div className="mb-8 p-6 bg-purple-900/30 rounded-lg border-2 border-purple-500">
          <div className="flex items-center gap-3 mb-4">
            <Server className="w-8 h-8 text-purple-400" />
            <h3 className="text-xl font-bold text-purple-300">Backend Layer (FastAPI)</h3>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-purple-800/40 rounded border border-purple-400">
              <p className="text-sm font-semibold text-purple-200">API Gateway</p>
              <p className="text-xs text-purple-300 mt-1">REST + WebSocket</p>
            </div>
            <div className="p-4 bg-purple-800/40 rounded border border-purple-400">
              <p className="text-sm font-semibold text-purple-200">Orchestrator</p>
              <p className="text-xs text-purple-300 mt-1">Node Management</p>
            </div>
          </div>
        </div>

        {/* MQTT Broker */}
        <div className="flex justify-center mb-8">
          <div className="p-6 bg-orange-900/30 rounded-lg border-2 border-orange-500 w-64">
            <div className="flex items-center gap-3 mb-2">
              <Network className="w-8 h-8 text-orange-400" />
              <h3 className="text-lg font-bold text-orange-300">MQTT Broker</h3>
            </div>
            <p className="text-xs text-orange-300">Eclipse Mosquitto</p>
            <div className="mt-3 space-y-1 text-xs text-orange-200">
              <p>• Edge-to-Edge Communication</p>
              <p>• Consensus Protocol Transport</p>
              <p>• Event Broadcasting</p>
            </div>
          </div>
        </div>

        {/* Edge Nodes Layer */}
        <div className="mb-8 p-6 bg-green-900/30 rounded-lg border-2 border-green-500">
          <div className="flex items-center gap-3 mb-4">
            <Camera className="w-8 h-8 text-green-400" />
            <h3 className="text-xl font-bold text-green-300">Edge Nodes Layer (Docker Containers)</h3>
          </div>
          <div className="grid grid-cols-4 gap-3">
            {['Cam-1A', 'Cam-1B', 'Cam-2A', 'Cam-2B'].map((cam) => (
              <div key={cam} className="p-3 bg-green-800/40 rounded border border-green-400">
                <p className="text-sm font-semibold text-green-200 text-center">{cam}</p>
                <div className="mt-2 space-y-1 text-xs text-green-300">
                  <p>• Layer 3-7 Logic</p>
                  <p>• ML Pipeline</p>
                  <p>• Scheduler</p>
                  <p>• Consensus Client</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Data Layer */}
        <div className="p-6 bg-slate-700/30 rounded-lg border-2 border-slate-500">
          <div className="flex items-center gap-3 mb-4">
            <Database className="w-8 h-8 text-slate-400" />
            <h3 className="text-xl font-bold text-slate-300">Data Layer</h3>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div className="p-4 bg-slate-800/40 rounded border border-slate-400">
              <p className="text-sm font-semibold text-slate-200">PostgreSQL</p>
              <p className="text-xs text-slate-300 mt-1">Config + Metadata</p>
            </div>
            <div className="p-4 bg-slate-800/40 rounded border border-slate-400">
              <p className="text-sm font-semibold text-slate-200">TimescaleDB</p>
              <p className="text-xs text-slate-300 mt-1">Time-series Metrics</p>
            </div>
            <div className="p-4 bg-slate-800/40 rounded border border-slate-400">
              <p className="text-sm font-semibold text-slate-200">Redis</p>
              <p className="text-xs text-slate-300 mt-1">Real-time Cache</p>
            </div>
          </div>
        </div>

        {/* Legend */}
        <div className="mt-8 p-4 bg-slate-800/50 rounded-lg">
          <h4 className="text-sm font-bold text-white mb-3">Architecture Notes:</h4>
          <div className="grid grid-cols-2 gap-3 text-xs text-slate-300">
            <div>
              <p className="font-semibold text-slate-200 mb-1">Frontend → Backend:</p>
              <p>WebSocket for real-time bidirectional communication</p>
            </div>
            <div>
              <p className="font-semibold text-slate-200 mb-1">Edge Nodes → MQTT:</p>
              <p>Lightweight pub/sub for consensus and state sharing</p>
            </div>
            <div>
              <p className="font-semibold text-slate-200 mb-1">Backend → Edge Nodes:</p>
              <p>MQTT commands for simulation control</p>
            </div>
            <div>
              <p className="font-semibold text-slate-200 mb-1">Edge Nodes → Backend:</p>
              <p>MQTT telemetry published, backend subscribes and forwards</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}