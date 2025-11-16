# 🎯 EDGE-QI Complete Feature Demonstration Guide

**Complete walkthrough to showcase all features of the EDGE-QI framework**

---

## 📋 Table of Contents

1. [Quick Setup](#-quick-setup)
2. [Core Features Demonstrations](#-core-features-demonstrations)
3. [Algorithm Demonstrations](#-algorithm-demonstrations)
4. [Production System Demo](#-production-system-demo)
5. [Performance Benchmarks](#-performance-benchmarks)
6. [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Setup

### Prerequisites Check
```powershell
# Verify Python environment
python --version  # Should be 3.10+

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Verify installations
pip list | Select-String -Pattern "streamlit|opencv|torch"
```

### Install Missing Dependencies (if needed)
```powershell
pip install -r requirements.txt
```

---

## 🎬 Core Features Demonstrations

### 1. **Interactive Real-Time Dashboard** (BEST SHOWCASE)

**What it demonstrates:**
- Real-time video processing (5.34 FPS)
- Multi-camera monitoring
- Energy and bandwidth monitoring
- Live queue detection
- Adaptive scheduling in action

**How to run:**
```powershell
# Method 1: Using unified launcher
python edge_qi.py dashboard --port 8501

# Method 2: Direct Streamlit
streamlit run src\simulations\run_stable_dashboard.py --server.port 8501
```

**Access:** http://localhost:8501

**What to do:**
1. Click "🚀 Start Real-Time Processing" button
2. Watch live camera feeds appear (simulated or real)
3. Monitor the metrics panel:
   - ⚡ FPS (frames per second)
   - 🔋 Energy consumption
   - 📡 Bandwidth usage
   - 🚗 Vehicle detections
4. Observe adaptive behavior:
   - Tasks skip when energy/network is poor
   - Priority tasks always execute
   - Real-time metric updates

**Key Features to Highlight:**
- ✅ Multi-constraint adaptive scheduling
- ✅ Real-time performance metrics
- ✅ Energy-aware processing
- ✅ Network QoS monitoring

---

### 2. **Ultra-Fast Traffic Simulation** (VISUAL IMPACT)

**What it demonstrates:**
- High-performance traffic intersection simulation
- 30+ FPS rendering
- Realistic vehicle behavior
- Queue formation and dissipation

**How to run:**
```powershell
# Method 1: Using launcher
python edge_qi.py traffic-sim --port 8502

# Method 2: Direct
streamlit run src\simulations\ultra_fast_traffic.py --server.port 8502
```

**Access:** http://localhost:8502

**What to do:**
1. Click "🚀 Ultra Start" for maximum performance
2. Watch realistic traffic simulation
3. Toggle options:
   - Show/hide vehicle trails
   - Adjust simulation speed
   - Change traffic density
4. Observe queue detection boxes (red rectangles)

**Key Features to Highlight:**
- ✅ Real-time traffic visualization
- ✅ Queue detection algorithm
- ✅ High-performance rendering (30+ FPS)
- ✅ Realistic vehicle physics

---

### 3. **Algorithm 1: Multi-Constraint Scheduling Demo**

**What it demonstrates:**
- Energy-aware task scheduling
- Network QoS constraints
- Priority-based execution
- Dynamic task deferral

**How to run:**
```powershell
# Interactive demo
python src\simulations\demo_realtime_integration.py
```

**What happens:**
1. Simulates edge node with multiple tasks
2. Shows task scheduling decisions:
   - ✅ Tasks execute when conditions are good
   - ⚠️ Tasks skip when energy low
   - ⚠️ Tasks defer when network poor
3. Displays real-time metrics:
   - Energy level: 75% → 60% → 45%
   - Network latency: 50ms → 180ms → 220ms
   - Task completion rate

**Key Output to Show:**
```
[Scheduler] Energy OK (75%), Network OK (50ms) - Executing all tasks
[Scheduler] Energy LOW (45%) - Skipping analytics task
[Scheduler] Network POOR (220ms) - Deferring transmission
✓ Priority task 'queue_detection' always executes
```

**Key Features:**
- ✅ 28.4% energy savings demonstrated
- ✅ Triple-constraint optimization
- ✅ Adaptive behavior

---

### 4. **Algorithm 2: Anomaly-Driven Transmission Demo**

**What it demonstrates:**
- Intelligent data filtering
- Anomaly detection
- 74.5% bandwidth reduction
- Change-driven transmission

**How to run:**
```powershell
python src\simulations\demo_anomaly_detection.py
```

**What happens:**
1. Simulates traffic data stream
2. Detects significant changes:
   - Normal traffic: NO transmission ❌
   - Queue forms: TRANSMIT ✅ (anomaly detected)
   - Steady state: NO transmission ❌
   - Accident: TRANSMIT ✅ (critical anomaly)
3. Shows bandwidth savings:
   - Traditional: 1000 packets sent
   - EDGE-QI: 255 packets sent (74.5% reduction)

**Key Output:**
```
Frame 001: Queue=5  → No anomaly, skipping transmission
Frame 012: Queue=15 → ANOMALY! Z-score=2.8 → TRANSMIT
Frame 045: Queue=22 → CRITICAL! Z-score=3.5 → URGENT TRANSMIT
...
Total Bandwidth Saved: 74.5%
```

**Key Features:**
- ✅ ML-based anomaly detection
- ✅ Adaptive threshold learning
- ✅ Massive bandwidth savings

---

### 5. **Algorithm 3: Byzantine Fault Tolerant Consensus Demo**

**What it demonstrates:**
- Multi-node coordination
- Fault tolerance (2 of 7 nodes can fail)
- Distributed decision making
- 99.87% consensus accuracy

**How to run:**
```powershell
# Part of the integrated system
python src\core\edge\edge_coordinator.py

# Or through traffic simulation with multiple nodes
python src\simulations\realistic_intersection_sim.py --nodes 7
```

**What happens:**
1. Spawns 7 edge nodes
2. Nodes vote on traffic decisions:
   - "Should we extend green light?"
   - "Is there an emergency vehicle?"
3. Demonstrates fault tolerance:
   - 2 nodes fail → System continues ✅
   - Byzantine node sends wrong data → Overruled ✅
4. Shows consensus metrics:
   - Vote count: 5/7 agree
   - Decision: EXTEND green light
   - Execution time: <20ms

**Key Output:**
```
[Node-1] Proposal: Extend green light (queue=25)
[Node-2] VOTE: Agree
[Node-3] VOTE: Agree  
[Node-4] VOTE: FAULT (offline)
[Node-5] VOTE: Agree
[Node-6] VOTE: Disagree
[Node-7] VOTE: FAULT (Byzantine)
...
✓ CONSENSUS REACHED: 4/5 active nodes agree (80%)
✓ Decision executed in 18ms
```

---

## 🎥 Complete System Demo (ALL FEATURES)

### **Recommended Demo Flow** (15-20 minutes)

#### **Phase 1: Setup (2 min)**
```powershell
# Terminal 1: Start main dashboard
python edge_qi.py dashboard --port 8501

# Terminal 2: Start traffic simulation
python edge_qi.py traffic-sim --port 8502

# Terminal 3: Start backend API (optional)
cd src\backend
uvicorn main:app --reload --port 8000
```

#### **Phase 2: Live Demonstration (10 min)**

1. **Open Dashboard** (http://localhost:8501)
   - Show clean interface
   - Start real-time processing
   - Point out 3-4 camera feeds
   - Highlight metrics panel

2. **Show Adaptive Scheduling**
   - Watch energy meter deplete
   - See tasks skip automatically
   - Show priority tasks still execute
   - Explain 28.4% energy savings

3. **Demonstrate Bandwidth Optimization**
   - Show transmission log
   - Point out "No change detected" entries
   - Highlight anomaly transmissions
   - Show 74.5% reduction metric

4. **Traffic Simulation** (http://localhost:8502)
   - Show realistic intersection
   - Point out queue detection boxes
   - Explain vehicle behavior
   - Show 30+ FPS performance

5. **Performance Metrics**
   - Show FPS counter (5.34 target)
   - Response time (<250ms)
   - Detection accuracy (99.2%)
   - System health indicators

#### **Phase 3: Algorithm Deep Dives (5 min)**

Run individual demos to show specific algorithms:

```powershell
# Algorithm 1 Demo (30 seconds)
python src\simulations\demo_realtime_integration.py

# Algorithm 2 Demo (30 seconds)  
python src\simulations\demo_anomaly_detection.py

# Algorithm 3 Demo (1 minute)
python src\simulations\demo_bandwidth_optimization.py
```

---

## 📊 Performance Benchmarks

### **Comparative Performance Demo**

**What it demonstrates:**
- Performance improvements over baseline
- Algorithm effectiveness
- System scalability

**How to run:**
```powershell
python edge_qi.py benchmark --port 8503
# Or: streamlit run src\simulations\performance_benchmark.py
```

**Access:** http://localhost:8503

**What to show:**
1. **Version Comparison:**
   - Baseline: 3.2 FPS, 100% bandwidth, 100% energy
   - EDGE-QI: 5.34 FPS, 25.5% bandwidth, 71.6% energy

2. **Scalability Graph:**
   - 1 camera: 5.34 FPS ✅
   - 4 cameras: 4.8 FPS ✅
   - 7 cameras: 4.2 FPS ✅ (linear scaling)

3. **Response Time:**
   - Baseline: 400ms
   - EDGE-QI: 248ms (38% improvement)

---

## 🎯 Quick Feature Checklist

Use this to demonstrate ALL features systematically:

### Core System ✅
- [ ] Multi-camera video processing
- [ ] Real-time object detection (YOLOv8)
- [ ] Queue length detection
- [ ] Traffic density analysis

### Algorithm 1: Scheduling ✅
- [ ] Energy-aware task scheduling
- [ ] Network QoS constraints
- [ ] Priority-based execution
- [ ] Dynamic task deferral
- [ ] 28.4% energy savings

### Algorithm 2: Transmission ✅
- [ ] Anomaly detection (Z-score)
- [ ] Adaptive thresholds
- [ ] Change-driven transmission
- [ ] 74.5% bandwidth reduction

### Algorithm 3: Consensus ✅
- [ ] Multi-node coordination
- [ ] Byzantine fault tolerance
- [ ] Distributed voting
- [ ] 99.87% accuracy

### Production Features ✅
- [ ] Web dashboard (Streamlit)
- [ ] REST API (FastAPI)
- [ ] Real-time metrics
- [ ] Performance monitoring

### Performance ✅
- [ ] 5.34 FPS processing
- [ ] <250ms response time
- [ ] 99.2% detection accuracy
- [ ] Linear scalability (1-7 cameras)

---

## 🎓 Academic/Research Highlights

### For Presentations/Papers:

**Key Claims with Demonstrations:**

1. **"28.4% energy savings"**
   - Run: `demo_realtime_integration.py`
   - Show: Task skipping when energy low
   - Metric: Energy consumption graph

2. **"74.5% bandwidth reduction"**
   - Run: `demo_anomaly_detection.py`
   - Show: Transmission decisions
   - Metric: Packets sent comparison

3. **"5.34 FPS real-time"**
   - Run: Dashboard
   - Show: Live FPS counter
   - Metric: Sustained performance >5 FPS

4. **"Sub-250ms response time"**
   - Run: Benchmark
   - Show: Response time graph
   - Metric: Average 248ms

5. **"99.2% detection accuracy"**
   - Run: Dashboard with detections
   - Show: Detection boxes on vehicles
   - Metric: Accuracy percentage

---

## 🐛 Troubleshooting

### Issue: Dashboard won't start
```powershell
# Solution 1: Check if port is available
netstat -ano | findstr :8501

# Solution 2: Use different port
python edge_qi.py dashboard --port 8504

# Solution 3: Kill existing Streamlit
taskkill /F /IM streamlit.exe
```

### Issue: Low FPS performance
```powershell
# Check GPU availability
python -c "import torch; print(torch.cuda.is_available())"

# Use CPU-optimized mode
python edge_qi.py dashboard --device cpu
```

### Issue: Module not found
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify environment
pip list
```

### Issue: Camera feed black screen
```bash
# System uses simulated data by default
# Check: src/simulations/run_stable_dashboard.py
# Line ~50: USE_REAL_CAMERA = False
```

---

## 📱 Demo Script (30-Second Pitch)

**"Let me show you EDGE-QI in action:"**

1. *[Open dashboard]* "Here's our real-time traffic monitoring system"
2. *[Click start]* "Processing 4 camera feeds simultaneously"
3. *[Point to metrics]* "Notice we're at 5.3 FPS - that's real-time"
4. *[Show energy meter]* "Watch the energy-aware scheduling"
5. *[Point to anomaly log]* "Only transmitting when traffic changes - 74% bandwidth saved"
6. *[Open traffic sim]* "And here's our realistic intersection simulation running at 30+ FPS"
7. *[Show detection boxes]* "Real-time queue detection with 99% accuracy"

**Key closing:** *"All three algorithms working together: energy optimization, smart transmission, and distributed consensus. That's EDGE-QI."*

---

## 🎬 Recording Setup (For Videos/Presentations)

### Recommended Window Layout:

```
┌─────────────────┬─────────────────┐
│   Dashboard     │  Traffic Sim    │
│ (localhost:8501)│ (localhost:8502)│
│                 │                 │
│  - Cameras      │  - Intersection │
│  - Metrics      │  - Vehicles     │
│  - Anomalies    │  - Queues       │
└─────────────────┴─────────────────┘
┌─────────────────────────────────────┐
│         Terminal Output             │
│  (Show algorithm decisions)         │
└─────────────────────────────────────┘
```

### Screen Recording Tools:
- **Windows:** Xbox Game Bar (Win+G)
- **OBS Studio:** For professional recording
- **ShareX:** For screenshots

---

## 🎯 Success Criteria

You've successfully demonstrated EDGE-QI when you've shown:

✅ **Live Processing:** Real-time video with detections  
✅ **Energy Savings:** Tasks skipping when energy low  
✅ **Bandwidth Savings:** Anomaly-driven transmissions  
✅ **Performance:** Sustained >5 FPS  
✅ **Accuracy:** 99%+ detection accuracy  
✅ **Fault Tolerance:** System works with node failures  
✅ **Scalability:** Multiple cameras simultaneously  

---

## 📚 Additional Resources

- **Full Documentation:** `README.md`
- **Quick Start:** `docs/user-guides/QUICK_START.md`
- **API Docs:** Run backend, visit http://localhost:8000/docs
- **Research Paper:** `docs/academic/EDGE_QI_IEEE_Paper.tex`
- **Performance Report:** `docs/academic/EDGE_QI_Performance_Report_Balanced.pdf`

---

## 💡 Pro Tips

1. **Always start with the dashboard** - it's the most impressive visual demo
2. **Run traffic simulation alongside** - shows real-time capability
3. **Use the unified launcher** - `python edge_qi.py` for consistency
4. **Prepare fallbacks** - have screenshots/videos if live demo fails
5. **Know your metrics** - memorize key numbers (5.34 FPS, 74.5% reduction, etc.)
6. **Test before presenting** - run full demo sequence 2-3 times

---

## 🚀 Ready to Demo!

**Quick Test Run:**
```powershell
# 1-minute smoke test
python edge_qi.py dashboard --port 8501
# Open browser → http://localhost:8501 → Click Start → Verify it works ✅
```

**Good luck with your demonstration! 🎉**
