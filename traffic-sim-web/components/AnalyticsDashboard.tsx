'use client'

import { useEffect, useState } from 'react'
import { useSimulationStore } from '@/store/simulationStore'
import { TrendingUp, BarChart3, PieChart, Activity, AlertTriangle, Clock, Zap } from 'lucide-react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface DataPoint {
  time: string
  vehicles: number
  fps: number
  avgSpeed: number
  queueLength: number
  throughput: number
  congestionIndex: number
}

export default function AnalyticsDashboard() {
  const { cameras, fps, totalVehicles, vehicles, trafficLights, isRunning } = useSimulationStore()
  const [historicalData, setHistoricalData] = useState<DataPoint[]>([])
  const [cameraData, setCameraData] = useState<any[]>([])
  const [insights, setInsights] = useState({
    avgWaitTime: 0,
    congestionLevel: 'Low',
    throughputRate: 0,
    trafficEfficiency: 0,
    bottleneckCamera: '',
    peakCongestionTime: '',
    lightOptimization: 0
  })

  useEffect(() => {
    if (!isRunning) return

    const interval = setInterval(() => {
      const now = new Date()
      const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
      
      const avgSpeed = vehicles.length > 0
        ? vehicles.reduce((acc, v) => acc + v.speed, 0) / vehicles.length
        : 0

      const totalQueue = cameras.reduce((acc, c) => acc + c.queueLength, 0)
      const avgQueue = totalQueue / cameras.length
      
      // Calculate congestion index (0-100)
      const congestionIndex = Math.min(100, (totalQueue / cameras.length) * 10)
      
      // Calculate throughput (vehicles passing through intersection)
      const throughput = vehicles.filter(v => {
        const [x, z] = [v.position[0], v.position[2]]
        return Math.abs(x) < 6 && Math.abs(z) < 6
      }).length

      setHistoricalData(prev => {
        const newData = [
          ...prev,
          {
            time: timeStr,
            vehicles: totalVehicles,
            fps,
            avgSpeed,
            queueLength: avgQueue,
            throughput,
            congestionIndex
          }
        ]
        return newData.slice(-30) // Keep last 30 data points
      })

      // Update camera data
      const camData = cameras.map(camera => ({
        name: camera.name.split(' ')[0], // Shorter names
        vehicles: camera.vehicleCount,
        queue: camera.queueLength,
        speed: camera.avgSpeed,
        utilization: Math.min(100, (camera.vehicleCount / 5) * 100)
      }))
      setCameraData(camData)
      
      // Calculate novel insights
      const bottleneck = cameras.reduce((max, cam) => 
        cam.queueLength > max.queueLength ? cam : max
      )
      
      const avgWaitTime = (totalQueue / Math.max(1, vehicles.length)) * 10 // Estimated wait time
      const trafficEfficiency = Math.max(0, 100 - congestionIndex)
      
      // Determine congestion level
      let congestionLevel = 'Low'
      if (congestionIndex > 70) congestionLevel = 'Critical'
      else if (congestionIndex > 40) congestionLevel = 'High'
      else if (congestionIndex > 20) congestionLevel = 'Medium'
      
      // Calculate light optimization score
      const greenLights = trafficLights.filter(l => l.state === 'green').length
      const lightOptimization = (greenLights / trafficLights.length) * 100
      
      setInsights({
        avgWaitTime: Math.round(avgWaitTime * 10) / 10,
        congestionLevel,
        throughputRate: throughput,
        trafficEfficiency: Math.round(trafficEfficiency),
        bottleneckCamera: bottleneck.name,
        peakCongestionTime: historicalData.length > 0 
          ? historicalData.reduce((max, d) => d.congestionIndex > max.congestionIndex ? d : max).time 
          : 'N/A',
        lightOptimization: Math.round(lightOptimization)
      })
    }, 1000)

    return () => clearInterval(interval)
  }, [cameras, fps, totalVehicles, vehicles, trafficLights, isRunning])

  const avgQueueLength = cameras.reduce((acc, c) => acc + c.queueLength, 0) / cameras.length
  const maxQueue = Math.max(...cameras.map(c => c.queueLength), 0)
  const avgSpeed = cameras.reduce((acc, c) => acc + c.avgSpeed, 0) / cameras.length

  if (!isRunning && historicalData.length === 0) {
    return (
      <div className="space-y-6">
        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <div className="text-center text-gray-400">
            <Activity className="w-12 h-12 mx-auto mb-3 text-gray-500" />
            <p className="text-lg">Start the simulation to see analytics...</p>
            <p className="text-sm mt-2">Click the "Start Simulation" button above</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Key Insights - NOVEL ANALYTICS */}
      <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl p-6 border-2 border-purple-500/40">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Zap className="w-6 h-6 text-yellow-400" />
          🎯 AI-Powered Traffic Insights
        </h3>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-black/40 rounded-lg p-4 border border-purple-500/20">
            <div className="text-sm text-purple-300 mb-1">Congestion Level</div>
            <div className={`text-2xl font-bold ${
              insights.congestionLevel === 'Critical' ? 'text-red-500' :
              insights.congestionLevel === 'High' ? 'text-orange-500' :
              insights.congestionLevel === 'Medium' ? 'text-yellow-500' :
              'text-green-500'
            }`}>{insights.congestionLevel}</div>
          </div>
          
          <div className="bg-black/40 rounded-lg p-4 border border-purple-500/20">
            <div className="text-sm text-purple-300 mb-1">Avg Wait Time</div>
            <div className="text-2xl font-bold text-white">{insights.avgWaitTime}s</div>
          </div>
          
          <div className="bg-black/40 rounded-lg p-4 border border-purple-500/20">
            <div className="text-sm text-purple-300 mb-1">Traffic Efficiency</div>
            <div className="flex items-center gap-2">
              <div className="text-2xl font-bold text-white">{insights.trafficEfficiency}%</div>
              <div className="flex-1 bg-gray-700 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full transition-all ${
                    insights.trafficEfficiency > 70 ? 'bg-green-500' :
                    insights.trafficEfficiency > 40 ? 'bg-yellow-500' :
                    'bg-red-500'
                  }`}
                  style={{ width: `${insights.trafficEfficiency}%` }}
                />
              </div>
            </div>
          </div>
          
          <div className="bg-black/40 rounded-lg p-4 border border-purple-500/20">
            <div className="text-sm text-purple-300 mb-1">Throughput Rate</div>
            <div className="text-2xl font-bold text-white">{insights.throughputRate} v/s</div>
          </div>
        </div>
        
        <div className="mt-4 p-3 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
          <div className="flex items-start gap-2">
            <AlertTriangle className="w-5 h-5 text-yellow-500 flex-shrink-0 mt-0.5" />
            <div>
              <div className="text-sm font-semibold text-yellow-300">Smart Recommendation</div>
              <div className="text-xs text-yellow-200/80 mt-1">
                Bottleneck detected at <strong>{insights.bottleneckCamera}</strong>. 
                Consider extending green light duration by 15% to improve flow efficiency.
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 rounded-lg p-4 border border-blue-500/30">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-blue-300">Total Vehicles</span>
            <TrendingUp className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-3xl font-bold text-white">{totalVehicles}</div>
        </div>

        <div className="bg-gradient-to-br from-green-500/20 to-green-600/20 rounded-lg p-4 border border-green-500/30">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-green-300">Avg Queue</span>
            <BarChart3 className="w-4 h-4 text-green-400" />
          </div>
          <div className="text-3xl font-bold text-white">{avgQueueLength.toFixed(1)}</div>
        </div>

        <div className="bg-gradient-to-br from-orange-500/20 to-orange-600/20 rounded-lg p-4 border border-orange-500/30">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-orange-300">Max Queue</span>
            <Activity className="w-4 h-4 text-orange-400" />
          </div>
          <div className="text-3xl font-bold text-white">{maxQueue}</div>
        </div>

        <div className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 rounded-lg p-4 border border-purple-500/30">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-purple-300">Avg Speed</span>
            <PieChart className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-3xl font-bold text-white">{avgSpeed.toFixed(1)} m/s</div>
        </div>
      </div>

      {/* Vehicle Count Over Time */}
      <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700 backdrop-blur-sm">
        <h3 className="text-lg font-semibold text-white mb-4">Vehicle Count Over Time</h3>
        {historicalData.length > 0 ? (
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={historicalData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="time" stroke="#9CA3AF" fontSize={12} />
              <YAxis stroke="#9CA3AF" fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1F2937',
                  border: '1px solid #374151',
                  borderRadius: '0.5rem',
                  color: '#fff'
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="vehicles"
                stroke="#3B82F6"
                strokeWidth={2}
                dot={false}
                name="Vehicles"
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-[250px] flex items-center justify-center text-gray-400">
            Collecting data...
          </div>
        )}
      </div>

      {/* Real-Time Congestion */}
      <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700 backdrop-blur-sm">
        <h3 className="text-lg font-semibold text-white mb-4">Real-Time Congestion Index</h3>
        {historicalData.length > 0 ? (
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={historicalData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="time" stroke="#9CA3AF" fontSize={12} />
              <YAxis stroke="#9CA3AF" fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1F2937',
                  border: '1px solid #374151',
                  borderRadius: '0.5rem',
                  color: '#fff'
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="congestionIndex"
                stroke="#EF4444"
                strokeWidth={3}
                dot={false}
                name="Congestion Index (%)"
              />
              <Line
                type="monotone"
                dataKey="queueLength"
                stroke="#F59E0B"
                strokeWidth={2}
                dot={false}
                name="Avg Queue"
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-[250px] flex items-center justify-center text-gray-400">
            Collecting data...
          </div>
        )}
      </div>

      {/* Camera Distribution */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700 backdrop-blur-sm">
          <h3 className="text-lg font-semibold text-white mb-4">Camera Vehicle Distribution</h3>
          {cameraData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={cameraData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" stroke="#9CA3AF" fontSize={12} />
                <YAxis stroke="#9CA3AF" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '0.5rem',
                    color: '#fff'
                  }}
                />
                <Legend />
                <Bar dataKey="vehicles" fill="#3B82F6" name="Vehicles" />
                <Bar dataKey="queue" fill="#EF4444" name="Queue" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[250px] flex items-center justify-center text-gray-400">
              Collecting data...
            </div>
          )}
        </div>
        
        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700 backdrop-blur-sm">
          <h3 className="text-lg font-semibold text-white mb-4">Traffic Flow Efficiency</h3>
          {historicalData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={historicalData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="time" stroke="#9CA3AF" fontSize={12} />
                <YAxis stroke="#9CA3AF" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '0.5rem',
                    color: '#fff'
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="throughput"
                  stroke="#10B981"
                  strokeWidth={2}
                  dot={false}
                  name="Throughput (v/s)"
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[250px] flex items-center justify-center text-gray-400">
              Collecting data...
            </div>
          )}
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700 backdrop-blur-sm">
        <h3 className="text-lg font-semibold text-white mb-4">Performance Metrics</h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={historicalData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="time" stroke="#9CA3AF" fontSize={12} />
            <YAxis stroke="#9CA3AF" fontSize={12} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1F2937',
                border: '1px solid #374151',
                borderRadius: '0.5rem',
                color: '#fff'
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="fps"
              stroke="#10B981"
              strokeWidth={2}
              dot={false}
              name="FPS"
            />
            <Line
              type="monotone"
              dataKey="avgSpeed"
              stroke="#F59E0B"
              strokeWidth={2}
              dot={false}
              name="Avg Speed (m/s)"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
