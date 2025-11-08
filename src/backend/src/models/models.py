"""
Database models for EDGE-QI system
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class EdgeNode(Base):
    """Edge node model"""
    __tablename__ = "edge_nodes"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    status = Column(String(20), default="idle")  # active, idle, fault
    location = Column(String(200))
    
    # Resource metrics
    cpu_usage = Column(Float, default=0.0)
    memory_usage = Column(Float, default=0.0)
    gpu_usage = Column(Float, default=0.0)
    network_status = Column(String(20), default="good")
    energy_consumption = Column(Float, default=0.0)
    
    # Network info
    ip_address = Column(String(50))
    port = Column(Integer)
    
    # Capabilities
    capabilities = Column(JSON)
    
    # Performance metrics
    total_detections = Column(Integer, default=0)
    average_latency = Column(Float, default=0.0)
    uptime = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_heartbeat = Column(DateTime)
    
    # Relationships
    detections = relationship("Detection", back_populates="node")


class Detection(Base):
    """Detection result model"""
    __tablename__ = "detections"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Node info
    node_id = Column(String(50), ForeignKey("edge_nodes.id"))
    stream_id = Column(String(50))
    
    # Detection info
    object_type = Column(String(50))
    confidence = Column(Float)
    bbox = Column(JSON)  # {x, y, width, height}
    
    # Location and metadata
    location = Column(String(200))
    metadata = Column(JSON)
    
    # Consensus info
    consensus_verified = Column(Boolean, default=False)
    consensus_confidence = Column(Float)
    
    # Relationships
    node = relationship("EdgeNode", back_populates="detections")


class SystemMetric(Base):
    """System-wide metrics model"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Node metrics
    total_nodes = Column(Integer, default=0)
    active_nodes = Column(Integer, default=0)
    idle_nodes = Column(Integer, default=0)
    fault_nodes = Column(Integer, default=0)
    
    # Detection metrics
    total_detections = Column(Integer, default=0)
    detections_per_second = Column(Float, default=0.0)
    
    # Performance metrics
    average_latency = Column(Float, default=0.0)
    average_cpu = Column(Float, default=0.0)
    average_memory = Column(Float, default=0.0)
    
    # Savings metrics
    bandwidth_saved = Column(Float, default=0.0)
    energy_saved = Column(Float, default=0.0)
    
    # Additional metadata
    metadata = Column(JSON)


class ConsensusRound(Base):
    """Byzantine consensus round model"""
    __tablename__ = "consensus_rounds"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    round_number = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Round info
    success = Column(Boolean, default=False)
    participants = Column(Integer)
    duration_ms = Column(Integer)
    
    # Voting details
    votes = Column(JSON)  # {node_id: vote}
    result = Column(JSON)
    
    # Fault tolerance
    byzantine_nodes = Column(JSON)  # List of suspected Byzantine nodes
    fault_tolerance_level = Column(Float)


class SystemLog(Base):
    """System log model"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Log info
    level = Column(String(20), index=True)  # info, warning, error, critical
    source = Column(String(100))
    message = Column(Text)
    
    # Additional details
    details = Column(JSON)
    node_id = Column(String(50))
    
    # Categorization
    category = Column(String(50))  # system, detection, consensus, network


class Alert(Base):
    """System alert model"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Alert info
    severity = Column(String(20))  # low, medium, high, critical
    title = Column(String(200))
    message = Column(Text)
    
    # Status
    acknowledged = Column(Boolean, default=False)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime)
    
    # Source
    source = Column(String(100))
    node_id = Column(String(50))
    
    # Additional data
    metadata = Column(JSON)
