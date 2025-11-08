import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import io from 'socket.io-client';

const EdgeQIContext = createContext(null);

export const useEdgeQI = () => {
  const context = useContext(EdgeQIContext);
  if (!context) {
    throw new Error('useEdgeQI must be used within EdgeQIProvider');
  }
  return context;
};

export const EdgeQIProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [systemMetrics, setSystemMetrics] = useState({
    totalNodes: 0,
    activeNodes: 0,
    totalDetections: 0,
    averageLatency: 0,
    bandwidthSaved: 0,
    energySaved: 0,
  });
  const [edgeNodes, setEdgeNodes] = useState([]);
  const [detections, setDetections] = useState([]);
  const [consensusData, setConsensusData] = useState([]);
  const [logs, setLogs] = useState([]);
  const [alerts, setAlerts] = useState([]);

  // Initialize WebSocket connection
  useEffect(() => {
    const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
    const newSocket = io(backendUrl, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: Infinity,
    });

    newSocket.on('connect', () => {
      console.log('✅ Connected to EDGE-QI backend');
      setConnected(true);
    });

    newSocket.on('disconnect', () => {
      console.log('❌ Disconnected from EDGE-QI backend');
      setConnected(false);
    });

    newSocket.on('system_metrics', (data) => {
      setSystemMetrics(data);
    });

    newSocket.on('edge_node_update', (data) => {
      setEdgeNodes((prev) => {
        const index = prev.findIndex((node) => node.id === data.id);
        if (index >= 0) {
          const updated = [...prev];
          updated[index] = { ...updated[index], ...data };
          return updated;
        }
        return [...prev, data];
      });
    });

    newSocket.on('detection_result', (data) => {
      setDetections((prev) => [data, ...prev].slice(0, 100));
    });

    newSocket.on('consensus_update', (data) => {
      setConsensusData((prev) => [data, ...prev].slice(0, 50));
    });

    newSocket.on('system_log', (data) => {
      setLogs((prev) => [data, ...prev].slice(0, 200));
    });

    newSocket.on('alert', (data) => {
      setAlerts((prev) => [{ ...data, id: Date.now(), timestamp: new Date() }, ...prev].slice(0, 50));
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  // Fetch initial data
  useEffect(() => {
    if (connected) {
      fetchSystemStatus();
      fetchEdgeNodes();
      fetchDetections();
    }
  }, [connected]);

  const fetchSystemStatus = useCallback(async () => {
    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${backendUrl}/api/system/status`);
      if (response.ok) {
        const data = await response.json();
        setSystemMetrics(data.metrics || systemMetrics);
      }
    } catch (error) {
      console.error('Error fetching system status:', error);
    }
  }, []);

  const fetchEdgeNodes = useCallback(async () => {
    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${backendUrl}/api/nodes`);
      if (response.ok) {
        const data = await response.json();
        console.log('📡 Fetched nodes:', data);
        // Backend returns array directly, not wrapped in {nodes: [...]}
        setEdgeNodes(Array.isArray(data) ? data : (data.nodes || []));
      }
    } catch (error) {
      console.error('Error fetching edge nodes:', error);
    }
  }, []);

  const fetchDetections = useCallback(async () => {
    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${backendUrl}/api/detections?limit=100`);
      if (response.ok) {
        const data = await response.json();
        console.log('📡 Fetched detections:', data);
        // Backend returns array directly
        setDetections(Array.isArray(data) ? data : (data.detections || []));
      }
    } catch (error) {
      console.error('Error fetching detections:', error);
    }
  }, []);

  const dismissAlert = useCallback((alertId) => {
    setAlerts((prev) => prev.filter((alert) => alert.id !== alertId));
  }, []);

  const clearLogs = useCallback(() => {
    setLogs([]);
  }, []);

  const value = {
    connected,
    socket,
    systemMetrics,
    edgeNodes,
    detections,
    consensusData,
    logs,
    alerts,
    dismissAlert,
    clearLogs,
    fetchSystemStatus,
    fetchEdgeNodes,
    fetchDetections,
  };

  return <EdgeQIContext.Provider value={value}>{children}</EdgeQIContext.Provider>;
};
