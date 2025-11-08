"""
Edge Communication Module

Handles inter-edge communication protocols for the EDGE-QI framework.
Implements secure, efficient communication between edge devices for
queue intelligence sharing and coordination.
"""

import json
import time
import asyncio
import hashlib
import logging
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from collections import defaultdict
import socket
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageType(Enum):
    """Types of messages exchanged between edge devices"""
    QUEUE_UPDATE = "queue_update"
    TRAFFIC_STATE = "traffic_state"
    ANOMALY_ALERT = "anomaly_alert"
    CONSENSUS_REQUEST = "consensus_request"
    CONSENSUS_RESPONSE = "consensus_response"
    HEARTBEAT = "heartbeat"
    COORDINATION_REQUEST = "coordination_request"
    COORDINATION_RESPONSE = "coordination_response"
    EMERGENCY_ALERT = "emergency_alert"
    HANDSHAKE = "handshake"
    ACK = "ack"
    NACK = "nack"

@dataclass
class EdgeMessage:
    """Message structure for inter-edge communication"""
    message_id: str
    sender_id: str
    receiver_id: str  # Can be "broadcast" for all edges
    message_type: MessageType
    timestamp: float
    data: Dict[str, Any]
    priority: int = 1  # 1=low, 5=high, 10=emergency
    ttl: int = 60  # Time to live in seconds
    checksum: str = ""
    
    def __post_init__(self):
        """Calculate checksum after initialization"""
        if not self.checksum:
            self.checksum = self.calculate_checksum()
    
    def calculate_checksum(self) -> str:
        """Calculate message checksum for integrity verification"""
        # Create a copy without checksum for calculation
        data_for_hash = {
            'message_id': self.message_id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'message_type': self.message_type.value,
            'timestamp': self.timestamp,
            'data': json.dumps(self.data, sort_keys=True),
            'priority': self.priority,
            'ttl': self.ttl
        }
        message_str = json.dumps(data_for_hash, sort_keys=True)
        return hashlib.sha256(message_str.encode()).hexdigest()[:16]
    
    def is_valid(self) -> bool:
        """Verify message integrity"""
        return self.checksum == self.calculate_checksum()
    
    def is_expired(self) -> bool:
        """Check if message has expired"""
        return time.time() - self.timestamp > self.ttl
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        result = asdict(self)
        result['message_type'] = self.message_type.value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EdgeMessage':
        """Create message from dictionary"""
        data['message_type'] = MessageType(data['message_type'])
        return cls(**data)
    
    def to_json(self) -> str:
        """Serialize message to JSON"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'EdgeMessage':
        """Deserialize message from JSON"""
        return cls.from_dict(json.loads(json_str))

class EdgeCommunication:
    """
    Communication manager for inter-edge device coordination.
    
    Handles:
    - Message routing and delivery
    - Security and authentication 
    - Network topology management
    - Quality of Service (QoS)
    - Fault tolerance and recovery
    """
    
    def __init__(self, 
                 edge_id: str,
                 listen_port: int = 8765,
                 max_connections: int = 10):
        self.edge_id = edge_id
        self.listen_port = listen_port
        self.max_connections = max_connections
        
        # Network state
        self.connected_edges: Dict[str, Dict[str, Any]] = {}
        self.message_queue = asyncio.Queue()
        self.pending_messages: Dict[str, EdgeMessage] = {}
        self.message_handlers: Dict[MessageType, Callable] = {}
        
        # Statistics
        self.stats = {
            'messages_sent': 0,
            'messages_received': 0,
            'messages_dropped': 0,
            'bytes_sent': 0,
            'bytes_received': 0,
            'connection_attempts': 0,
            'successful_connections': 0
        }
        
        # State management
        self.is_running = False
        self.server = None
        self.background_tasks = []
        
        logger.info(f"Edge Communication initialized for {edge_id} on port {listen_port}")
    
    def register_handler(self, message_type: MessageType, handler: Callable):
        """Register a handler for specific message types"""
        self.message_handlers[message_type] = handler
        logger.info(f"Registered handler for {message_type.value}")
    
    async def start(self):
        """Start the communication service"""
        self.is_running = True
        
        # Start message processing
        task = asyncio.create_task(self._process_message_queue())
        self.background_tasks.append(task)
        
        # Start heartbeat service
        task = asyncio.create_task(self._heartbeat_service())
        self.background_tasks.append(task)
        
        # Start cleanup service
        task = asyncio.create_task(self._cleanup_service())
        self.background_tasks.append(task)
        
        logger.info(f"Edge communication service started for {self.edge_id}")
    
    async def stop(self):
        """Stop the communication service"""
        self.is_running = False
        
        # Cancel background tasks
        for task in self.background_tasks:
            task.cancel()
        
        # Close connections
        for edge_id in list(self.connected_edges.keys()):
            await self.disconnect_edge(edge_id)
        
        logger.info(f"Edge communication service stopped for {self.edge_id}")
    
    async def connect_to_edge(self, target_edge_id: str, host: str, port: int) -> bool:
        """Establish connection to another edge device"""
        try:
            self.stats['connection_attempts'] += 1
            
            # Create connection info
            connection_info = {
                'edge_id': target_edge_id,
                'host': host,
                'port': port,
                'connected_at': time.time(),
                'last_heartbeat': time.time(),
                'status': 'connecting'
            }
            
            # Simulate connection (in real implementation, use actual networking)
            await asyncio.sleep(0.1)  # Simulate network delay
            
            # Add to connected edges
            self.connected_edges[target_edge_id] = connection_info
            connection_info['status'] = 'connected'
            
            # Send handshake
            handshake_msg = EdgeMessage(
                message_id=f"handshake_{int(time.time())}",
                sender_id=self.edge_id,
                receiver_id=target_edge_id,
                message_type=MessageType.HANDSHAKE,
                timestamp=time.time(),
                data={'edge_capabilities': self._get_edge_capabilities()}
            )
            
            await self.send_message(handshake_msg)
            
            self.stats['successful_connections'] += 1
            logger.info(f"Connected to edge {target_edge_id} at {host}:{port}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to edge {target_edge_id}: {e}")
            return False
    
    async def disconnect_edge(self, edge_id: str):
        """Disconnect from an edge device"""
        if edge_id in self.connected_edges:
            del self.connected_edges[edge_id]
            logger.info(f"Disconnected from edge {edge_id}")
    
    async def send_message(self, message: EdgeMessage) -> bool:
        """Send message to target edge(s)"""
        try:
            if message.receiver_id == "broadcast":
                # Broadcast to all connected edges
                success_count = 0
                for edge_id in self.connected_edges:
                    msg_copy = EdgeMessage(
                        message_id=f"{message.message_id}_{edge_id}",
                        sender_id=message.sender_id,
                        receiver_id=edge_id,
                        message_type=message.message_type,
                        timestamp=message.timestamp,
                        data=message.data.copy(),
                        priority=message.priority,
                        ttl=message.ttl
                    )
                    if await self._send_to_edge(msg_copy, edge_id):
                        success_count += 1
                
                self.stats['messages_sent'] += success_count
                return success_count > 0
            
            else:
                # Send to specific edge
                if message.receiver_id in self.connected_edges:
                    success = await self._send_to_edge(message, message.receiver_id)
                    if success:
                        self.stats['messages_sent'] += 1
                    return success
                else:
                    logger.warning(f"Edge {message.receiver_id} not connected")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to send message {message.message_id}: {e}")
            self.stats['messages_dropped'] += 1
            return False
    
    async def _send_to_edge(self, message: EdgeMessage, edge_id: str) -> bool:
        """Send message to specific edge"""
        try:
            # Simulate network transmission
            json_data = message.to_json()
            self.stats['bytes_sent'] += len(json_data.encode())
            
            # Add to pending messages for ACK tracking
            self.pending_messages[message.message_id] = message
            
            # Simulate successful transmission
            await asyncio.sleep(0.01)  # Network latency
            
            logger.debug(f"Sent message {message.message_id} to {edge_id}")
            return True
            
        except Exception as e:
            logger.error(f"Network error sending to {edge_id}: {e}")
            return False
    
    async def receive_message(self, message: EdgeMessage):
        """Process received message"""
        try:
            # Validate message
            if not message.is_valid():
                logger.warning(f"Invalid message received: {message.message_id}")
                self.stats['messages_dropped'] += 1
                return
            
            if message.is_expired():
                logger.warning(f"Expired message received: {message.message_id}")
                self.stats['messages_dropped'] += 1
                return
            
            # Update statistics
            self.stats['messages_received'] += 1
            self.stats['bytes_received'] += len(message.to_json().encode())
            
            # Handle specific message types
            if message.message_type in self.message_handlers:
                await self.message_handlers[message.message_type](message)
            else:
                await self._default_message_handler(message)
            
            # Send ACK if not a broadcast
            if message.receiver_id != "broadcast":
                ack_msg = EdgeMessage(
                    message_id=f"ack_{message.message_id}",
                    sender_id=self.edge_id,
                    receiver_id=message.sender_id,
                    message_type=MessageType.ACK,
                    timestamp=time.time(),
                    data={'original_message_id': message.message_id}
                )
                await self.send_message(ack_msg)
            
        except Exception as e:
            logger.error(f"Error processing message {message.message_id}: {e}")
    
    async def _default_message_handler(self, message: EdgeMessage):
        """Default handler for unregistered message types"""
        logger.info(f"Received {message.message_type.value} from {message.sender_id}")
        
        # Handle common message types
        if message.message_type == MessageType.HEARTBEAT:
            await self._handle_heartbeat(message)
        elif message.message_type == MessageType.HANDSHAKE:
            await self._handle_handshake(message)
        elif message.message_type == MessageType.ACK:
            await self._handle_ack(message)
    
    async def _handle_heartbeat(self, message: EdgeMessage):
        """Handle heartbeat messages"""
        if message.sender_id in self.connected_edges:
            self.connected_edges[message.sender_id]['last_heartbeat'] = time.time()
    
    async def _handle_handshake(self, message: EdgeMessage):
        """Handle handshake messages"""
        logger.info(f"Handshake from {message.sender_id}")
        # Could implement capability negotiation here
    
    async def _handle_ack(self, message: EdgeMessage):
        """Handle acknowledgment messages"""
        original_id = message.data.get('original_message_id')
        if original_id in self.pending_messages:
            del self.pending_messages[original_id]
    
    async def _process_message_queue(self):
        """Background task to process message queue"""
        while self.is_running:
            try:
                # Process any queued messages
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in message processing: {e}")
    
    async def _heartbeat_service(self):
        """Background heartbeat service"""
        while self.is_running:
            try:
                # Send heartbeat to all connected edges
                heartbeat_msg = EdgeMessage(
                    message_id=f"heartbeat_{int(time.time())}",
                    sender_id=self.edge_id,
                    receiver_id="broadcast",
                    message_type=MessageType.HEARTBEAT,
                    timestamp=time.time(),
                    data={'status': 'alive', 'load': self._get_current_load()}
                )
                
                await self.send_message(heartbeat_msg)
                await asyncio.sleep(30)  # Send heartbeat every 30 seconds
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in heartbeat service: {e}")
    
    async def _cleanup_service(self):
        """Background cleanup service"""
        while self.is_running:
            try:
                current_time = time.time()
                
                # Clean up expired pending messages
                expired_messages = [
                    msg_id for msg_id, msg in self.pending_messages.items()
                    if msg.is_expired()
                ]
                for msg_id in expired_messages:
                    del self.pending_messages[msg_id]
                
                # Check for disconnected edges (no heartbeat for 2 minutes)
                disconnected_edges = [
                    edge_id for edge_id, info in self.connected_edges.items()
                    if current_time - info['last_heartbeat'] > 120
                ]
                for edge_id in disconnected_edges:
                    logger.warning(f"Edge {edge_id} appears disconnected")
                    await self.disconnect_edge(edge_id)
                
                await asyncio.sleep(60)  # Cleanup every minute
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cleanup service: {e}")
    
    def _get_edge_capabilities(self) -> Dict[str, Any]:
        """Get current edge device capabilities"""
        return {
            'queue_detection': True,
            'traffic_analysis': True,
            'anomaly_detection': True,
            'max_streams': 4,
            'compute_power': 'medium'
        }
    
    def _get_current_load(self) -> float:
        """Get current system load (0.0 to 1.0)"""
        # In real implementation, would check actual system metrics
        return 0.3  # Simulated load
    
    def get_network_topology(self) -> Dict[str, Any]:
        """Get current network topology"""
        return {
            'edge_id': self.edge_id,
            'connected_edges': list(self.connected_edges.keys()),
            'connection_count': len(self.connected_edges),
            'network_health': self._calculate_network_health()
        }
    
    def _calculate_network_health(self) -> float:
        """Calculate overall network health score"""
        if not self.connected_edges:
            return 0.0
        
        current_time = time.time()
        healthy_connections = sum(
            1 for info in self.connected_edges.values()
            if current_time - info['last_heartbeat'] < 60
        )
        
        return healthy_connections / len(self.connected_edges)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get communication statistics"""
        stats = self.stats.copy()
        stats['connected_edges'] = len(self.connected_edges)
        stats['pending_messages'] = len(self.pending_messages)
        stats['network_health'] = self._calculate_network_health()
        stats['uptime'] = time.time() if self.is_running else 0
        return stats

