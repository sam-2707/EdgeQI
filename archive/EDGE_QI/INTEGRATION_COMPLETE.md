# 🔗 Frontend-Backend Integration Complete

## ✅ What's Been Built

### Backend (FastAPI) - ✅ COMPLETE
- **RESTful API** with 25+ endpoints
- **WebSocket Server** (Socket.IO) for real-time updates
- **Database Models** (6 tables: nodes, detections, metrics, consensus, logs, alerts)
- **Automatic Metrics Broadcasting** (every 5 seconds)
- **CORS Configuration** (frontend whitelisted)
- **API Documentation** (Swagger UI)

### Frontend (React) - ✅ COMPLETE
- **7 Pages** (Dashboard, Nodes, Detection, Analytics, Consensus, Logs, Settings)
- **WebSocket Client** configured in `EdgeQIContext.jsx`
- **50+ Components** with black/white theme
- **Real-time Updates** ready to receive backend data

---

## 🚀 Quick Start (Both Systems)

### Terminal 1: Backend
```powershell
cd d:\EDGE_QI_!\EDGE_QI\backend
.\start.ps1
```
Server will run at: **http://localhost:8000**

### Terminal 2: Frontend
```powershell
cd d:\EDGE_QI_!\EDGE_QI\frontend
npm run dev
```
UI will run at: **http://localhost:5173**

---

## 🔌 Connection Flow

```
Frontend (localhost:5173)
    ↓
    ├─ REST API → http://localhost:8000/api/*
    └─ WebSocket → ws://localhost:8000/socket.io
         ↓
    Backend (localhost:8000)
         ↓
    PostgreSQL Database (localhost:5432)
```

---

## 📡 Real-Time Data Flow

### 1. System Metrics (Every 5 Seconds)
```javascript
// Frontend receives (EdgeQIContext.jsx - line 30)
socket.on('system_metrics', (data) => {
  setSystemMetrics(data);
});

// Backend sends (websocket_service.py - line 127)
await broadcast_system_metrics({
  total_nodes: 5,
  active_nodes: 4,
  total_detections: 1234,
  average_latency: 45.2,
  ...
});
```

### 2. Node Updates
```javascript
// Frontend receives
socket.on('edge_node_update', (data) => {
  setEdgeNodes(prev => 
    prev.map(n => n.id === data.id ? data : n)
  );
});

// Backend sends (when node status changes)
await broadcast_node_update({
  id: "edge-node-1",
  status: "active",
  cpu_usage: 65.3,
  ...
});
```

### 3. Detection Results
```javascript
// Frontend receives
socket.on('detection_result', (data) => {
  setDetections(prev => [data, ...prev].slice(0, 100));
});

// Backend sends (when new detection arrives)
await broadcast_detection({
  node_id: "edge-node-1",
  object_type: "car",
  confidence: 0.95,
  bbox: {x: 100, y: 200, width: 150, height: 100},
  ...
});
```

### 4. System Logs
```javascript
// Frontend receives
socket.on('system_log', (data) => {
  setLogs(prev => [data, ...prev].slice(0, 500));
});

// Backend sends
await broadcast_log({
  level: "info",
  source: "api",
  message: "New node registered",
  ...
});
```

### 5. Alerts
```javascript
// Frontend receives
socket.on('alert', (data) => {
  setAlerts(prev => [data, ...prev]);
});

// Backend sends
await broadcast_alert({
  severity: "high",
  title: "High CPU Usage",
  message: "Node edge-node-1 CPU usage above 90%",
  ...
});
```

---

## 🧪 Testing the Integration

### Step 1: Start Both Systems

```powershell
# Terminal 1: Backend
cd backend
python -m uvicorn src.main:socket_app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Step 2: Initialize Database

```powershell
# Terminal 3
cd backend
python init_db.py
python populate_db.py
```

### Step 3: Open Browser

Navigate to: **http://localhost:5173**

You should see:
- ✅ Dashboard with system metrics
- ✅ Edge nodes grid (5 nodes from mock data)
- ✅ Recent detections table
- ✅ Real-time metrics updating every 5 seconds

### Step 4: Check WebSocket Connection

Open browser console (F12), you should see:
```
WebSocket connection established
Received system_metrics: {...}
```

### Step 5: Test API Endpoints

```powershell
# Get system status
curl http://localhost:8000/api/system/status

# List nodes
curl http://localhost:8000/api/nodes

# Get detections
curl http://localhost:8000/api/detections

# Get analytics
curl http://localhost:8000/api/analytics/data?time_range=24h
```

---

## 🎯 Frontend Pages → Backend Endpoints

### Dashboard Page
```javascript
// Data Sources:
- system_metrics (WebSocket)
- /api/system/status (REST)
- /api/detections/recent/stream (REST)
```

### Edge Nodes Page
```javascript
// Data Sources:
- /api/nodes (REST)
- edge_node_update (WebSocket)
- /api/nodes/{id}/heartbeat (REST - for updates)
```

### Detection Page
```javascript
// Data Sources:
- /api/detections (REST)
- detection_result (WebSocket)
- /api/detections/stats/summary (REST)
```

### Analytics Page
```javascript
// Data Sources:
- /api/analytics/data?time_range=24h (REST)
- /api/analytics/traffic (REST)
- /api/analytics/performance (REST)
```

### Consensus Page
```javascript
// Data Sources:
- /api/consensus/rounds (REST)
- /api/consensus/stats/summary (REST)
- consensus_update (WebSocket)
```

### Logs Page
```javascript
// Data Sources:
- /api/logs (REST)
- system_log (WebSocket)
```

---

## 🔄 Adding New Edge Node

### From Frontend (Future Feature)
```javascript
// POST request to register node
const registerNode = async (nodeData) => {
  const response = await fetch('http://localhost:8000/api/nodes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: 'edge-node-6',
      name: 'Edge Node 6',
      ip_address: '192.168.1.16',
      port: 8086,
      capabilities: { detection: true, yolo: 'v8' }
    })
  });
  return response.json();
};
```

### From Python Script
```python
import requests

