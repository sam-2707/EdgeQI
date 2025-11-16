# 🚀 Start EDGE-QI Demo (No Camera Needed!)

**Perfect for presentations and testing without hardware!**

---

## ✅ What This Demo Does

Your backend now runs in **DEMO MODE** which means:

- ✅ **Real system monitoring** (CPU, memory, battery)
- ✅ **Real bandwidth optimization** (Algorithm 2 working)
- ✅ **Simulated traffic detections** (no camera needed!)
- ✅ **Real anomaly detection** (triggers on traffic spikes)
- ✅ **Live WebSocket updates** (every 2 seconds)

**You can demonstrate everything without connecting a camera!**

---

## 🏃 Quick Start (2 Minutes)

### Step 1: Install Dependencies (if needed)
```powershell
pip install fastapi uvicorn psutil python-socketio
```

**Optional (for full features):**
```powershell
pip install ultralytics torch opencv-python numpy
```

### Step 2: Start Backend
```powershell
cd src/backend
python server.py
```

**Expected Output:**
```
🚀 Starting EDGE-QI Backend Server...
✅ System Monitor initialized
✅ Anomaly Transmitter initialized
✅ Detection Service initialized
✅ Background tasks started (Demo mode - No camera needed)
🎬 Starting detection simulation (Demo mode - No camera needed)
✅ Server startup complete

INFO:     Uvicorn running on http://localhost:8000
```

### Step 3: Open API Docs
```
http://localhost:8000/docs
```

### Step 4: Watch Live Data
```
http://localhost:8000/health
```

---

## 🎬 Demo Mode Features

### Real System Metrics (Every 2 seconds)
- **CPU Usage**: Real percentage from your system
- **Memory Usage**: Actual GB used
- **Battery Level**: Real charge status
- **Network I/O**: Actual bandwidth

### Simulated Traffic Detection
The system generates **realistic traffic patterns**:

| Period | Frames | Vehicles | Behavior |
|--------|--------|----------|----------|
| Low Traffic | 0-30 | 3-8 | Normal transmission |
| Normal Traffic | 30-70 | 8-15 | Baseline establishment |
| Rush Hour | 70-100 | 20-40 | **Anomaly triggers!** |

### Bandwidth Optimization (Algorithm 2)
- Tracks vehicle counts in sliding window
- Calculates statistical baseline (mean, std dev)
- Detects anomalies using z-score (> 2.0σ)
- **Only transmits during anomalies**
- **Result: 60-80% bandwidth saved!**

---

## 📊 What You'll See

### Console Output:
```
🚗 Frame 15: 7 vehicles (Skipped - Normal traffic)
🚗 Frame 32: 12 vehicles (Skipped - Normal traffic)
🚗 Frame 75: 28 vehicles (Transmitted - High traffic anomaly)
🚗 Frame 76: 31 vehicles (Transmitted - High traffic anomaly)
🚗 Frame 95: 9 vehicles (Skipped - Normal traffic)
```

### WebSocket Events:
```javascript
// Broadcast every 2 seconds
{
  "cpu": 28.6,
  "memory": 88.6,
  "battery": 85,
  "detection": {
    "fps": 5.0,
    "frame_count": 150,
    "total_detections": 1800
  },
  "anomaly": {
    "frames_processed": 150,
    "frames_transmitted": 35,
    "bandwidth_saved_pct": 76.7
  }
}
```

### API Endpoints:
- `GET /health` - Service status
- `GET /api/system/metrics/real` - Real system metrics
- `GET /api/anomaly/stats` - Bandwidth savings
- `GET /api/detection/stats` - Detection statistics

---

## 🎯 Perfect for Demonstrations

### **30-Second Pitch:**
1. Start server: `python server.py`
2. Open http://localhost:8000/docs
3. Show real-time metrics updating
4. Explain: "Real system monitoring + Algorithm 2 working"

