# 🚀 EDGE-QI Improvement Plan & Backend Integration

## 📊 Current Status

### ✅ **Completed**
- **Frontend**: 100% Complete - Professional React dashboard
- **Edge Nodes**: Core algorithms and 8-layer architecture
- **ML Models**: YOLOv8 training and quantization
- **Infrastructure**: Docker compose with MQTT, TimescaleDB, Redis

### ⚠️ **Missing/Incomplete**
- **Backend API**: FastAPI server needs to be implemented
- **Backend-Frontend Integration**: WebSocket connections not established
- **Database Models**: Need Pydantic/SQLAlchemy models
- **API Endpoints**: REST endpoints not created
- **Authentication**: No auth system implemented

---

## 🎯 Frontend Improvements

### **Priority 1: Critical Enhancements**

#### 1. TypeScript Migration
**Why**: Type safety, better IDE support, fewer runtime errors
```bash
# Current: JavaScript (.jsx)
# Proposed: TypeScript (.tsx)

# Benefits:
- Type checking at compile time
- Better IntelliSense
- Easier refactoring
- Self-documenting code
```

**Implementation**:
```typescript
// Example: EdgeQIContext.tsx
interface SystemMetrics {
  totalNodes: number;
  activeNodes: number;
  totalDetections: number;
  averageLatency: number;
  bandwidthSaved: number;
  energySaved: number;
}

interface EdgeNode {
  id: string;
  status: 'active' | 'idle' | 'fault';
  cpuUsage: number;
  memoryUsage: number;
  networkStatus: string;
  energyConsumption: number;
}
```

#### 2. Advanced State Management
**Why**: Better performance, easier debugging, predictable state
```bash
# Options:
1. Zustand (Recommended) - Lightweight, simple
2. Redux Toolkit - Full-featured
3. Jotai - Atomic state management
```

**Implementation with Zustand**:
```typescript
// stores/systemStore.ts
import create from 'zustand';

interface SystemStore {
  metrics: SystemMetrics;
  nodes: EdgeNode[];
  detections: Detection[];
  updateMetrics: (metrics: SystemMetrics) => void;
  addDetection: (detection: Detection) => void;
}

export const useSystemStore = create<SystemStore>((set) => ({
  metrics: initialMetrics,
  nodes: [],
  detections: [],
  updateMetrics: (metrics) => set({ metrics }),
  addDetection: (detection) => 
    set((state) => ({ 
      detections: [detection, ...state.detections].slice(0, 100) 
    })),
}));
```

#### 3. Error Boundary Components
**Why**: Graceful error handling, better UX
```typescript
// components/ErrorBoundary.tsx
class ErrorBoundary extends React.Component<Props, State> {
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to error tracking service (Sentry, LogRocket)
    logErrorToService(error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

### **Priority 2: Performance Optimizations**

#### 1. Virtual Scrolling for Large Lists
**Why**: Handle thousands of logs/detections efficiently
```typescript
// Using react-window
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={logs.length}
  itemSize={50}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>
      {logs[index]}
    </div>
  )}
</FixedSizeList>
```

#### 2. Chart Data Aggregation
**Why**: Better performance with large datasets
```typescript
// Aggregate data points for better chart performance
const aggregateData = (data: DataPoint[], bucketSize: number) => {
  return data.reduce((acc, point, index) => {
    if (index % bucketSize === 0) {
      acc.push(point);
    }
    return acc;
  }, []);
};
```

#### 3. Web Workers for Heavy Computations
**Why**: Keep UI thread responsive
```typescript
// workers/dataProcessor.worker.ts
self.onmessage = (e) => {
  const processedData = processLargeDataset(e.data);
  self.postMessage(processedData);
};
```

### **Priority 3: User Experience**

#### 1. Advanced Filtering & Search
```typescript
// Multi-field search with debouncing
const useAdvancedSearch = () => {
  const [filters, setFilters] = useState({
    search: '',
    dateRange: [startDate, endDate],
    status: [],
    types: [],
  });
  
  const debouncedSearch = useDebouncedValue(filters.search, 300);
  
  const filteredData = useMemo(() => {
    return data.filter(item => 
      matchesAllFilters(item, filters)
    );
  }, [data, debouncedSearch, filters]);
  
  return { filteredData, filters, setFilters };
};
```

#### 2. Data Export in Multiple Formats
```typescript
// Export to CSV, JSON, Excel, PDF
const exportData = (data: any[], format: 'csv' | 'json' | 'xlsx' | 'pdf') => {
  switch (format) {
    case 'csv':
      return exportToCSV(data);
    case 'json':
      return exportToJSON(data);
    case 'xlsx':
      return exportToExcel(data);
    case 'pdf':
      return exportToPDF(data);
  }
};
```

#### 3. Customizable Dashboards
```typescript
// Drag-and-drop dashboard widgets
import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

