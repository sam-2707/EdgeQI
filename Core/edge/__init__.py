"""
Edge Collaboration Module for EDGE-QI Framework

This module provides distributed edge computing capabilities for coordinating
queue intelligence across multiple edge devices in a smart surveillance network.

Components:
- EdgeCoordinator: Main coordination service for edge devices
- DistributedQueueManager: Manages queue data across multiple edges
- ConsensusProtocol: Implements consensus algorithms for distributed decisions
- EdgeCommunication: Handles inter-edge communication protocols
"""

from .edge_coordinator import EdgeCoordinator
from .distributed_queue_manager import DistributedQueueManager
from .consensus_protocol import ConsensusProtocol, ConsensusType
from .edge_communication import EdgeCommunication, EdgeMessage, MessageType

__all__ = [
    'EdgeCoordinator',
    'DistributedQueueManager', 
    'ConsensusProtocol',
    'ConsensusType',
    'EdgeCommunication',
    'EdgeMessage',
    'MessageType'
]