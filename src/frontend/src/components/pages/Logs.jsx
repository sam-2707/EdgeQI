import React, { useState, useRef, useEffect } from 'react';
import { useEdgeQI } from '../../contexts/EdgeQIContext';
import {
  FileText,
  Download,
  Trash2,
  Filter,
  Search,
  AlertCircle,
  Info,
  CheckCircle,
  XCircle,
} from 'lucide-react';

const Logs = () => {
  const { logs, clearLogs } = useEdgeQI();
  const [filterLevel, setFilterLevel] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [autoScroll, setAutoScroll] = useState(true);
  const logsEndRef = useRef(null);

  const logLevels = ['all', 'info', 'warning', 'error', 'success'];

  const filteredLogs = logs.filter((log) => {
    const matchesLevel =
      filterLevel === 'all' || log.level === filterLevel;
    const matchesSearch =
      searchQuery === '' ||
      log.message?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      log.source?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesLevel && matchesSearch;
  });

  useEffect(() => {
    if (autoScroll && logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs, autoScroll]);

  const getLogIcon = (level) => {
    switch (level) {
      case 'error':
        return <XCircle className="w-4 h-4 text-red-400" />;
      case 'warning':
        return <AlertCircle className="w-4 h-4 text-yellow-400" />;
      case 'success':
        return <CheckCircle className="w-4 h-4 text-green-400" />;
      default:
        return <Info className="w-4 h-4 text-blue-400" />;
    }
  };

  const getLogColor = (level) => {
    switch (level) {
      case 'error':
        return 'text-red-400';
      case 'warning':
        return 'text-yellow-400';
      case 'success':
        return 'text-green-400';
      default:
        return 'text-blue-400';
    }
  };

  const exportLogs = () => {
    const logsText = filteredLogs
      .map(
        (log) =>
          `[${new Date(log.timestamp).toISOString()}] [${log.level.toUpperCase()}] ${
            log.source || 'SYSTEM'
          }: ${log.message}`
      )
      .join('\n');

    const blob = new Blob([logsText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `edge-qi-logs-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold">System Logs</h2>
          <p className="text-sm text-neutral-400 mt-1">
            {filteredLogs.length} of {logs.length} logs
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-500" />
            <input
              type="text"
              placeholder="Search logs..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input pl-9 w-64"
            />
          </div>

          {/* Filter */}
          <select
            value={filterLevel}
            onChange={(e) => setFilterLevel(e.target.value)}
            className="input text-sm"
          >
            {logLevels.map((level) => (
              <option key={level} value={level}>
                {level.charAt(0).toUpperCase() + level.slice(1)}
              </option>
            ))}
          </select>

          {/* Auto Scroll Toggle */}
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={autoScroll}
              onChange={(e) => setAutoScroll(e.target.checked)}
              className="w-4 h-4"
            />
            <span className="text-sm">Auto-scroll</span>
          </label>

          {/* Actions */}
          <button
            onClick={exportLogs}
            className="btn-secondary flex items-center gap-2"
          >
            <Download className="w-4 h-4" />
            Export
          </button>

          <button
            onClick={clearLogs}
            className="btn-secondary flex items-center gap-2 text-red-400 hover:text-red-300"
          >
            <Trash2 className="w-4 h-4" />
            Clear
          </button>
        </div>
      </div>

      {/* Log Statistics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          label="Total Logs"
          value={logs.length}
          color="text-neutral-400"
        />
        <StatCard
          label="Errors"
          value={logs.filter((l) => l.level === 'error').length}
          color="text-red-400"
        />
        <StatCard
          label="Warnings"
          value={logs.filter((l) => l.level === 'warning').length}
          color="text-yellow-400"
        />
        <StatCard
          label="Info"
          value={logs.filter((l) => l.level === 'info').length}
          color="text-blue-400"
        />
      </div>

      {/* Logs Display */}
      <div className="card p-6">
        <div className="bg-black rounded-lg p-4 h-[600px] overflow-y-auto font-mono text-sm">
          {filteredLogs.length === 0 ? (
            <div className="h-full flex items-center justify-center text-neutral-500">
              <div className="text-center">
                <FileText className="w-12 h-12 mx-auto mb-4 text-neutral-700" />
                <p>No logs to display</p>
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              {filteredLogs.map((log, idx) => (
                <div
                  key={idx}
                  className="flex gap-3 p-2 rounded hover:bg-white/5 transition-colors"
                >
                  <div className="flex-shrink-0 mt-0.5">
                    {getLogIcon(log.level)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-neutral-500 text-xs">
                        {new Date(log.timestamp).toLocaleTimeString()}
                      </span>
                      <span
                        className={`text-xs font-bold uppercase ${getLogColor(
                          log.level
                        )}`}
                      >
                        {log.level}
                      </span>
                      {log.source && (
                        <span className="text-neutral-600 text-xs">
                          [{log.source}]
                        </span>
                      )}
                    </div>
                    <p className="text-neutral-300 break-words">
                      {log.message}
                    </p>
                    {log.details && (
                      <pre className="mt-1 text-xs text-neutral-500 overflow-x-auto">
                        {JSON.stringify(log.details, null, 2)}
                      </pre>
                    )}
                  </div>
                </div>
              ))}
              <div ref={logsEndRef} />
            </div>
          )}
        </div>
      </div>

      {/* Legend */}
      <div className="card p-4">
        <h3 className="font-semibold mb-3">Log Levels</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <LegendItem
            icon={Info}
            label="Info"
            description="General information"
            color="text-blue-400"
          />
          <LegendItem
            icon={CheckCircle}
            label="Success"
            description="Successful operations"
            color="text-green-400"
          />
          <LegendItem
            icon={AlertCircle}
            label="Warning"
            description="Warning messages"
            color="text-yellow-400"
          />
          <LegendItem
            icon={XCircle}
            label="Error"
            description="Error conditions"
            color="text-red-400"
          />
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ label, value, color }) => (
  <div className="card p-4">
    <p className="text-sm text-neutral-400 mb-1">{label}</p>
    <p className={`text-2xl font-bold ${color}`}>{value}</p>
  </div>
);

const LegendItem = ({ icon: Icon, label, description, color }) => (
  <div className="flex items-start gap-3">
    <Icon className={`w-5 h-5 ${color} flex-shrink-0 mt-0.5`} />
    <div>
      <p className={`font-medium ${color}`}>{label}</p>
      <p className="text-xs text-neutral-500">{description}</p>
    </div>
  </div>
);

export default Logs;
