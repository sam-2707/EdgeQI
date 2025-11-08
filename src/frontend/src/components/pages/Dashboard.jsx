import React from 'react';
import { useEdgeQI } from '../../contexts/EdgeQIContext';
import {
  Activity,
  Network,
  Camera,
  Zap,
  TrendingDown,
  Server,
  AlertTriangle,
  CheckCircle,
} from 'lucide-react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

const Dashboard = () => {
  const { systemMetrics, edgeNodes, detections } = useEdgeQI();

  // Calculate metrics
  const activeNodes = edgeNodes.filter((n) => n.status === 'active').length;
  const faultyNodes = edgeNodes.filter((n) => n.status === 'fault').length;
  const recentDetections = detections.slice(0, 10);

  // Mock time-series data for charts
  const performanceData = Array.from({ length: 20 }, (_, i) => ({
    time: `${20 - i}m`,
    latency: Math.random() * 50 + 10,
    throughput: Math.random() * 100 + 50,
    cpuUsage: Math.random() * 60 + 20,
  }));

  const energyData = Array.from({ length: 12 }, (_, i) => ({
    hour: `${i}:00`,
    consumption: Math.random() * 30 + 40,
    saved: Math.random() * 20 + 10,
  }));

  const detectionStats = [
    { category: 'Vehicle', count: 1245 },
    { category: 'Pedestrian', count: 892 },
    { category: 'Bicycle', count: 234 },
    { category: 'Bus', count: 156 },
    { category: 'Truck', count: 89 },
  ];

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          icon={Network}
          label="Active Nodes"
          value={activeNodes}
          total={edgeNodes.length}
          trend="+2.5%"
          trendUp={true}
        />
        <MetricCard
          icon={Camera}
          label="Total Detections"
          value={systemMetrics.totalDetections || 0}
          subtitle="Last 24h"
          trend="+12.3%"
          trendUp={true}
        />
        <MetricCard
          icon={Zap}
          label="Avg Latency"
          value={`${Math.round(systemMetrics.averageLatency || 0)}ms`}
          trend="-5.2%"
          trendUp={true}
        />
        <MetricCard
          icon={TrendingDown}
          label="Bandwidth Saved"
          value={`${Math.round(systemMetrics.bandwidthSaved || 74.5)}%`}
          subtitle="Anomaly-driven"
          trend="+1.2%"
          trendUp={true}
        />
      </div>

      {/* System Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Performance Chart */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">System Performance</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
              <XAxis
                dataKey="time"
                stroke="#737373"
                style={{ fontSize: '12px' }}
              />
              <YAxis stroke="#737373" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0a0a0a',
                  border: '1px solid #262626',
                  borderRadius: '8px',
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="latency"
                stroke="#ffffff"
                strokeWidth={2}
                dot={false}
                name="Latency (ms)"
              />
              <Line
                type="monotone"
                dataKey="throughput"
                stroke="#737373"
                strokeWidth={2}
                dot={false}
                name="Throughput"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Energy Consumption */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">Energy Consumption</h3>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={energyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
              <XAxis
                dataKey="hour"
                stroke="#737373"
                style={{ fontSize: '12px' }}
              />
              <YAxis stroke="#737373" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0a0a0a',
                  border: '1px solid #262626',
                  borderRadius: '8px',
                }}
              />
              <Legend />
              <Area
                type="monotone"
                dataKey="consumption"
                stackId="1"
                stroke="#ffffff"
                fill="#525252"
                name="Consumed (kWh)"
              />
              <Area
                type="monotone"
                dataKey="saved"
                stackId="2"
                stroke="#a3a3a3"
                fill="#262626"
                name="Saved (kWh)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detection Statistics & Node Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Detection Stats */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">Detection Statistics</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={detectionStats}>
              <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
              <XAxis
                dataKey="category"
                stroke="#737373"
                style={{ fontSize: '12px' }}
              />
              <YAxis stroke="#737373" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0a0a0a',
                  border: '1px solid #262626',
                  borderRadius: '8px',
                }}
              />
              <Bar dataKey="count" fill="#ffffff" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Node Status */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">Edge Node Status</h3>
          <div className="space-y-3">
            <StatusItem
              icon={CheckCircle}
              label="Active Nodes"
              value={activeNodes}
              color="text-green-400"
            />
            <StatusItem
              icon={Server}
              label="Idle Nodes"
              value={edgeNodes.filter((n) => n.status === 'idle').length}
              color="text-yellow-400"
            />
            <StatusItem
              icon={AlertTriangle}
              label="Faulty Nodes"
              value={faultyNodes}
              color="text-red-400"
            />
            <StatusItem
              icon={Activity}
              label="Total Capacity"
              value={`${edgeNodes.length} nodes`}
              color="text-neutral-400"
            />
          </div>

          <div className="mt-6 pt-6 border-t border-neutral-800">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-neutral-400">System Health</span>
              <span className="text-sm font-semibold">
                {Math.round((activeNodes / edgeNodes.length) * 100) || 0}%
              </span>
            </div>
            <div className="w-full h-2 bg-neutral-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-white rounded-full transition-all duration-500"
                style={{
                  width: `${(activeNodes / edgeNodes.length) * 100 || 0}%`,
                }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Recent Detections */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Detections</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-neutral-800">
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Timestamp
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Node ID
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Object Type
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Confidence
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Location
                </th>
              </tr>
            </thead>
            <tbody>
              {recentDetections.length === 0 ? (
                <tr>
                  <td colSpan="5" className="text-center py-8 text-neutral-500">
                    No recent detections
                  </td>
                </tr>
              ) : (
                recentDetections.map((detection, idx) => (
                  <tr
                    key={idx}
                    className="border-b border-neutral-800 hover:bg-white/5 transition-colors"
                  >
                    <td className="py-3 px-4 text-sm">
                      {new Date(detection.timestamp).toLocaleTimeString()}
                    </td>
                    <td className="py-3 px-4 text-sm font-mono">
                      {detection.nodeId || 'N/A'}
                    </td>
                    <td className="py-3 px-4 text-sm">{detection.type}</td>
                    <td className="py-3 px-4 text-sm">
                      <span className="badge-success">
                        {Math.round(detection.confidence * 100)}%
                      </span>
                    </td>
                    <td className="py-3 px-4 text-sm text-neutral-400">
                      {detection.location || 'Unknown'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ icon: Icon, label, value, total, subtitle, trend, trendUp }) => (
  <div className="metric-card">
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <p className="stat-label">{label}</p>
        <div className="mt-2 flex items-baseline gap-2">
          <span className="stat-value">
            {value}
            {total && <span className="text-neutral-500">/{total}</span>}
          </span>
        </div>
        {subtitle && (
          <p className="text-xs text-neutral-500 mt-1">{subtitle}</p>
        )}
        {trend && (
          <p
            className={`text-xs mt-2 ${
              trendUp ? 'text-green-400' : 'text-red-400'
            }`}
          >
            {trend}
          </p>
        )}
      </div>
      <div className="p-3 bg-white/5 rounded-lg">
        <Icon className="w-6 h-6" />
      </div>
    </div>
  </div>
);

const StatusItem = ({ icon: Icon, label, value, color }) => (
  <div className="flex items-center justify-between p-3 bg-neutral-900 rounded-lg">
    <div className="flex items-center gap-3">
      <Icon className={`w-5 h-5 ${color}`} />
      <span className="text-sm font-medium">{label}</span>
    </div>
    <span className="text-sm font-bold">{value}</span>
  </div>
);

export default Dashboard;