<ResponsiveGridLayout
  layouts={layouts}
  onLayoutChange={saveLayout}
  draggableHandle=".drag-handle"
>
  <div key="metrics">
    <MetricsCard />
  </div>
  <div key="chart">
    <PerformanceChart />
  </div>
</ResponsiveGridLayout>
```

### **Priority 4: Advanced Features**

#### 1. Real-time Collaboration
```typescript
// Using WebRTC or SharedWorker for multi-user
const useCollaboration = () => {
  const [activeUsers, setActiveUsers] = useState([]);
  const [sharedCursor, setSharedCursor] = useState(null);
  
  useEffect(() => {
    // Broadcast cursor position
    socket.emit('cursor-move', cursorPosition);
    
    // Listen for other users
    socket.on('user-cursor', (data) => {
      setSharedCursor(data);
    });
  }, []);
};
```

#### 2. Advanced Alerting System
```typescript
// Rule-based alerting with conditions
interface AlertRule {
  id: string;
  name: string;
  condition: (metrics: SystemMetrics) => boolean;
  severity: 'low' | 'medium' | 'high' | 'critical';
  action: 'notify' | 'email' | 'webhook';
  cooldown: number; // minutes
}

const alertRules: AlertRule[] = [
  {
    id: 'high-cpu',
    name: 'High CPU Usage',
    condition: (m) => m.avgCpuUsage > 90,
    severity: 'high',
    action: 'notify',
    cooldown: 5,
  },
];
```

#### 3. Historical Playback
```typescript
// Time-travel through historical data
const useHistoricalPlayback = () => {
  const [currentTime, setCurrentTime] = useState(Date.now());
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  
  const data = useMemo(() => 
    getDataAtTimestamp(currentTime),
    [currentTime]
  );
  
  return { data, currentTime, isPlaying, controls };
};
```

### **Priority 5: Testing & Quality**

#### 1. Unit Tests
```typescript
// __tests__/components/Dashboard.test.tsx
import { render, screen } from '@testing-library/react';
import Dashboard from '../Dashboard';

describe('Dashboard', () => {
  it('displays system metrics', () => {
    render(<Dashboard />);
    expect(screen.getByText(/Active Nodes/i)).toBeInTheDocument();
  });
  
  it('updates metrics in real-time', async () => {
    const { rerender } = render(<Dashboard />);
    // Test WebSocket updates
  });
});
```

#### 2. E2E Tests
```typescript
// e2e/dashboard.spec.ts
import { test, expect } from '@playwright/test';

test('dashboard loads and displays data', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await expect(page.locator('.metric-card')).toHaveCount(4);
  await expect(page.locator('canvas')).toBeVisible(); // Charts
});
```

#### 3. Performance Monitoring
```typescript
// Add performance monitoring
import { onLCP, onFID, onCLS } from 'web-vitals';

onLCP(console.log);
onFID(console.log);
onCLS(console.log);