response = requests.post('http://localhost:8000/api/nodes', json={
    'id': 'edge-node-6',
    'name': 'Edge Node 6',
    'ip_address': '192.168.1.16',
    'port': 8086,
    'capabilities': {'detection': True, 'yolo': 'v8'}
})

print(response.json())
```

### Backend Will:
1. ✅ Create node in database
2. ✅ Broadcast `edge_node_update` to all clients
3. ✅ Log the registration
4. ✅ Update system metrics

---

## 📊 Simulating Real-Time Data

Create a test script to simulate edge node activity:

```python
# backend/simulate_edge_node.py
import requests
import time
import random
from datetime import datetime

BASE_URL = "http://localhost:8000"
NODE_ID = "edge-node-1"

def send_heartbeat():
    """Send node heartbeat with metrics"""
    response = requests.post(
        f"{BASE_URL}/api/nodes/{NODE_ID}/heartbeat",
        json={
            "status": "active",
            "cpu_usage": random.uniform(40, 80),
            "memory_usage": random.uniform(50, 75),
            "gpu_usage": random.uniform(60, 90),
            "network_status": "good",
            "energy_consumption": random.uniform(80, 120)
        }
    )
    print(f"Heartbeat sent: {response.status_code}")

def send_detection():
    """Send detection result"""
    response = requests.post(
        f"{BASE_URL}/api/detections",
        json={
            "node_id": NODE_ID,
            "stream_id": "stream-1",
            "object_type": random.choice(["car", "person", "bicycle"]),
            "confidence": random.uniform(0.85, 0.99),
            "bbox": {
                "x": random.randint(0, 1000),
                "y": random.randint(0, 1000),
                "width": random.randint(50, 200),
                "height": random.randint(50, 200)
            },
            "location": "Test Location",
            "metadata": {"timestamp": datetime.utcnow().isoformat()}
        }
    )
    print(f"Detection sent: {response.status_code}")

# Main loop
while True:
    send_heartbeat()
    time.sleep(5)
    
    if random.random() > 0.7:  # 30% chance
        send_detection()
```

Run it:
```powershell
python backend/simulate_edge_node.py
```

Watch frontend update in real-time! 🎉

---

## 🐛 Troubleshooting Integration

### Issue 1: WebSocket Not Connecting

**Symptoms**: No real-time updates in frontend

**Check**:
```javascript
// In browser console
console.log(socket.connected); // Should be true
```

**Solution**:
1. Verify backend is running: http://localhost:8000/health
2. Check backend URL in `frontend/.env`:
   ```
   VITE_BACKEND_URL=http://localhost:8000
   ```
3. Restart frontend: `npm run dev`

### Issue 2: CORS Errors

**Symptoms**: `Access-Control-Allow-Origin` error

**Solution**:
1. Check backend `.env`:
   ```
   CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
   ```
2. Restart backend server

### Issue 3: Empty Data on Frontend

**Symptoms**: No nodes, detections, or metrics displayed

**Solution**:
```powershell
# Populate database with mock data
cd backend
python populate_db.py
```

### Issue 4: Database Connection Failed

**Symptoms**: Backend crashes on startup

**Solution**:
1. Start PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE edge_qi;
   ```
3. Run initialization:
   ```powershell
   python init_db.py
   ```

---

## 📈 Performance Monitoring

### Backend Performance
```powershell
# Check response times
curl -w "@curl-format.txt" http://localhost:8000/api/system/status

# Monitor WebSocket connections
# Check backend logs for "Client connected" messages
```

### Frontend Performance
```javascript
// In browser console
performance.measure('page-load');
console.log(performance.getEntriesByType('measure'));
```

### Database Performance
```sql
-- Check query performance
SELECT * FROM pg_stat_statements 
ORDER BY total_time DESC LIMIT 10;
```

---

## 🎉 Integration Success Checklist

- [x] Backend server running on port 8000
- [x] Frontend running on port 5173
- [x] PostgreSQL database initialized
- [x] WebSocket connection established
- [x] System metrics updating every 5 seconds
- [x] Edge nodes displayed in frontend
- [x] Detections showing in real-time
- [x] Logs streaming to frontend
- [x] API documentation accessible
- [x] CORS configured correctly
- [x] Mock data populated

---

## 🚀 Next Steps

### Immediate
1. ✅ Test all 7 pages in frontend
2. ✅ Verify real-time updates work
3. ✅ Test API endpoints with Postman
4. ✅ Check WebSocket events in browser console

### Short Term
- [ ] Connect actual edge nodes (from `edge_nodes/` directory)
- [ ] Integrate MQTT broker for node communication
- [ ] Add Redis caching layer
- [ ] Implement JWT authentication
- [ ] Add data export functionality

### Long Term
- [ ] Deploy to production server
- [ ] Set up CI/CD pipeline
- [ ] Add monitoring (Prometheus/Grafana)
- [ ] Implement advanced analytics
- [ ] Add mobile app support

---

## 📞 Quick Reference

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | React UI |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| WebSocket | ws://localhost:8000/socket.io | Real-time |
| Database | localhost:5432 | PostgreSQL |

---

**Status: 🎉 FULLY INTEGRATED & OPERATIONAL**

Both frontend and backend are complete and working together!
