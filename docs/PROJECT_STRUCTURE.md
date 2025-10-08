# EDGE-QI Framework - Project Structure

## 📁 Directory Structure

```
EDGE-QI/
├── 🚀 Core Entry Points
│   ├── edge_qi.py              # Unified launcher (NEW)
│   ├── main.py                 # Core EDGE-QI system
│   └── requirements.txt        # Dependencies
│
├── 📊 Dashboard & Visualization
│   ├── run_stable_dashboard.py      # Stable web dashboard
│   ├── ultra_fast_traffic.py        # Optimized traffic simulation
│   ├── performance_benchmark.py     # Performance comparison
│   └── App/
│       ├── dashboard.py             # Main dashboard logic
│       └── subscriber.py            # MQTT subscriber
│
├── 🧠 Core Framework
│   ├── communication/
│   │   └── mqtt_client.py          # MQTT communication
│   ├── monitor/
│   │   ├── energy_monitor.py       # Energy monitoring
│   │   └── network_monitor.py      # Network monitoring
│   ├── scheduler/
│   │   └── scheduler.py            # Task scheduling
│   ├── simulation/
│   │   ├── realtime_simulator.py   # Real-time data simulation
│   │   └── realtime_integrator.py  # Data integration pipeline
│   └── summarizer/
│       └── summarizer.py           # Data summarization
│
├── 🤖 Machine Learning
│   ├── tasks/
│   │   ├── base_task.py            # Base task interface
│   │   ├── temp_task.py            # Temperature sensing
│   │   ├── anomaly_task.py         # Anomaly detection
│   │   └── vision_task.py          # Computer vision
│   └── models/
│       ├── anomaly_detection/      # Anomaly models
│       └── temp_prediction/        # Temperature models
│
├── 🎯 Demonstrations
│   ├── demo_realtime_integration.py    # Real-time processing demo
│   ├── demo_headless_realtime.py       # Headless processing
│   ├── demo_anomaly_detection.py       # Anomaly detection demo
│   └── demo_bandwidth_optimization.py  # Bandwidth optimization
│
├── 🔧 Hardware Support
│   ├── jetson_nano/               # NVIDIA Jetson Nano support
│   └── raspberry_pi/              # Raspberry Pi support
│       └── sensors.py             # Sensor interfaces
│
├── 🧪 Testing & Documentation
│   ├── tests/                     # Comprehensive test suite
│   └── docs/                      # Documentation
│       ├── SYSTEM_BLOCK_DIAGRAM.md
│       ├── DASHBOARD.md
│       └── REALTIME_INTEGRATION_GUIDE.md
│
└── 📈 Reports & Analysis
    └── edge_qi_demo_report.json  # Demo execution reports
```

## 🚀 Quick Start Commands

### Unified Launcher (Recommended)
```bash
# Launch main system
python edge_qi.py core-system

# Launch dashboard
python edge_qi.py dashboard --port 8501

# Traffic simulation
python edge_qi.py traffic-sim --port 8502

# Headless demo
python edge_qi.py headless --duration 60

# Performance benchmark
python edge_qi.py benchmark

# Anomaly detection demo
python edge_qi.py anomaly-demo
```

### Direct Execution
```bash
# Core system
python main.py

# Stable dashboard
streamlit run run_stable_dashboard.py

# Ultra-fast traffic simulation
streamlit run ultra_fast_traffic.py --server.port 8502

# Headless processing
python demo_headless_realtime.py

# Performance comparison
streamlit run performance_benchmark.py --server.port 8503
```

## 📊 Component Status

### ✅ Fully Implemented
- Core scheduler and task management
- Energy and network monitoring  
- Real-time data simulation and integration
- MQTT communication
- Machine learning task pipeline
- Web-based dashboard with real-time visualization
- Traffic simulation with performance optimization
- Anomaly detection system
- Comprehensive demo applications

### 🚧 Partially Implemented
- Hardware abstraction layer
- Production deployment configurations
- Comprehensive test coverage

### 📋 Architecture Features
- **Modular Design**: Clear separation of concerns
- **Real-time Processing**: Sub-second latency for critical tasks
- **Scalable Architecture**: Multi-edge coordination support
- **Energy Aware**: Dynamic resource management
- **QoS Optimized**: Adaptive quality based on network conditions
- **ML Integrated**: Built-in machine learning pipeline
- **Web Dashboard**: Real-time monitoring and control
- **Hardware Agnostic**: Support for various edge devices
