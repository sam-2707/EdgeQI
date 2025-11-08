import React, { useState, useRef } from 'react';
import { useEdgeQI } from '../../contexts/EdgeQIContext';
import {
  Camera,
  Play,
  Pause,
  Square,
  Upload,
  Download,
  Grid3x3,
  Maximize2,
  Eye,
  Filter,
} from 'lucide-react';

const Detection = () => {
  const { detections } = useEdgeQI();
  const [selectedStream, setSelectedStream] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // grid or single
  const [filterType, setFilterType] = useState('all');
  const videoRef = useRef(null);

  const objectTypes = ['all', 'vehicle', 'pedestrian', 'bicycle', 'bus', 'truck'];

  const filteredDetections =
    filterType === 'all'
      ? detections
      : detections.filter((d) => d.type?.toLowerCase() === filterType);

  const mockStreams = [
    { id: 'stream-1', name: 'Intersection A', status: 'active', fps: 30 },
    { id: 'stream-2', name: 'Intersection B', status: 'active', fps: 30 },
    { id: 'stream-3', name: 'Highway 101', status: 'active', fps: 25 },
    { id: 'stream-4', name: 'Downtown Plaza', status: 'idle', fps: 0 },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold">Object Detection</h2>
          <p className="text-sm text-neutral-400 mt-1">
            Real-time YOLOv8 detection streams
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-neutral-900 rounded-lg p-1">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-md transition-colors ${
                viewMode === 'grid'
                  ? 'bg-white text-black'
                  : 'text-neutral-400 hover:text-white'
              }`}
              title="Grid View"
            >
              <Grid3x3 className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('single')}
              className={`p-2 rounded-md transition-colors ${
                viewMode === 'single'
                  ? 'bg-white text-black'
                  : 'text-neutral-400 hover:text-white'
              }`}
              title="Single View"
            >
              <Maximize2 className="w-4 h-4" />
            </button>
          </div>

          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="input text-sm"
          >
            {objectTypes.map((type) => (
              <option key={type} value={type}>
                {type.charAt(0).toUpperCase() + type.slice(1)}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Video Streams */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {mockStreams.map((stream) => (
            <div key={stream.id} className="card p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Camera className="w-4 h-4" />
                  <h3 className="font-semibold">{stream.name}</h3>
                </div>
                <div className="flex items-center gap-2">
                  <span
                    className={`${
                      stream.status === 'active'
                        ? 'badge-success'
                        : 'badge-warning'
                    }`}
                  >
                    {stream.status}
                  </span>
                  <span className="text-xs text-neutral-500">
                    {stream.fps} FPS
                  </span>
                </div>
              </div>

              <div className="aspect-video bg-neutral-900 rounded-lg flex items-center justify-center mb-3 relative overflow-hidden">
                <div className="absolute inset-0 flex items-center justify-center">
                  <Camera className="w-12 h-12 text-neutral-700" />
                </div>
                {stream.status === 'active' && (
                  <div className="absolute top-2 left-2">
                    <div className="flex items-center gap-1 bg-red-500 text-white text-xs px-2 py-1 rounded">
                      <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
                      LIVE
                    </div>
                  </div>
                )}
              </div>

              <div className="flex items-center justify-between">
                <div className="flex gap-2">
                  <button className="btn-secondary p-2">
                    {stream.status === 'active' ? (
                      <Pause className="w-4 h-4" />
                    ) : (
                      <Play className="w-4 h-4" />
                    )}
                  </button>
                  <button className="btn-secondary p-2">
                    <Square className="w-4 h-4" />
                  </button>
                </div>
                <button
                  onClick={() => setSelectedStream(stream)}
                  className="btn-ghost p-2"
                >
                  <Eye className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card p-6">
          <div className="aspect-video bg-neutral-900 rounded-lg flex items-center justify-center relative overflow-hidden mb-4">
            <Camera className="w-16 h-16 text-neutral-700" />
            <div className="absolute top-4 left-4">
              <div className="flex items-center gap-2 bg-red-500 text-white text-sm px-3 py-1.5 rounded">
                <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
                LIVE DETECTION
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex gap-3">
              <button className="btn-primary flex items-center gap-2">
                <Play className="w-4 h-4" />
                Start Detection
              </button>
              <button className="btn-secondary flex items-center gap-2">
                <Square className="w-4 h-4" />
                Stop
              </button>
            </div>

            <div className="flex gap-2">
              <button className="btn-ghost flex items-center gap-2">
                <Upload className="w-4 h-4" />
                Upload Video
              </button>
              <button className="btn-ghost flex items-center gap-2">
                <Download className="w-4 h-4" />
                Export
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Detection Results */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold mb-4">Detection Results</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-neutral-800">
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Timestamp
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Stream
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Object Type
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Confidence
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Bounding Box
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-neutral-400">
                  Action
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredDetections.length === 0 ? (
                <tr>
                  <td colSpan="6" className="text-center py-8 text-neutral-500">
                    No detections found
                  </td>
                </tr>
              ) : (
                filteredDetections.slice(0, 20).map((detection, idx) => (
                  <tr
                    key={idx}
                    className="border-b border-neutral-800 hover:bg-white/5 transition-colors"
                  >
                    <td className="py-3 px-4 text-sm">
                      {new Date(detection.timestamp).toLocaleTimeString()}
                    </td>
                    <td className="py-3 px-4 text-sm font-mono">
                      {detection.streamId || 'stream-1'}
                    </td>
                    <td className="py-3 px-4 text-sm capitalize">
                      {detection.type}
                    </td>
                    <td className="py-3 px-4 text-sm">
                      <div className="flex items-center gap-2">
                        <span className="badge-success">
                          {Math.round(detection.confidence * 100)}%
                        </span>
                        <div className="w-16 h-1.5 bg-neutral-800 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-green-500 rounded-full"
                            style={{
                              width: `${detection.confidence * 100}%`,
                            }}
                          />
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-sm font-mono text-neutral-400">
                      {detection.bbox
                        ? `[${detection.bbox.join(', ')}]`
                        : 'N/A'}
                    </td>
                    <td className="py-3 px-4 text-sm">
                      <button className="btn-ghost py-1 px-2 text-xs">
                        View
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Detection Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard label="Total Detections" value={detections.length} />
        <StatCard
          label="Avg Confidence"
          value={`${Math.round(
            detections.reduce((acc, d) => acc + d.confidence, 0) /
              detections.length || 0
          )}%`}
        />
        <StatCard
          label="Detection Rate"
          value={`${detections.length > 0 ? '30' : '0'} /sec`}
        />
        <StatCard label="Active Streams" value={mockStreams.length} />
      </div>
    </div>
  );
};

const StatCard = ({ label, value }) => (
  <div className="card p-4">
    <p className="text-sm text-neutral-400 mb-1">{label}</p>
    <p className="text-2xl font-bold">{value}</p>
  </div>
);

export default Detection;