// Or use services like:
// - Vercel Analytics
// - Google Analytics 4
// - New Relic
// - Datadog RUM
```

---

## 🔧 Backend Implementation Plan

### **Phase 1: FastAPI Server Setup**

#### 1. Project Structure
```
backend/
├── src/
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # Configuration
│   ├── database.py             # DB connection
│   ├── dependencies.py         # DI helpers
│   │
│   ├── models/                 # Database models
│   │   ├── node.py
│   │   ├── detection.py
│   │   ├── consensus.py
│   │   └── log.py
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── node.py
│   │   ├── detection.py
│   │   └── metrics.py
│   │
│   ├── routers/                # API endpoints
│   │   ├── system.py           # /api/system/*
│   │   ├── nodes.py            # /api/nodes/*
│   │   ├── detection.py        # /api/detections/*
│   │   ├── analytics.py        # /api/analytics/*
│   │   └── websocket.py        # WebSocket handler
│   │
│   ├── services/               # Business logic
│   │   ├── node_service.py
│   │   ├── detection_service.py
│   │   ├── consensus_service.py
│   │   └── mqtt_service.py
│   │
│   └── utils/                  # Helper functions
│       ├── logger.py
│       ├── cache.py
│       └── validators.py
│
├── tests/
│   ├── test_api.py
│   ├── test_services.py
│   └── test_websocket.py
│
├── requirements.txt
├── .env.example
└── README.md
```

#### 2. Main Application (main.py)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import socketio

# Create FastAPI app
app = FastAPI(
    title="EDGE-QI API",
    description="Backend for EDGE-QI Smart City Platform",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Socket.IO setup
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
)

socket_app = socketio.ASGIApp(sio, app)

# Import routers
from src.routers import system, nodes, detection, analytics, websocket

# Register routes
app.include_router(system.router, prefix="/api/system", tags=["system"])
app.include_router(nodes.router, prefix="/api/nodes", tags=["nodes"])
app.include_router(detection.router, prefix="/api/detections", tags=["detection"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

# WebSocket events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('connection_established', {'status': 'connected'}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    # Initialize database
    await init_db()
    # Connect to MQTT
    await connect_mqtt()
    # Start background tasks
    asyncio.create_task(metrics_broadcaster())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:socket_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

#### 3. Database Models (models/node.py)
```python
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class EdgeNode(Base):
    __tablename__ = "edge_nodes"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, default="idle")  # active, idle, fault
    location = Column(String)
    
    # Resource metrics
    cpu_usage = Column(Float, default=0.0)
    memory_usage = Column(Float, default=0.0)
    network_status = Column(String, default="good")
    energy_consumption = Column(Float, default=0.0)
    
    # Metadata
    ip_address = Column(String)
    port = Column(Integer)
    capabilities = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_heartbeat = Column(DateTime)
```

#### 4. Pydantic Schemas (schemas/node.py)
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class NodeBase(BaseModel):
    id: str
    name: str
    status: str = "idle"
    location: Optional[str] = None

class NodeCreate(NodeBase):
    ip_address: str
    port: int
    capabilities: dict

class NodeUpdate(BaseModel):
    status: Optional[str] = None
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    network_status: Optional[str] = None
    energy_consumption: Optional[float] = None

class Node(NodeBase):
    cpu_usage: float
    memory_usage: float
    network_status: str
    energy_consumption: float
    last_heartbeat: Optional[datetime]
    
    class Config:
        orm_mode = True
```

#### 5. API Endpoints (routers/system.py)
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import SystemMetrics
from ..services import system_service

router = APIRouter()

@router.get("/status", response_model=SystemMetrics)
async def get_system_status(db: Session = Depends(get_db)):
    """Get overall system metrics"""
    return await system_service.get_system_metrics(db)

@router.get("/health")
async def system_health():
    """System health check"""
    return {
        "database": await check_db_health(),
        "mqtt": await check_mqtt_health(),
        "redis": await check_redis_health(),
    }

@router.get("/nodes/summary")
async def get_nodes_summary(db: Session = Depends(get_db)):
    """Get node statistics"""
    return await system_service.get_node_summary(db)
```

#### 6. WebSocket Broadcasting (services/websocket_service.py)
```python
import asyncio
from typing import Dict, Any

class WebSocketService:
    def __init__(self, sio):
        self.sio = sio
        
    async def broadcast_system_metrics(self, metrics: Dict[str, Any]):
        """Broadcast system metrics to all connected clients"""
        await self.sio.emit('system_metrics', metrics)
    
    async def broadcast_node_update(self, node_data: Dict[str, Any]):
        """Broadcast node status update"""
        await self.sio.emit('edge_node_update', node_data)
    
    async def broadcast_detection(self, detection: Dict[str, Any]):
        """Broadcast new detection result"""
        await self.sio.emit('detection_result', detection)
    
    async def broadcast_log(self, log_entry: Dict[str, Any]):
        """Broadcast system log"""
        await self.sio.emit('system_log', log_entry)
    
    async def metrics_broadcaster(self):
        """Background task to broadcast metrics every 5 seconds"""
        while True:
            try:
                metrics = await self.get_current_metrics()
                await self.broadcast_system_metrics(metrics)
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Error broadcasting metrics: {e}")
                await asyncio.sleep(5)
