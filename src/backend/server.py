"""
EDGE-QI Backend API Server - Standalone Version
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import socketio
from datetime import datetime, timedelta
import random
from typing import Optional
import os

# Create FastAPI app
app = FastAPI(
    title="EDGE-QI API",
    description="Backend for EDGE-QI Smart City Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for detection images
# This will serve files from frontend/public/detections
static_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "public")
if os.path.exists(static_path):
    app.mount("/detections", StaticFiles(directory=os.path.join(static_path, "detections")), name="detections")

# Socket.IO setup
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
)

socket_app = socketio.ASGIApp(sio, app, socketio_path='/socket.io')

# WebSocket events
@sio.event
async def connect(sid, environ):
    print(f"✅ Client connected: {sid}")
    await sio.emit('connection_established', {
        'status': 'connected',
        'timestamp': datetime.utcnow().isoformat()
    }, room=sid)

@sio.event
async def disconnect(sid):
    print(f"❌ Client disconnected: {sid}")

# Mock data - Real Edge Nodes with Camera Feeds
MOCK_NODES = [
    {
        "id": "edge-node-1",
        "name": "Downtown Intersection - Main Street",
        "status": "active",
        "location": "Main Street & 5th Avenue",
        "description": "High-traffic urban intersection monitoring. Detects vehicles (cars, buses, trucks) and pedestrians for traffic management and safety.",
        "camera_type": "4K PTZ Camera",
        "camera_view": "Aerial Street View",
        "cpu_usage": round(random.uniform(60, 85), 1),
        "memory_usage": round(random.uniform(55, 75), 1),
        "gpu_usage": round(random.uniform(70, 90), 1),
        "network_status": "excellent",
        "energy_consumption": round(random.uniform(120, 150), 1),
        "ip_address": "192.168.1.11",
        "port": 8081,
        "capabilities": {"detection": True, "yolo": "v8n", "classes": ["car", "person", "bicycle", "bus", "truck"]},
        "total_detections": 1847,
        "average_latency": 42.3,
        "uptime": 99.8,
        "last_heartbeat": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "live_feed": "/detections/camera_1_street_view.jpg"
    },
    {
        "id": "edge-node-2",
        "name": "Highway 101 Overpass",
        "status": "active",
        "location": "Highway 101 Mile Marker 45",
        "description": "Highway traffic monitoring with vehicle classification. Tracks cars, buses, and trucks for traffic flow analysis and incident detection.",
        "camera_type": "Panoramic HD Camera",
        "camera_view": "Highway Overpass View",
        "cpu_usage": round(random.uniform(55, 75), 1),
        "memory_usage": round(random.uniform(50, 70), 1),
        "gpu_usage": round(random.uniform(65, 85), 1),
        "network_status": "good",
        "energy_consumption": round(random.uniform(100, 130), 1),
        "ip_address": "192.168.1.12",
        "port": 8082,
        "capabilities": {"detection": True, "yolo": "v8n", "classes": ["car", "bus", "truck"]},
        "total_detections": 2134,
        "average_latency": 38.5,
        "uptime": 98.5,
        "last_heartbeat": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "live_feed": "/detections/camera_2_highway.jpg"
    },
    {
        "id": "edge-node-3",
        "name": "Residential Complex - Parking Area",
        "status": "active",
        "location": "Greenview Residential Complex",
        "description": "Parking lot surveillance with vehicle and micro-mobility detection. Monitors cars, vans, and tricycles for security and space management.",
        "camera_type": "Fixed Dome Camera",
        "camera_view": "Bird's Eye View",
        "cpu_usage": round(random.uniform(45, 65), 1),
        "memory_usage": round(random.uniform(40, 60), 1),
        "gpu_usage": round(random.uniform(55, 75), 1),
        "network_status": "excellent",
        "energy_consumption": round(random.uniform(85, 110), 1),
        "ip_address": "192.168.1.13",
        "port": 8083,
        "capabilities": {"detection": True, "yolo": "v8n", "classes": ["car", "van", "tricycle"]},
        "total_detections": 892,
        "average_latency": 35.7,
        "uptime": 99.2,
        "last_heartbeat": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "live_feed": "/detections/camera_3_parking.jpg"
    },
    {
        "id": "edge-node-4",
        "name": "Commercial District - Plaza Entrance",
        "status": "active",
        "location": "City Plaza Commercial District",
        "description": "Mixed-use area monitoring for pedestrian and vehicle traffic. Detects cars and people for crowd management and safety.",
        "camera_type": "4K Fixed Camera",
        "camera_view": "Street Level View",
        "cpu_usage": round(random.uniform(50, 70), 1),
        "memory_usage": round(random.uniform(45, 65), 1),
        "gpu_usage": round(random.uniform(60, 80), 1),
        "network_status": "good",
        "energy_consumption": round(random.uniform(95, 120), 1),
        "ip_address": "192.168.1.14",
        "port": 8084,
        "capabilities": {"detection": True, "yolo": "v8n", "classes": ["car", "person"]},
        "total_detections": 1456,
        "average_latency": 44.2,
        "uptime": 97.8,
        "last_heartbeat": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "live_feed": "/detections/camera_4_plaza.jpg"
    },
    {
        "id": "edge-node-5",
        "name": "School Zone - Safety Monitor",
        "status": "active",
        "location": "Lincoln Elementary School",
        "description": "School zone safety monitoring. Real-time detection of vehicles and pedestrians during school hours for child safety.",
        "camera_type": "Smart Traffic Camera",
        "camera_view": "Crosswalk View",
        "cpu_usage": round(random.uniform(55, 75), 1),
        "memory_usage": round(random.uniform(50, 70), 1),
        "gpu_usage": round(random.uniform(65, 85), 1),
        "network_status": "excellent",
        "energy_consumption": round(random.uniform(90, 115), 1),
        "ip_address": "192.168.1.15",
        "port": 8085,
        "capabilities": {"detection": True, "yolo": "v8n", "classes": ["car", "person", "bicycle"]},
        "total_detections": 1203,
        "average_latency": 39.8,
        "uptime": 99.5,
        "last_heartbeat": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "live_feed": "/detections/camera_5_school.jpg"
    }
]

MOCK_DETECTIONS = [
    # Camera 1 - Downtown Intersection (0000280_01401_d_0000619.jpg)
    {"id": 1, "timestamp": (datetime.utcnow() - timedelta(seconds=5)).isoformat(), "node_id": "edge-node-1", "stream_id": "stream-1", "object_type": "car", "confidence": 0.82, "bbox": {"x": 80, "y": 235, "width": 75, "height": 45}, "location": "Main Street & 5th Avenue", "image": "/detections/camera_1_street_view.jpg"},
    {"id": 2, "timestamp": (datetime.utcnow() - timedelta(seconds=5)).isoformat(), "node_id": "edge-node-1", "stream_id": "stream-1", "object_type": "car", "confidence": 0.83, "bbox": {"x": 155, "y": 260, "width": 70, "height": 40}, "location": "Main Street & 5th Avenue", "image": "/detections/camera_1_street_view.jpg"},
    {"id": 3, "timestamp": (datetime.utcnow() - timedelta(seconds=5)).isoformat(), "node_id": "edge-node-1", "stream_id": "stream-1", "object_type": "car", "confidence": 0.80, "bbox": {"x": 100, "y": 338, "width": 60, "height": 35}, "location": "Main Street & 5th Avenue", "image": "/detections/camera_1_street_view.jpg"},
    {"id": 4, "timestamp": (datetime.utcnow() - timedelta(seconds=5)).isoformat(), "node_id": "edge-node-1", "stream_id": "stream-1", "object_type": "car", "confidence": 0.82, "bbox": {"x": 155, "y": 265, "width": 65, "height": 38}, "location": "Main Street & 5th Avenue", "image": "/detections/camera_1_street_view.jpg"},
    {"id": 5, "timestamp": (datetime.utcnow() - timedelta(seconds=5)).isoformat(), "node_id": "edge-node-1", "stream_id": "stream-1", "object_type": "car", "confidence": 0.61, "bbox": {"x": 197, "y": 235, "width": 58, "height": 32}, "location": "Main Street & 5th Avenue", "image": "/detections/camera_1_street_view.jpg"},
    {"id": 6, "timestamp": (datetime.utcnow() - timedelta(seconds=5)).isoformat(), "node_id": "edge-node-1", "stream_id": "stream-1", "object_type": "car", "confidence": 0.70, "bbox": {"x": 315, "y": 345, "width": 72, "height": 42}, "location": "Main Street & 5th Avenue", "image": "/detections/camera_1_street_view.jpg"},
    {"id": 7, "timestamp": (datetime.utcnow() - timedelta(seconds=5)).isoformat(), "node_id": "edge-node-1", "stream_id": "stream-1", "object_type": "car", "confidence": 0.82, "bbox": {"x": 445, "y": 265, "width": 68, "height": 40}, "location": "Main Street & 5th Avenue", "image": "/detections/camera_1_street_view.jpg"},
    {"id": 8, "timestamp": (datetime.utcnow() - timedelta(seconds=5)).isoformat(), "node_id": "edge-node-1", "stream_id": "stream-1", "object_type": "car", "confidence": 0.35, "bbox": {"x": 475, "y": 235, "width": 55, "height": 30}, "location": "Main Street & 5th Avenue", "image": "/detections/camera_1_street_view.jpg"},
    {"id": 9, "timestamp": (datetime.utcnow() - timedelta(seconds=5)).isoformat(), "node_id": "edge-node-1", "stream_id": "stream-1", "object_type": "car", "confidence": 0.55, "bbox": {"x": 425, "y": 193, "width": 62, "height": 35}, "location": "Main Street & 5th Avenue", "image": "/detections/camera_1_street_view.jpg"},
    {"id": 10, "timestamp": (datetime.utcnow() - timedelta(seconds=5)).isoformat(), "node_id": "edge-node-1", "stream_id": "stream-1", "object_type": "car", "confidence": 0.78, "bbox": {"x": 527, "y": 318, "width": 70, "height": 42}, "location": "Main Street & 5th Avenue", "image": "/detections/camera_1_street_view.jpg"},
    {"id": 11, "timestamp": (datetime.utcnow() - timedelta(seconds=5)).isoformat(), "node_id": "edge-node-1", "stream_id": "stream-1", "object_type": "pedestrian", "confidence": 0.31, "bbox": {"x": 510, "y": 354, "width": 25, "height": 45}, "location": "Main Street & 5th Avenue", "image": "/detections/camera_1_street_view.jpg"},
    
    # Camera 2 - Highway 101 (0000199_01269_d_0000166.jpg)
    {"id": 12, "timestamp": (datetime.utcnow() - timedelta(seconds=8)).isoformat(), "node_id": "edge-node-2", "stream_id": "stream-2", "object_type": "car", "confidence": 0.50, "bbox": {"x": 258, "y": 162, "width": 85, "height": 48}, "location": "Highway 101 Mile Marker 45", "image": "/detections/camera_2_highway.jpg"},
    {"id": 13, "timestamp": (datetime.utcnow() - timedelta(seconds=8)).isoformat(), "node_id": "edge-node-2", "stream_id": "stream-2", "object_type": "bus", "confidence": 0.47, "bbox": {"x": 305, "y": 192, "width": 95, "height": 52}, "location": "Highway 101 Mile Marker 45", "image": "/detections/camera_2_highway.jpg"},
    {"id": 14, "timestamp": (datetime.utcnow() - timedelta(seconds=8)).isoformat(), "node_id": "edge-node-2", "stream_id": "stream-2", "object_type": "car", "confidence": 0.69, "bbox": {"x": 357, "y": 230, "width": 78, "height": 45}, "location": "Highway 101 Mile Marker 45", "image": "/detections/camera_2_highway.jpg"},
    {"id": 15, "timestamp": (datetime.utcnow() - timedelta(seconds=8)).isoformat(), "node_id": "edge-node-2", "stream_id": "stream-2", "object_type": "car", "confidence": 0.52, "bbox": {"x": 410, "y": 245, "width": 72, "height": 42}, "location": "Highway 101 Mile Marker 45", "image": "/detections/camera_2_highway.jpg"},
    {"id": 16, "timestamp": (datetime.utcnow() - timedelta(seconds=8)).isoformat(), "node_id": "edge-node-2", "stream_id": "stream-2", "object_type": "truck", "confidence": 0.45, "bbox": {"x": 425, "y": 270, "width": 88, "height": 50}, "location": "Highway 101 Mile Marker 45", "image": "/detections/camera_2_highway.jpg"},
    {"id": 17, "timestamp": (datetime.utcnow() - timedelta(seconds=8)).isoformat(), "node_id": "edge-node-2", "stream_id": "stream-2", "object_type": "car", "confidence": 0.59, "bbox": {"x": 520, "y": 289, "width": 75, "height": 44}, "location": "Highway 101 Mile Marker 45", "image": "/detections/camera_2_highway.jpg"},
    {"id": 18, "timestamp": (datetime.utcnow() - timedelta(seconds=8)).isoformat(), "node_id": "edge-node-2", "stream_id": "stream-2", "object_type": "car", "confidence": 0.63, "bbox": {"x": 370, "y": 350, "width": 80, "height": 46}, "location": "Highway 101 Mile Marker 45", "image": "/detections/camera_2_highway.jpg"},
    {"id": 19, "timestamp": (datetime.utcnow() - timedelta(seconds=8)).isoformat(), "node_id": "edge-node-2", "stream_id": "stream-2", "object_type": "car", "confidence": 0.27, "bbox": {"x": 550, "y": 327, "width": 68, "height": 40}, "location": "Highway 101 Mile Marker 45", "image": "/detections/camera_2_highway.jpg"},
    
    # Camera 3 - Residential Parking (0000026_03000_d_0000030.jpg)
    {"id": 20, "timestamp": (datetime.utcnow() - timedelta(seconds=12)).isoformat(), "node_id": "edge-node-3", "stream_id": "stream-3", "object_type": "car", "confidence": 0.76, "bbox": {"x": 125, "y": 76, "width": 65, "height": 42}, "location": "Greenview Residential Complex", "image": "/detections/camera_3_parking.jpg"},
    {"id": 21, "timestamp": (datetime.utcnow() - timedelta(seconds=12)).isoformat(), "node_id": "edge-node-3", "stream_id": "stream-3", "object_type": "car", "confidence": 0.79, "bbox": {"x": 375, "y": 98, "width": 68, "height": 44}, "location": "Greenview Residential Complex", "image": "/detections/camera_3_parking.jpg"},
    {"id": 22, "timestamp": (datetime.utcnow() - timedelta(seconds=12)).isoformat(), "node_id": "edge-node-3", "stream_id": "stream-3", "object_type": "car", "confidence": 0.78, "bbox": {"x": 465, "y": 78, "width": 70, "height": 45}, "location": "Greenview Residential Complex", "image": "/detections/camera_3_parking.jpg"},
    {"id": 23, "timestamp": (datetime.utcnow() - timedelta(seconds=12)).isoformat(), "node_id": "edge-node-3", "stream_id": "stream-3", "object_type": "car", "confidence": 0.78, "bbox": {"x": 485, "y": 98, "width": 66, "height": 43}, "location": "Greenview Residential Complex", "image": "/detections/camera_3_parking.jpg"},
    {"id": 24, "timestamp": (datetime.utcnow() - timedelta(seconds=12)).isoformat(), "node_id": "edge-node-3", "stream_id": "stream-3", "object_type": "car", "confidence": 0.48, "bbox": {"x": 510, "y": 120, "width": 62, "height": 38}, "location": "Greenview Residential Complex", "image": "/detections/camera_3_parking.jpg"},
    {"id": 25, "timestamp": (datetime.utcnow() - timedelta(seconds=12)).isoformat(), "node_id": "edge-node-3", "stream_id": "stream-3", "object_type": "car", "confidence": 0.76, "bbox": {"x": 145, "y": 158, "width": 64, "height": 40}, "location": "Greenview Residential Complex", "image": "/detections/camera_3_parking.jpg"},
    {"id": 26, "timestamp": (datetime.utcnow() - timedelta(seconds=12)).isoformat(), "node_id": "edge-node-3", "stream_id": "stream-3", "object_type": "car", "confidence": 0.81, "bbox": {"x": 145, "y": 188, "width": 66, "height": 42}, "location": "Greenview Residential Complex", "image": "/detections/camera_3_parking.jpg"},
    {"id": 27, "timestamp": (datetime.utcnow() - timedelta(seconds=12)).isoformat(), "node_id": "edge-node-3", "stream_id": "stream-3", "object_type": "van", "confidence": 0.95, "bbox": {"x": 155, "y": 220, "width": 72, "height": 48}, "location": "Greenview Residential Complex", "image": "/detections/camera_3_parking.jpg"},
    {"id": 28, "timestamp": (datetime.utcnow() - timedelta(seconds=12)).isoformat(), "node_id": "edge-node-3", "stream_id": "stream-3", "object_type": "car", "confidence": 0.85, "bbox": {"x": 175, "y": 278, "width": 68, "height": 44}, "location": "Greenview Residential Complex", "image": "/detections/camera_3_parking.jpg"},
    {"id": 29, "timestamp": (datetime.utcnow() - timedelta(seconds=12)).isoformat(), "node_id": "edge-node-3", "stream_id": "stream-3", "object_type": "car", "confidence": 0.70, "bbox": {"x": 195, "y": 308, "width": 64, "height": 40}, "location": "Greenview Residential Complex", "image": "/detections/camera_3_parking.jpg"},
    {"id": 30, "timestamp": (datetime.utcnow() - timedelta(seconds=12)).isoformat(), "node_id": "edge-node-3", "stream_id": "stream-3", "object_type": "tricycle", "confidence": 0.41, "bbox": {"x": 210, "y": 325, "width": 45, "height": 32}, "location": "Greenview Residential Complex", "image": "/detections/camera_3_parking.jpg"},
    
    # Camera 4 - Commercial Plaza (0000287_00601_d_0000762.jpg)
    {"id": 31, "timestamp": (datetime.utcnow() - timedelta(seconds=15)).isoformat(), "node_id": "edge-node-4", "stream_id": "stream-4", "object_type": "car", "confidence": 0.41, "bbox": {"x": 80, "y": 128, "width": 75, "height": 48}, "location": "City Plaza Commercial District", "image": "/detections/camera_4_plaza.jpg"},
    {"id": 32, "timestamp": (datetime.utcnow() - timedelta(seconds=15)).isoformat(), "node_id": "edge-node-4", "stream_id": "stream-4", "object_type": "car", "confidence": 0.34, "bbox": {"x": 155, "y": 148, "width": 68, "height": 44}, "location": "City Plaza Commercial District", "image": "/detections/camera_4_plaza.jpg"},
    {"id": 33, "timestamp": (datetime.utcnow() - timedelta(seconds=15)).isoformat(), "node_id": "edge-node-4", "stream_id": "stream-4", "object_type": "car", "confidence": 0.28, "bbox": {"x": 280, "y": 128, "width": 72, "height": 46}, "location": "City Plaza Commercial District", "image": "/detections/camera_4_plaza.jpg"},
    {"id": 34, "timestamp": (datetime.utcnow() - timedelta(seconds=15)).isoformat(), "node_id": "edge-node-4", "stream_id": "stream-4", "object_type": "car", "confidence": 0.36, "bbox": {"x": 220, "y": 168, "width": 70, "height": 42}, "location": "City Plaza Commercial District", "image": "/detections/camera_4_plaza.jpg"},
    {"id": 35, "timestamp": (datetime.utcnow() - timedelta(seconds=15)).isoformat(), "node_id": "edge-node-4", "stream_id": "stream-4", "object_type": "car", "confidence": 0.27, "bbox": {"x": 380, "y": 138, "width": 66, "height": 40}, "location": "City Plaza Commercial District", "image": "/detections/camera_4_plaza.jpg"},
    {"id": 36, "timestamp": (datetime.utcnow() - timedelta(seconds=15)).isoformat(), "node_id": "edge-node-4", "stream_id": "stream-4", "object_type": "car", "confidence": 0.26, "bbox": {"x": 390, "y": 188, "width": 64, "height": 38}, "location": "City Plaza Commercial District", "image": "/detections/camera_4_plaza.jpg"},
    {"id": 37, "timestamp": (datetime.utcnow() - timedelta(seconds=15)).isoformat(), "node_id": "edge-node-4", "stream_id": "stream-4", "object_type": "car", "confidence": 0.80, "bbox": {"x": 175, "y": 268, "width": 78, "height": 50}, "location": "City Plaza Commercial District", "image": "/detections/camera_4_plaza.jpg"},
    {"id": 38, "timestamp": (datetime.utcnow() - timedelta(seconds=15)).isoformat(), "node_id": "edge-node-4", "stream_id": "stream-4", "object_type": "car", "confidence": 0.77, "bbox": {"x": 155, "y": 238, "width": 74, "height": 46}, "location": "City Plaza Commercial District", "image": "/detections/camera_4_plaza.jpg"},
    {"id": 39, "timestamp": (datetime.utcnow() - timedelta(seconds=15)).isoformat(), "node_id": "edge-node-4", "stream_id": "stream-4", "object_type": "car", "confidence": 0.59, "bbox": {"x": 140, "y": 308, "width": 70, "height": 44}, "location": "City Plaza Commercial District", "image": "/detections/camera_4_plaza.jpg"},
    {"id": 40, "timestamp": (datetime.utcnow() - timedelta(seconds=15)).isoformat(), "node_id": "edge-node-4", "stream_id": "stream-4", "object_type": "people", "confidence": 0.28, "bbox": {"x": 380, "y": 268, "width": 35, "height": 55}, "location": "City Plaza Commercial District", "image": "/detections/camera_4_plaza.jpg"},
    {"id": 41, "timestamp": (datetime.utcnow() - timedelta(seconds=15)).isoformat(), "node_id": "edge-node-4", "stream_id": "stream-4", "object_type": "car", "confidence": 0.87, "bbox": {"x": 485, "y": 268, "width": 76, "height": 48}, "location": "City Plaza Commercial District", "image": "/detections/camera_4_plaza.jpg"},
    {"id": 42, "timestamp": (datetime.utcnow() - timedelta(seconds=15)).isoformat(), "node_id": "edge-node-4", "stream_id": "stream-4", "object_type": "car", "confidence": 0.84, "bbox": {"x": 505, "y": 308, "width": 72, "height": 46}, "location": "City Plaza Commercial District", "image": "/detections/camera_4_plaza.jpg"},
    
    # Additional recent detections from other cameras
    {"id": 43, "timestamp": (datetime.utcnow() - timedelta(seconds=20)).isoformat(), "node_id": "edge-node-5", "stream_id": "stream-5", "object_type": "car", "confidence": 0.78, "bbox": {"x": 200, "y": 150, "width": 70, "height": 42}, "location": "Lincoln Elementary School", "image": "/detections/camera_5_school.jpg"},
    {"id": 44, "timestamp": (datetime.utcnow() - timedelta(seconds=20)).isoformat(), "node_id": "edge-node-5", "stream_id": "stream-5", "object_type": "person", "confidence": 0.82, "bbox": {"x": 150, "y": 180, "width": 30, "height": 60}, "location": "Lincoln Elementary School", "image": "/detections/camera_5_school.jpg"},
    {"id": 45, "timestamp": (datetime.utcnow() - timedelta(seconds=20)).isoformat(), "node_id": "edge-node-5", "stream_id": "stream-5", "object_type": "bicycle", "confidence": 0.65, "bbox": {"x": 180, "y": 200, "width": 40, "height": 50}, "location": "Lincoln Elementary School", "image": "/detections/camera_5_school.jpg"},
]

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

# API Endpoints

@app.get("/")
async def root():
    return {
        "name": "EDGE-QI API",
        "version": "1.0.0",
        "description": "Backend for EDGE-QI Smart City Platform",
        "docs": "/docs",
        "websocket": "/socket.io"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

# System Endpoints
@app.get("/api/system/status")
async def system_status():
    metrics = {
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
    # Broadcast to websocket
    await sio.emit('system_metrics', metrics)
    return metrics

@app.get("/api/system/health")
async def system_health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "not_connected",
        "mqtt": "unknown",
        "redis": "unknown"
    }

@app.get("/api/system/nodes/summary")
async def nodes_summary():
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

# Node Endpoints
@app.get("/api/nodes")
async def list_nodes(status: Optional[str] = Query(None)):
    if status:
        return [n for n in MOCK_NODES if n["status"] == status]
    return MOCK_NODES

@app.get("/api/nodes/{node_id}")
async def get_node(node_id: str):
    for node in MOCK_NODES:
        if node["id"] == node_id:
            return node
    return {"error": "Node not found"}

# Detection Endpoints
@app.get("/api/detections")
async def list_detections(limit: int = Query(100)):
    return MOCK_DETECTIONS[:limit]

@app.get("/api/detections/stats/summary")
async def detection_summary():
    return {
        "total": len(MOCK_DETECTIONS),
        "time_range": "24h",
        "average_confidence": 0.92,
        "by_type": {"car": 20, "person": 15, "bicycle": 10, "motorcycle": 3, "bus": 2}
    }

# Analytics Endpoints
@app.get("/api/analytics/data")
async def analytics_data():
    return {
        "traffic_trends": [{"time": f"{h}:00", "detections": random.randint(10, 50)} for h in range(24)],
        "performance_metrics": [{"time": f"{h}:00", "latency": round(random.uniform(20, 80), 1)} for h in range(24)],
        "detection_distribution": [{"name": obj, "value": random.randint(5, 30)} for obj in ["car", "person", "bicycle", "motorcycle", "bus"]],
        "bandwidth_comparison": [{"time": f"{h}:00", "saved": round(random.uniform(50, 200), 1)} for h in range(24)],
        "energy_efficiency": [{"time": f"{h}:00", "saved": round(random.uniform(1, 10), 1)} for h in range(24)],
        "node_activity": [{"node": f"Node {i}", "detections": random.randint(50, 300)} for i in range(1, 6)]
    }

# Logs Endpoints
@app.get("/api/logs")
async def list_logs(limit: int = Query(100)):
    return MOCK_LOGS[:limit]

# Consensus Endpoints
@app.get("/api/consensus/rounds")
async def list_consensus_rounds():
    return [
        {
            "id": i,
            "round_number": i,
            "timestamp": (datetime.utcnow() - timedelta(minutes=i*5)).isoformat(),
            "success": i % 4 != 0,
            "participants": random.randint(3, 5),
            "duration_ms": random.randint(50, 200),
            "votes": {},
            "result": {},
            "byzantine_nodes": [],
            "fault_tolerance_level": 0.8
        }
        for i in range(1, 11)
    ]

@app.get("/api/consensus/stats/summary")
async def consensus_summary():
    return {
        "total_rounds": 10,
        "successful_rounds": 7,
        "success_rate": 70.0,
        "average_duration_ms": 125.0,
        "average_participants": 4.0
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting EDGE-QI Backend Server...")
    print("✅ Server started successfully (mock data mode)")
    print("📡 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/socket.io")
    uvicorn.run(socket_app, host="0.0.0.0", port=8000, log_level="info")
