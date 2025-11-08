import React, { useState } from 'react';
import { Camera, Activity, Wifi, AlertCircle } from 'lucide-react';

const LiveCameraFeed = ({ node, detections = [] }) => {
  const [imageError, setImageError] = useState(false);

  // Get detections for this node
  const nodeDetections = detections.filter(d => d.node_id === node.id).slice(0, 10);

  // Status indicator color
  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'idle': return 'bg-yellow-500';
      case 'fault': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  // Network status color
  const getNetworkColor = (status) => {
    switch (status) {
      case 'excellent': return 'text-green-500';
      case 'good': return 'text-blue-500';
      case 'poor': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  return (
    <div className="bg-black border-2 border-white">
      {/* Header */}
      <div className="bg-neutral-950 border-b-2 border-white p-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <Camera className="w-5 h-5 text-white" />
              <h3 className="text-lg font-bold text-white">{node.name}</h3>
              <div className={`w-2 h-2 rounded-full ${getStatusColor(node.status)} animate-pulse`} />
            </div>
            <p className="text-sm text-gray-400">{node.location}</p>
            <p className="text-xs text-gray-500 mt-1">{node.description}</p>
          </div>
          <div className="text-right">
            <div className={`flex items-center gap-1 ${getNetworkColor(node.network_status)}`}>
              <Wifi className="w-4 h-4" />
              <span className="text-xs font-semibold uppercase">{node.network_status}</span>
            </div>
            <div className="text-xs text-gray-500 mt-1">{node.camera_type}</div>
          </div>
        </div>
      </div>

      {/* Camera Feed */}
      <div className="relative bg-gray-900 aspect-video">
        {!imageError && node.live_feed ? (
          <img
            src={node.live_feed}
            alt={`${node.name} live feed`}
            className="w-full h-full object-cover"
            onError={() => setImageError(true)}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-500">
            <div className="text-center">
              <AlertCircle className="w-16 h-16 mx-auto mb-2" />
              <p className="text-sm">Live Feed Unavailable</p>
              <p className="text-xs mt-1">Using detection data only</p>
            </div>
          </div>
        )}
        
        {/* Live indicator */}
        <div className="absolute top-3 left-3 bg-red-600 text-white px-3 py-1 text-xs font-bold flex items-center gap-2">
          <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
          LIVE
        </div>

        {/* Camera view type */}
        <div className="absolute top-3 right-3 bg-black bg-opacity-70 text-white px-3 py-1 text-xs">
          {node.camera_view}
        </div>
      </div>

      {/* Stats Bar */}
      <div className="grid grid-cols-5 border-t-2 border-white">
        <div className="p-3 border-r-2 border-white">
          <div className="text-xs text-gray-400">DETECTIONS</div>
          <div className="text-lg font-bold text-white">{node.total_detections.toLocaleString()}</div>
        </div>
        <div className="p-3 border-r-2 border-white">
          <div className="text-xs text-gray-400">LATENCY</div>
          <div className="text-lg font-bold text-white">{node.average_latency}ms</div>
        </div>
        <div className="p-3 border-r-2 border-white">
          <div className="text-xs text-gray-400">CPU</div>
          <div className="text-lg font-bold text-white">{node.cpu_usage}%</div>
        </div>
        <div className="p-3 border-r-2 border-white">
          <div className="text-xs text-gray-400">MEMORY</div>
          <div className="text-lg font-bold text-white">{node.memory_usage}%</div>
        </div>
        <div className="p-3">
          <div className="text-xs text-gray-400">UPTIME</div>
          <div className="text-lg font-bold text-white">{node.uptime}%</div>
        </div>
      </div>

      {/* Recent Detections */}
      {nodeDetections.length > 0 && (
        <div className="border-t-2 border-white p-4 bg-neutral-950">
          <div className="flex items-center gap-2 mb-3">
            <Activity className="w-4 h-4 text-white" />
            <h4 className="font-bold text-sm text-white">RECENT DETECTIONS</h4>
            <span className="text-xs text-gray-500">({nodeDetections.length})</span>
          </div>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {nodeDetections.map((detection) => (
              <div
                key={detection.id}
                className="flex items-center justify-between p-2 bg-neutral-900 border border-gray-700 text-xs"
              >
                <div className="flex items-center gap-3">
                  <span className="font-bold uppercase text-white">{detection.object_type}</span>
                  <span className="text-gray-500">
                    {new Date(detection.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-20 bg-gray-700 h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-white h-full"
                      style={{ width: `${detection.confidence * 100}%` }}
                    />
                  </div>
                  <span className="font-mono font-bold min-w-[3rem] text-right text-white">
                    {(detection.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Node Info */}
      <div className="border-t-2 border-white p-4 bg-neutral-900">
        <div className="grid grid-cols-2 gap-4 text-xs">
          <div>
            <span className="text-gray-400">Node ID:</span>
            <span className="ml-2 font-mono font-bold text-white">{node.id}</span>
          </div>
          <div>
            <span className="text-gray-400">IP Address:</span>
            <span className="ml-2 font-mono font-bold text-white">{node.ip_address}:{node.port}</span>
          </div>
          <div>
            <span className="text-gray-400">Model:</span>
            <span className="ml-2 font-bold text-white">YOLOv8n</span>
          </div>
          <div>
            <span className="text-gray-400">Classes:</span>
            <span className="ml-2 font-bold text-white">{node.capabilities.classes?.join(', ')}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LiveCameraFeed;
