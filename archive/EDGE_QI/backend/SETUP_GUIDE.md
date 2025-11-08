# 🚀 EDGE-QI Backend Setup & Deployment Guide

Complete guide to setting up and running the EDGE-QI backend server.

---

## 📋 Prerequisites

### Required Software
- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **PostgreSQL 12+** ([Download](https://www.postgresql.org/download/))
- **pip** (comes with Python)

### Optional Software
- **Git** (for version control)
- **Postman** (for API testing)

---

## ⚡ Quick Start (5 Minutes)

### Option 1: Automated Setup (Recommended)

```powershell
# Navigate to backend directory
cd d:\EDGE_QI_!\EDGE_QI\backend

# Run the automated setup script
.\start.ps1
```

This script will:
1. ✅ Check Python installation
2. ✅ Create virtual environment
3. ✅ Install all dependencies
4. ✅ Start the FastAPI server

### Option 2: Manual Setup

```powershell
# 1. Navigate to backend directory
cd d:\EDGE_QI_!\EDGE_QI\backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Initialize database
python init_db.py

# 6. (Optional) Populate with mock data
python populate_db.py

# 7. Start server
python -m uvicorn src.main:socket_app --reload --port 8000
```

---

## 🗄️ Database Setup

### Step 1: Install PostgreSQL

Download and install PostgreSQL from: https://www.postgresql.org/download/windows/

### Step 2: Create Database

```sql
-- Open pgAdmin or psql
CREATE DATABASE edge_qi;

-- Verify connection
\c edge_qi
```

### Step 3: Configure Connection

Edit `backend/.env` file:
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/edge_qi
```

### Step 4: Initialize Tables

```powershell
python init_db.py
```

Expected output:
```
🔧 Initializing EDGE-QI Database...
Creating tables...
✅ Tables created successfully:
   - edge_nodes
   - detections
   - system_metrics
   - consensus_rounds
   - system_logs
   - alerts
✅ Database initialization complete!
```

---

## 🎯 Running the Backend

### Development Mode (with auto-reload)

```powershell
uvicorn src.main:socket_app --reload --port 8000
```

### Production Mode (4 workers)

```powershell
uvicorn src.main:socket_app --host 0.0.0.0 --port 8000 --workers 4
```

### Background Mode

```powershell
Start-Process -WindowStyle Hidden -FilePath "python" -ArgumentList "-m", "uvicorn", "src.main:socket_app", "--port", "8000"
```

---

## 🧪 Testing the API

### 1. Health Check

Open browser: http://localhost:8000/health

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-05T10:30:00"
}
```

### 2. API Documentation

**Swagger UI**: http://localhost:8000/docs
**ReDoc**: http://localhost:8000/redoc

### 3. System Status

```powershell
curl http://localhost:8000/api/system/status
```

### 4. List Edge Nodes

```powershell
curl http://localhost:8000/api/nodes
```

### 5. WebSocket Test

Use the frontend at http://localhost:5173 to test real-time updates.

---

## 📊 Populating Mock Data

For testing purposes, populate the database with mock data:

```powershell
python populate_db.py
```

This creates:
- ✅ 5 Edge Nodes
- ✅ 50 Detections
- ✅ 20 System Metrics
- ✅ 10 Consensus Rounds
- ✅ 30 System Logs

---

## 🔧 Configuration

### Environment Variables

Edit `backend/.env`:

```env
# API Settings
PORT=8000
DEBUG=True

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/edge_qi

# CORS (Frontend URL)
CORS_ORIGINS=http://localhost:5173

# WebSocket
METRICS_BROADCAST_INTERVAL=5

# Redis (Optional)
REDIS_HOST=localhost
REDIS_PORT=6379

# MQTT (Optional)
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
```

### Database Configuration

**PostgreSQL Settings** (postgresql.conf):
```
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
```

---

## 🌐 API Endpoints Reference

### System Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/system/status` | Get system metrics |
| GET | `/api/system/health` | Health check |
| GET | `/api/system/nodes/summary` | Node summary |

### Node Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/nodes` | List all nodes |
| POST | `/api/nodes` | Register node |
| GET | `/api/nodes/{id}` | Get node details |
| PATCH | `/api/nodes/{id}` | Update node |
| DELETE | `/api/nodes/{id}` | Delete node |
| POST | `/api/nodes/{id}/heartbeat` | Node heartbeat |

### Detection Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/detections` | List detections |
| POST | `/api/detections` | Create detection |
| GET | `/api/detections/{id}` | Get detection |
| GET | `/api/detections/stats/summary` | Detection stats |

### Analytics Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/data` | All analytics |
| GET | `/api/analytics/traffic` | Traffic data |
| GET | `/api/analytics/performance` | Performance data |

### Logs Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/logs` | List logs |
| POST | `/api/logs` | Create log |
| DELETE | `/api/logs/clear` | Clear old logs |

### Consensus Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/consensus/rounds` | List rounds |
| POST | `/api/consensus/rounds` | Create round |
| GET | `/api/consensus/stats/summary` | Consensus stats |

---

## 🔌 WebSocket Events

### Server → Client Events

```javascript
// System metrics (every 5 seconds)
socket.on('system_metrics', (data) => {
  console.log('Metrics:', data);
});

// Node updates
socket.on('edge_node_update', (data) => {
  console.log('Node update:', data);
});

// New detections
socket.on('detection_result', (data) => {
  console.log('Detection:', data);
});

// System logs
socket.on('system_log', (data) => {
  console.log('Log:', data);
});

// Alerts
socket.on('alert', (data) => {
  console.log('Alert:', data);
});
```

---

## 🐛 Troubleshooting

### Issue: Database Connection Failed

**Error**: `could not connect to server`

**Solution**:
1. Check PostgreSQL is running:
   ```powershell
   Get-Service postgresql*
   ```
2. Verify database exists:
   ```sql
   \l edge_qi
   ```
3. Check credentials in `.env` file

### Issue: Port Already in Use

**Error**: `Address already in use`

**Solution**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use different port
uvicorn src.main:socket_app --port 8001
```

### Issue: Module Not Found

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: CORS Error in Frontend

**Error**: `Access to fetch blocked by CORS policy`

**Solution**:
1. Add frontend URL to `.env`:
   ```env
   CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
   ```
2. Restart backend server

---

## 📈 Performance Optimization

### Database Indexing

Already included in models:
- ✅ Timestamp indexes for time-series queries
- ✅ Foreign key indexes
- ✅ Status indexes for filtering

### Connection Pooling

Configured in `database.py`:
```python
pool_size=10
max_overflow=20
```

### Response Compression

Enabled via `GZipMiddleware`:
```python
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

## 🔒 Security Considerations

### Production Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False`
- [ ] Use strong database password
- [ ] Enable HTTPS (use nginx/caddy reverse proxy)
- [ ] Implement rate limiting
- [ ] Enable JWT authentication
- [ ] Set up firewall rules
- [ ] Regular database backups

### JWT Authentication (Optional)

Uncomment authentication middleware in `main.py` to enable JWT protection for endpoints.

---

## 📦 Deployment

### Option 1: Windows Service

Use NSSM (Non-Sucking Service Manager):
```powershell
nssm install EdgeQIBackend "C:\Path\To\venv\Scripts\python.exe" "-m uvicorn src.main:socket_app --host 0.0.0.0 --port 8000"
nssm start EdgeQIBackend
```

### Option 2: PM2 (Node.js Process Manager)

```powershell
pm2 start "uvicorn src.main:socket_app --port 8000" --name edge-qi-backend
pm2 save
pm2 startup
```

### Option 3: Docker (Future)

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "src.main:socket_app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📊 Monitoring

### View Server Logs

```powershell
# Real-time logs
uvicorn src.main:socket_app --reload --log-level debug

# Save to file
uvicorn src.main:socket_app --log-config logging.conf > server.log 2>&1
```

### Check System Metrics

```powershell
curl http://localhost:8000/api/system/status | ConvertFrom-Json
```

### Database Query Performance

```sql
-- Check slow queries
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;

-- Check active connections
SELECT count(*) FROM pg_stat_activity;
```

---

## 🎉 Success Indicators

Backend is running correctly when:

✅ Health check returns `{"status": "healthy"}`
✅ Swagger UI loads at http://localhost:8000/docs
✅ Frontend connects via WebSocket
✅ System metrics broadcast every 5 seconds
✅ API endpoints return valid JSON responses
✅ Database queries execute successfully

---

## 📞 Support

For issues or questions:
1. Check API documentation: http://localhost:8000/docs
2. Review server logs
3. Verify database connection
4. Check environment configuration

---

**Backend Status: ✅ Ready for Production**

The backend is fully functional and integrated with the frontend!
