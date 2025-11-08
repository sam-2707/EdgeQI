import React, { useState, useEffect } from 'react';
import { useEdgeQI } from '../contexts/EdgeQIContext';
import LiveCameraFeed from '../components/LiveCameraFeed';
import { Camera, Grid, List, RefreshCw } from 'lucide-react';

const CamerasPage = () => {
  const { edgeNodes, detections } = useEdgeQI();
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
  const [filterStatus, setFilterStatus] = useState('all'); // 'all', 'active', 'idle', 'fault'
  const [lastUpdate, setLastUpdate] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setLastUpdate(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Safety check - ensure edgeNodes is an array
  const nodes = Array.isArray(edgeNodes) ? edgeNodes : [];

  // Filter nodes
  const filteredNodes = nodes.filter(node => {
    if (filterStatus === 'all') return true;
    return node.status === filterStatus;
  });

  const activeCount = nodes.filter(n => n.status === 'active').length;
  const idleCount = nodes.filter(n => n.status === 'idle').length;
  const faultCount = nodes.filter(n => n.status === 'fault').length;

  return (
    <div className="p-6 space-y-6 bg-black min-h-screen">
      {/* Header */}
      <div className="bg-neutral-950 border-2 border-white p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <Camera className="w-8 h-8 text-white" />
              <h1 className="text-3xl font-bold text-white">LIVE CAMERA FEEDS</h1>
            </div>
            <p className="text-gray-400">Real-time monitoring from all edge nodes</p>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-400">Last Update</div>
            <div className="font-mono font-bold text-white">{lastUpdate.toLocaleTimeString()}</div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-4 gap-4">
          <div className="p-4 bg-neutral-900 border-2 border-white">
            <div className="text-sm text-gray-400 mb-1">TOTAL CAMERAS</div>
            <div className="text-3xl font-bold text-white">{nodes.length}</div>
          </div>
          <div className="p-4 bg-neutral-900 border-2 border-green-500">
            <div className="text-sm text-green-400 mb-1">ACTIVE</div>
            <div className="text-3xl font-bold text-green-500">{activeCount}</div>
          </div>
          <div className="p-4 bg-neutral-900 border-2 border-yellow-500">
            <div className="text-sm text-yellow-400 mb-1">IDLE</div>
            <div className="text-3xl font-bold text-yellow-500">{idleCount}</div>
          </div>
          <div className="p-4 bg-neutral-900 border-2 border-red-500">
            <div className="text-sm text-red-400 mb-1">FAULT</div>
            <div className="text-3xl font-bold text-red-500">{faultCount}</div>
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="bg-neutral-950 border-2 border-white p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <label className="text-sm font-bold text-white">FILTER:</label>
            <div className="flex gap-2">
              <button
                onClick={() => setFilterStatus('all')}
                className={`px-4 py-2 font-bold text-sm border-2 transition-colors ${
                  filterStatus === 'all' 
                    ? 'bg-white text-black border-white' 
                    : 'bg-black text-white border-white hover:bg-neutral-900'
                }`}
              >
                ALL ({nodes.length})
              </button>
              <button
                onClick={() => setFilterStatus('active')}
                className={`px-4 py-2 font-bold text-sm border-2 transition-colors ${
                  filterStatus === 'active' 
                    ? 'bg-green-500 text-black border-green-500' 
                    : 'bg-black text-green-500 border-green-500 hover:bg-neutral-900'
                }`}
              >
                ACTIVE ({activeCount})
              </button>
              <button
                onClick={() => setFilterStatus('idle')}
                className={`px-4 py-2 font-bold text-sm border-2 transition-colors ${
                  filterStatus === 'idle' 
                    ? 'bg-yellow-500 text-black border-yellow-500' 
                    : 'bg-black text-yellow-500 border-yellow-500 hover:bg-neutral-900'
                }`}
              >
                IDLE ({idleCount})
              </button>
              <button
                onClick={() => setFilterStatus('fault')}
                className={`px-4 py-2 font-bold text-sm border-2 transition-colors ${
                  filterStatus === 'fault' 
                    ? 'bg-red-500 text-black border-red-500' 
                    : 'bg-black text-red-500 border-red-500 hover:bg-neutral-900'
                }`}
              >
                FAULT ({faultCount})
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <label className="text-sm font-bold text-white">VIEW:</label>
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 border-2 border-white transition-colors ${
                viewMode === 'grid' 
                  ? 'bg-white text-black' 
                  : 'bg-black text-white hover:bg-neutral-900'
              }`}
              title="Grid View"
            >
              <Grid className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 border-2 border-white transition-colors ${
                viewMode === 'list' 
                  ? 'bg-white text-black' 
                  : 'bg-black text-white hover:bg-neutral-900'
              }`}
              title="List View"
            >
              <List className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Camera Feeds */}
      {filteredNodes.length === 0 ? (
        <div className="bg-neutral-950 border-2 border-white p-12 text-center">
          <Camera className="w-16 h-16 mx-auto mb-4 text-gray-600" />
          <h3 className="text-xl font-bold mb-2 text-white">No Cameras Found</h3>
          <p className="text-gray-400">
            {filterStatus === 'all'
              ? 'No camera nodes are currently available.'
              : `No cameras with status "${filterStatus}".`}
          </p>
        </div>
      ) : (
        <div className={viewMode === 'grid' ? 'grid grid-cols-2 gap-6' : 'space-y-6'}>
          {filteredNodes.map((node) => (
            <LiveCameraFeed key={node.id} node={node} detections={detections} />
          ))}
        </div>
      )}

      {/* Footer Info */}
      <div className="bg-neutral-950 text-white p-4 border-2 border-white">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin" />
            <span>Auto-refreshing every 5 seconds</span>
          </div>
          <div>
            Total Detections Today: <span className="font-bold">
              {nodes.reduce((sum, node) => sum + node.total_detections, 0).toLocaleString()}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CamerasPage;