```

#### 7. MQTT Integration (services/mqtt_service.py)
```python
import paho.mqtt.client as mqtt
from typing import Callable

class MQTTService:
    def __init__(self, broker_host: str, broker_port: int):
        self.client = mqtt.Client()
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.callbacks = {}
        
    def connect(self):
        """Connect to MQTT broker"""
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(self.broker_host, self.broker_port, 60)
        self.client.loop_start()
    
    def subscribe(self, topic: str, callback: Callable):
        """Subscribe to MQTT topic"""
        self.callbacks[topic] = callback
        self.client.subscribe(topic)
    
    def publish(self, topic: str, payload: dict):
        """Publish to MQTT topic"""
        import json
        self.client.publish(topic, json.dumps(payload))
    
    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker: {rc}")
        # Resubscribe on reconnect
        for topic in self.callbacks.keys():
            client.subscribe(topic)
    
    def _on_message(self, client, userdata, msg):
        """Handle incoming MQTT messages"""
        topic = msg.topic
        if topic in self.callbacks:
            import json
            payload = json.loads(msg.payload)
            self.callbacks[topic](payload)

# Topics
TOPICS = {
    'NODE_HEARTBEAT': 'edge-qi/nodes/+/heartbeat',
    'DETECTION': 'edge-qi/detection/+',
    'CONSENSUS': 'edge-qi/consensus/+',
    'METRICS': 'edge-qi/metrics/+',
}
```

### **Phase 2: Database Setup**

#### 1. TimescaleDB Initialization (docker/timescaledb/init.sql)
```sql
-- Create TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Edge Nodes Table
CREATE TABLE edge_nodes (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'idle',
    location VARCHAR(200),
    cpu_usage FLOAT DEFAULT 0.0,
    memory_usage FLOAT DEFAULT 0.0,
    network_status VARCHAR(20) DEFAULT 'good',
    energy_consumption FLOAT DEFAULT 0.0,
    ip_address VARCHAR(50),
    port INTEGER,
    capabilities JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_heartbeat TIMESTAMPTZ
);

-- Detections Table (Time-series)
CREATE TABLE detections (
    id SERIAL,
    timestamp TIMESTAMPTZ NOT NULL,
    node_id VARCHAR(50) REFERENCES edge_nodes(id),
    stream_id VARCHAR(50),
    object_type VARCHAR(50),
    confidence FLOAT,
    bbox JSONB,
    location VARCHAR(200),
    metadata JSONB
);

-- Convert to hypertable for time-series optimization
SELECT create_hypertable('detections', 'timestamp');

-- System Metrics Table (Time-series)
CREATE TABLE system_metrics (
    timestamp TIMESTAMPTZ NOT NULL,
    total_nodes INTEGER,
    active_nodes INTEGER,
    total_detections INTEGER,
    average_latency FLOAT,
    bandwidth_saved FLOAT,
    energy_saved FLOAT,
    metadata JSONB
);

SELECT create_hypertable('system_metrics', 'timestamp');

-- Consensus Rounds Table
CREATE TABLE consensus_rounds (
    id SERIAL PRIMARY KEY,
    round_number INTEGER NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    success BOOLEAN,
    participants INTEGER,
    duration_ms INTEGER,
    votes JSONB,
    result JSONB
);

-- System Logs Table
CREATE TABLE system_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    level VARCHAR(20),
    source VARCHAR(100),
    message TEXT,
    details JSONB
);

-- Indexes for performance
CREATE INDEX idx_detections_timestamp ON detections(timestamp DESC);
CREATE INDEX idx_detections_node_id ON detections(node_id);
CREATE INDEX idx_system_metrics_timestamp ON system_metrics(timestamp DESC);
CREATE INDEX idx_logs_timestamp ON system_logs(timestamp DESC);
CREATE INDEX idx_logs_level ON system_logs(level);

-- Retention policies (optional)
SELECT add_retention_policy('detections', INTERVAL '30 days');
SELECT add_retention_policy('system_metrics', INTERVAL '90 days');
SELECT add_retention_policy('system_logs', INTERVAL '7 days');
```

### **Phase 3: Integration with Edge Nodes**

#### 1. Edge Node → Backend Communication
```python
# In edge_node_complete.py
import requests
import json

