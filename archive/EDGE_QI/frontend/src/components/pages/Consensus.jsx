import React, { useState } from 'react';
import { useEdgeQI } from '../../contexts/EdgeQIContext';
import {
  GitBranch,
  CheckCircle,
  XCircle,
  Clock,
  Shield,
  AlertTriangle,
  Users,
  Vote,
} from 'lucide-react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

const Consensus = () => {
  const { consensusData, edgeNodes } = useEdgeQI();
  const [selectedRound, setSelectedRound] = useState(null);

  // Mock consensus data
  const consensusHistory = Array.from({ length: 20 }, (_, i) => ({
    round: i + 1,
    success: Math.random() > 0.1,
    participants: Math.floor(Math.random() * 3 + 5),
    duration: Math.floor(Math.random() * 200 + 50),
    timestamp: new Date(Date.now() - (20 - i) * 60000),
  }));

  const nodeVoting = [
    { status: 'Agreed', count: 6, color: '#ffffff' },
    { status: 'Disagreed', count: 1, color: '#737373' },
    { status: 'Byzantine', count: 0, color: '#525252' },
  ];

  const consensusMetrics = Array.from({ length: 15 }, (_, i) => ({
    time: `${i}m`,
    consensusRate: Math.random() * 10 + 90,
    avgDuration: Math.random() * 50 + 100,
  }));

  const faultTolerance = [
    { round: 1, faults: 0, tolerated: 2 },
    { round: 2, faults: 1, tolerated: 2 },
    { round: 3, faults: 0, tolerated: 2 },
    { round: 4, faults: 0, tolerated: 2 },
    { round: 5, faults: 1, tolerated: 2 },
  ];

  const successRate =
    (consensusHistory.filter((r) => r.success).length /
      consensusHistory.length) *
    100;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold">Byzantine Consensus Protocol</h2>
        <p className="text-sm text-neutral-400 mt-1">
          Distributed fault-tolerant decision making
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard
          icon={GitBranch}
          label="Total Rounds"
          value={consensusHistory.length}
          subtitle="Last hour"
        />
        <MetricCard
          icon={CheckCircle}
          label="Success Rate"
          value={`${Math.round(successRate)}%`}
          subtitle="Consensus achieved"
        />
        <MetricCard
          icon={Users}
          label="Active Participants"
          value={edgeNodes.filter((n) => n.status === 'active').length}
          subtitle={`of ${edgeNodes.length} nodes`}
        />
        <MetricCard
          icon={Shield}
          label="Fault Tolerance"
          value="f ≤ 2"
          subtitle="Byzantine nodes"
        />
      </div>

      {/* Consensus Performance */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Consensus Metrics Chart */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">Consensus Performance</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={consensusMetrics}>
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
                dataKey="consensusRate"
                stroke="#ffffff"
                strokeWidth={2}
                dot={false}
                name="Success Rate (%)"
              />
              <Line
                type="monotone"
                dataKey="avgDuration"
                stroke="#737373"
                strokeWidth={2}
                dot={false}
                name="Duration (ms)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Node Voting Distribution */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">Current Round Votes</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={nodeVoting}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={2}
                dataKey="count"
              >
                {nodeVoting.map((entry, index) => (
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
          <div className="grid grid-cols-3 gap-2 mt-4">
            {nodeVoting.map((item, idx) => (
              <div key={idx} className="text-center">
                <div
                  className="w-3 h-3 rounded-full mx-auto mb-1"
                  style={{ backgroundColor: item.color }}
                />
                <p className="text-xs text-neutral-400">{item.status}</p>
                <p className="text-lg font-bold">{item.count}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Fault Tolerance */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold mb-4">Byzantine Fault Tolerance</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={faultTolerance}>
            <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
            <XAxis
              dataKey="round"
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
              dataKey="faults"
              fill="#737373"
              name="Detected Faults"
              radius={[4, 4, 0, 0]}
            />
            <Bar
              dataKey="tolerated"
              fill="#ffffff"
              name="Fault Tolerance"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Consensus History */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold mb-4">Consensus History</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-neutral-800">
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Round
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Status
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Participants
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Duration
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Timestamp
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Action
                </th>
              </tr>
            </thead>
            <tbody>
              {consensusHistory.slice().reverse().map((round, idx) => (
                <tr
                  key={idx}
                  className="border-b border-neutral-800 hover:bg-white/5 transition-colors"
                >
                  <td className="py-3 px-4 text-sm font-mono">#{round.round}</td>
                  <td className="py-3 px-4 text-sm">
                    {round.success ? (
                      <span className="badge-success flex items-center gap-1 w-fit">
                        <CheckCircle className="w-3 h-3" />
                        Success
                      </span>
                    ) : (
                      <span className="badge-error flex items-center gap-1 w-fit">
                        <XCircle className="w-3 h-3" />
                        Failed
                      </span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-sm">
                    {round.participants} nodes
                  </td>
                  <td className="py-3 px-4 text-sm">
                    {round.duration}ms
                  </td>
                  <td className="py-3 px-4 text-sm text-neutral-400">
                    {round.timestamp.toLocaleTimeString()}
                  </td>
                  <td className="py-3 px-4 text-sm">
                    <button
                      onClick={() => setSelectedRound(round)}
                      className="btn-ghost py-1 px-2 text-xs"
                    >
                      Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Protocol Information */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">Protocol Details</h3>
          <div className="space-y-3">
            <InfoRow label="Algorithm" value="Practical Byzantine Fault Tolerance (PBFT)" />
            <InfoRow label="Fault Tolerance" value="f ≤ (n-1)/3" />
            <InfoRow label="Min Nodes Required" value="3f + 1" />
            <InfoRow label="Current Nodes" value={`${edgeNodes.length} nodes`} />
            <InfoRow label="Consensus Threshold" value="2f + 1 votes" />
          </div>
        </div>

        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-4">Security Status</h3>
          <div className="space-y-3">
            <SecurityItem
              icon={Shield}
              label="Byzantine Protection"
              status="Active"
              color="text-green-400"
            />
            <SecurityItem
              icon={CheckCircle}
              label="Message Authentication"
              status="Enabled"
              color="text-green-400"
            />
            <SecurityItem
              icon={GitBranch}
              label="State Replication"
              status="Synchronized"
              color="text-green-400"
            />
            <SecurityItem
              icon={AlertTriangle}
              label="Fault Detection"
              status="Monitoring"
              color="text-yellow-400"
            />
          </div>
        </div>
      </div>

      {/* Round Details Modal */}
      {selectedRound && (
        <div
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedRound(null)}
        >
          <div
            className="card p-6 max-w-2xl w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">Round #{selectedRound.round}</h2>
              <button
                onClick={() => setSelectedRound(null)}
                className="btn-ghost"
              >
                Close
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <DetailCard label="Status" value={selectedRound.success ? "Success" : "Failed"} />
              <DetailCard label="Participants" value={`${selectedRound.participants} nodes`} />
              <DetailCard label="Duration" value={`${selectedRound.duration}ms`} />
              <DetailCard label="Timestamp" value={selectedRound.timestamp.toLocaleString()} />
            </div>

            <div className="mt-6">
              <h3 className="font-semibold mb-3">Node Votes</h3>
              <div className="space-y-2">
                {Array.from({ length: selectedRound.participants }).map((_, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-3 bg-neutral-900 rounded-lg"
                  >
                    <span className="font-mono text-sm">Node-{idx + 1}</span>
                    <span className="badge-success">Agreed</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const MetricCard = ({ icon: Icon, label, value, subtitle }) => (
  <div className="card p-5">
    <div className="flex items-center gap-2 text-neutral-400 mb-2">
      <Icon className="w-4 h-4" />
      <span className="text-sm">{label}</span>
    </div>
    <p className="text-3xl font-bold mb-1">{value}</p>
    {subtitle && <p className="text-xs text-neutral-500">{subtitle}</p>}
  </div>
);

const InfoRow = ({ label, value }) => (
  <div className="flex justify-between items-center py-2 border-b border-neutral-800 last:border-0">
    <span className="text-sm text-neutral-400">{label}</span>
    <span className="text-sm font-medium">{value}</span>
  </div>
);

const SecurityItem = ({ icon: Icon, label, status, color }) => (
  <div className="flex items-center justify-between p-3 bg-neutral-900 rounded-lg">
    <div className="flex items-center gap-3">
      <Icon className={`w-5 h-5 ${color}`} />
      <span className="text-sm font-medium">{label}</span>
    </div>
    <span className="text-sm text-neutral-400">{status}</span>
  </div>
);

const DetailCard = ({ label, value }) => (
  <div className="bg-neutral-900 rounded-lg p-4">
    <p className="text-sm text-neutral-400 mb-1">{label}</p>
    <p className="text-lg font-bold">{value}</p>
  </div>
);

export default Consensus;
