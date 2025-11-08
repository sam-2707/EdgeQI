import React, { useState } from 'react';
import { useEdgeQI } from '../../contexts/EdgeQIContext';
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  Calendar,
  Download,
  FileText,
  Clock,
} from 'lucide-react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const Analytics = () => {
  const { detections, edgeNodes } = useEdgeQI();
  const [timeRange, setTimeRange] = useState('24h');

  // Mock analytics data
  const trafficTrends = Array.from({ length: 24 }, (_, i) => ({
    hour: `${i}:00`,
    vehicles: Math.floor(Math.random() * 500 + 200),
    pedestrians: Math.floor(Math.random() * 200 + 50),
    bicycles: Math.floor(Math.random() * 50 + 10),
  }));

  const nodePerformance = Array.from({ length: 10 }, (_, i) => ({
    time: `${i * 6}m`,
    latency: Math.random() * 30 + 10,
    accuracy: Math.random() * 5 + 95,
    throughput: Math.random() * 50 + 50,
  }));

  const detectionDistribution = [
    { name: 'Vehicle', value: 45, color: '#ffffff' },
    { name: 'Pedestrian', value: 25, color: '#a3a3a3' },
    { name: 'Bicycle', value: 15, color: '#737373' },
    { name: 'Bus', value: 10, color: '#525252' },
    { name: 'Truck', value: 5, color: '#262626' },
  ];

  const bandwidthSavings = Array.from({ length: 12 }, (_, i) => ({
    month: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i],
    traditional: 100,
    edgeQI: Math.random() * 30 + 20,
    savings: Math.random() * 70 + 65,
  }));

  const energyEfficiency = Array.from({ length: 7 }, (_, i) => ({
    day: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i],
    quantized: Math.random() * 20 + 30,
    standard: Math.random() * 30 + 70,
  }));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold">Analytics & Reports</h2>
          <p className="text-sm text-neutral-400 mt-1">
            System performance and insights
          </p>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="input text-sm"
          >
            <option value="1h">Last Hour</option>
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>

          <button className="btn-secondary flex items-center gap-2">
            <Download className="w-4 h-4" />
            Export Report
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard
          icon={BarChart3}
          label="Total Traffic"
          value="12,458"
          change="+12.5%"
          positive={true}
        />
        <MetricCard
          icon={TrendingDown}
          label="Bandwidth Saved"
          value="74.5%"
          change="+2.3%"
          positive={true}
        />
        <MetricCard
          icon={TrendingDown}
          label="Energy Saved"
          value="65.8%"
          change="+1.8%"
          positive={true}
        />
        <MetricCard
          icon={Clock}
          label="Avg Response Time"
          value="45ms"
          change="-8.2%"
          positive={true}
        />
      </div>

      {/* Traffic Trends */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold mb-4">Traffic Volume Trends</h3>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={trafficTrends}>
            <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
            <XAxis dataKey="hour" stroke="#737373" style={{ fontSize: '12px' }} />
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
              dataKey="vehicles"
              stackId="1"
              stroke="#ffffff"
              fill="#737373"
              name="Vehicles"
            />
            <Area
              type="monotone"
              dataKey="pedestrians"
              stackId="1"
              stroke="#a3a3a3"
              fill="#525252"
              name="Pedestrians"
            />
            <Area
              type="monotone"
              dataKey="bicycles"
              stackId="1"
              stroke="#525252"
              fill="#262626"
              name="Bicycles"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Performance & Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Node Performance */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">Node Performance</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={nodePerformance}>
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
                dataKey="accuracy"
                stroke="#a3a3a3"
                strokeWidth={2}
                dot={false}
                name="Accuracy (%)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Detection Distribution */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">Detection Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={detectionDistribution}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={2}
                dataKey="value"
              >
                {detectionDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0a0a0a',
                  border: '1px solid #262626',
                  borderRadius: '8px',
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="grid grid-cols-2 gap-2 mt-4">
            {detectionDistribution.map((item, idx) => (
              <div key={idx} className="flex items-center gap-2">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: item.color }}
                />
                <span className="text-sm text-neutral-400">{item.name}</span>
                <span className="text-sm font-semibold ml-auto">
                  {item.value}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bandwidth & Energy Efficiency */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bandwidth Savings */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">
            Bandwidth Optimization (Monthly)
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={bandwidthSavings}>
              <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
              <XAxis
                dataKey="month"
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
              <Bar
                dataKey="traditional"
                fill="#525252"
                name="Traditional (GB)"
                radius={[4, 4, 0, 0]}
              />
              <Bar
                dataKey="edgeQI"
                fill="#ffffff"
                name="EDGE-QI (GB)"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Energy Efficiency */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">
            Energy Efficiency (Weekly)
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={energyEfficiency}>
              <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
              <XAxis
                dataKey="day"
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
              <Bar
                dataKey="standard"
                fill="#525252"
                name="Standard (kWh)"
                radius={[4, 4, 0, 0]}
              />
              <Bar
                dataKey="quantized"
                fill="#ffffff"
                name="Quantized (kWh)"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Reports Summary */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold mb-4">Available Reports</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <ReportCard
            title="System Performance Report"
            description="Comprehensive analysis of system metrics"
            date="November 5, 2025"
          />
          <ReportCard
            title="Energy Efficiency Analysis"
            description="Model quantization impact on energy usage"
            date="November 4, 2025"
          />
          <ReportCard
            title="Bandwidth Optimization Report"
            description="Anomaly-driven transmission effectiveness"
            date="November 3, 2025"
          />
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ icon: Icon, label, value, change, positive }) => (
  <div className="card p-5">
    <div className="flex items-center gap-2 text-neutral-400 mb-2">
      <Icon className="w-4 h-4" />
      <span className="text-sm">{label}</span>
    </div>
    <div className="flex items-baseline justify-between">
      <p className="text-3xl font-bold">{value}</p>
      <span
        className={`text-sm font-medium ${
          positive ? 'text-green-400' : 'text-red-400'
        }`}
      >
        {change}
      </span>
    </div>
  </div>
);

const ReportCard = ({ title, description, date }) => (
  <div className="bg-neutral-900 rounded-lg p-4 hover:bg-neutral-800 transition-colors cursor-pointer">
    <div className="flex items-start gap-3">
      <div className="p-2 bg-white/5 rounded-lg">
        <FileText className="w-5 h-5" />
      </div>
      <div className="flex-1 min-w-0">
        <h4 className="font-semibold mb-1">{title}</h4>
        <p className="text-sm text-neutral-400 mb-2">{description}</p>
        <p className="text-xs text-neutral-500">{date}</p>
      </div>
    </div>
  </div>
);

export default Analytics;
