"""
Edge Nodes API endpoints (Mock Data Version)
"""
from fastapi import APIRouter, Query
from typing import List, Optional
from datetime import datetime
import random

router = APIRouter()

# Mock data
MOCK_NODES = [
    {
        "id": f"edge-node-{i}",
        "name": f"Edge Node {i}",
        "status": ["active", "active", "active", "idle", "fault"][i-1],
        "location": f"Location {i}",
        "cpu_usage": random.uniform(30, 80),
        "memory_usage": random.uniform(40, 75),
        "gpu_usage": random.uniform(50, 90),
        "network_status": "good" if i < 5 else "poor",
        "energy_consumption": random.uniform(80, 150),
        "ip_address": f"192.168.1.{10+i}",
        "port": 8080 + i,
        "capabilities": {"detection": True, "yolo": "v8"},
        "total_detections": random.randint(100, 1000),
        "average_latency": random.uniform(20, 80),
        "uptime": random.uniform(80, 100),
        "last_heartbeat": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    for i in range(1, 6)
]


@router.get("/")
async def list_nodes(status: Optional[str] = Query(None)):
    """List all edge nodes"""
    if status:
        return [n for n in MOCK_NODES if n["status"] == status]
    return MOCK_NODES


@router.get("/{node_id}")
async def get_node(node_id: str):
    """Get specific edge node by ID"""
    for node in MOCK_NODES:
        if node["id"] == node_id:
            return node
    return {"error": "Node not found"}
