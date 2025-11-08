"""
System API endpoints
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/status")
async def system_status():
    """
    Get current system metrics (mock data for now)
    """
    return {
        'total_nodes': 5,
        'active_nodes': 4,
        'idle_nodes': 1,
        'fault_nodes': 0,
        'total_detections': 1234,
        'detections_per_second': 2.5,
        'average_latency': 45.2,
        'average_cpu': 62.5,
        'average_memory': 58.3,
        'bandwidth_saved': 234.5,
        'energy_saved': 12.3,
        'timestamp': datetime.utcnow().isoformat()
    }


@router.get("/health")
async def health_check():
    """
    System health check
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow(),
        "database": "not_connected",
        "mqtt": "unknown",
        "redis": "unknown"
    }


@router.get("/nodes/summary")
async def nodes_summary():
    """
    Get node summary statistics (mock data)
    """
    return {
        'total': 5,
        'active': 4,
        'idle': 1,
        'fault': 0,
        'total_detections': 1234,
        'average_cpu': 62.5,
        'average_memory': 58.3,
        'total_energy': 456.7
    }
