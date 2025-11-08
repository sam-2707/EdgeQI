import React, { useState } from 'react';
import {
  Settings as SettingsIcon,
  Save,
  RotateCcw,
  Bell,
  Shield,
  Database,
  Zap,
  Network,
  Eye,
  AlertCircle,
} from 'lucide-react';

const Settings = () => {
  const [settings, setSettings] = useState({
    // System Settings
    systemName: 'EDGE-QI System',
    refreshInterval: 5000,
    logRetention: 7,
    
    // Detection Settings
    detectionThreshold: 0.5,
    maxDetectionsPerFrame: 100,
    modelType: 'yolov8n',
    
    // Node Settings
    maxNodes: 20,
    nodeTimeout: 30,
    healthCheckInterval: 10,
    
    // Consensus Settings
    consensusAlgorithm: 'pbft',
    maxByzantineNodes: 2,
    consensusTimeout: 5000,
    
    // Energy Settings
    energyOptimization: true,
    modelQuantization: true,
    
    // Notifications
    enableNotifications: true,
    notifyOnError: true,
    notifyOnConsensus: false,
    notifyOnNodeFailure: true,
  });

  const [hasChanges, setHasChanges] = useState(false);

  const handleChange = (key, value) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
    setHasChanges(true);
  };

  const handleSave = () => {
    console.log('Saving settings:', settings);
    // In production, send to backend
    setHasChanges(false);
  };

  const handleReset = () => {
    // Reset to defaults
    setHasChanges(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold">Settings</h2>
          <p className="text-sm text-neutral-400 mt-1">
            Configure system parameters and preferences
          </p>
        </div>

        <div className="flex items-center gap-3">
          {hasChanges && (
            <span className="flex items-center gap-2 text-sm text-yellow-400">
              <AlertCircle className="w-4 h-4" />
              Unsaved changes
            </span>
          )}
          <button
            onClick={handleReset}
            className="btn-secondary flex items-center gap-2"
          >
            <RotateCcw className="w-4 h-4" />
            Reset
          </button>
          <button
            onClick={handleSave}
            disabled={!hasChanges}
            className="btn-primary flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            Save Changes
          </button>
        </div>
      </div>

      {/* System Settings */}
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-white/5 rounded-lg">
            <SettingsIcon className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-semibold">System Settings</h3>
        </div>

        <div className="space-y-4">
          <SettingRow
            label="System Name"
            description="Display name for this EDGE-QI instance"
          >
            <input
              type="text"
              value={settings.systemName}
              onChange={(e) => handleChange('systemName', e.target.value)}
              className="input w-full max-w-md"
            />
          </SettingRow>

          <SettingRow
            label="Refresh Interval"
            description="Dashboard data refresh rate (milliseconds)"
          >
            <input
              type="number"
              value={settings.refreshInterval}
              onChange={(e) =>
                handleChange('refreshInterval', parseInt(e.target.value))
              }
              min="1000"
              max="60000"
              step="1000"
              className="input w-32"
            />
          </SettingRow>

          <SettingRow
            label="Log Retention"
            description="Number of days to keep system logs"
          >
            <input
              type="number"
              value={settings.logRetention}
              onChange={(e) =>
                handleChange('logRetention', parseInt(e.target.value))
              }
              min="1"
              max="365"
              className="input w-32"
            />
          </SettingRow>
        </div>
      </div>

      {/* Detection Settings */}
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-white/5 rounded-lg">
            <Eye className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-semibold">Detection Settings</h3>
        </div>

        <div className="space-y-4">
          <SettingRow
            label="Detection Threshold"
            description="Minimum confidence score for object detection (0-1)"
          >
            <input
              type="range"
              value={settings.detectionThreshold}
              onChange={(e) =>
                handleChange('detectionThreshold', parseFloat(e.target.value))
              }
              min="0"
              max="1"
              step="0.05"
              className="w-48"
            />
            <span className="text-sm font-medium ml-3">
              {settings.detectionThreshold.toFixed(2)}
            </span>
          </SettingRow>

          <SettingRow
            label="Model Type"
            description="YOLOv8 model variant for detection"
          >
            <select
              value={settings.modelType}
              onChange={(e) => handleChange('modelType', e.target.value)}
              className="input w-48"
            >
              <option value="yolov8n">YOLOv8n (Nano)</option>
              <option value="yolov8s">YOLOv8s (Small)</option>
              <option value="yolov8m">YOLOv8m (Medium)</option>
              <option value="yolov8l">YOLOv8l (Large)</option>
            </select>
          </SettingRow>

          <SettingRow
            label="Max Detections Per Frame"
            description="Maximum number of objects to detect in a single frame"
          >
            <input
              type="number"
              value={settings.maxDetectionsPerFrame}
              onChange={(e) =>
                handleChange('maxDetectionsPerFrame', parseInt(e.target.value))
              }
              min="1"
              max="1000"
              className="input w-32"
            />
          </SettingRow>
        </div>
      </div>

      {/* Edge Node Settings */}
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-white/5 rounded-lg">
            <Network className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-semibold">Edge Node Settings</h3>
        </div>

        <div className="space-y-4">
          <SettingRow
            label="Maximum Nodes"
            description="Maximum number of edge nodes in the network"
          >
            <input
              type="number"
              value={settings.maxNodes}
              onChange={(e) =>
                handleChange('maxNodes', parseInt(e.target.value))
              }
              min="1"
              max="100"
              className="input w-32"
            />
          </SettingRow>

          <SettingRow
            label="Node Timeout"
            description="Node inactivity timeout in seconds"
          >
            <input
              type="number"
              value={settings.nodeTimeout}
              onChange={(e) =>
                handleChange('nodeTimeout', parseInt(e.target.value))
              }
              min="10"
              max="300"
              className="input w-32"
            />
          </SettingRow>

          <SettingRow
            label="Health Check Interval"
            description="Node health check frequency in seconds"
          >
            <input
              type="number"
              value={settings.healthCheckInterval}
              onChange={(e) =>
                handleChange('healthCheckInterval', parseInt(e.target.value))
              }
              min="5"
              max="60"
              className="input w-32"
            />
          </SettingRow>
        </div>
      </div>

      {/* Consensus Settings */}
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-white/5 rounded-lg">
            <Shield className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-semibold">Consensus Settings</h3>
        </div>

        <div className="space-y-4">
          <SettingRow
            label="Consensus Algorithm"
            description="Byzantine fault tolerance algorithm"
          >
            <select
              value={settings.consensusAlgorithm}
              onChange={(e) => handleChange('consensusAlgorithm', e.target.value)}
              className="input w-48"
            >
              <option value="pbft">PBFT</option>
              <option value="raft">Raft</option>
              <option value="paxos">Paxos</option>
            </select>
          </SettingRow>

          <SettingRow
            label="Max Byzantine Nodes"
            description="Maximum number of Byzantine (faulty) nodes tolerated"
          >
            <input
              type="number"
              value={settings.maxByzantineNodes}
              onChange={(e) =>
                handleChange('maxByzantineNodes', parseInt(e.target.value))
              }
              min="0"
              max="10"
              className="input w-32"
            />
          </SettingRow>

          <SettingRow
            label="Consensus Timeout"
            description="Maximum time to wait for consensus (milliseconds)"
          >
            <input
              type="number"
              value={settings.consensusTimeout}
              onChange={(e) =>
                handleChange('consensusTimeout', parseInt(e.target.value))
              }
              min="1000"
              max="30000"
              step="1000"
              className="input w-32"
            />
          </SettingRow>
        </div>
      </div>

      {/* Energy Optimization */}
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-white/5 rounded-lg">
            <Zap className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-semibold">Energy Optimization</h3>
        </div>

        <div className="space-y-4">
          <SettingRow
            label="Energy Optimization"
            description="Enable adaptive energy optimization algorithms"
          >
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.energyOptimization}
                onChange={(e) =>
                  handleChange('energyOptimization', e.target.checked)
                }
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-neutral-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-white"></div>
            </label>
          </SettingRow>

          <SettingRow
            label="Model Quantization"
            description="Use quantized models for reduced energy consumption"
          >
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.modelQuantization}
                onChange={(e) =>
                  handleChange('modelQuantization', e.target.checked)
                }
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-neutral-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-white"></div>
            </label>
          </SettingRow>
        </div>
      </div>

      {/* Notifications */}
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-white/5 rounded-lg">
            <Bell className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-semibold">Notifications</h3>
        </div>

        <div className="space-y-4">
          <SettingRow
            label="Enable Notifications"
            description="Receive system notifications and alerts"
          >
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.enableNotifications}
                onChange={(e) =>
                  handleChange('enableNotifications', e.target.checked)
                }
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-neutral-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-white"></div>
            </label>
          </SettingRow>

          <SettingRow
            label="Notify on Errors"
            description="Alert when system errors occur"
          >
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.notifyOnError}
                onChange={(e) =>
                  handleChange('notifyOnError', e.target.checked)
                }
                disabled={!settings.enableNotifications}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-neutral-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-white disabled:opacity-50"></div>
            </label>
          </SettingRow>

          <SettingRow
            label="Notify on Consensus"
            description="Alert when consensus rounds complete"
          >
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.notifyOnConsensus}
                onChange={(e) =>
                  handleChange('notifyOnConsensus', e.target.checked)
                }
                disabled={!settings.enableNotifications}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-neutral-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-white disabled:opacity-50"></div>
            </label>
          </SettingRow>

          <SettingRow
            label="Notify on Node Failure"
            description="Alert when edge nodes become unavailable"
          >
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.notifyOnNodeFailure}
                onChange={(e) =>
                  handleChange('notifyOnNodeFailure', e.target.checked)
                }
                disabled={!settings.enableNotifications}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-neutral-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-white disabled:opacity-50"></div>
            </label>
          </SettingRow>
        </div>
      </div>
    </div>
  );
};

const SettingRow = ({ label, description, children }) => (
  <div className="flex items-center justify-between py-4 border-b border-neutral-800 last:border-0">
    <div className="flex-1 mr-4">
      <p className="font-medium">{label}</p>
      <p className="text-sm text-neutral-400 mt-1">{description}</p>
    </div>
    <div className="flex-shrink-0">{children}</div>
  </div>
);

export default Settings;
