# EDGE-QI Backend API

FastAPI backend for the EDGE-QI Smart City Object Detection Platform.

## Features

- **RESTful API** with FastAPI
- **WebSocket Support** for real-time updates (Socket.IO)
- **PostgreSQL Database** with SQLAlchemy ORM
- **Real-time Metrics Broadcasting**
- **Comprehensive API Documentation** (Swagger/ReDoc)

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip or conda

### Setup

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Initialize database**:
```bash
# Make sure PostgreSQL is running
# Create database: edge_qi
python -m src.database
```

## Running the Server

### Development Mode
```bash
uvicorn src.main:socket_app --reload --port 8000
```

### Production Mode
```bash
uvicorn src.main:socket_app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### System
- `GET /api/system/status` - Get system metrics
- `GET /api/system/health` - Health check
- `GET /api/system/nodes/summary` - Node summary

### Edge Nodes
- `GET /api/nodes` - List all nodes
- `POST /api/nodes` - Register new node
- `GET /api/nodes/{id}` - Get node details
- `PATCH /api/nodes/{id}` - Update node
- `DELETE /api/nodes/{id}` - Deregister node
- `POST /api/nodes/{id}/heartbeat` - Node heartbeat

### Detections
- `GET /api/detections` - List detections
- `POST /api/detections` - Create detection
- `GET /api/detections/{id}` - Get detection
- `GET /api/detections/stats/summary` - Detection stats
- `GET /api/detections/recent/stream` - Recent detections

### Analytics
- `GET /api/analytics/data` - All analytics data
- `GET /api/analytics/traffic` - Traffic analytics
- `GET /api/analytics/performance` - Performance analytics
- `GET /api/analytics/distribution` - Distribution analytics

### Logs
- `GET /api/logs` - List logs
- `POST /api/logs` - Create log
- `DELETE /api/logs/clear` - Clear old logs

### Consensus
- `GET /api/consensus/rounds` - List consensus rounds
- `POST /api/consensus/rounds` - Create consensus round
- `GET /api/consensus/rounds/{id}` - Get round details
- `GET /api/consensus/stats/summary` - Consensus stats

## WebSocket Events

### Client → Server
- `connect` - Client connection established
- `disconnect` - Client disconnected
- `request_data` - Request specific data

### Server → Client
- `connection_established` - Connection confirmed
- `system_metrics` - System metrics update (every 5s)
- `edge_node_update` - Node status update
- `detection_result` - New detection
- `consensus_update` - Consensus round update
- `system_log` - New log entry
- `alert` - System alert

## Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   │
│   ├── models/              # SQLAlchemy models
│   │   └── models.py
│   │
│   ├── schemas/             # Pydantic schemas
│   │   └── schemas.py
│   │
│   ├── routers/             # API endpoints
│   │   ├── system.py
│   │   ├── nodes.py
│   │   ├── detection.py
│   │   ├── analytics.py
│   │   ├── logs.py
│   │   └── consensus.py
│   │
│   └── services/            # Business logic
│       ├── websocket_service.py
│       └── system_service.py
│
├── requirements.txt
├── .env.example
└── README.md
```

## Environment Variables

```env
# API Settings
API_TITLE=EDGE-QI API
API_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/edge_qi

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# MQTT
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883

# WebSocket
METRICS_BROADCAST_INTERVAL=5
```

## Development

### Run tests
```bash
pytest tests/
```

### Code formatting
```bash
black src/
isort src/
```

### Type checking
```bash
mypy src/
```

## License

MIT License
