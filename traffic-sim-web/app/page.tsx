'use client'

import { Suspense } from 'react'
import TrafficSimulation from '@/components/TrafficSimulation'
import ControlPanel from '@/components/ControlPanel'
import AnalyticsDashboard from '@/components/AnalyticsDashboard'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
        {/* Header */}
        <header className="bg-black/50 backdrop-blur-md border-b border-white/10">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  🚦 EDGE-QI Traffic Simulation
                </h1>
                <p className="text-gray-400 mt-1">
                  High-Performance 3D Intersection Monitoring with WebGL
                </p>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <div className="text-sm text-gray-400">System Status</div>
                  <div className="text-green-400 font-semibold flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                    Online
                  </div>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <div className="container mx-auto px-6 py-6">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* 3D Simulation View - Takes 3/4 of space */}
            <div className="lg:col-span-3">
              <div className="bg-black/30 backdrop-blur-md rounded-2xl border border-white/10 overflow-hidden shadow-2xl">
                <div className="p-4 border-b border-white/10">
                  <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                    <span className="text-2xl">🗺️</span>
                    Live 3D Intersection View
                  </h2>
                  <p className="text-sm text-gray-400 mt-1">
                    Real-time vehicle tracking with 7 cameras • 3 traffic signals • WebGL rendering
                  </p>
                </div>
                <div className="relative">
                  <Suspense fallback={<LoadingFallback />}>
                    <TrafficSimulation />
                  </Suspense>
                </div>
              </div>
            </div>

            {/* Control Panel - Takes 1/4 of space */}
            <div className="lg:col-span-1">
              <ControlPanel />
            </div>
          </div>

          {/* Analytics Dashboard - Full width below */}
          <div className="mt-6">
            <AnalyticsDashboard />
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 py-6 border-t border-white/10">
          <div className="container mx-auto px-6 text-center text-gray-400 text-sm">
            <p>EDGE-QI Framework v2.0 • Built with Next.js, Three.js & WebGL</p>
          </div>
        </footer>
      </main>
  )
}

function LoadingFallback() {
  return (
    <div className="flex items-center justify-center h-[600px] bg-gray-900">
      <div className="text-center">
        <div className="inline-block w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="mt-4 text-gray-400">Loading 3D Simulation...</p>
      </div>
    </div>
  )
}
