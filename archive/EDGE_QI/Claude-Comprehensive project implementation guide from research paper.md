# Comprehensive project implementation guide from research paper

**Created:** 11/1/2025 3:19:45  
**Updated:** 11/1/2025 3:30:14  
**Exported:** 11/1/2025 3:32:23  
**Link:** [https://claude.ai/chat/8c183732-43f0-4159-a019-8fc8dae2ac61](https://claude.ai/chat/8c183732-43f0-4159-a019-8fc8dae2ac61)  

## Prompt:
11/1/2025, 3:19:47 AM

> File: DS.pdf

> File: gemini-chat.2025-10-31.pdf

no what i want you to do is create a more in depth analysis , just put out more detail as to how the project should lok what it should connect more test cases edge cases everything should be there

it should be an in depth analysis of every detail of the report

make it as detailed as possible as to how it should look what should be there on front end pages how many should be there and all that stuff and then the grpahs should be shown the features like the edge cases critical cases all of them should be simulated also 

also which dataset to use how to use what to show 
how it works , how it should work, what to check 

in basic want you to make an entire report as to how to build or make an project out of this DS.pdf paper

the report should minimum be atleast 7 to 8 pages
and the report shuold be in the format of prompts or explaining it to create a project kind of report

in depth anaylsis no token limit for the answer.

follow the instrucitions given



## Response:
11/1/2025, 3:22:59 AM

# EDGE-QI: Comprehensive Implementation Blueprint
## A Complete Project Development Guide

---

## Executive Summary

This document provides an exhaustive, production-ready implementation plan for building a full-stack simulation and visualization platform based on the EDGE-QI framework described in the research paper "EDGE-QI: An Energy and QoS-Aware Intelligent Edge Framework for Adaptive IoT Task Scheduling in Smart City Applications."

This is not merely a conceptual overview—this is a step-by-step guide that a development team can use to transform the academic paper into a functioning, demonstrable system. Every component, every algorithm, every edge case, and every visual element is detailed here.

**Project Goal**: Create a high-fidelity simulation environment that demonstrates all eight layers of the EDGE-QI architecture, implements both core algorithms (Multi-Constraint Adaptive Scheduling and Anomaly-Driven Data Transmission), showcases the distributed consensus protocol, and provides a professional, real-time dashboard for monitoring and controlling the entire system.

---

## Part 1: Technology Stack & Architecture Decisions

### 1.1 Front-End Technology Stack

**Framework: Next.js 14+ (App Router)**

*Reasoning*: Next.js provides server-side rendering capabilities, excellent performance optimization, and built-in API routes. The App Router architecture enables better code organization and streaming capabilities for real-time data.

**UI Component Library: Shadcn/UI + Radix UI**

*Reasoning*: Shadcn provides beautiful, accessible components that you own (not a dependency). Built on Radix UI primitives, ensuring accessibility compliance. Fully customizable with Tailwind CSS.

**Styling: Tailwind CSS v3+**

*Reasoning*: Utility-first CSS framework that enables rapid development while maintaining consistency. Perfect for responsive design and real-time dynamic styling based on system states.

**Real-Time Communication: Socket.IO Client**

*Reasoning*: Bidirectional, event-based communication perfect for real-time dashboard updates. Automatic reconnection, binary support, and multiplexing capabilities.

**State Management: Zustand + React Query (TanStack Query)**

*Reasoning*: Zustand for global client state (selected node, simulation controls). React Query for server state management with automatic caching, refetching, and optimistic updates.

**Map Visualization: Mapbox GL JS (via react-map-gl)**

*Reasoning*: High-performance vector map rendering with WebGL. Superior to Leaflet for data-intensive overlays. Supports custom markers, animations, and real-time updates.

**Charts & Visualizations: Recharts + D3.js**

*Reasoning*: Recharts for standard charts (gauges, line charts, bar charts). D3.js for custom visualizations like network topology graphs and consensus voting animations.

**Video/Image Display: Custom React Component with Canvas API**

*Reasoning*: Native canvas rendering for displaying processed video frames with bounding boxes. Better performance than img tags for rapid frame updates.

### 1.2 Back-End Technology Stack

**API Server: FastAPI (Python 3.11+)**

*Reasoning*: Asynchronous framework with automatic OpenAPI documentation. Native WebSocket support. Type hints enable better code quality and IDE support.

**Message Broker: Eclipse Mosquitto (MQTT Broker)**

*Reasoning*: Lightweight, standards-compliant MQTT broker perfect for IoT device communication. Supports QoS levels, retained messages, and last will testament.

**Edge Node Implementation: Python 3.11+ (Asyncio-based)**

*Reasoning*: Each edge node runs as an independent Python application. Asyncio enables concurrent task scheduling, network communication, and ML inference without threading complexity.

**ML Framework: PyTorch 2.0+ with TorchVision**

*Reasoning*: Industry-standard deep learning framework. Excellent model zoo with pre-trained weights. Native quantization support for creating low-power models as specified in the paper.

**Computer Vision: OpenCV-Python (cv2)**

*Reasoning*: Essential for video processing, frame manipulation, drawing bounding boxes, and image transformations.

**MQTT Client: paho-mqtt (Python)**

*Reasoning*: Official Eclipse Paho MQTT client. Stable, well-documented, supports all MQTT features needed for edge collaboration.

**Data Storage: PostgreSQL + TimescaleDB extension**

*Reasoning*: PostgreSQL for structured data (node configurations, task definitions). TimescaleDB extension for time-series data (metrics, logs, anomaly scores). Essential for historical data analysis.

**Caching Layer: Redis**

*Reasoning*: In-memory cache for real-time metrics, current node states, and consensus voting data. Pub/Sub capabilities for additional real-time messaging.

**Containerization: Docker + Docker Compose**

*Reasoning*: Each edge node must run in isolation to properly simulate distributed systems. Docker Compose orchestrates the entire stack (nodes, broker, databases, API server).

### 1.3 System Architecture Overview

**EDGE-QI System Architecture Diagram**

````jsx
import React from 'react';
import { Camera, Server, Database, Wifi, Activity, Box, Network } from 'lucide-react';

export default function ArchitectureDiagram() {
  return (
    <div className="w-full h-full bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8 overflow-auto">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">EDGE-QI System Architecture</h2>
        
        {/* Frontend Layer */}
        <div className="mb-8 p-6 bg-blue-900/30 rounded-lg border-2 border-blue-500">
          <div className="flex items-center gap-3 mb-4">
            <Activity className="w-8 h-8 text-blue-400" />
            <h3 className="text-xl font-bold text-blue-300">Frontend Layer (Next.js)</h3>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div className="p-4 bg-blue-800/40 rounded border border-blue-400">
              <p className="text-sm font-semibold text-blue-200">Map Dashboard</p>
              <p className="text-xs text-blue-300 mt-1">Mapbox GL JS</p>
            </div>
            <div className="p-4 bg-blue-800/40 rounded border border-blue-400">
              <p className="text-sm font-semibold text-blue-200">Node Monitors</p>
              <p className="text-xs text-blue-300 mt-1">Real-time Metrics</p>
            </div>
            <div className="p-4 bg-blue-800/40 rounded border border-blue-400">
              <p className="text-sm font-semibold text-blue-200">Sim Controls</p>
              <p className="text-xs text-blue-300 mt-1">Event Triggers</p>
            </div>
          </div>
        </div>

        {/* Communication Layer */}
        <div className="flex justify-center mb-8">
          <div className="flex items-center gap-4">
            <div className="h-12 w-1 bg-green-500"></div>
            <Wifi className="w-8 h-8 text-green-400 animate-pulse" />
            <span className="text-sm text-green-300">Socket.IO WebSocket</span>
          </div>
        </div>

        {/* Backend Layer */}
        <div className="mb-8 p-6 bg-purple-900/30 rounded-lg border-2 border-purple-500">
          <div className="flex items-center gap-3 mb-4">
            <Server className="w-8 h-8 text-purple-400" />
            <h3 className="text-xl font-bold text-purple-300">Backend Layer (FastAPI)</h3>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-purple-800/40 rounded border border-purple-400">
              <p className="text-sm font-semibold text-purple-200">API Gateway</p>
              <p className="text-xs text-purple-300 mt-1">REST + WebSocket</p>
            </div>
            <div className="p-4 bg-purple-800/40 rounded border border-purple-400">
              <p className="text-sm font-semibold text-purple-200">Orchestrator</p>
              <p className="text-xs text-purple-300 mt-1">Node Management</p>
            </div>
          </div>
        </div>

        {/* MQTT Broker */}
        <div className="flex justify-center mb-8">
          <div className="p-6 bg-orange-900/30 rounded-lg border-2 border-orange-500 w-64">
            <div className="flex items-center gap-3 mb-2">
              <Network className="w-8 h-8 text-orange-400" />
              <h3 className="text-lg font-bold text-orange-300">MQTT Broker</h3>
            </div>
            <p className="text-xs text-orange-300">Eclipse Mosquitto</p>
            <div className="mt-3 space-y-1 text-xs text-orange-200">
              <p>• Edge-to-Edge Communication</p>
              <p>• Consensus Protocol Transport</p>
              <p>• Event Broadcasting</p>
            </div>
          </div>
        </div>

        {/* Edge Nodes Layer */}
        <div className="mb-8 p-6 bg-green-900/30 rounded-lg border-2 border-green-500">
          <div className="flex items-center gap-3 mb-4">
            <Camera className="w-8 h-8 text-green-400" />
            <h3 className="text-xl font-bold text-green-300">Edge Nodes Layer (Docker Containers)</h3>
          </div>
          <div className="grid grid-cols-4 gap-3">
            {['Cam-1A', 'Cam-1B', 'Cam-2A', 'Cam-2B'].map((cam) => (
              <div key={cam} className="p-3 bg-green-800/40 rounded border border-green-400">
                <p className="text-sm font-semibold text-green-200 text-center">{cam}</p>
                <div className="mt-2 space-y-1 text-xs text-green-300">
                  <p>• Layer 3-7 Logic</p>
                  <p>• ML Pipeline</p>
                  <p>• Scheduler</p>
                  <p>• Consensus Client</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Data Layer */}
        <div className="p-6 bg-slate-700/30 rounded-lg border-2 border-slate-500">
          <div className="flex items-center gap-3 mb-4">
            <Database className="w-8 h-8 text-slate-400" />
            <h3 className="text-xl font-bold text-slate-300">Data Layer</h3>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div className="p-4 bg-slate-800/40 rounded border border-slate-400">
              <p className="text-sm font-semibold text-slate-200">PostgreSQL</p>
              <p className="text-xs text-slate-300 mt-1">Config + Metadata</p>
            </div>
            <div className="p-4 bg-slate-800/40 rounded border border-slate-400">
              <p className="text-sm font-semibold text-slate-200">TimescaleDB</p>
              <p className="text-xs text-slate-300 mt-1">Time-series Metrics</p>
            </div>
            <div className="p-4 bg-slate-800/40 rounded border border-slate-400">
              <p className="text-sm font-semibold text-slate-200">Redis</p>
              <p className="text-xs text-slate-300 mt-1">Real-time Cache</p>
            </div>
          </div>
        </div>

        {/* Legend */}
        <div className="mt-8 p-4 bg-slate-800/50 rounded-lg">
          <h4 className="text-sm font-bold text-white mb-3">Architecture Notes:</h4>
          <div className="grid grid-cols-2 gap-3 text-xs text-slate-300">
            <div>
              <p className="font-semibold text-slate-200 mb-1">Frontend → Backend:</p>
              <p>WebSocket for real-time bidirectional communication</p>
            </div>
            <div>
              <p className="font-semibold text-slate-200 mb-1">Edge Nodes → MQTT:</p>
              <p>Lightweight pub/sub for consensus and state sharing</p>
            </div>
            <div>
              <p className="font-semibold text-slate-200 mb-1">Backend → Edge Nodes:</p>
              <p>MQTT commands for simulation control</p>
            </div>
            <div>
              <p className="font-semibold text-slate-200 mb-1">Edge Nodes → Backend:</p>
              <p>MQTT telemetry published, backend subscribes and forwards</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
````

**Architecture Flow**:

1. **User Interaction**: User interacts with Next.js dashboard (clicks button to trigger low battery scenario)
2. **Frontend → Backend**: Socket.IO event sent to FastAPI server with command payload
3. **Backend Processing**: FastAPI validates command, publishes MQTT message to specific node topic
4. **MQTT Distribution**: Mosquitto broker routes message to subscribed edge node container
5. **Edge Node Processing**: Node receives command, updates internal state, executes algorithms
6. **Edge Node → MQTT**: Node publishes telemetry (metrics, logs, decisions) back to MQTT
7. **MQTT → Backend**: FastAPI subscribes to all node telemetry topics
8. **Backend → Frontend**: FastAPI forwards processed data via Socket.IO to dashboard
9. **Dashboard Update**: React components re-render with new data, visualizations update in real-time

---

## Part 2: Comprehensive File Structure

Here is the complete project structure with detailed explanations for each directory and key files:

```
EDGE-QI-Platform/
│
├── 📁 frontend/                          # Next.js 14+ application
│   ├── 📁 app/                           # App Router structure
│   │   ├── 📁 (dashboard)/               # Dashboard route group
│   │   │   ├── page.tsx                  # Main dashboard page
│   │   │   ├── layout.tsx                # Dashboard-specific layout
│   │   │   └── 📁 components/            # Dashboard-specific components
│   │   │       ├── MapView.tsx           # Mapbox interactive map
│   │   │       ├── NodeDetailPanel.tsx   # Selected node details
│   │   │       ├── GlobalMetrics.tsx     # System-wide statistics
│   │   │       ├── SimulationControls.tsx # Event trigger buttons
│   │   │       └── ConsensusVisualizer.tsx # BFT voting visualization
│   │   │
│   │   ├── 📁 nodes/[nodeId]/            # Dynamic route for node detail
│   │   │   └── page.tsx                  # Full-page node monitoring
│   │   │
│   │   ├── 📁 analytics/                 # Historical analysis pages
│   │   │   ├── page.tsx                  # Analytics dashboard
│   │   │   ├── energy/page.tsx           # Energy consumption analysis
│   │   │   ├── bandwidth/page.tsx        # Bandwidth usage analysis
│   │   │   └── anomalies/page.tsx        # Anomaly detection history
│   │   │
│   │   ├── 📁 api/                       # API routes (if needed for SSR)
│   │   │   └── test-connection/route.ts  # Health check endpoint
│   │   │
│   │   ├── layout.tsx                    # Root layout with providers
│   │   └── globals.css                   # Global styles + Tailwind imports
│   │
│   ├── 📁 components/                    # Shared React components
│   │   ├── 📁 ui/                        # Shadcn UI components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── gauge.tsx                 # Custom gauge for metrics
│   │   │   ├── badge.tsx
│   │   │   ├── tabs.tsx
│   │   │   └── ... (other Shadcn components)
│   │   │
│   │   ├── 📁 charts/                    # Chart components
│   │   │   ├── EnergyGauge.tsx           # Battery level visualization
│   │   │   ├── NetworkLatencyChart.tsx   # Real-time latency graph
│   │   │   ├── BandwidthChart.tsx        # Bandwidth usage over time
│   │   │   ├── TaskQueueChart.tsx        # Task queue visualization
│   │   │   └── AnomalyTimelineChart.tsx  # Anomaly detection timeline
│   │   │
│   │   ├── 📁 map/                       # Map-related components
│   │   │   ├── EdgeNodeMarker.tsx        # Custom map marker for nodes
│   │   │   ├── IntersectionOverlay.tsx   # Traffic light visualization
│   │   │   └── ConsensusLinkAnimation.tsx # Animated lines for node communication
│   │   │
│   │   ├── 📁 node/                      # Node-specific components
│   │   │   ├── LiveVideoFeed.tsx         # Displays MQTT video stream
│   │   │   ├── ConstraintStatus.tsx      # Energy/Network/Task indicators
│   │   │   ├── SchedulerStateTable.tsx   # Algorithm 1 task queue table
│   │   │   ├── TransmissionLog.tsx       # Algorithm 2 decision log
│   │   │   ├── MLModelIndicator.tsx      # Shows full vs quantized model
│   │   │   └── ConsensusStatusCard.tsx   # Node's role in consensus
│   │   │
│   │   └── 📁 layout/                    # Layout components
│   │       ├── Navbar.tsx                # Top navigation
│   │       ├── Sidebar.tsx               # Side navigation (if needed)
│   │       └── StatusBar.tsx             # Global system status
│   │
│   ├── 📁 lib/                           # Utility functions and services
│   │   ├── socket-client.ts              # Socket.IO client singleton
│   │   ├── api-client.ts                 # Axios/Fetch wrapper for REST
│   │   ├── 📁 stores/                    # Zustand stores
│   │   │   ├── simulation-store.ts       # Simulation control state
│   │   │   ├── nodes-store.ts            # Node data cache
│   │   │   └── ui-store.ts               # UI preferences
│   │   │
│   │   └── 📁 utils/                     # Helper functions
│   │       ├── format-metrics.ts         # Format numbers, units
│   │       ├── color-helpers.ts          # State → color mapping
│   │       └── date-helpers.ts           # Timestamp formatting
│   │
│   ├── 📁 hooks/                         # Custom React hooks
│   │   ├── useSocket.ts                  # Socket.IO connection hook
│   │   ├── useNodeData.ts                # Real-time node data hook
│   │   ├── useSimulationControl.ts       # Control hook for events
│   │   └── useConsensusState.ts          # Consensus protocol state
│   │
│   ├── 📁 types/                         # TypeScript type definitions
│   │   ├── node.types.ts                 # Edge node data structures
│   │   ├── metrics.types.ts              # Metric types
│   │   ├── events.types.ts               # Socket.IO event types
│   │   └── algorithm.types.ts            # Algorithm input/output types
│   │
│   ├── 📄 package.json
│   ├── 📄 tsconfig.json
│   ├── 📄 tailwind.config.js
│   ├── 📄 next.config.js
│   └── 📄 .env.local                     # Environment variables
│
│
├── 📁 backend/                           # FastAPI application
│   ├── 📁 app/
│   │   ├── 📄 main.py                    # FastAPI app entry point
│   │   │
│   │   ├── 📁 api/                       # API endpoints
│   │   │   ├── 📁 v1/
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   ├── 📄 nodes.py           # Node management endpoints
│   │   │   │   ├── 📄 simulation.py      # Simulation control endpoints
│   │   │   │   ├── 📄 metrics.py         # Metrics query endpoints
│   │   │   │   ├── 📄 analytics.py       # Historical data endpoints
│   │   │   │   └── 📄 websocket.py       # WebSocket handler
│   │   │   │
│   │   │   └── 📄 router.py              # API router aggregator
│   │   │
│   │   ├── 📁 services/                  # Business logic layer
│   │   │   ├── 📄 mqtt_service.py        # MQTT pub/sub management
│   │   │   ├── 📄 orchestrator.py        # Node orchestration logic
│   │   │   ├── 📄 telemetry_processor.py # Process node telemetry
│   │   │   ├── 📄 event_dispatcher.py    # Dispatch commands to nodes
│   │   │   └── 📄 consensus_tracker.py   # Track consensus voting
│   │   │
│   │   ├── 📁 models/                    # Pydantic models
│   │   │   ├── 📄 node.py                # Node configuration model
│   │   │   ├── 📄 metrics.py             # Metrics data model
│   │   │   ├── 📄 task.py                # Task model
│   │   │   ├── 📄 event.py               # Simulation event model
│   │   │   └── 📄 consensus.py           # Consensus state model
│   │   │
│   │   ├── 📁 db/                        # Database layer
│   │   │   ├── 📄 postgres.py            # PostgreSQL connection
│   │   │   ├── 📄 timescale.py           # TimescaleDB queries
│   │   │   ├── 📄 redis_client.py        # Redis connection
│   │   │   └── 📁 queries/               # SQL query builders
│   │   │       ├── 📄 nodes.sql
│   │   │       ├── 📄 metrics.sql
│   │   │       └── 📄 anomalies.sql
│   │   │
│   │   ├── 📁 core/                      # Core utilities
│   │   │   ├── 📄 config.py              # Configuration management
│   │   │   ├── 📄 logging.py             # Logging setup
│   │   │   └── 📄 security.py            # Security utilities (if needed)
│   │   │
│   │   └── 📁 schemas/                   # Response schemas
│   │       ├── 📄 node_response.py
│   │       ├── 📄 metrics_response.py
│   │       └── 📄 error_response.py
│   │
│   ├── 📄 requirements.txt               # Python dependencies
│   ├── 📄 Dockerfile                     # Backend container
│   └── 📄 .env                           # Environment variables
│
│
├── 📁 edge_nodes/                        # Edge node implementation
│   ├── 📄 node_main.py                   # Entry point for each node
│   │
│   ├── 📁 layers/                        # EDGE-QI layers implementation
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📄 layer_1_input.py           # Layer 1: Input Source
│   │   │   # VideoCapture, frame reading, dataset loading
│   │   │
│   │   ├── 📄 layer_2_processing.py      # Layer 2: Data Processing
│   │   │   # Frame validation, corruption detection, normalization
│   │   │
│   │   ├── 📄 layer_3_ml.py              # Layer 3: ML Intelligence
│   │   │   # YOLO inference, bounding boxes, queue calculation
│   │   │   # Model switching (full vs quantized)
│   │   │
│   │   ├── 📄 layer_4_core.py            # Layer 4: Core Processing
│   │   │   # Multi-Constraint Scheduler (Algorithm 1)
│   │   │   # Energy monitor, network monitor
│   │   │
│   │   ├── 📄 layer_5_collaboration.py   # Layer 5: Edge Collaboration
│   │   │   # BFT Consensus Protocol
│   │   │   # State broadcasting, voting mechanism
│   │   │
│   │   ├── 📄 layer_6_bandwidth.py       # Layer 6: Bandwidth Optimization
│   │   │   # Anomaly-Driven Transmission (Algorithm 2)
│   │   │   # Adaptive streaming logic
│   │   │
│   │   └── 📄 layer_7_external.py        # Layer 7: External Systems
│   │       # Traffic light control API integration
│   │
│   ├── 📁 algorithms/                    # Core algorithms from paper
│   │   ├── 📄 __init__.py
│   │   ├── 📄 algorithm_1_scheduler.py   # Algorithm 1 implementation
│   │   ├── 📄 algorithm_2_transmission.py # Algorithm 2 implementation
│   │   └── 📄 consensus_bft.py           # BFT consensus implementation
│   │
│   ├── 📁 ml/                            # Machine Learning components
│   │   ├── 📄 yolo_detector.py           # YOLOv8 wrapper
│   │   ├── 📄 model_manager.py           # Model loading and switching
│   │   ├── 📄 anomaly_detector.py        # Statistical + ML anomaly detection
│   │   └── 📄 metrics_calculator.py      # Queue length, speed, etc.
│   │
│   ├── 📁 monitors/                      # System monitors for Algorithm 1
│   │   ├── 📄 energy_monitor.py          # Battery simulation
│   │   ├── 📄 network_monitor.py         # Latency/bandwidth simulation
│   │   └── 📄 task_monitor.py            # Task queue management
│   │
│   ├── 📁 comms/                         # Communication modules
│   │   ├── 📄 mqtt_client.py             # MQTT pub/sub client
│   │   └── 📄 message_protocol.py        # Message format definitions
│   │
│   ├── 📁 config/                        # Configuration
│   │   ├── 📄 node_config.py             # Node-specific config
│   │   └── 📄 thresholds.py              # E.threshold, N.threshold, etc.
│   │
│   ├── 📁 utils/                         # Utilities
│   │   ├── 📄 logger.py                  # Logging utilities
│   │   ├── 📄 video_utils.py             # Video processing helpers
│   │   └── 📄 state_manager.py           # Node state persistence
│   │
│   ├── 📄 requirements.txt               # Python dependencies
│   └── 📄 Dockerfile                     # Node container template
│
│
├── 📁 datasets/                          # Training and testing data
│   ├── 📁 VisDrone2019-DET-train/        # Main dataset
│   │   ├── 📁 images/
│   │   ├── 📁 annotations/
│   │   └── 📄 README.txt
│   │
│   ├── 📁 video_feeds/                   # Video files for simulation
│   │   ├── intersection_1_ns.mp4
│   │   ├── intersection_1_ew.mp4
│   │   ├── intersection_2_ns.mp4
│   │   ├── intersection_2_ew.mp4
│   │   └── intersection_3.mp4
│   │
│   └── 📁 historical_data/               # For D_history in Algorithm 2
│       ├── queue_averages.json           # Historical queue data
│       └── traffic_patterns.csv          # Traffic pattern data
│
│
├── 📁 models/                            # Pre-trained ML models
│   ├── 📄 yolov8n.pt                     # Full-precision YOLOv8 Nano
│   ├── 📄 yolov8n_quantized.tflite       # Quantized version
│   ├── 📄 isolation_forest.pkl           # Trained anomaly detector
│   └── 📄 model_metadata.json            # Model versioning info
│
│
├── 📁 docker/                            # Docker configuration
│   ├── 📄 docker-compose.yml             # Full stack orchestration
│   ├── 📄 docker-compose.dev.yml         # Development overrides
│   ├── 📄 .env.example                   # Environment template
│   │
│   ├── 📁 mosquitto/                     # MQTT broker config
│   │   └── 📄 mosquitto.conf
│   │
│   ├── 📁 postgres/                      # PostgreSQL initialization
│   │   ├── 📄 init.sql                   # Schema creation
│   │   └── 📄 seed.sql                   # Sample data
│   │
│   └── 📁 redis/
│       └── 📄 redis.conf
│
│
├── 📁 tests/                             # Testing suite
│   ├── 📁 unit/                          # Unit tests
│   │   ├── test_algorithm_1.py
│   │   ├── test_algorithm_2.py
│   │   ├── test_consensus.py
│   │   └── test_ml_pipeline.py
│   │
│   ├── 📁 integration/                   # Integration tests
│   │   ├── test_node_lifecycle.py
│   │   ├── test_mqtt_communication.py
│   │   └── test_dashboard_updates.py
│   │
│   └── 📁 e2e/                           # End-to-end scenarios
│       ├── test_scenario_1_low_energy.py
│       ├── test_scenario_2_network_congestion.py
│       ├── test_scenario_3_anomaly_filtering.py
│       └── test_scenario_4_consensus.py
│
│
├── 📁 docs/                              # Documentation
│   ├── 📄 ARCHITECTURE.md                # System architecture details
│   ├── 📄 API_REFERENCE.md               # Backend API documentation
│   ├── 📄 ALGORITHMS.md                  # Algorithm explanations
│   ├── 📄 DEPLOYMENT.md                  # Deployment instructions
│   ├── 📄 DATASET_GUIDE.md               # Dataset usage guide
│   ├── 📄 SCENARIOS.md                   # Test scenario documentation
│   └── 📁 images/                        # Documentation images
│
│
├── 📁 scripts/                           # Utility scripts
│   ├── 📄 setup.sh                       # Initial setup script
│   ├── 📄 download_dataset.py            # Download VisDrone dataset
│   ├── 📄 prepare_models.py              # Download and quantize YOLO
│   ├── 📄 generate_historical_data.py    # Create D_history data
│   ├── 📄 start_simulation.sh            # Launch all containers
│   └── 📄 run_scenario.py                # Execute specific test scenario
│
│
├── 📄 README.md                          # Project overview
├── 📄 LICENSE
├── 📄 .gitignore
└── 📄 CONTRIBUTING.md
```

---

## Part 3: Dataset Selection and Preparation

### 3.1 Primary Dataset: VisDrone2019-DET

**Why VisDrone?**

The EDGE-QI paper focuses on smart city traffic monitoring with cameras overlooking intersections. The VisDrone dataset is perfect because:

1. **Aerial/Elevated Perspective**: Captured from drones, mimicking the elevated camera viewpoint typical of traffic monitoring systems
2. **Dense Traffic Scenes**: Contains crowded intersections with multiple vehicles, exactly what the queue detection system needs
3. **Pre-Annotated Bounding Boxes**: Comes with detailed annotations for vehicles, saving significant manual labeling effort
4. **Variety of Scenarios**: Includes different weather conditions, times of day, and traffic densities
5. **Large Scale**: Over 10,000 images in the training set provides ample data for validation

**Dataset Specifications**:
- **Source**: VisDrone2019-DET (Detection Track)
- **Download Link**: http://aiskyeye.com/download/object-detection-2/
- **Size**: ~3.5 GB (images + annotations)
- **Format**: Images (.jpg) + Annotations (.txt in YOLO format)
- **Classes**: Includes 'car', 'van', 'bus', 'truck' categories essential for traffic analysis

### 3.2 Video Dataset Preparation

For simulation purposes, you need continuous video streams, not just static images. Here's the strategy:

**Option 1: Public Traffic Camera Datasets**
- **UA-DETRAC**: Dataset specifically for traffic monitoring with full videos
  - Source: https://detrac-db.rit.albany.edu/
  - 10 hours of traffic video from 24 locations in Beijing and Tianjin
  - Perfect for continuous stream simulation

**Option 2: Synthesize Videos from VisDrone**
Create synthetic video sequences by:
1. Taking sequential frames from VisDrone and stitching them into video files
2. Using OpenCV to create time-lapse style videos
3. Adding realistic motion blur and temporal consistency

**Implementation Script** (`scripts/prepare_video_datasets.py`):
```python
# This script will:
# 1. Download UA-DETRAC or process VisDrone sequences
# 2. Extract 5-10 minute clips for each intersection
# 3. Standardize to 1920x1080 at 30fps
# 4. Organize by intersection and viewing angle
```

### 3.3 Historical Data Generation for Algorithm 2

Algorithm 2 requires historical data (D_history) to calculate anomaly scores. You must generate synthetic historical traffic patterns.

**Generate `datasets/historical_data/queue_averages.json`**:

This file stores average queue lengths for each 15-minute block of each day of the week:

```json
{
  "intersection_1": {
    "monday": {
      "00:00": { "mean": 0.5, "std_dev": 0.3, "samples": 120 },
      "00:15": { "mean": 0.3, "std_dev": 0.2, "samples": 120 },
      ...
      "08:00": { "mean": 18.2, "std_dev": 4.1, "samples": 120 },
      "08:15": { "mean": 22.5, "std_dev": 3.8, "samples": 120 },
      ...
    },
    "tuesday": { ... },
    ...
  },
  "intersection_2": { ... },
  "intersection_3": { ... }
}
```

**Generation Strategy**:
1. Model realistic traffic patterns (morning rush: 7-9 AM, evening rush: 5-7 PM)
2. Add day-of-week variations (weekends are lighter)
3. Include seasonal patterns if desired
4. Use Gaussian distributions to add natural variance

**Script**: `scripts/generate_historical_data.py` will create this file with 672 time blocks (96 per day × 7 days) for each intersection.

---

## Part 4: Frontend Implementation - Complete UI Specification

### 4.1 Page Structure and Navigation

The dashboard consists of **4 primary pages**:

#### **Page 1: Live Dashboard (Main Page)** - `/dashboard`

**Layout**: Three-panel layout optimized for 1920x1080 and above

**Left Panel (30% width)**: Global Map View
- **Component**: Mapbox GL JS map centered on simulated city area
- **Map Style**: Dark theme (mapbox://styles/mapbox/dark-v11) to reduce eye strain in control room
- **Overlays**:
  - 3-4 intersection markers at fixed coordinates
  - Each marker shows node status with color coding:
    - 🟢 Green: All systems nominal
    - 🟡 Yellow: Warning state (low battery 20-40%, network latency 200-500ms)
    - 🟠 Orange: Degraded state (low battery 10-20%, network latency 500-800ms)
    - 🔴 Red: Critical state (battery <10%, network timeout, critical anomaly detected)
  - Animated lines between nodes during consensus voting (pulsing line from node to node)
  - Traffic light status icons (green/yellow/red circles) at each intersection
- **Interactions**:
  - Click node → select that node (highlight and load data into center panel)
  - Hover node → tooltip with basic stats (battery %, last update time)
  - Double-click intersection → zoom to that intersection

**Center Panel (50% width)**: Node Detail View
- **Top Bar**: Selected node identifier ("Cam-1A") with status badge
- **Video Feed Section**:
  - Canvas element displaying latest processed frame from node
  - Overlaid bounding boxes drawn in real-time (green for detected vehicles)
  - Status overlay (top-right corner of video):
    ```
    MODEL: yolov8n (Full Precision)  [or "yolov8n (Quantized)"]
    STREAM: HIGH (3 Mbps)            [or "LOW (500 kbps)" or "PAUSED"]
    FPS: 28
    ```
  - Timestamp overlay (bottom-left): Last frame time
- **Constraint Gauges Section** (below video):
  - Three semi-circular gauges in a row:
    - **Energy Gauge**: 0-100%, color gradient (red<20%, yellow 20-40%, green>40%)
      - Shows "CHARGING" animation if battery is increasing
    - **Network Latency Gauge**: 0-1000ms, (green<100ms, yellow 100-300ms, red>300ms)
    - **Network Bandwidth Gauge**: 0-50 Mbps, (red<1Mbps, yellow 1-5Mbps, green>5Mbps)
- **Scheduler State Table**:
  - Live-updating table showing current task queue (Algorithm 1 visualization)
  - Columns: [Task ID | Priority | Status | Action Taken | Timestamp]
  - Row colors: Critical=red, High=orange, Medium=yellow, Low=green
  - Status values: "Running", "Running (Reduced)", "Queued", "Deferred (Energy)", "Deferred (Network)"
  - Auto-scrolls to show most recent task at top
- **Transmission Log**:
  - Terminal-style scrolling log (Algorithm 2 visualization)
  - Each entry format:
    ```
    [15:42:31] Queue: 8 cars | Avg: 7.2 | Z-Score: 0.31 | Decision: DISCARD
    [15:42:46] Queue: 24 cars | Avg: 7.2 | Z-Score: 3.8 | Decision: TRANSMIT (HIGH)
    ```
  - Color coding: DISCARD=gray, TRANSMIT=green, HIGH_PRIORITY=red

**Right Panel (20% width)**: Simulation Controls & System Metrics
- **Simulation Controls Card**:
  - Header: "Event Simulator" with node selector dropdown
  - Button groups:
    - **Energy Events**: "Low Battery (15%)", "Critical Battery (5%)", "Start Charging", "Full Battery"
    - **Network Events**: "High Latency (800ms)", "Low Bandwidth (500kbps)", "Network Timeout", "Restore Network"
    - **Traffic Events**: "Heavy Traffic", "Accident", "Emergency Vehicle", "Clear Road"
    - **System Events**: "Stop All Nodes", "Restart All Nodes"
  - Each button click triggers immediate visual feedback (button color change + confirmation toast)
  
- **Global System Metrics Card**:
  - **Total Energy Saved**: Line chart showing cumulative energy savings vs. baseline (updated every 5 seconds)
  - **Total Bandwidth Saved**: Stacked area chart showing bandwidth saved through anomaly filtering
  - **Active Consensus Sessions**: Counter badge showing ongoing BFT voting
  - **System Uptime**: Timer showing elapsed simulation time

#### **Page 2: Node Detail Page** - `/nodes/[nodeId]`

**Purpose**: Full-screen view for monitoring a single node in detail

**Layout**: Single scrollable page with sections

**Section 1: Hero Section**
- Large node identifier with status badge
- Quick stats cards (4 cards in a row):
  - Total frames processed
  - Anomalies detected
  - Tasks completed
  - Consensus votes participated

**Section 2: Live Metrics Grid**
- **Column 1**: Live video feed (larger than dashboard version)
- **Column 2**: Three-column charts
  - Energy consumption over time (line chart, last 5 minutes)
  - Network latency over time (line chart, last 5 minutes)
  - Bandwidth usage over time (area chart, last 5 minutes)

**Section 3: Algorithm Visualizations**
- **Tab 1: Multi-Constraint Scheduler (Algorithm 1)**
  - Flow diagram showing decision tree
  - Current values highlighted (e.g., "E.energy_level = 18% < E.threshold ✓")
  - Decision output shown in large badge
- **Tab 2: Anomaly Transmission (Algorithm 2)**
  - Dual chart:
    - Top: Current queue vs. historical average (bar chart)
    - Bottom: Z-score calculation visualization (normal distribution curve with current value marker)
  - Decision output: "TRANSMIT" or "DISCARD" with reasoning text

**Section 4: Detailed Logs**
- Full event log with filtering (by priority, by algorithm, by timestamp)
- Export to CSV button

#### **Page 3: Analytics Dashboard** - `/analytics`

**Purpose**: Historical analysis and pattern identification

**Layout**: Multi-chart dashboard

**Chart 1: Energy Consumption Analysis**
- Dual Y-axis line chart:
  - Y1: Average battery level for all nodes over last 24 hours
  - Y2: Number of "low energy" events
- Comparison: "Energy-aware scheduling" vs. "Baseline (always full-precision model)"
  - Paper claims 28.4% energy savings

**Chart 2: Bandwidth Usage Analysis**
- Stacked area chart showing:
  - Blue area: Bandwidth consumed by transmitted data
  - Gray area: Bandwidth saved by DISCARD decisions (Algorithm 2)
- Total savings percentage badge
  - Paper claims 74.5% bandwidth reduction

**Chart 3: Task Completion Analysis**
- Grouped bar chart:
  - X-axis: Task priority levels (Critical, High, Medium, Low)
  - Bars: "Completed on time" vs. "Deferred" vs. "Failed"
- Shows effectiveness of priority-based scheduling

**Chart 4: Anomaly Detection Heatmap**
- Calendar-style heatmap showing anomaly frequency
- Each cell = 1 hour block
- Color intensity = number of anomalies detected
- Click cell → drill down to specific anomalies

**Chart 5: Consensus Performance**
- Timeline visualization showing:
  - Duration of each consensus session
  - Number of nodes participating
  - Consensus outcome (agreed/failed)
- Average consensus time metric

**Chart 6: Response Time Analysis**
- Histogram distribution:
  - Paper shows EDGE-QI maintains sub-250ms response times
  - Compare against baseline (400-800ms)
- 95th percentile, 99th percentile markers

#### **Page 4: System Configuration** - `/config`

**Purpose**: Configure thresholds and system parameters

**Section 1: Energy Thresholds**
-



## Prompt:
11/1/2025, 3:23:25 AM

Continue



## Response:
11/1/2025, 3:25:51 AM

**Section 1: Energy Thresholds**
- Slider inputs with live preview:
  - `E.threshold` (default: 20%) - "Low energy threshold for Algorithm 1"
  - `E.critical` (default: 10%) - "Critical battery level"
  - `E.charging_rate` (default: 5%/min) - "Simulated charging speed"
- Visual indicator showing current threshold on energy gauge
- "Reset to Paper Defaults" button

**Section 2: Network Thresholds**
- Slider inputs:
  - `N.threshold_latency` (default: 200ms) - "High latency threshold"
  - `N.threshold_bandwidth` (default: 1 Mbps) - "Minimum bandwidth threshold"
- Network tier configuration table (editable):
  | Tier | Bitrate | Resolution | Use Case |
  |------|---------|------------|----------|
  | Ultra-Low | 150 kbps | 320x240 | Emergency only |
  | Low | 500 kbps | 640x480 | Network congestion |
  | Medium | 1.5 Mbps | 1280x720 | Normal operation |
  | High | 3 Mbps | 1920x1080 | Good network |
  | Ultra-High | 6 Mbps | 1920x1080 | Optimal conditions |

**Section 3: Anomaly Detection Parameters**
- **Statistical Anomaly (Z-Score)**:
  - `theta_critical` (default: 3.0 standard deviations) - "Critical anomaly threshold"
  - `theta_high` (default: 2.5) - "High priority threshold"
  - `theta_medium` (default: 2.0) - "Medium priority threshold"
  - `theta_low` (default: 1.5) - "Low priority threshold"
- **ML Anomaly (Isolation Forest)**:
  - `contamination` (default: 0.1) - "Expected anomaly proportion"
  - `n_estimators` (default: 100) - "Number of trees"
- Visual preview: Mock data with current thresholds overlaid

**Section 4: Consensus Protocol**
- Byzantine Fault Tolerance settings:
  - `f_tolerance` (default: 1) - "Maximum faulty nodes tolerated (f = (n-1)/3)"
  - `consensus_timeout` (default: 5000ms) - "Voting timeout"
  - `quorum_percentage` (default: 67%) - "Minimum agreement percentage"
- Node participation configuration:
  - Checkboxes to enable/disable each node from consensus
  - Warning: "Need at least 3f+1 nodes for BFT consensus"

**Section 5: Task Priorities**
- Drag-and-drop priority editor:
  - List of task types (e.g., "Anomaly Detection", "Queue Calculation", "Speed Estimation", "Video Upload")
  - Drag to reorder by priority
  - Assign CRITICAL, HIGH, MEDIUM, LOW badges
- "requires_network" toggle for each task

**Section 6: Simulation Settings**
- Simulation speed multiplier (0.5x to 10x real-time)
- Random event injection:
  - Enable/disable automatic event generation
  - Event frequency slider (events per minute)
  - Event type probabilities (battery drain, network spike, traffic surge)

**Save Button**: "Apply Configuration" (distributes new config to all edge nodes via MQTT)

---

### 4.2 Component-Level UI Specifications

#### **Component: Live Video Feed (Center Panel)**

**Visual Design**:
- **Aspect Ratio**: 16:9 locked
- **Dimensions**: Responsive, max 800x450px on dashboard, 1200x675px on node detail page
- **Border**: 2px solid color that matches node status (green/yellow/orange/red)
- **Background**: Black (#000000) when no stream active
- **Loading State**: Skeleton animation with "Connecting to Cam-1A..." text

**Video Processing Pipeline** (this is what the backend sends):
1. Edge node processes video frame with YOLO
2. OpenCV draws bounding boxes on frame
3. Frame compressed to JPEG (quality based on adaptive streaming tier)
4. JPEG encoded to base64 string
5. Published to MQTT topic: `edge-qi/nodes/{node_id}/video`
6. Backend subscribes, forwards to frontend via Socket.IO event: `video_frame`
7. Frontend decodes base64, displays on canvas

**Overlay Elements**:
- **Top-Left**: Node identifier badge with pulsing dot animation when active
- **Top-Right**: Status overlay card (semi-transparent dark background):
  ```
  MODEL: yolov8n (Full) ✓
  STREAM: HIGH (3 Mbps)
  FPS: 28 | QUEUE: 12
  ```
- **Bottom-Left**: Timestamp in format "15:42:31.245"
- **Bottom-Right**: ML metrics:
  ```
  DETECTIONS: 12 vehicles
  AVG SPEED: 15 mph
  ```

**Interaction**:
- Click video → full-screen mode
- Right-click → context menu: "Save Frame", "Copy Metrics", "Report Issue"

**Edge Case Handling**:
- **No stream active (Algorithm 2 DISCARD decision)**: Show static last frame with overlay "STREAM PAUSED (No Anomaly)"
- **Node offline**: Gray out video, show "Node Offline - Last seen: 2m ago"
- **Low bandwidth mode**: Add "pixelated" effect overlay to visually indicate degraded quality
- **Model switching**: Brief flash animation when switching from full to quantized model

#### **Component: Constraint Status Gauges**

**Implementation**: Three Recharts RadialBarChart components

**Energy Gauge Design**:
- **Range**: 0-100%
- **Color Gradient**:
  - 0-10%: Bright red (#DC2626) with pulsing animation
  - 10-20%: Red (#EF4444)
  - 20-40%: Yellow (#FBBF24)
  - 40-60%: Light green (#84CC16)
  - 60-100%: Green (#22C55E)
- **Center Display**: Large percentage number + "BATTERY" label
- **Charging Indicator**: When battery is increasing, show lightning bolt icon with upward animation
- **Critical State**: When <10%, add red glow effect and sound alert (optional)

**Network Latency Gauge Design**:
- **Range**: 0-1000ms (reverse scale: lower is better)
- **Color Logic**:
  - 0-100ms: Green (excellent)
  - 100-300ms: Yellow (acceptable)
  - 300-500ms: Orange (degraded)
  - 500-1000ms: Red (poor)
- **Center Display**: Latency value + "ms" + "LATENCY" label
- **Trend Indicator**: Small arrow showing if latency is increasing/decreasing

**Network Bandwidth Gauge Design**:
- **Range**: 0-50 Mbps
- **Color Logic**:
  - 0-1 Mbps: Red (insufficient)
  - 1-5 Mbps: Yellow (limited)
  - 5-20 Mbps: Light green (good)
  - 20-50 Mbps: Green (excellent)
- **Center Display**: Bandwidth + "Mbps" + "BANDWIDTH" label
- **Usage Bar**: Thin bar below gauge showing current usage vs. available

**Real-Time Update**:
- Gauges update every 1 second via Socket.IO event: `node_metrics_update`
- Smooth animation transitions (500ms ease-in-out)
- Threshold markers drawn as subtle lines on gauge arc

#### **Component: Scheduler State Table (Algorithm 1 Visualization)**

**Table Structure**:
```
| Task ID    | Priority  | Status              | Details                    | Timestamp   | Actions |
|------------|-----------|---------------------|----------------------------|-------------|---------|
| task_00142 | CRITICAL  | Running (Reduced)   | Anomaly Detection - 15% bat| 15:42:31    | [View]  |
| task_00141 | HIGH      | Queued             | Calculate queue length      | 15:42:30    | [View]  |
| task_00140 | MEDIUM    | Deferred (Network) | Upload 1-min summary        | 15:42:25    | [Retry] |
| task_00139 | LOW       | Completed          | Statistical analysis        | 15:42:20    | [View]  |
```

**Visual Design**:
- **Priority Badge Colors**:
  - CRITICAL: Red badge with white text, bold
  - HIGH: Orange badge
  - MEDIUM: Yellow badge with dark text
  - LOW: Green badge
- **Status Colors**:
  - Running: Blue text with spinner icon
  - Running (Reduced): Blue text with "⚡" icon (low-power mode)
  - Queued: Gray text with clock icon
  - Deferred: Orange text with pause icon
  - Completed: Green text with checkmark
  - Failed: Red text with X icon

**Row Highlighting**:
- New row insertion: Green flash animation (500ms)
- Status change: Yellow pulse animation
- Critical tasks: Subtle red glow on left border

**Details Column Content**:
- Shows the Algorithm 1 decision logic output:
  - "Anomaly Detection - 15% battery" (indicates low energy triggered reduced processing)
  - "Deferred due to network latency: 850ms > 200ms threshold"
  - "Priority override - CRITICAL task executed despite constraints"

**Sorting & Filtering**:
- Default sort: Timestamp descending (newest first)
- Filter dropdown: "All", "Running", "Queued", "Deferred", "Completed", "By Priority"
- Search box: Filter by task ID or details text

**Pagination**:
- Show 10 tasks per page
- Auto-scroll to top when new critical task arrives

**Real-Time Updates**:
- Socket.IO event: `task_queue_update` (emitted when task status changes)
- Optimistic UI updates: Change status immediately, rollback if confirmation not received in 3s

#### **Component: Transmission Log (Algorithm 2 Visualization)**

**Visual Design**: Terminal-style scrolling log

**Log Entry Format**:
```
[15:42:31] DATA: queue=8 cars, speed=15mph | HISTORY: avg=7.2, std=2.1 | 
           ANOMALY: z-score=0.31, ml-score=0.15 | DECISION: DISCARD (Redundant)

[15:42:46] DATA: queue=24 cars, speed=5mph | HISTORY: avg=7.2, std=2.1 | 
           ANOMALY: z-score=3.8, ml-score=0.89 | DECISION: TRANSMIT (HIGH_PRIORITY)
           REASON: Z-score exceeds critical threshold (3.8 > 3.0)
```

**Color Coding**:
- Timestamp: Dim gray
- DATA: White
- HISTORY: Light blue
- ANOMALY: Yellow
- DECISION:
  - DISCARD: Gray
  - TRANSMIT (NORMAL): Green
  - TRANSMIT (HIGH_PRIORITY): Bright red, bold

**Icons**:
- DISCARD: ❌ (red X)
- TRANSMIT: ✅ (green checkmark)
- HIGH_PRIORITY: ⚠️ (warning triangle)

**Filtering Controls** (above log):
- Buttons: "All", "Transmit Only", "Discard Only", "High Priority Only"
- Time range selector: "Last 5 min", "Last hour", "Custom range"

**Scroll Behavior**:
- Auto-scroll to bottom when new entry arrives (unless user has scrolled up)
- "Jump to Latest" button appears when user scrolls up
- Max entries displayed: 100 (older entries archived to database, accessible via "Load More")

**Export Function**:
- "Export Log" button → downloads CSV with all entries for selected time range

**Real-Time Updates**:
- Socket.IO event: `transmission_decision` (emitted after Algorithm 2 runs)
- Entries appear with fade-in animation

#### **Component: Consensus Visualizer**

**Purpose**: Visualize the BFT consensus protocol (Layer 5: Edge Collaboration)

**Visual Design**: Interactive network graph

**Graph Structure**:
- **Nodes**: Circles representing each edge device
  - Diameter: 60px
  - Color: Matches node status
  - Label: Node ID (e.g., "Cam-1A")
  - Inner icon: Camera icon
- **Edges**: Lines connecting nodes during voting
  - Animated dashed lines during active consensus
  - Solid lines after consensus reached
  - Color: Green for agreement votes, red for disagreement

**Consensus Phases Visualization**:

1. **Phase 1: Proposal**
   - One node (proposer) glows bright blue
   - Sends message to all other nodes (animated arrows flowing out)
   - Status text: "Cam-1A proposes: 'Change intersection-1 light to green'"

2. **Phase 2: Pre-Prepare**
   - All nodes receive proposal (arrows reach nodes, nodes flash white)
   - Status text: "Nodes validating proposal..."

3. **Phase 3: Prepare**
   - Nodes broadcast prepare messages to each other
   - Full mesh of animated lines between all nodes
   - Vote counter appears: "Prepare Votes: 3/4"

4. **Phase 4: Commit**
   - Nodes that agree send commit messages
   - Green checkmarks appear on agreeing nodes
   - Vote counter: "Commit Votes: 4/4"

5. **Phase 5: Reply**
   - All nodes execute the decision
   - All nodes flash green
   - Status text: "CONSENSUS REACHED: Change light to green"
   - Timestamp and decision logged

**Failed Consensus Handling**:
- If votes don't reach quorum: All nodes flash red
- Status text: "CONSENSUS FAILED: Insufficient votes (2/4, need 3)"
- Retry indicator: "Retry in 3s..."

**Info Panel** (right side of visualizer):
- **Current Session**: Session ID, proposer, proposal content
- **Voting Progress**: Progress bar showing vote collection
- **Participants**: List of nodes with their vote status:
  ```
  ✅ Cam-1A (Proposer) - AGREE
  ✅ Cam-1B - AGREE
  ✅ Cam-2A - AGREE
  ⏳ Cam-2B - PENDING
  ```
- **History**: Last 5 consensus sessions with outcomes

**Real-Time Updates**:
- Socket.IO events:
  - `consensus_started` - Initiate visualization
  - `consensus_vote` - Update individual vote
  - `consensus_complete` - Show final result

**Interaction**:
- Click node → show node's consensus history
- Hover edge → tooltip showing message content
- Click session in history → replay that consensus session

---

### 4.3 Map View Detailed Specification

**Map Configuration**:
- **Library**: Mapbox GL JS via react-map-gl
- **Style**: `mapbox://styles/mapbox/dark-v11`
- **Initial View**: 
  - Center: Coordinates of simulated city center (e.g., `[77.5946, 12.9716]` for Bangalore)
  - Zoom: 14 (neighborhood level)
- **Controls**:
  - Navigation controls (zoom in/out, compass)
  - Scale bar (bottom-left)
  - Disable rotation (locked to north-up)

**Intersection Placement** (example for 3 intersections):
```javascript
const intersections = [
  { 
    id: 'intersection-1', 
    name: 'MG Road & Brigade Road',
    coords: [77.5946, 12.9716], 
    nodes: ['Cam-1A', 'Cam-1B'] 
  },
  { 
    id: 'intersection-2', 
    name: 'Kasturba Road & Residency Road',
    coords: [77.5985, 12.9698], 
    nodes: ['Cam-2A', 'Cam-2B'] 
  },
  { 
    id: 'intersection-3', 
    name: 'Highway Exit 12',
    coords: [77.6020, 12.9730], 
    nodes: ['Cam-3A'] 
  }
];
```

**Node Marker Design**:
- **Base Marker**: Custom SVG icon
  - Outer ring: 40px diameter, 3px stroke
  - Inner circle: 32px diameter, filled with status color
  - Camera icon in center (white)
- **Status Glow Effect**:
  - Normal: No glow
  - Warning: Yellow pulsing glow (1s pulse cycle)
  - Critical: Red pulsing glow (0.5s pulse cycle, faster)
  - Anomaly detected: Add orange ring animation expanding outward

**Traffic Light Visualization**:
- Small circles (12px diameter) positioned at intersection center
- Colors: Green, yellow, or red to match current light state
- Update every 2 seconds based on external system state

**Consensus Animation**:
- When consensus starts between nodes:
  1. Draw animated line from proposer to other participants
  2. Line style: Dashed, gradient from blue to purple
  3. Animate dash offset to create "flowing" effect
  4. Duration: 2 seconds
  5. When consensus completes, line becomes solid and fades out

**Popup on Click**:
- Click node marker → show popup with:
  - Node ID and status badge
  - Battery: 85%
  - Latency: 45ms
  - Last update: 2 seconds ago
  - "View Details" button → navigates to `/nodes/[nodeId]`

**Layer Order** (bottom to top):
1. Base map
2. Road network
3. Consensus animation lines
4. Traffic light indicators
5. Node markers
6. Popups

---

### 4.4 Chart Specifications

#### **Chart 1: Energy Consumption Over Time (Line Chart)**

**Location**: Node Detail Page, Analytics Page

**Data Source**: TimescaleDB query:
```sql
SELECT time_bucket('5 seconds', timestamp) AS bucket,
       avg(energy_level) as avg_energy
FROM node_metrics
WHERE node_id = $1 AND timestamp > now() - interval '5 minutes'
GROUP BY bucket
ORDER BY bucket;
```

**Chart Configuration**:
- **Library**: Recharts LineChart
- **X-Axis**: Time (format: "15:42:30")
- **Y-Axis**: Battery percentage (0-100%)
- **Line Color**: Gradient from red (low) to green (high)
- **Area Fill**: Light gradient under line
- **Grid**: Horizontal grid lines only
- **Tooltip**: Shows exact time, battery %, and state (charging/discharging)
- **Reference Lines**:
  - Red line at 10% (critical threshold)
  - Orange line at 20% (low threshold)
- **Annotations**: Mark points where model switched to quantized version

**Update Frequency**: Every 5 seconds (new data point appended, old data slides out)

#### **Chart 2: Bandwidth Usage (Stacked Area Chart)**

**Location**: Analytics Page

**Purpose**: Show bandwidth savings from Algorithm 2

**Data Structure**:
```javascript
[
  { 
    time: '15:00', 
    transmitted: 2.5,  // MB actually transmitted
    saved: 12.3        // MB saved by DISCARD decisions
  },
  ...
]
```

**Chart Configuration**:
- **Library**: Recharts AreaChart
- **X-Axis**: Time (5-minute buckets)
- **Y-Axis**: Data in MB
- **Areas**:
  - Blue area (top): Data transmitted
  - Gray area (bottom): Data saved
- **Stacking**: True
- **Tooltip**: Shows transmitted, saved, and total potential
- **Legend**: "Transmitted", "Saved by Anomaly Filtering"
- **Summary Badge** (above chart): 
  ```
  Total Saved: 245.7 MB (74.5%) ← Matches paper claim
  ```

#### **Chart 3: Response Time Distribution (Box Plot / Violin Plot)**

**Location**: Analytics Page

**Purpose**: Validate paper's claim of sub-250ms response times

**Data Source**: Query all task completion times from last 24 hours

**Chart Configuration**:
- **Library**: D3.js (custom implementation)
- **X-Axis**: Categories:
  - "EDGE-QI"
  - "Baseline (no optimization)"
- **Y-Axis**: Response time in milliseconds
- **Violin Shape**: Shows distribution density
- **Box Elements**:
  - Median line (bold)
  - 25th and 75th percentile box
  - Min/max whiskers
  - Outlier dots
- **Color**: EDGE-QI in green, Baseline in red
- **Annotations**:
  - Median for EDGE-QI: ~180ms
  - Median for Baseline: ~600ms
  - Reference line at 250ms (paper's threshold)

#### **Chart 4: Task Priority Completion Rates (Grouped Bar Chart)**

**Location**: Analytics Page

**Chart Configuration**:
- **Library**: Recharts BarChart
- **X-Axis**: Priority levels (CRITICAL, HIGH, MEDIUM, LOW)
- **Y-Axis**: Percentage (0-100%)
- **Bar Groups** (3 bars per priority):
  - Green bar: "Completed on time"
  - Orange bar: "Deferred but completed"
  - Red bar: "Failed"
- **Tooltip**: Shows count and percentage
- **Expected Pattern**: Critical and High tasks should have near 100% completion rate (proves Algorithm 1 priority enforcement works)

---

## Part 5: Backend Implementation - Detailed Architecture

### 5.1 FastAPI Application Structure

**Main Application** (`backend/app/main.py`):

```python
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import socketio

# Create FastAPI app
app = FastAPI(
    title="EDGE-QI Backend API",
    description="Orchestration and telemetry service for EDGE-QI edge nodes",
    version="1.0.0"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO setup for real-time communication
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*'
)
socket_app = socketio.ASGIApp(sio, app)

# Import routers
from app.api.v1 import nodes, simulation, metrics, analytics, websocket

# Register routes
app.include_router(nodes.router, prefix="/api/v1/nodes", tags=["nodes"])
app.include_router(simulation.router, prefix="/api/v1/simulation", tags=["simulation"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["metrics"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "edge-qi-backend"}

# Startup event: Initialize MQTT subscriptions
@app.on_event("startup")
async def startup_event():
    from app.services.mqtt_service import mqtt_service
    await mqtt_service.connect()
    await mqtt_service.subscribe_to_all_nodes()
```

**MQTT Service** (`backend/app/services/mqtt_service.py`):

This is the critical component that bridges edge nodes and the frontend.

```python
import paho.mqtt.client as mqtt
import json
import asyncio
from app.core.config import settings

class MQTTService:
    def __init__(self):
        self.client = mqtt.Client(client_id="edge-qi-backend")
        self.connected = False
        self.message_handlers = {}
        
    async def connect(self):
        """Connect to Mosquitto broker"""
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        self.client.connect(
            host=settings.MQTT_BROKER_HOST,
            port=settings.MQTT_BROKER_PORT,
            keepalive=60
        )
        
        # Start MQTT loop in background thread
        self.client.loop_start()
        
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(f"✅ Connected to MQTT broker")
        else:
            print(f"❌ MQTT connection failed with code {rc}")
    
    def _on_message(self, client, userdata, msg):
        """Route incoming MQTT messages to appropriate handlers"""
        topic = msg.topic
        payload = json.loads(msg.payload.decode())
        
        # Parse topic to determine message type
        # Topic format: edge-qi/nodes/{node_id}/{message_type}
        parts = topic.split('/')
        if len(parts) >= 4:
            node_id = parts[2]
            message_type = parts[3]
            
            # Forward to Socket.IO clients
            asyncio.create_task(
                self._forward_to_frontend(node_id, message_type, payload)
            )
    
    async def _forward_to_frontend(self, node_id, message_type, payload):
        """Forward MQTT data to connected frontend clients via Socket.IO"""
        from app.main import sio
        
        # Emit to all connected clients
        await sio.emit(
            event=f'{message_type}_update',
            data={
                'node_id': node_id,
                'data': payload,
                'timestamp': payload.get('timestamp')
            }
        )
    
    async def subscribe_to_all_nodes(self):
        """Subscribe to all node telemetry topics"""
        # Subscribe to wildcard topics for all nodes
        topics = [
            "edge-qi/nodes/+/metrics",      # Node metrics (battery, latency, etc.)
            "edge-qi/nodes/+/video",        # Video frames
            "edge-qi/nodes/+/scheduler",    # Algorithm 1 decisions
            "edge-qi/nodes/+/transmission", # Algorithm 2 decisions
            "edge-qi/nodes/+/consensus",    # Consensus protocol messages
            "edge-qi/nodes/+/logs",         # General logs
        ]
        
        for topic in topics:
            self.client.subscribe(topic, qos=1)
            print(f"📡 Subscribed to {topic}")
    
    async def publish_command(self, node_id: str, command: str, params: dict):
        """Send command to specific edge node"""
        topic = f"edge-qi/commands/{node_id}"
        payload = json.dumps({
            'command': command,
            'params': params,
            'timestamp': datetime.now().isoformat()
        })
        
        self.client.publish(topic, payload, qos=1)

# Singleton instance
mqtt_service = MQTTService()
```

**Simulation Controller API** (`backend/app/api/v1/simulation.py`):

This endpoint handles UI button clicks to trigger edge cases.

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.mqtt_service import mqtt_service

router = APIRouter()

class SimulationEvent(BaseModel):
    node_id: str
    event_type: str  # 'energy', 'network', 'traffic', 'system'
    parameters: dict

@router.post("/trigger-event")
async def trigger_simulation_event(event: SimulationEvent):
    """
    Trigger a simulated event on a specific edge node
    
    Examples:
    - Low battery: {"node_id": "Cam-1A", "event_type": "energy", 
                    "parameters": {"battery_level": 15}}
    - High latency: {"node_id": "Cam-1A", "event_type": "network", 
                     "parameters": {"latency_ms": 800}}
    - Accident: {"node_id": "Cam-1A", "event_type": "traffic", 
                 "parameters": {"scenario": "accident", "severity": "high"}}
    """
    
    # Validate node exists
    valid_nodes = ["Cam-1A", "Cam-1B", "Cam-2A", "Cam-2B", "Cam-3A"]
    if event.node_id not in valid_nodes:
        raise HTTPException(status_code=404, detail=f"Node {event.node_id} not found")
    
    # Publish command via MQTT
    await mqtt_service.publish_command(
        node_id=event.node_id,
        command=f"simulate_{event.event_type}",
        params=event.parameters
    )
    
    return {
        "status": "success",
        "message": f"Event triggered on {event.node_id}",
        "event": event.dict()
    }

@router.post("/reset-all")
async def reset_all_nodes():
    """Reset all nodes to normal operating state"""
    valid_nodes = ["Cam-1A", "Cam-1B", "Cam-2A", "Cam-2B", "Cam-3A"]
    
    for node_id in valid_nodes:
        await mqtt_service.publish_command(
            node_id=node_id,
            command="reset_to_normal",
            params={}
        )
    
    return {"status": "success", "message": "All nodes reset"}
```

---

### 5.2 Edge Node Implementation - Complete Layer Architecture

**Node Entry Point** (`edge_nodes/node_main.py`):

```python
import asyncio
import os
from layers import (
    InputLayer,
    ProcessingLayer,
    MLLayer,
    CoreLayer,
    CollaborationLayer,
    BandwidthLayer,
    ExternalLayer
)
from config.node_config import NodeConfig

async def main():
    # Load node configuration from environment
    node_id = os.getenv('NODE_ID', 'Cam-1A')
    config = NodeConfig(node_id=node_id)
    
    print(f"🚀 Starting EDGE-QI Node: {node_id}")
    
    # Initialize all layers
    input_layer = InputLayer(config)
    processing_layer = ProcessingLayer()
    ml_layer = MLLayer(config)
    core_layer = CoreLayer(config)
    collaboration_layer = CollaborationLayer(config)
    bandwidth_layer = BandwidthLayer(config)
    external_layer = ExternalLayer(config)
    
    # Main processing loop
    while True:
        try:
            # Layer 1: Get input frame
            frame = await input_layer.get_frame()
            
            # Layer 2: Process and clean frame
            processed_frame = processing_layer.process(frame)
            
            # Layer 3: ML inference
            # Check energy level first to determine which model to use
            energy_level = core_layer.get_energy_level()
            detections = await ml_layer.detect_objects(
                processed_frame, 
                use_quantized=(energy_level < config.ENERGY_THRESHOLD)
            )
            
            # Calculate traffic metrics
            queue_length = ml_layer.calculate_queue_length(detections)
            avg_speed = ml_layer.estimate_speed(detections)
            
            # Layer 4: Task scheduling
            task = {
                'type': 'process_frame',
                'priority': core_layer.determine_priority(queue_length),
                'requires_network': False,
                'data': {'queue_length': queue_length, 'speed': avg_speed}
            }
            
            should_execute = await core_layer.schedule_task(task)
            
            if not should_execute:
                # Task deferred, skip this iteration
                continue
            
            # Layer 5: Collaboration (if applicable)
            # Check if consensus is needed for this frame
            if collaboration_layer.should_initiate_consensus(queue_length):
                consensus_result = await collaboration_layer.propose_action({
                    'action': 'change_light',
                    'intersection': config.intersection_id,
                    'queue_state': queue_length
                })
                
                if consensus_result['agreed']:



## Prompt:
11/1/2025, 3:26:14 AM

Continue



## Response:
11/1/2025, 3:28:05 AM

```python
                    # Layer 7: Execute agreed action
                    await external_layer.control_traffic_light(
                        consensus_result['action']
                    )
            
            # Layer 6: Bandwidth optimization
            # Determine if we should transmit this data
            transmission_decision = await bandwidth_layer.decide_transmission(
                current_data={'queue_length': queue_length, 'speed': avg_speed},
                frame=processed_frame,
                detections=detections
            )
            
            if transmission_decision['should_transmit']:
                # Adjust quality based on network conditions
                stream_quality = bandwidth_layer.get_adaptive_quality()
                
                # Encode frame with appropriate quality
                encoded_frame = bandwidth_layer.encode_frame(
                    processed_frame,
                    detections,
                    quality=stream_quality
                )
                
                # Publish to MQTT
                await bandwidth_layer.publish_frame(encoded_frame)
                await bandwidth_layer.publish_metrics({
                    'queue_length': queue_length,
                    'speed': avg_speed,
                    'energy': energy_level,
                    'latency': core_layer.get_network_latency(),
                    'model_type': 'quantized' if energy_level < config.ENERGY_THRESHOLD else 'full'
                })
            
            # Small delay to prevent overwhelming the system
            await asyncio.sleep(0.033)  # ~30 FPS
            
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
```

**Layer 4: Core Processing - Algorithm 1 Implementation** (`edge_nodes/layers/layer_4_core.py`):

```python
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum
import time

class TaskPriority(Enum):
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1

@dataclass
class Task:
    task_id: str
    priority: TaskPriority
    requires_network: bool
    data: Dict
    timestamp: float

class CoreLayer:
    def __init__(self, config):
        self.config = config
        
        # Simulated monitors
        self.energy_level = 100.0  # Start at full battery
        self.network_latency = 50.0  # Start with good network
        self.network_bandwidth = 20.0  # 20 Mbps
        
        # Task queue
        self.task_queue = []
        self.deferred_tasks = {
            'energy': [],
            'network': []
        }
        
        # Thresholds from paper
        self.E_THRESHOLD = config.ENERGY_THRESHOLD  # 20%
        self.N_LATENCY_THRESHOLD = config.NETWORK_LATENCY_THRESHOLD  # 200ms
        self.N_BANDWIDTH_MIN = config.NETWORK_BANDWIDTH_MIN  # 1 Mbps
        
        # State tracking for dashboard
        self.current_task = None
        self.last_decision = None
        
    def get_energy_level(self) -> float:
        """Get current battery level (simulated)"""
        # Simulate battery drain based on processing
        self.energy_level -= 0.01  # Drain 1% per iteration
        
        # Simulate charging if enabled
        if hasattr(self, 'is_charging') and self.is_charging:
            self.energy_level = min(100.0, self.energy_level + 0.05)
        
        return max(0.0, self.energy_level)
    
    def get_network_latency(self) -> float:
        """Get current network latency (simulated)"""
        return self.network_latency
    
    def get_network_bandwidth(self) -> float:
        """Get current network bandwidth (simulated)"""
        return self.network_bandwidth
    
    def determine_priority(self, queue_length: int) -> TaskPriority:
        """Determine task priority based on queue length"""
        if queue_length > 20:  # Heavy congestion
            return TaskPriority.CRITICAL
        elif queue_length > 10:
            return TaskPriority.HIGH
        elif queue_length > 5:
            return TaskPriority.MEDIUM
        else:
            return TaskPriority.LOW
    
    async def schedule_task(self, task: Task) -> bool:
        """
        Algorithm 1: Multi-Constraint Adaptive Task Scheduling
        
        Returns True if task should execute, False if deferred
        """
        # Get current system state
        energy = self.get_energy_level()
        latency = self.get_network_latency()
        bandwidth = self.get_network_bandwidth()
        
        decision_log = {
            'task_id': task['type'],
            'priority': task['priority'],
            'energy_level': energy,
            'network_latency': latency,
            'network_bandwidth': bandwidth,
            'decision': None,
            'reason': None,
            'timestamp': time.time()
        }
        
        # Algorithm 1, Line 5-12: Check energy constraints
        if energy < self.E_THRESHOLD:
            if task['priority'] == TaskPriority.CRITICAL:
                # Execute with reduced processing
                decision_log['decision'] = 'EXECUTE_REDUCED'
                decision_log['reason'] = f'Critical task but low energy ({energy:.1f}% < {self.E_THRESHOLD}%)'
                self.last_decision = decision_log
                await self._publish_scheduler_decision(decision_log)
                return True
            else:
                # Defer to low-energy queue
                self.deferred_tasks['energy'].append(task)
                decision_log['decision'] = 'DEFERRED_ENERGY'
                decision_log['reason'] = f'Non-critical task deferred due to low energy ({energy:.1f}%)'
                self.last_decision = decision_log
                await self._publish_scheduler_decision(decision_log)
                return False
        
        # Algorithm 1, Line 13-18: Check network constraints
        if latency > self.N_LATENCY_THRESHOLD or bandwidth < self.N_BANDWIDTH_MIN:
            if task['requires_network']:
                # Defer to network queue
                self.deferred_tasks['network'].append(task)
                decision_log['decision'] = 'DEFERRED_NETWORK'
                decision_log['reason'] = f'Network issue: latency={latency:.0f}ms > {self.N_LATENCY_THRESHOLD}ms or bandwidth={bandwidth:.1f}Mbps < {self.N_BANDWIDTH_MIN}Mbps'
                self.last_decision = decision_log
                await self._publish_scheduler_decision(decision_log)
                return False
        
        # Algorithm 1, Line 19: Execute task normally
        decision_log['decision'] = 'EXECUTE_NORMAL'
        decision_log['reason'] = 'All constraints satisfied'
        self.last_decision = decision_log
        await self._publish_scheduler_decision(decision_log)
        return True
    
    async def _publish_scheduler_decision(self, decision: Dict):
        """Publish scheduler decision to MQTT for dashboard"""
        from comms.mqtt_client import mqtt_client
        
        topic = f"edge-qi/nodes/{self.config.node_id}/scheduler"
        await mqtt_client.publish(topic, decision)
    
    async def handle_simulation_command(self, command: str, params: Dict):
        """Handle simulation commands from backend"""
        if command == 'simulate_energy':
            self.energy_level = params.get('battery_level', 15)
            self.is_charging = params.get('charging', False)
        
        elif command == 'simulate_network':
            self.network_latency = params.get('latency_ms', 800)
            self.network_bandwidth = params.get('bandwidth_mbps', 0.5)
        
        elif command == 'reset_to_normal':
            self.energy_level = 100.0
            self.network_latency = 50.0
            self.network_bandwidth = 20.0
            self.is_charging = False
```

**Layer 6: Bandwidth Optimization - Algorithm 2 Implementation** (`edge_nodes/layers/layer_6_bandwidth.py`):

```python
import json
import numpy as np
from sklearn.ensemble import IsolationForest
from scipy import stats
from typing import Dict, Tuple
import cv2
import base64

class BandwidthLayer:
    def __init__(self, config):
        self.config = config
        self.node_id = config.node_id
        
        # Load historical data for anomaly detection
        self.historical_data = self._load_historical_data()
        
        # Initialize ML-based anomaly detector
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self._train_anomaly_detector()
        
        # Thresholds from paper (Algorithm 2, Line 5-12)
        self.THETA_CRITICAL = 3.0   # 3 standard deviations
        self.THETA_HIGH = 2.5
        self.THETA_MEDIUM = 2.0
        self.THETA_LOW = 1.5
        
        # Adaptive streaming tiers from paper
        self.STREAMING_TIERS = {
            'ULTRA_LOW': {'bitrate': 150, 'resolution': (320, 240), 'quality': 20},
            'LOW': {'bitrate': 500, 'resolution': (640, 480), 'quality': 40},
            'MEDIUM': {'bitrate': 1500, 'resolution': (1280, 720), 'quality': 60},
            'HIGH': {'bitrate': 3000, 'resolution': (1920, 1080), 'quality': 80},
            'ULTRA_HIGH': {'bitrate': 6000, 'resolution': (1920, 1080), 'quality': 95}
        }
        
        self.current_tier = 'MEDIUM'
        self.transmission_log = []
        
    def _load_historical_data(self) -> Dict:
        """Load historical queue averages for Algorithm 2"""
        try:
            with open('datasets/historical_data/queue_averages.json', 'r') as f:
                data = json.load(f)
                return data.get(self.config.intersection_id, {})
        except FileNotFoundError:
            print("⚠️  Historical data not found, using defaults")
            return self._generate_default_patterns()
    
    def _generate_default_patterns(self) -> Dict:
        """Generate default traffic patterns if historical data missing"""
        patterns = {}
        for hour in range(24):
            for minute in [0, 15, 30, 45]:
                time_key = f"{hour:02d}:{minute:02d}"
                # Simulate rush hour patterns
                if 7 <= hour <= 9 or 17 <= hour <= 19:
                    mean = 15 + np.random.normal(0, 2)
                else:
                    mean = 5 + np.random.normal(0, 1)
                patterns[time_key] = {
                    'mean': max(0, mean),
                    'std_dev': mean * 0.3,
                    'samples': 120
                }
        return {'monday': patterns}  # Simplified
    
    def _train_anomaly_detector(self):
        """Train Isolation Forest on historical patterns"""
        # Generate training data from historical patterns
        training_samples = []
        for day_data in self.historical_data.values():
            for time_block, stats in day_data.items():
                # Generate samples around mean
                samples = np.random.normal(
                    stats['mean'], 
                    stats['std_dev'], 
                    size=20
                )
                training_samples.extend(samples)
        
        X = np.array(training_samples).reshape(-1, 1)
        self.isolation_forest.fit(X)
    
    def _get_current_time_block(self) -> str:
        """Get current 15-minute time block"""
        from datetime import datetime
        now = datetime.now()
        minute_block = (now.minute // 15) * 15
        return f"{now.hour:02d}:{minute_block:02d}"
    
    async def decide_transmission(
        self, 
        current_data: Dict, 
        frame: np.ndarray, 
        detections: list
    ) -> Dict:
        """
        Algorithm 2: Anomaly-Driven Data Transmission
        
        Returns decision dictionary with transmission recommendation
        """
        queue_length = current_data['queue_length']
        speed = current_data['speed']
        
        # Algorithm 2, Line 3: Calculate anomaly score
        anomaly_score = self._calculate_statistical_anomaly(queue_length)
        ml_anomaly_score = self._calculate_ml_anomaly(queue_length)
        
        # Algorithm 2, Line 4: Calculate significance
        significance = self._calculate_significance(current_data)
        
        decision = {
            'current_queue': queue_length,
            'historical_mean': None,
            'historical_std': None,
            'z_score': anomaly_score,
            'ml_score': ml_anomaly_score,
            'significance': significance,
            'decision': None,
            'priority': None,
            'reason': None,
            'should_transmit': False
        }
        
        # Get historical data for current time
        time_block = self._get_current_time_block()
        historical = self.historical_data.get('monday', {}).get(time_block, {})
        decision['historical_mean'] = historical.get('mean', 5.0)
        decision['historical_std'] = historical.get('std_dev', 2.0)
        
        # Algorithm 2, Line 5-6: Critical anomaly or high significance
        if anomaly_score > self.THETA_CRITICAL or significance > 0.8:
            decision['decision'] = 'TRANSMIT'
            decision['priority'] = 'HIGH'
            decision['reason'] = f'Critical anomaly detected (z-score: {anomaly_score:.2f} > {self.THETA_CRITICAL})'
            decision['should_transmit'] = True
        
        # Algorithm 2, Line 7-8: Medium anomaly
        elif anomaly_score > self.THETA_MEDIUM or significance > 0.5:
            decision['decision'] = 'TRANSMIT'
            decision['priority'] = 'NORMAL'
            decision['reason'] = f'Significant change detected (z-score: {anomaly_score:.2f})'
            decision['should_transmit'] = True
        
        # Algorithm 2, Line 9-10: Low anomaly - defer for batch
        elif anomaly_score > self.THETA_LOW:
            decision['decision'] = 'DEFER'
            decision['priority'] = 'LOW'
            decision['reason'] = 'Minor change - defer for batch transmission'
            decision['should_transmit'] = False  # Could batch later
        
        # Algorithm 2, Line 11-12: No anomaly - discard
        else:
            decision['decision'] = 'DISCARD'
            decision['priority'] = None
            decision['reason'] = f'Redundant data (z-score: {anomaly_score:.2f} < {self.THETA_LOW})'
            decision['should_transmit'] = False
        
        # Log decision
        self.transmission_log.append(decision)
        await self._publish_transmission_decision(decision)
        
        return decision
    
    def _calculate_statistical_anomaly(self, queue_length: float) -> float:
        """Calculate Z-score for statistical anomaly detection"""
        time_block = self._get_current_time_block()
        historical = self.historical_data.get('monday', {}).get(time_block, {})
        
        mean = historical.get('mean', 5.0)
        std_dev = historical.get('std_dev', 2.0)
        
        if std_dev == 0:
            return 0.0
        
        z_score = abs((queue_length - mean) / std_dev)
        return z_score
    
    def _calculate_ml_anomaly(self, queue_length: float) -> float:
        """Calculate ML-based anomaly score using Isolation Forest"""
        X = np.array([[queue_length]])
        score = self.isolation_forest.score_samples(X)[0]
        
        # Convert to 0-1 scale (lower score = more anomalous)
        normalized_score = (score + 0.5) * -2  # Invert and scale
        return max(0.0, min(1.0, normalized_score))
    
    def _calculate_significance(self, current_data: Dict) -> float:
        """Calculate overall significance of current observation"""
        # Combine multiple factors
        queue_significance = min(1.0, current_data['queue_length'] / 30.0)
        speed_significance = max(0.0, 1.0 - current_data['speed'] / 30.0)
        
        # Weighted average
        return 0.7 * queue_significance + 0.3 * speed_significance
    
    def get_adaptive_quality(self) -> str:
        """Determine current streaming quality based on network conditions"""
        from layers.layer_4_core import CoreLayer
        
        # This would reference the CoreLayer's network monitor
        # For now, simplified logic
        latency = 100  # Would get from CoreLayer
        bandwidth = 10  # Would get from CoreLayer
        
        if bandwidth < 0.5:
            return 'ULTRA_LOW'
        elif bandwidth < 2:
            return 'LOW'
        elif bandwidth < 5:
            return 'MEDIUM'
        elif bandwidth < 10:
            return 'HIGH'
        else:
            return 'ULTRA_HIGH'
    
    def encode_frame(
        self, 
        frame: np.ndarray, 
        detections: list, 
        quality: str
    ) -> Dict:
        """Encode frame with bounding boxes at specified quality"""
        tier = self.STREAMING_TIERS[quality]
        
        # Resize frame
        resized = cv2.resize(frame, tier['resolution'])
        
        # Draw bounding boxes
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            # Scale coordinates to new resolution
            scale_x = tier['resolution'][0] / frame.shape[1]
            scale_y = tier['resolution'][1] / frame.shape[0]
            x1, x2 = int(x1 * scale_x), int(x2 * scale_x)
            y1, y2 = int(y1 * scale_y), int(y2 * scale_y)
            
            cv2.rectangle(resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                resized, 
                det['class'], 
                (x1, y1 - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, 
                (0, 255, 0), 
                2
            )
        
        # Encode as JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), tier['quality']]
        _, buffer = cv2.imencode('.jpg', resized, encode_param)
        
        # Convert to base64
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return {
            'frame': frame_base64,
            'quality': quality,
            'bitrate': tier['bitrate'],
            'resolution': tier['resolution'],
            'size_bytes': len(buffer)
        }
    
    async def publish_frame(self, encoded_frame: Dict):
        """Publish encoded frame to MQTT"""
        from comms.mqtt_client import mqtt_client
        
        topic = f"edge-qi/nodes/{self.node_id}/video"
        await mqtt_client.publish(topic, encoded_frame)
    
    async def publish_metrics(self, metrics: Dict):
        """Publish node metrics to MQTT"""
        from comms.mqtt_client import mqtt_client
        
        topic = f"edge-qi/nodes/{self.node_id}/metrics"
        await mqtt_client.publish(topic, metrics)
    
    async def _publish_transmission_decision(self, decision: Dict):
        """Publish Algorithm 2 decision to MQTT for dashboard log"""
        from comms.mqtt_client import mqtt_client
        
        topic = f"edge-qi/nodes/{self.node_id}/transmission"
        await mqtt_client.publish(topic, decision)
```

**Layer 5: Edge Collaboration - BFT Consensus** (`edge_nodes/layers/layer_5_collaboration.py`):

```python
import asyncio
from typing import Dict, List, Optional
from enum import Enum
import time
import hashlib

class ConsensusPhase(Enum):
    IDLE = 0
    PRE_PREPARE = 1
    PREPARE = 2
    COMMIT = 3
    REPLY = 4

class CollaborationLayer:
    def __init__(self, config):
        self.config = config
        self.node_id = config.node_id
        self.peer_nodes = config.peer_nodes  # List of other nodes at same intersection
        
        # BFT parameters (from paper)
        self.f = (len(self.peer_nodes) - 1) // 3  # Max faulty nodes tolerated
        self.quorum = 2 * self.f + 1  # Minimum votes needed
        
        # Consensus state
        self.current_phase = ConsensusPhase.IDLE
        self.current_proposal = None
        self.votes_received = {}
        self.consensus_log = []
        
        # Timeouts
        self.CONSENSUS_TIMEOUT = 5.0  # 5 seconds
        
    def should_initiate_consensus(self, queue_length: int) -> bool:
        """
        Determine if consensus is needed
        
        Consensus is initiated when:
        - Queue length crosses critical threshold
        - Multiple nodes detecting same event
        - Traffic light timing needs coordination
        """
        # Only propose if this node is the designated proposer for this round
        # (In practice, could use round-robin or other selection)
        is_proposer = self._is_proposer()
        
        # Critical queue requires coordination
        needs_consensus = queue_length > 20
        
        # Not already in consensus
        not_busy = self.current_phase == ConsensusPhase.IDLE
        
        return is_proposer and needs_consensus and not_busy
    
    def _is_proposer(self) -> bool:
        """Simple proposer selection: alphabetically first node"""
        all_nodes = [self.node_id] + self.peer_nodes
        all_nodes.sort()
        return all_nodes[0] == self.node_id
    
    async def propose_action(self, proposal: Dict) -> Dict:
        """
        Initiate BFT consensus protocol
        
        Returns consensus result
        """
        print(f"🗳️  {self.node_id} initiating consensus for: {proposal['action']}")
        
        # Generate unique proposal ID
        proposal_id = hashlib.sha256(
            f"{self.node_id}{time.time()}{proposal}".encode()
        ).hexdigest()[:16]
        
        self.current_proposal = {
            'id': proposal_id,
            'proposer': self.node_id,
            'action': proposal['action'],
            'data': proposal,
            'timestamp': time.time()
        }
        
        # Phase 1: PRE-PREPARE
        # Broadcast proposal to all peers
        await self._broadcast_message({
            'phase': 'PRE_PREPARE',
            'proposal': self.current_proposal
        })
        
        self.current_phase = ConsensusPhase.PRE_PREPARE
        
        # Phase 2: PREPARE
        # Wait for prepare messages from peers
        self.votes_received = {'prepare': {}, 'commit': {}}
        prepare_success = await self._wait_for_votes('prepare', self.quorum)
        
        if not prepare_success:
            return await self._consensus_failed("Insufficient PREPARE votes")
        
        # Send own prepare vote
        await self._broadcast_message({
            'phase': 'PREPARE',
            'proposal_id': proposal_id,
            'vote': 'agree',
            'voter': self.node_id
        })
        
        self.current_phase = ConsensusPhase.PREPARE
        
        # Phase 3: COMMIT
        # Wait for commit messages
        commit_success = await self._wait_for_votes('commit', self.quorum)
        
        if not commit_success:
            return await self._consensus_failed("Insufficient COMMIT votes")
        
        # Send own commit
        await self._broadcast_message({
            'phase': 'COMMIT',
            'proposal_id': proposal_id,
            'vote': 'agree',
            'voter': self.node_id
        })
        
        self.current_phase = ConsensusPhase.COMMIT
        
        # Phase 4: REPLY - Consensus reached!
        result = {
            'agreed': True,
            'proposal_id': proposal_id,
            'action': proposal['action'],
            'votes': len(self.votes_received['commit']) + 1,
            'quorum': self.quorum,
            'duration_ms': (time.time() - self.current_proposal['timestamp']) * 1000
        }
        
        # Log consensus success
        self.consensus_log.append(result)
        await self._publish_consensus_result(result)
        
        # Reset state
        self.current_phase = ConsensusPhase.IDLE
        self.current_proposal = None
        
        print(f"✅ Consensus reached: {result}")
        return result
    
    async def _wait_for_votes(self, vote_type: str, required: int) -> bool:
        """Wait for required number of votes with timeout"""
        start_time = time.time()
        
        while True:
            # Check if we have enough votes
            if len(self.votes_received[vote_type]) >= required - 1:  # -1 because we vote too
                return True
            
            # Check timeout
            if time.time() - start_time > self.CONSENSUS_TIMEOUT:
                return False
            
            await asyncio.sleep(0.1)
    
    async def handle_consensus_message(self, message: Dict):
        """
        Handle incoming consensus messages from peers
        
        Called by MQTT client when message arrives
        """
        phase = message.get('phase')
        
        if phase == 'PRE_PREPARE':
            # Received proposal from proposer
            proposal = message['proposal']
            
            # Validate proposal
            if self._validate_proposal(proposal):
                # Send PREPARE vote
                await self._broadcast_message({
                    'phase': 'PREPARE',
                    'proposal_id': proposal['id'],
                    'vote': 'agree',
                    'voter': self.node_id
                })
        
        elif phase == 'PREPARE':
            # Received prepare vote from peer
            voter = message['voter']
            proposal_id = message['proposal_id']
            
            if self.current_proposal and proposal_id == self.current_proposal['id']:
                self.votes_received['prepare'][voter] = message['vote']
        
        elif phase == 'COMMIT':
            # Received commit vote from peer
            voter = message['voter']
            proposal_id = message['proposal_id']
            
            if self.current_proposal and proposal_id == self.current_proposal['id']:
                self.votes_received['commit'][voter] = message['vote']
    
    def _validate_proposal(self, proposal: Dict) -> bool:
        """Validate received proposal"""
        # Check proposal structure
        required_fields = ['id', 'proposer', 'action', 'data', 'timestamp']
        if not all(field in proposal for field in required_fields):
            return False
        
        # Check timestamp is recent (within 10 seconds)
        age = time.time() - proposal['timestamp']
        if age > 10:
            return False
        
        # Check proposer is valid
        if proposal['proposer'] not in ([self.node_id] + self.peer_nodes):
            return False
        
        return True
    
    async def _consensus_failed(self, reason: str) -> Dict:
        """Handle consensus failure"""
        result = {
            'agreed': False,
            'reason': reason,
            'proposal_id': self.current_proposal['id'] if self.current_proposal else None,
            'votes_received': {
                'prepare': len(self.votes_received.get('prepare', {})),
                'commit': len(self.votes_received.get('commit', {}))
            },
            'quorum_required': self.quorum
        }
        
        print(f"❌ Consensus failed: {reason}")
        
        self.consensus_log.append(result)
        await self._publish_consensus_result(result)
        
        # Reset state
        self.current_phase = ConsensusPhase.IDLE
        self.current_proposal = None
        self.votes_received = {}
        
        return result
    
    async def _broadcast_message(self, message: Dict):
        """Broadcast message to all peer nodes via MQTT"""
        from comms.mqtt_client import mqtt_client
        
        # Add sender info
        message['sender'] = self.node_id
        message['timestamp'] = time.time()
        
        # Publish to consensus topic
        topic = f"edge-qi/consensus/{self.config.intersection_id}"
        await mqtt_client.publish(topic, message)
    
    async def _publish_consensus_result(self, result: Dict):
        """Publish consensus result to dashboard"""
        from comms.mqtt_client import mqtt_client
        
        topic = f"edge-qi/nodes/{self.node_id}/consensus"
        await mqtt_client.publish(topic, result)
```

---

## Part 6: Comprehensive Test Scenarios

### Scenario 1: Low Energy with Critical Task

**Test ID**: `SCENARIO_1_LOW_ENERGY_CRITICAL`

**Objective**: Validate Algorithm 1's energy-aware scheduling with priority enforcement

**Initial Conditions**:
- Node: Cam-1A
- Battery Level: 85%
- Network: Normal (latency: 50ms, bandwidth: 20 Mbps)
- Traffic: Light (queue: 3 cars)

**Test Steps**:
1. **Step 1**: Start simulation, observe normal operation
   - **Expected**: Video streaming at HIGH quality (3 Mbps)
   - **Expected**: Dashboard shows green energy gauge
   - **Expected**: ML using full-precision YOLOv8n model

2. **Step 2**: Click "Low Battery (15%)" button in simulation controls
   - **Action**: Backend publishes MQTT command to Cam-1A
   - **Expected**: Cam-1A energy monitor updates to 15%
   - **Expected**: Dashboard energy gauge turns red
   - **Expected**: Alert appears: "LOW BATTERY WARNING - Cam-1A"

3. **Step 3**: Trigger accident (critical event)
   - **Action**: Click "Accident" button for Cam-1A
   - **Expected**: Video feed shows large queue (25+ cars)
   - **Expected**: ML detects anomaly (high z-score)

4. **Step 4**: Observe Algorithm 1 decision
   - **Expected**: Scheduler State Table shows new row:
     ```
     task_00501 | CRITICAL | Running (Reduced) | Anomaly detection - 15% battery | 16:23:45
     ```
   - **Expected**: Video overlay changes to "MODEL: yolov8n (Quantized)"
   - **Expected**: System logs show: "Algorithm 1: E.energy_level (15%) < E.threshold (20%) AND task.priority = CRITICAL → Execute with reduced processing"

5. **Step 5**:



## Prompt:
11/1/2025, 3:28:13 AM

Continue



## Response:
11/1/2025, 3:30:14 AM

**Step 5**: Verify reduced processing mode
   - **Expected**: Bounding boxes still appear but may be slightly less accurate
   - **Expected**: Frame processing speed increases (higher FPS due to lighter model)
   - **Expected**: Energy drain rate decreases (observable in energy gauge trend)
   - **Expected**: Dashboard shows "POWER SAVING MODE ACTIVE" badge

6. **Step 6**: Trigger non-critical task during low energy
   - **Action**: Simulate normal traffic (queue: 5 cars) - generates LOW priority task
   - **Expected**: Scheduler State Table shows:
     ```
     task_00502 | LOW | Deferred (Energy) | Queue calculation deferred | 16:23:50
     ```
   - **Expected**: Task added to deferred queue, not executed
   - **Expected**: Transmission Log shows: "DISCARD - Task deferred due to energy constraints"

7. **Step 7**: Restore energy
   - **Action**: Click "Start Charging" button
   - **Expected**: Energy gauge shows upward trend with lightning bolt icon
   - **Expected**: After reaching 40%, model switches back to full-precision
   - **Expected**: Video overlay changes to "MODEL: yolov8n (Full Precision)"
   - **Expected**: Deferred tasks begin executing

**Validation Metrics**:
- Energy consumption reduced by ~30% during quantized model usage
- Critical task completed despite low energy (100% critical task completion rate)
- Non-critical tasks deferred successfully (0% low-priority task execution during energy constraint)
- Model switch latency < 500ms

**Dashboard Artifacts**:
- Screenshot of scheduler table showing "Running (Reduced)" status
- Screenshot of model switch animation
- Energy chart showing drain rate before/after quantization

---

### Scenario 2: Network Congestion with Adaptive Streaming

**Test ID**: `SCENARIO_2_NETWORK_ADAPTIVE_STREAMING`

**Objective**: Validate Algorithm 1's network-aware scheduling and Layer 6's adaptive streaming

**Initial Conditions**:
- Node: Cam-2A
- Battery Level: 75%
- Network: Good (latency: 60ms, bandwidth: 15 Mbps)
- Traffic: Moderate (queue: 8 cars)

**Test Steps**:
1. **Step 1**: Establish baseline
   - **Expected**: Video streaming at HIGH quality (3 Mbps, 1920x1080)
   - **Expected**: Video overlay shows "STREAM: HIGH (3 Mbps)"
   - **Expected**: Network latency gauge shows green (60ms)

2. **Step 2**: Trigger high latency
   - **Action**: Click "High Latency (800ms)" in simulation controls
   - **Expected**: Network latency gauge turns red
   - **Expected**: Alert appears: "NETWORK DEGRADATION - Cam-2A"

3. **Step 3**: Observe adaptive streaming response
   - **Expected**: Within 2 seconds, video quality degrades visibly
   - **Expected**: Video overlay updates to "STREAM: LOW (500 kbps)"
   - **Expected**: Resolution changes to 640x480 (visible pixelation)
   - **Expected**: System logs: "Adaptive Streaming: HIGH → LOW due to latency 800ms > 200ms"

4. **Step 4**: Trigger network-dependent task
   - **Action**: System generates "Upload 1-min summary video" task (requires_network = TRUE)
   - **Expected**: Scheduler State Table shows:
     ```
     task_00601 | MEDIUM | Deferred (Network) | Video upload - high latency | 16:25:10
     ```
   - **Expected**: Task NOT executed, added to network queue

5. **Step 5**: Worsen network conditions
   - **Action**: Click "Low Bandwidth (500 kbps)"
   - **Expected**: Bandwidth gauge turns red
   - **Expected**: Video quality drops further to "ULTRA_LOW (150 kbps, 320x240)"
   - **Expected**: Frame rate drops to ~10 FPS
   - **Expected**: Despite degraded quality, stream remains active (critical alerts still deliverable)

6. **Step 6**: Verify critical alert delivery in poor network
   - **Action**: Trigger accident during low bandwidth
   - **Expected**: Anomaly detected despite poor video quality
   - **Expected**: HIGH_PRIORITY alert transmitted successfully
   - **Expected**: Transmission Log shows:
     ```
     [16:25:45] Queue: 28 cars | Z-Score: 4.2 | Decision: TRANSMIT (HIGH_PRIORITY)
     Network: DEGRADED (800ms, 0.5 Mbps) - Alert delivered via ULTRA_LOW stream
     ```

7. **Step 7**: Restore network
   - **Action**: Click "Restore Network"
   - **Expected**: Latency gauge turns green (50ms)
   - **Expected**: Video quality gradually improves: LOW → MEDIUM → HIGH
   - **Expected**: Deferred tasks begin executing
   - **Expected**: Network queue empties: "task_00601" changes to "Running"

8. **Step 8**: Verify bandwidth savings
   - **Action**: Navigate to Analytics page, check bandwidth chart
   - **Expected**: Chart shows significant reduction during degraded period
   - **Expected**: During ULTRA_LOW mode: bandwidth usage ~0.15 Mbps vs. baseline 3 Mbps
   - **Expected**: ~95% bandwidth reduction while maintaining alert capability

**Validation Metrics**:
- Adaptive streaming transition latency < 2 seconds
- Zero critical alerts lost during network degradation
- Bandwidth usage scales proportionally with tier:
  - ULTRA_LOW: 150 kbps ± 50 kbps
  - LOW: 500 kbps ± 100 kbps
  - HIGH: 3 Mbps ± 500 kbps
- Network-dependent tasks deferred 100% during constraint

**Dashboard Artifacts**:
- Video recording showing quality degradation transition
- Bandwidth chart showing tiered usage
- Scheduler table showing deferred network tasks

---

### Scenario 3: Anomaly Detection and Transmission Filtering

**Test ID**: `SCENARIO_3_ANOMALY_FILTERING`

**Objective**: Validate Algorithm 2's anomaly-driven transmission and bandwidth savings

**Initial Conditions**:
- Node: Cam-1B
- Battery Level: 90%
- Network: Normal
- Traffic: Empty road (queue: 0 cars)
- Time: 03:00 AM (simulated low-traffic period)

**Test Steps**:
1. **Step 1**: Establish normal low-traffic baseline
   - **Expected**: Video feed shows empty intersection
   - **Expected**: Queue length: 0-1 cars consistently
   - **Expected**: Historical average for 03:00 AM: ~0.5 cars

2. **Step 2**: Observe redundant data filtering
   - **Expected**: Every ~30 seconds, Transmission Log shows:
     ```
     [03:00:30] Queue: 0 cars | History: 0.5 | Z-Score: 0.15 | Decision: DISCARD
     [03:01:00] Queue: 1 car | History: 0.5 | Z-Score: 0.20 | Decision: DISCARD
     ```
   - **Expected**: Video overlay shows "STREAM: PAUSED (Nominal)"
   - **Expected**: Video feed displays static last frame (not live streaming)
   - **Expected**: Bandwidth usage chart shows near-zero usage

3. **Step 3**: Single vehicle anomaly (minor)
   - **Action**: Simulate single speeding vehicle passing through
   - **Expected**: Queue briefly becomes 3 cars
   - **Expected**: Z-score calculation: (3 - 0.5) / 0.3 = ~8.3 (far exceeds THETA_CRITICAL = 3.0)
   - **Expected**: Transmission Log shows:
     ```
     [03:01:15] Queue: 3 cars | History: 0.5 | Z-Score: 8.3 | ML-Score: 0.92
     Decision: TRANSMIT (HIGH_PRIORITY)
     Reason: Z-score exceeds critical threshold (8.3 > 3.0)
     ```
   - **Expected**: Video stream immediately resumes
   - **Expected**: Dashboard alert: "ANOMALY DETECTED - Cam-1B"

4. **Step 4**: Return to normal
   - **Expected**: After vehicle passes, queue returns to 0
   - **Expected**: After 2-3 normal readings, system returns to DISCARD mode
   - **Expected**: Transmission Log shows:
     ```
     [03:02:00] Queue: 0 cars | History: 0.5 | Z-Score: 0.15 | Decision: DISCARD
     Stream paused - returning to nominal state
     ```

5. **Step 5**: Transition to rush hour (time-based historical change)
   - **Action**: Advance simulation time to 08:00 AM
   - **Expected**: Historical average changes: 0.5 → 18.2 cars
   - **Expected**: Queue naturally increases to 15-20 cars (normal for rush hour)
   - **Expected**: Z-score remains LOW: (18 - 18.2) / 4.1 = ~0.05
   - **Expected**: Transmission Log shows:
     ```
     [08:00:30] Queue: 18 cars | History: 18.2 | Z-Score: 0.05 | Decision: DISCARD
     Note: High queue but within expected rush hour pattern
     ```
   - **Expected**: Despite high queue count, no anomaly (system adapts to time-of-day)

6. **Step 6**: True anomaly during rush hour
   - **Action**: Trigger accident during rush hour
   - **Expected**: Queue jumps to 35 cars (well above rush hour norm)
   - **Expected**: Z-score: (35 - 18.2) / 4.1 = ~4.1 > THETA_CRITICAL
   - **Expected**: ML anomaly detector also flags (unusual pattern beyond just count)
   - **Expected**: Transmission Log shows:
     ```
     [08:05:00] Queue: 35 cars | History: 18.2 | Z-Score: 4.1 | ML-Score: 0.87
     Decision: TRANSMIT (HIGH_PRIORITY)
     Reason: Multi-factor anomaly - Statistical + ML detection
     ```

7. **Step 7**: Calculate bandwidth savings
   - **Action**: Check Analytics page after 1-hour simulation
   - **Expected**: Transmission statistics:
     - Total possible transmissions: 120 (1 per 30 seconds)
     - Actual transmissions: 8 (only anomalies)
     - DISCARD decisions: 112 (93.3% filtered)
   - **Expected**: Bandwidth chart shows:
     - Potential data without filtering: 720 MB (120 × 6 MB avg frame)
     - Actual data transmitted: 48 MB (8 × 6 MB)
     - **Savings: 672 MB (93.3%)** ← Validates paper's 74.5% claim

**Validation Metrics**:
- Anomaly detection accuracy: 100% (no false negatives for critical events)
- Redundant data filtering: >90% of normal operation
- Time-adaptive thresholds working correctly (rush hour vs. night)
- Zero missed critical events
- Bandwidth savings: 75-95% depending on traffic pattern

**Dashboard Artifacts**:
- Transmission Log showing DISCARD vs. TRANSMIT patterns
- Bandwidth savings chart
- Anomaly timeline showing detection points
- Z-score distribution chart

---

### Scenario 4: Multi-Node Consensus Protocol

**Test ID**: `SCENARIO_4_BFT_CONSENSUS`

**Objective**: Validate Layer 5's distributed consensus protocol for coordinated decision-making

**Initial Conditions**:
- Nodes: Cam-1A, Cam-1B, Cam-2A, Cam-2B (4 nodes at 2 intersections)
- All nodes: Normal battery, normal network
- Traffic: Normal
- BFT parameters: f = 1 (can tolerate 1 faulty node), quorum = 3 votes

**Test Steps**:
1. **Step 1**: Establish multi-node monitoring
   - **Expected**: Map view shows 4 active nodes (all green)
   - **Expected**: Intersection-1 monitored by Cam-1A (N/S) and Cam-1B (E/W)
   - **Expected**: Intersection-2 monitored by Cam-2A (N/S) and Cam-2B (E/W)

2. **Step 2**: Trigger coordinated event
   - **Action**: Simulate emergency vehicle approaching Intersection-1 from North
   - **Expected**: Cam-1A (facing N/S) detects emergency vehicle first
   - **Expected**: Queue length: 15+ cars (critical threshold)
   - **Expected**: Cam-1A initiates consensus as proposer

3. **Step 3**: Observe PRE-PREPARE phase
   - **Expected**: Consensus Visualizer shows:
     - Cam-1A node glows bright blue (proposer)
     - Animated arrows flow from Cam-1A to Cam-1B, Cam-2A, Cam-2B
   - **Expected**: Status text: "Cam-1A proposes: 'Set Intersection-1 N/S to GREEN, E/W to RED'"
   - **Expected**: Info panel shows:
     ```
     Session ID: abc123
     Proposer: Cam-1A
     Proposal: Emergency vehicle clearance
     Phase: PRE-PREPARE
     ```

4. **Step 4**: Observe PREPARE phase
   - **Expected**: All receiving nodes validate proposal
   - **Expected**: Nodes broadcast PREPARE votes to each other
   - **Expected**: Consensus Visualizer shows full mesh of animated lines between all 4 nodes
   - **Expected**: Vote counter updates: "Prepare Votes: 1/3... 2/3... 3/3 ✓"
   - **Expected**: System logs from each node:
     ```
     Cam-1B: Received PRE-PREPARE from Cam-1A - Proposal valid - Sending PREPARE vote
     Cam-2A: Received PRE-PREPARE from Cam-1A - Proposal valid - Sending PREPARE vote
     Cam-2B: Received PRE-PREPARE from Cam-1A - Proposal valid - Sending PREPARE vote
     ```

5. **Step 5**: Observe COMMIT phase
   - **Expected**: After quorum reached on PREPARE, nodes move to COMMIT
   - **Expected**: Green checkmarks appear on agreeing nodes (Cam-1A, Cam-1B, Cam-2A)
   - **Expected**: Vote counter: "Commit Votes: 3/3 ✓"
   - **Expected**: Consensus Visualizer shows solid green lines between nodes

6. **Step 6**: Consensus completion
   - **Expected**: All nodes flash green simultaneously
   - **Expected**: Status text: "✅ CONSENSUS REACHED: Set lights for emergency vehicle"
   - **Expected**: Duration displayed: "Consensus time: 1.8 seconds"
   - **Expected**: Consensus history updates:
     ```
     [08:15:45] Session abc123: AGREED (4/4 votes, 1.8s)
     Action: Emergency vehicle clearance - Intersection-1
     ```

7. **Step 7**: Execute agreed action
   - **Expected**: External systems layer activates
   - **Expected**: Traffic light at Intersection-1 changes: N/S → GREEN, E/W → RED
   - **Expected**: Map view shows traffic light indicator change
   - **Expected**: All nodes log execution: "Consensus action executed"

8. **Step 8**: Test Byzantine fault tolerance
   - **Action**: Simulate Cam-2B failure (node goes offline)
   - **Expected**: Map marker for Cam-2B turns gray
   - **Expected**: System detects node offline

9. **Step 9**: New consensus with failed node
   - **Action**: Trigger another emergency event
   - **Expected**: Consensus still succeeds with only 3 active nodes
   - **Expected**: Quorum calculation: f = 0 (only 3 nodes), quorum = 2 votes needed
   - **Expected**: Consensus Visualizer shows only Cam-1A, Cam-1B, Cam-2A participating
   - **Expected**: System logs: "Cam-2B unresponsive - Consensus proceeding with 3/4 nodes"
   - **Expected**: Consensus reaches AGREED state with 3 votes

10. **Step 10**: Test consensus failure scenario
    - **Action**: Bring Cam-2B back online but simulate network partition (Cam-2B can't communicate)
    - **Action**: Trigger consensus requiring all 4 nodes
    - **Expected**: PRE-PREPARE messages sent but Cam-2B doesn't respond
    - **Expected**: PREPARE phase times out after 5 seconds
    - **Expected**: Consensus Visualizer shows:
      - Cam-1A, Cam-1B, Cam-2A with green checkmarks
      - Cam-2B with red X and "TIMEOUT" label
    - **Expected**: Status text: "❌ CONSENSUS FAILED: Insufficient votes (3/4, need 4)"
    - **Expected**: System retries or falls back to local decision

11. **Step 11**: Verify no redundant work
    - **Action**: Both Cam-1A and Cam-1B see same traffic at Intersection-1
    - **Expected**: Only ONE node (Cam-1A as proposer) performs full analysis
    - **Expected**: Cam-1B receives consensus result and uses shared state
    - **Expected**: Analytics shows 50% reduction in duplicate computation

**Validation Metrics**:
- Consensus success rate: >95% under normal conditions
- Consensus latency: <3 seconds for 4-node network
- Byzantine fault tolerance: System functions with f faulty nodes (f = (n-1)/3)
- Zero inconsistent states across nodes after consensus
- Duplicate computation reduction: ~50% for overlapping camera coverage

**Dashboard Artifacts**:
- Consensus Visualizer animation recording
- Voting progress screenshots
- Failed consensus scenario showing timeout
- Computation savings chart

---

### Scenario 5: End-to-End Multi-Constraint Stress Test

**Test ID**: `SCENARIO_5_MULTI_CONSTRAINT_STRESS`

**Objective**: Validate system behavior under simultaneous constraints (low energy + poor network + high traffic)

**Initial Conditions**:
- Node: Cam-3A (single node at isolated intersection)
- Battery: 18%
- Network: Latency 650ms, Bandwidth 0.8 Mbps
- Traffic: Heavy (queue: 22 cars)

**Test Steps**:
1. **Step 1**: System faces triple constraint
   - **Expected**: Energy gauge: Red (18%)
   - **Expected**: Network latency gauge: Red (650ms)
   - **Expected**: Network bandwidth gauge: Red (0.8 Mbps)
   - **Expected**: Dashboard shows "MULTIPLE CONSTRAINTS ACTIVE" warning badge

2. **Step 2**: Critical task arrives
   - **Action**: Accident detected (queue jumps to 30 cars)
   - **Expected**: Task priority: CRITICAL
   - **Expected**: Algorithm 1 evaluation:
     ```
     E.energy_level (18%) < E.threshold (20%) → TRUE
     task.priority = CRITICAL → TRUE
     Decision: Execute with reduced processing
     
     N.latency (650ms) > N.threshold (200ms) → TRUE
     task.requires_network = FALSE (local processing)
     Decision: Can execute locally
     ```

3. **Step 3**: Observe algorithm coordination
   - **Expected**: Scheduler uses quantized model (energy constraint)
   - **Expected**: Video quality drops to ULTRA_LOW (network constraint)
   - **Expected**: Anomaly detection still runs (critical priority overrides constraints)
   - **Expected**: Transmission Log:
     ```
     [16:30:15] Queue: 30 cars | Z-Score: 5.2 | Decision: TRANSMIT (HIGH_PRIORITY)
     Constraints: LOW_ENERGY + POOR_NETWORK
     Action: Reduced model + Ultra-low stream + Priority transmission
     Alert delivered successfully despite constraints
     ```

4. **Step 4**: Non-critical tasks deferred
   - **Action**: System generates "Statistical analysis" task (LOW priority, requires network)
   - **Expected**: Scheduler immediately defers:
     ```
     task_00801 | LOW | Deferred (Energy + Network) | Postponed until constraints resolve
     ```

5. **Step 5**: Verify graceful degradation
   - **Expected**: Critical alerts still delivered (100% success rate)
   - **Expected**: Video stream active but heavily degraded (150 kbps, 320x240, 10 FPS)
   - **Expected**: Energy drain minimized (quantized model saves ~30% power)
   - **Expected**: System remains functional, not crashed or frozen

6. **Step 6**: Progressive constraint resolution
   - **Action**: Click "Restore Network"
   - **Expected**: Network constraints lift
   - **Expected**: Video quality improves: ULTRA_LOW → LOW → MEDIUM
   - **Expected**: Network-deferred tasks begin executing
   - **Expected**: Energy constraint still active (model remains quantized)

7. **Step 7**: Full recovery
   - **Action**: Click "Start Charging"
   - **Expected**: Battery increases to 45%
   - **Expected**: Model switches to full-precision
   - **Expected**: Video quality reaches HIGH
   - **Expected**: All deferred tasks cleared
   - **Expected**: System returns to normal operation

**Validation Metrics**:
- Zero critical alert failures despite triple constraint
- Task completion rate by priority:
  - CRITICAL: 100%
  - HIGH: 85%
  - MEDIUM: 40%
  - LOW: 10%
- System response time remains <250ms for critical tasks
- Energy savings: 28-30% during constrained period
- Bandwidth usage: 95% reduction during ultra-low mode

---

## Part 7: Implementation Timeline and Development Phases

### Phase 1: Foundation (Weeks 1-2)
- Set up project structure and Docker environment
- Implement MQTT broker and basic pub/sub
- Create Next.js frontend skeleton with routing
- Set up PostgreSQL + TimescaleDB + Redis
- Implement FastAPI backend with WebSocket support

### Phase 2: Core Algorithms (Weeks 3-4)
- Implement Algorithm 1 (Multi-Constraint Scheduler)
- Implement Algorithm 2 (Anomaly-Driven Transmission)
- Download and prepare VisDrone dataset
- Train and quantize YOLOv8 models
- Generate historical traffic data

### Phase 3: Edge Node Logic (Weeks 5-6)
- Implement all 7 EDGE-QI layers
- Integrate YOLO inference pipeline
- Implement energy and network monitors
- Create simulation command handlers
- Test individual node functionality

### Phase 4: Consensus Protocol (Week 7)
- Implement BFT consensus algorithm
- Create inter-node communication
- Test consensus with 4-node network
- Implement fault tolerance mechanisms

### Phase 5: Frontend Dashboard (Weeks 8-9)
- Build Map View with Mapbox
- Create Node Detail panels
- Implement real-time charts (Recharts)
- Build Consensus Visualizer
- Create Simulation Controls
- Implement Analytics pages

### Phase 6: Integration (Week 10)
- Connect all components via MQTT + Socket.IO
- Implement end-to-end data flow
- Test all 5 scenarios
- Performance optimization

### Phase 7: Polish & Documentation (Week 11)
- UI/UX refinements
- Error handling and edge cases
- Write comprehensive documentation
- Create demo videos
- Prepare presentation materials

---

## Part 8: Validation and Success Criteria

### Performance Benchmarks (from paper)
1. **Energy Savings**: Achieve 25-30% reduction vs. baseline (paper claims 28.4%)
2. **Bandwidth Reduction**: Achieve 70-80% savings (paper claims 74.5%)
3. **Response Time**: Maintain <250ms for all critical tasks
4. **Task Completion**: 100% completion rate for CRITICAL tasks
5. **Consensus Latency**: <5 seconds for 4-node BFT

### Functional Requirements
1. All 8 layers of EDGE-QI implemented and functional
2. Both algorithms (1 & 2) producing correct decisions
3. BFT consensus reaching agreement in >95% of cases
4. Real-time dashboard updates with <1 second latency
5. All 5 test scenarios passing validation metrics

### User Experience Requirements
1. Dashboard loads in <3 seconds
2. Video streams display within 2 seconds of node activation
3. Simulation controls respond within 500ms
4. Charts update smoothly without jank
5. No data loss during network interruptions

This comprehensive implementation blueprint provides everything needed to transform the EDGE-QI research paper into a fully functional, demonstrable system. The project showcases distributed edge computing, real-time optimization algorithms, and Byzantine fault tolerance in a realistic smart city traffic monitoring context.





---
Powered by [Claude Exporter](https://www.claudexporter.com)