### **5-Minute Demo:**
1. Show `/health` endpoint - all services active
2. Show `/api/system/metrics/real` - real CPU/memory
3. Show `/api/anomaly/stats` - bandwidth savings
4. Watch console - see anomaly detection in action
5. Explain: "70%+ bandwidth saved by only transmitting anomalies"

### **15-Minute Full Demo:**
1. Start backend + frontend dashboard
2. Show real-time dashboard updates
3. Explain simulation vs real camera (same algorithms)
4. Show bandwidth savings accumulating
5. Explain z-score anomaly detection
6. Demo API endpoints interactively
7. Show WebSocket live updates

---

## 📈 Expected Performance

After **~100 frames** (20 seconds at 5 FPS):

| Metric | Expected Value |
|--------|---------------|
| **Frames Processed** | 100 |
| **Frames Transmitted** | 20-30 |
| **Bandwidth Saved** | **70-80%** ⭐ |
| **Anomalies Detected** | 5-10 |
| **CPU Usage** | 30-50% |
| **Memory** | 2-4 GB |

---

## 🔧 Configuration

### Change Simulation Speed
Edit `simulate_detection_stream()` in `server.py`:

```python
# Faster demo (10 FPS)
await asyncio.sleep(0.1)

# Slower demo (2 FPS)
await asyncio.sleep(0.5)
```

### Adjust Anomaly Threshold
Edit startup in `server.py`:

```python
anomaly_transmitter = AnomalyDrivenTransmitter(
    window_size=30,      # Baseline window size
    anomaly_threshold=2.0  # Lower = more sensitive
)
```

### Change Traffic Patterns
Edit `simulate_detection_stream()`:

```python
# More traffic
vehicle_count = random.randint(30, 60)

# Less traffic
vehicle_count = random.randint(1, 5)
```

---

## 🎊 Ready for Real Camera?

When you want to switch to a real camera:

### Option 1: USB Webcam
```python
# In startup_event(), replace simulate_detection_stream with:
async def process_real_camera():
    await detection_service.process_video_stream(
        source=0,  # Webcam
        callback=handle_detections,
        target_fps=5
    )

asyncio.create_task(process_real_camera())
```

### Option 2: Video File
```python
source="path/to/traffic_video.mp4"
```

### Option 3: IP Camera (RTSP)
```python
source="rtsp://admin:password@192.168.1.100:554/stream"
```

---

## 🐛 Troubleshooting

### "Module not found"
```powershell
pip install fastapi uvicorn psutil python-socketio
```

### "Port 8000 already in use"
```powershell
# Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### "Services not available"
- Server runs in mock mode (still works!)
- To enable real services: `pip install ultralytics torch`

### "Simulation not starting"
- Check console for errors
- Services need ~5 seconds to initialize
- Look for "🎬 Starting detection simulation"

---

## 📞 Quick Commands

**Start server:**
```powershell
cd src/backend
python server.py
```

**Test services:**
```powershell
python test_services.py
```

**Check health:**
```powershell
curl http://localhost:8000/health
```

**Get metrics:**
```powershell
curl http://localhost:8000/api/system/metrics/real
```

**Stop server:**
```
Ctrl + C
```

---

## 🎉 Success Indicators

✅ Server starts without errors  
✅ See "🎬 Starting detection simulation"  
✅ Console shows "🚗 Frame X: Y vehicles"  
✅ `/health` returns all services true  
✅ `/api/anomaly/stats` shows bandwidth saved  
✅ Dashboard (if running) updates every 2 seconds  

---

## 💡 Pro Tips

1. **Let it run for 30+ seconds** to establish baseline
2. **Watch console** for "Transmitted" vs "Skipped" 
3. **Check bandwidth savings** after 100 frames
4. **Open multiple browser tabs** to test WebSocket
5. **Use /docs** for interactive API testing

---

**🎊 You now have a fully functional demo without needing any camera! 🎊**

**Perfect for:**
- 📊 Class presentations
- 🎤 Conference demos
- 💼 Client meetings
- 🧪 Algorithm testing
- 📈 Performance benchmarking

**Start now:** `python server.py` ✨
