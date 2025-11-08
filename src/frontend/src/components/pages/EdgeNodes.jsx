import React, { useState } from 'react';
import { useEdgeQI } from '../../contexts/EdgeQIContext';
import {
  Server,
  Activity,
  Cpu,
  HardDrive,
  Wifi,
  Zap,
  AlertCircle,
  CheckCircle,
  XCircle,
  RefreshCw,
  Filter,
} from 'lucide-react';

const EdgeNodes = () => {
  const { edgeNodes, fetchEdgeNodes } = useEdgeQI();
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedNode, setSelectedNode] = useState(null);

  const filteredNodes =
    filterStatus === 'all'
      ? edgeNodes
      : edgeNodes.filter((node) => node.status === filterStatus);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="w-5 h-5 text-green-400" />;
      case 'idle':
        return <Activity className="w-5 h-5 text-yellow-400" />;
      case 'fault':
        return <XCircle className="w-5 h-5 text-red-400" />;
      default:
        return <AlertCircle className="w-5 h-5 text-neutral-400" />;
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      active: 'badge-success',
      idle: 'badge-warning',
      fault: 'badge-error',
    };
    return badges[status] || 'badge-info';
  };

  return (
    <div className="space-y-6">
      {/* Header & Filters */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold">Edge Nodes</h2>
          <p className="text-sm text-neutral-400 mt-1">
            {filteredNodes.length} of {edgeNodes.length} nodes
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-neutral-900 rounded-lg p-1">
            <button
              onClick={() => setFilterStatus('all')}
              className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                filterStatus === 'all'
                  ? 'bg-white text-black'
                  : 'text-neutral-400 hover:text-white'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilterStatus('active')}
              className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                filterStatus === 'active'
                  ? 'bg-white text-black'
                  : 'text-neutral-400 hover:text-white'
              }`}
            >
              Active
            </button>
            <button
              onClick={() => setFilterStatus('idle')}
              className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                filterStatus === 'idle'
                  ? 'bg-white text-black'
                  : 'text-neutral-400 hover:text-white'
              }`}
            >
              Idle
            </button>
            <button
              onClick={() => setFilterStatus('fault')}
              className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                filterStatus === 'fault'
                  ? 'bg-white text-black'
                  : 'text-neutral-400 hover:text-white'
              }`}
            >
              Fault
            </button>
          </div>

          <button
            onClick={fetchEdgeNodes}
            className="btn-secondary flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
        </div>
      </div>

      {/* Nodes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredNodes.length === 0 ? (
          <div className="col-span-full card p-12 text-center">
            <Server className="w-12 h-12 text-neutral-600 mx-auto mb-4" />
            <p className="text-neutral-400">No nodes found</p>
          </div>
        ) : (
          filteredNodes.map((node) => (
            <div
              key={node.id}
              onClick={() => setSelectedNode(node)}
              className="card p-5 hover:border-neutral-700 cursor-pointer transition-all duration-200"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-white/5 rounded-lg">
                    {getStatusIcon(node.status)}
                  </div>
                  <div>
                    <h3 className="font-semibold">{node.id || 'Unknown Node'}</h3>
                    <span className={`${getStatusBadge(node.status)} mt-1`}>
                      {node.status}
                    </span>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <MetricRow
                  icon={Cpu}
                  label="CPU Usage"
                  value={`${node.cpuUsage || 0}%`}
                  progress={node.cpuUsage || 0}
                />
                <MetricRow
                  icon={HardDrive}
                  label="Memory"
                  value={`${node.memoryUsage || 0}%`}
                  progress={node.memoryUsage || 0}
                />
                <MetricRow
                  icon={Wifi}
                  label="Network"
                  value={node.networkStatus || 'Good'}
                />
                <MetricRow
                  icon={Zap}
                  label="Energy"
                  value={`${node.energyConsumption || 0}W`}
                />
              </div>

              {node.lastUpdate && (
                <div className="mt-4 pt-4 border-t border-neutral-800 text-xs text-neutral-500">
                  Last update: {new Date(node.lastUpdate).toLocaleTimeString()}
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Node Detail Modal */}
      {selectedNode && (
        <div
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedNode(null)}
        >
          <div
            className="card p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="p-3 bg-white/5 rounded-lg">
                  {getStatusIcon(selectedNode.status)}
                </div>
                <div>
                  <h2 className="text-2xl font-bold">{selectedNode.id}</h2>
                  <span className={`${getStatusBadge(selectedNode.status)} mt-2`}>
                    {selectedNode.status}
                  </span>
                </div>
              </div>
              <button
                onClick={() => setSelectedNode(null)}
                className="btn-ghost"
              >
                Close
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <DetailCard
                icon={Cpu}
                label="CPU Usage"
                value={`${selectedNode.cpuUsage || 0}%`}
              />
              <DetailCard
                icon={HardDrive}
                label="Memory Usage"
                value={`${selectedNode.memoryUsage || 0}%`}
              />
              <DetailCard
                icon={Wifi}
                label="Network Status"
                value={selectedNode.networkStatus || 'Unknown'}
              />
              <DetailCard
                icon={Zap}
                label="Energy Consumption"
                value={`${selectedNode.energyConsumption || 0}W`}
              />
              <DetailCard
                icon={Activity}
                label="Uptime"
                value={selectedNode.uptime || 'N/A'}
              />
              <DetailCard
                icon={Server}
                label="Location"
                value={selectedNode.location || 'Unknown'}
              />
            </div>

            {selectedNode.logs && selectedNode.logs.length > 0 && (
              <div className="mt-6">
                <h3 className="font-semibold mb-3">Recent Logs</h3>
                <div className="bg-neutral-900 rounded-lg p-4 space-y-2 max-h-60 overflow-y-auto">
                  {selectedNode.logs.map((log, idx) => (
                    <div key={idx} className="text-sm font-mono text-neutral-400">
                      {log}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

const MetricRow = ({ icon: Icon, label, value, progress }) => (
  <div className="flex items-center justify-between">
    <div className="flex items-center gap-2 text-sm text-neutral-400">
      <Icon className="w-4 h-4" />
      <span>{label}</span>
    </div>
    <div className="flex items-center gap-2">
      <span className="text-sm font-medium">{value}</span>
      {progress !== undefined && (
        <div className="w-16 h-1.5 bg-neutral-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-white rounded-full transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  </div>
);

const DetailCard = ({ icon: Icon, label, value }) => (
  <div className="bg-neutral-900 rounded-lg p-4">
    <div className="flex items-center gap-2 text-neutral-400 mb-2">
      <Icon className="w-4 h-4" />
      <span className="text-sm">{label}</span>
    </div>
    <p className="text-xl font-bold">{value}</p>
  </div>
);

export default EdgeNodes;
