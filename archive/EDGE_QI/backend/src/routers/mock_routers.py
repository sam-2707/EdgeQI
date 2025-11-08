"""
Detection, Analytics, Logs, Consensus routers with mock data
"""
from fastapi import APIRouter, Query
from datetime import datetime, timedelta
import random

# Detection Router
detection_router = APIRouter()

MOCK_DETECTIONS = [
    {
        "id": i,
        "timestamp": (datetime.utcnow() - timedelta(minutes=i*2)).isoformat(),
        "node_id": f"edge-node-{random.randint(1, 5)}",
        "stream_id": f"stream-{random.randint(1, 3)}",
        "object_type": random.choice(["car", "person", "bicycle", "motorcycle", "bus"]),
        "confidence": round(random.uniform(0.85, 0.99), 2),
        "bbox": {"x": random.randint(0, 1000), "y": random.randint(0, 1000), "width": random.randint(50, 200), "height": random.randint(50, 200)},
        "location": f"Location {random.randint(1, 5)}"
    }
    for i in range(1, 51)
]

@detection_router.get("/")
async def list_detections(limit: int = Query(100)):
    return MOCK_DETECTIONS[:limit]

@detection_router.get("/stats/summary")
async def detection_summary():
    return {
        "total": len(MOCK_DETECTIONS),
        "time_range": "24h",
        "average_confidence": 0.92,
        "by_type": {"car": 20, "person": 15, "bicycle": 10, "motorcycle": 3, "bus": 2}
    }


# Analytics Router
analytics_router = APIRouter()

@analytics_router.get("/data")
async def analytics_data():
    return {
        "traffic_trends": [{"time": f"{h}:00", "detections": random.randint(10, 50)} for h in range(24)],
        "performance_metrics": [{"time": f"{h}:00", "latency": round(random.uniform(20, 80), 1)} for h in range(24)],
        "detection_distribution": [{"name": obj, "value": random.randint(5, 30)} for obj in ["car", "person", "bicycle", "motorcycle", "bus"]],
        "bandwidth_comparison": [{"time": f"{h}:00", "saved": round(random.uniform(50, 200), 1)} for h in range(24)],
        "energy_efficiency": [{"time": f"{h}:00", "saved": round(random.uniform(1, 10), 1)} for h in range(24)],
        "node_activity": [{"node": f"Node {i}", "detections": random.randint(50, 300)} for i in range(1, 6)]
    }


# Logs Router
logs_router = APIRouter()

MOCK_LOGS = [
    {
        "id": i,
        "timestamp": (datetime.utcnow() - timedelta(minutes=i*3)).isoformat(),
        "level": random.choice(["info", "warning", "error"]),
        "source": random.choice(["api", "detection", "system", "network"]),
        "message": random.choice([
            "System started successfully",
            "Node heartbeat received",
            "Detection processed",
            "High CPU usage detected",
            "Network latency increased"
        ])
    }
    for i in range(1, 31)
]

@logs_router.get("/")
async def list_logs(limit: int = Query(100)):
    return MOCK_LOGS[:limit]


# Consensus Router
consensus_router = APIRouter()

@consensus_router.get("/rounds")
async def list_consensus_rounds():
    return [
        {
            "id": i,
            "round_number": i,
            "timestamp": (datetime.utcnow() - timedelta(minutes=i*5)).isoformat(),
            "success": i % 4 != 0,  # 75% success rate
            "participants": random.randint(3, 5),
            "duration_ms": random.randint(50, 200),
            "votes": {},
            "result": {},
            "byzantine_nodes": [],
            "fault_tolerance_level": 0.8
        }
        for i in range(1, 11)
    ]

@consensus_router.get("/stats/summary")
async def consensus_summary():
    return {
        "total_rounds": 10,
        "successful_rounds": 7,
        "success_rate": 70.0,
        "average_duration_ms": 125.0,
        "average_participants": 4.0
    }