class EdgeNodeClient:
    def __init__(self, node_id: str, backend_url: str):
        self.node_id = node_id
        self.backend_url = backend_url
        self.mqtt_client = mqtt.Client()
        
    def register_node(self):
        """Register node with backend"""
        response = requests.post(
            f"{self.backend_url}/api/nodes/register",
            json={
                "id": self.node_id,
                "name": f"Node-{self.node_id}",
                "capabilities": self.get_capabilities(),
                "ip_address": self.get_ip(),
                "port": 8080,
            }
        )
        return response.json()
    
    def send_heartbeat(self):
        """Send heartbeat with metrics"""
        self.mqtt_client.publish(
            f"edge-qi/nodes/{self.node_id}/heartbeat",
            json.dumps({
                "node_id": self.node_id,
                "timestamp": datetime.utcnow().isoformat(),
                "cpu_usage": self.get_cpu_usage(),
                "memory_usage": self.get_memory_usage(),
                "status": "active",
            })
        )
    
    def publish_detection(self, detection_result):
        """Publish detection to backend"""
        self.mqtt_client.publish(
            f"edge-qi/detection/{self.node_id}",
            json.dumps(detection_result)
        )
```

### **Phase 4: Authentication & Security**

#### 1. JWT Authentication
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Login endpoint
@router.post("/auth/login")
async def login(username: str, password: str):
    # Verify credentials
    user = verify_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
```

---

## 📋 Implementation Checklist

### **Frontend (Additional)**
- [ ] TypeScript migration
- [ ] Advanced state management (Zustand)
- [ ] Error boundaries
- [ ] Virtual scrolling for logs
- [ ] Data export (CSV, JSON, Excel)
- [ ] Advanced filtering
- [ ] Unit tests
- [ ] E2E tests
- [ ] Performance monitoring

### **Backend (Core)**
- [ ] FastAPI project setup
- [ ] Database models (SQLAlchemy)
- [ ] Pydantic schemas
- [ ] API endpoints
  - [ ] `/api/system/status`
  - [ ] `/api/nodes`
  - [ ] `/api/detections`
  - [ ] `/api/analytics`
- [ ] WebSocket server (Socket.IO)
- [ ] MQTT integration
- [ ] TimescaleDB setup
- [ ] Redis caching
- [ ] JWT authentication
- [ ] API documentation (Swagger)
- [ ] Unit tests
- [ ] Integration tests

### **Integration**
- [ ] Connect frontend to backend
- [ ] WebSocket real-time updates
- [ ] Edge nodes → Backend MQTT
- [ ] Database persistence
- [ ] Cache layer
- [ ] Error handling
- [ ] Logging system
- [ ] Monitoring (Prometheus/Grafana)

---

## 🚀 Quick Start Commands

### **Start Backend Development**
```bash
# Create backend structure
cd backend/src
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy asyncpg python-socketio paho-mqtt redis pydantic python-jose passlib

# Create requirements.txt
pip freeze > requirements.txt

# Run server
uvicorn main:socket_app --reload --port 8000
```

### **Start Infrastructure**
```bash
# Start Docker services
docker-compose up -d mqtt-broker timescaledb redis

# Check services
docker-compose ps
```

### **Connect Frontend**
```bash
# Update .env
echo "VITE_BACKEND_URL=http://localhost:8000" > .env

# Start frontend
npm run dev
```

---

## 📊 Priority Order

### **Week 1: Core Backend**
1. FastAPI server setup
2. Database models
3. Basic API endpoints
4. WebSocket server

### **Week 2: Integration**
1. Connect edge nodes to backend
2. MQTT message handling
3. Database persistence
4. Frontend-backend integration

### **Week 3: Features**
1. Real-time updates working
2. Authentication system
3. Caching layer
4. Error handling

### **Week 4: Polish**
1. Testing
2. Documentation
3. Performance optimization
4. Security hardening

---

## 🎯 Success Metrics

### **Performance**
- API response time < 100ms
- WebSocket latency < 50ms
- Database query time < 20ms
- Frontend load time < 2s

### **Reliability**
- 99.9% uptime
- Zero data loss
- Automatic reconnection
- Graceful error handling

### **Scalability**
- Support 100+ edge nodes
- Handle 10,000+ detections/minute
- Store 90 days of data
- Serve 50+ concurrent users

---

**Would you like me to start implementing any of these improvements?**