# Utility functions for message creation
def create_queue_update_message(sender_id: str, receiver_id: str, queue_data: Dict[str, Any]) -> EdgeMessage:
    """Create a queue update message"""
    return EdgeMessage(
        message_id=f"queue_update_{int(time.time())}",
        sender_id=sender_id,
        receiver_id=receiver_id,
        message_type=MessageType.QUEUE_UPDATE,
        timestamp=time.time(),
        data=queue_data,
        priority=3
    )

def create_traffic_state_message(sender_id: str, receiver_id: str, traffic_data: Dict[str, Any]) -> EdgeMessage:
    """Create a traffic state message"""
    return EdgeMessage(
        message_id=f"traffic_state_{int(time.time())}",
        sender_id=sender_id,
        receiver_id=receiver_id,
        message_type=MessageType.TRAFFIC_STATE,
        timestamp=time.time(),
        data=traffic_data,
        priority=4
    )

def create_emergency_alert_message(sender_id: str, alert_data: Dict[str, Any]) -> EdgeMessage:
    """Create an emergency alert message (broadcast)"""
    return EdgeMessage(
        message_id=f"emergency_{int(time.time())}",
        sender_id=sender_id,
        receiver_id="broadcast",
        message_type=MessageType.EMERGENCY_ALERT,
        timestamp=time.time(),
        data=alert_data,
        priority=10,
        ttl=300  # 5 minutes TTL for emergency messages
    )