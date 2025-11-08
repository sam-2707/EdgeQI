"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============= Node Schemas =============

class NodeBase(BaseModel):
    id: str
    name: str
    status: str = "idle"
    location: Optional[str] = None


class NodeCreate(NodeBase):
    ip_address: str
    port: int
    capabilities: Dict[str, Any] = {}


class NodeUpdate(BaseModel):
    status: Optional[str] = None
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    gpu_usage: Optional[float] = None
    network_status: Optional[str] = None
    energy_consumption: Optional[float] = None
    last_heartbeat: Optional[datetime] = None


class Node(NodeBase):
    cpu_usage: float
    memory_usage: float
    gpu_usage: float = 0.0
    network_status: str
    energy_consumption: float
    ip_address: Optional[str] = None
    port: Optional[int] = None
    capabilities: Dict[str, Any] = {}
    total_detections: int = 0
    average_latency: float = 0.0
    uptime: float = 0.0
    last_heartbeat: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============= Detection Schemas =============

class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float


class DetectionBase(BaseModel):
    node_id: str
    stream_id: str
    object_type: str
    confidence: float
    bbox: BoundingBox
    location: Optional[str] = None


class DetectionCreate(DetectionBase):
    metadata: Dict[str, Any] = {}


class Detection(DetectionBase):
    id: int
    timestamp: datetime
    consensus_verified: bool = False
    consensus_confidence: Optional[float] = None
    metadata: Dict[str, Any] = {}
    
    class Config:
        from_attributes = True


# ============= System Metrics Schemas =============

class SystemMetrics(BaseModel):
    total_nodes: int
    active_nodes: int
    idle_nodes: int = 0
    fault_nodes: int = 0
    total_detections: int
    detections_per_second: float = 0.0
    average_latency: float
    average_cpu: float = 0.0
    average_memory: float = 0.0
    bandwidth_saved: float
    energy_saved: float
    timestamp: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============= Consensus Schemas =============

class ConsensusRoundBase(BaseModel):
    round_number: int
    success: bool
    participants: int
    duration_ms: int


class ConsensusRoundCreate(ConsensusRoundBase):
    votes: Dict[str, Any]
    result: Dict[str, Any]
    byzantine_nodes: List[str] = []
    fault_tolerance_level: float


class ConsensusRound(ConsensusRoundBase):
    id: int
    timestamp: datetime
    votes: Dict[str, Any]
    result: Dict[str, Any]
    byzantine_nodes: List[str] = []
    fault_tolerance_level: float
    
    class Config:
        from_attributes = True


# ============= Log Schemas =============

class LogBase(BaseModel):
    level: str
    source: str
    message: str


class LogCreate(LogBase):
    details: Dict[str, Any] = {}
    node_id: Optional[str] = None
    category: Optional[str] = None


class Log(LogBase):
    id: int
    timestamp: datetime
    details: Dict[str, Any] = {}
    node_id: Optional[str] = None
    category: Optional[str] = None
    
    class Config:
        from_attributes = True


# ============= Alert Schemas =============

class AlertBase(BaseModel):
    severity: str
    title: str
    message: str


class AlertCreate(AlertBase):
    source: str
    node_id: Optional[str] = None
    metadata: Dict[str, Any] = {}


class Alert(AlertBase):
    id: int
    timestamp: datetime
    acknowledged: bool = False
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    source: str
    node_id: Optional[str] = None
    metadata: Dict[str, Any] = {}
    
    class Config:
        from_attributes = True


# ============= Analytics Schemas =============

class TimeSeriesData(BaseModel):
    timestamp: datetime
    value: float


class AnalyticsData(BaseModel):
    label: str
    data: List[TimeSeriesData]


class AnalyticsResponse(BaseModel):
    traffic_trends: List[Dict[str, Any]]
    performance_metrics: List[Dict[str, Any]]
    detection_distribution: List[Dict[str, Any]]
    bandwidth_comparison: List[Dict[str, Any]]
    energy_efficiency: List[Dict[str, Any]]
    node_activity: List[Dict[str, Any]]


# ============= Health Check Schema =============

class HealthCheck(BaseModel):
    status: str
    version: str
    timestamp: datetime
    database: str = "unknown"
    mqtt: str = "unknown"
    redis: str = "unknown"
