'use client'

import { useSimulationStore } from '@/store/simulationStore'
import { Play, Pause, RotateCcw, Camera, Activity, Zap, Settings } from 'lucide-react'

export default function ControlPanel() {
  const {
    isRunning,
    isPaused,
    fps,
    totalVehicles,
    cameras,
    toggleSimulation,
    pauseSimulation,
    resetSimulation,
    toggleCamera
  } = useSimulationStore()

  const activeCameras = cameras.filter(c => c.active).length
  const avgVehicleCount = cameras.reduce((acc, c) => acc + c.vehicleCount, 0) / cameras.length
  const avgQueueLength = cameras.reduce((acc, c) => acc + c.queueLength, 0) / cameras.length

  return (
    <div className="space-y-6">
      {/* Status Card */}
      <div className="bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-xl p-6 border border-blue-500/20 backdrop-blur-sm">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5 text-blue-400" />
          System Status
        </h3>
        
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-black/30 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-1">Status</div>
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${isRunning ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
              <span className="text-white font-medium">
                {isRunning ? (isPaused ? 'Paused' : 'Running') : 'Stopped'}
              </span>
            </div>
          </div>
          
          <div className="bg-black/30 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-1">FPS</div>
            <div className="text-2xl font-bold text-white">{fps}</div>
          </div>
          
          <div className="bg-black/30 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-1">Vehicles</div>
            <div className="text-2xl font-bold text-white">{totalVehicles}</div>
          </div>
          
          <div className="bg-black/30 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-1">Active Cameras</div>
            <div className="text-2xl font-bold text-white">{activeCameras}/{cameras.length}</div>
          </div>
        </div>
      </div>

      {/* Control Buttons */}
      <div className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 rounded-xl p-6 border border-purple-500/20 backdrop-blur-sm">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Settings className="w-5 h-5 text-purple-400" />
          Controls
        </h3>
        
        <div className="space-y-3">
          <button
            onClick={toggleSimulation}
            className={`w-full py-3 px-4 rounded-lg font-medium flex items-center justify-center gap-2 transition-all ${
              isRunning
                ? 'bg-red-500 hover:bg-red-600 text-white'
                : 'bg-green-500 hover:bg-green-600 text-white'
            }`}
          >
            {isRunning ? (
              <>
                <Pause className="w-5 h-5" />
                Stop Simulation
              </>
            ) : (
              <>
                <Play className="w-5 h-5" />
                Start Simulation
              </>
            )}
          </button>
          
          <button
            onClick={resetSimulation}
            className="w-full py-3 px-4 rounded-lg font-medium flex items-center justify-center gap-2 bg-blue-500 hover:bg-blue-600 text-white transition-all"
          >
            <RotateCcw className="w-5 h-5" />
            Reset Simulation
          </button>
        </div>
      </div>

      {/* Camera Controls */}
      <div className="bg-gradient-to-br from-green-500/10 to-blue-500/10 rounded-xl p-6 border border-green-500/20 backdrop-blur-sm">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Camera className="w-5 h-5 text-green-400" />
          Camera Controls
        </h3>
        
        <div className="space-y-2">
          {cameras.map(camera => (
            <button
              key={camera.id}
              onClick={() => toggleCamera(camera.id)}
              className={`w-full py-3 px-4 rounded-lg font-medium flex items-center justify-between transition-all ${
                camera.active
                  ? 'bg-green-500/20 border-2 border-green-500 text-green-400'
                  : 'bg-gray-700/50 border-2 border-gray-600 text-gray-400 hover:bg-gray-600/50'
              }`}
            >
              <span className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${camera.active ? 'bg-green-500' : 'bg-gray-500'}`} />
                {camera.name}
              </span>
              <span className="text-sm">
                {camera.vehicleCount} vehicles
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Traffic Metrics */}
      <div className="bg-gradient-to-br from-orange-500/10 to-red-500/10 rounded-xl p-6 border border-orange-500/20 backdrop-blur-sm">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5 text-orange-400" />
          Traffic Metrics
        </h3>
        
        <div className="space-y-3">
          <div className="bg-black/30 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-1">Avg Vehicle Count</div>
            <div className="text-2xl font-bold text-white">{avgVehicleCount.toFixed(1)}</div>
          </div>
          
          <div className="bg-black/30 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-1">Avg Queue Length</div>
            <div className="text-2xl font-bold text-white">{avgQueueLength.toFixed(1)}</div>
          </div>
          
          <div className="bg-black/30 rounded-lg p-4">
            <div className="text-sm text-gray-400 mb-1">System Health</div>
            <div className="flex items-center gap-2">
              <div className="flex-1 bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full transition-all"
                  style={{ width: `${Math.min(100, (fps / 60) * 100)}%` }}
                />
              </div>
              <span className="text-white font-medium">{Math.round((fps / 60) * 100)}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
