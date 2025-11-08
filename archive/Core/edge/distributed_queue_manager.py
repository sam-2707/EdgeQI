"""
Distributed Queue Manager

Manages queue intelligence data across multiple edge devices.
Implements distributed queue detection, analysis, and optimization
with real-time synchronization and conflict resolution.
"""

import asyncio
import time
import json
import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
from enum import Enum
import numpy as np

from .edge_communication import EdgeCommunication, EdgeMessage, MessageType, create_queue_update_message
from .consensus_protocol import ConsensusProtocol, propose_traffic_signal_change

logger = logging.getLogger(__name__)

class QueueEventType(Enum):
    """Types of queue events"""
    QUEUE_FORMED = "queue_formed"
    QUEUE_DISSOLVED = "queue_dissolved"
    QUEUE_EXTENDED = "queue_extended"
    QUEUE_REDUCED = "queue_reduced"
    CONGESTION_DETECTED = "congestion_detected"
    CONGESTION_CLEARED = "congestion_cleared"
    ANOMALY_DETECTED = "anomaly_detected"

@dataclass
class DistributedQueue:
    """Distributed representation of a queue across multiple camera views"""
    queue_id: str
    primary_edge: str  # Edge device with primary view
    contributing_edges: List[str]  # Other edges that can see parts of this queue
    queue_type: str  # "pedestrian", "vehicle", "mixed"
    location: Tuple[float, float]  # Global coordinates
    length: float
    average_wait_time: float
    density: float
    direction: Tuple[float, float]  # Movement direction
    confidence: float
    last_updated: float
    metadata: Dict[str, Any]

@dataclass
class QueueEvent:
    """Queue-related event for distributed tracking"""
    event_id: str
    queue_id: str
    event_type: QueueEventType
    edge_id: str
    timestamp: float
    data: Dict[str, Any]
    confidence: float
    processed_by: Set[str]  # Edges that have processed this event

@dataclass
class EdgeQueueData:
    """Queue data from a specific edge device"""
    edge_id: str
    camera_id: str
    local_queues: List[Dict[str, Any]]
    traffic_density: float
    flow_rate: float
    timestamp: float
    camera_position: Tuple[float, float]
    camera_orientation: float
    coverage_area: List[Tuple[float, float]]  # Polygon defining coverage

class DistributedQueueManager:
    """
    Manages queue intelligence across multiple edge devices.
    
    Features:
    - Multi-view queue fusion and correlation
    - Distributed queue state synchronization
    - Conflict resolution and consensus-based decisions
    - Cross-edge queue tracking and handoff
    - Global queue optimization recommendations
    """
    
    def __init__(self, 
                 edge_id: str,
                 communication: EdgeCommunication,
                 consensus: ConsensusProtocol,
                 camera_position: Tuple[float, float] = (0.0, 0.0),
                 camera_orientation: float = 0.0):
        self.edge_id = edge_id
        self.communication = communication
        self.consensus = consensus
        self.camera_position = camera_position
        self.camera_orientation = camera_orientation
        
        # Queue management state
        self.global_queues: Dict[str, DistributedQueue] = {}
        self.local_queue_data: Dict[str, EdgeQueueData] = {}  # edge_id -> data
        self.queue_events: deque = deque(maxlen=1000)
        self.queue_correlations: Dict[str, List[str]] = {}  # queue_id -> [related_queue_ids]
        
        # Synchronization state
        self.last_sync_time = 0.0
        self.sync_interval = 10.0  # Sync every 10 seconds
        self.pending_updates: Dict[str, Dict[str, Any]] = {}
        
        # Analytics and optimization
        self.queue_analytics = {
            'total_queues': 0,
            'average_wait_time': 0.0,
            'peak_congestion_time': 0.0,
            'efficiency_score': 1.0,
            'optimization_opportunities': []
        }
        
        # Edge coordination
        self.edge_capabilities: Dict[str, Dict[str, Any]] = {}
        self.coverage_map: Dict[str, List[Tuple[float, float]]] = {}
        
        # Register message handlers
        self.communication.register_handler(
            MessageType.QUEUE_UPDATE,
            self._handle_queue_update
        )
        
        logger.info(f"Distributed Queue Manager initialized for edge {edge_id}")
    
    async def start(self):
        """Start the distributed queue management service"""
        # Start background synchronization
        asyncio.create_task(self._sync_service())
        asyncio.create_task(self._analytics_service())
        asyncio.create_task(self._optimization_service())
        
        logger.info(f"Distributed queue management started for {self.edge_id}")
    
    async def update_local_queues(self, queue_data: List[Dict[str, Any]], camera_id: str = "default"):
        """Update local queue detection results"""
        current_time = time.time()
        
        # Create edge queue data
        edge_data = EdgeQueueData(
            edge_id=self.edge_id,
            camera_id=camera_id,
            local_queues=queue_data,
            traffic_density=self._calculate_traffic_density(queue_data),
            flow_rate=self._calculate_flow_rate(queue_data),
            timestamp=current_time,
            camera_position=self.camera_position,
            camera_orientation=self.camera_orientation,
            coverage_area=self._get_coverage_area()
        )
        
        # Store local data
        self.local_queue_data[self.edge_id] = edge_data
        
        # Process queue changes
        await self._process_queue_changes(queue_data)
        
        # Schedule update broadcast
        self.pending_updates[self.edge_id] = {
            'edge_data': edge_data,
            'timestamp': current_time
        }
        
        logger.debug(f"Updated local queues: {len(queue_data)} queues detected")
    
    async def _process_queue_changes(self, new_queue_data: List[Dict[str, Any]]):
        """Process changes in local queue detection"""
        current_time = time.time()
        
        # Compare with previous state to detect events
        previous_queues = {q.queue_id: q for q in self.global_queues.values() 
                          if q.primary_edge == self.edge_id}
        
        current_queue_ids = set()
        
        for queue_info in new_queue_data:
            queue_id = f"{self.edge_id}_{queue_info.get('id', int(current_time))}"
            current_queue_ids.add(queue_id)
            
            # Check if this is a new queue
            if queue_id not in previous_queues:
                await self._create_queue_event(
                    queue_id, 
                    QueueEventType.QUEUE_FORMED,
                    queue_info
                )
            else:
                # Check for significant changes
                prev_queue = previous_queues[queue_id]
                if self._has_significant_change(prev_queue, queue_info):
                    event_type = (QueueEventType.QUEUE_EXTENDED 
                                if queue_info.get('length', 0) > prev_queue.length
                                else QueueEventType.QUEUE_REDUCED)
                    await self._create_queue_event(queue_id, event_type, queue_info)
        
        # Detect dissolved queues
        for prev_queue_id in previous_queues:
            if prev_queue_id not in current_queue_ids:
                await self._create_queue_event(
                    prev_queue_id,
                    QueueEventType.QUEUE_DISSOLVED,
                    {}
                )
    
    async def _create_queue_event(self, queue_id: str, event_type: QueueEventType, data: Dict[str, Any]):
        """Create and process a queue event"""
        event_id = f"{self.edge_id}_{event_type.value}_{int(time.time())}"
        
        event = QueueEvent(
            event_id=event_id,
            queue_id=queue_id,
            event_type=event_type,
            edge_id=self.edge_id,
            timestamp=time.time(),
            data=data,
            confidence=data.get('confidence', 0.8),
            processed_by={self.edge_id}
        )
        
        self.queue_events.append(event)
        
        # Broadcast significant events
        if event_type in [QueueEventType.QUEUE_FORMED, QueueEventType.CONGESTION_DETECTED, 
                         QueueEventType.ANOMALY_DETECTED]:
            await self._broadcast_queue_event(event)
        
        logger.info(f"Created queue event {event_type.value} for queue {queue_id}")
    
    async def _broadcast_queue_event(self, event: QueueEvent):
        """Broadcast queue event to other edges"""
        message_data = {
            'event_id': event.event_id,
            'queue_id': event.queue_id,
            'event_type': event.event_type.value,
            'timestamp': event.timestamp,
            'data': event.data,
            'confidence': event.confidence
        }
        
        # Create and send message
        message = EdgeMessage(
            message_id=f"queue_event_{event.event_id}",
            sender_id=self.edge_id,
            receiver_id="broadcast",
            message_type=MessageType.QUEUE_UPDATE,
            timestamp=time.time(),
            data={'event': message_data},
            priority=5 if event.event_type == QueueEventType.ANOMALY_DETECTED else 3
        )
        
        await self.communication.send_message(message)
    
    async def _handle_queue_update(self, message: EdgeMessage):
        """Handle queue updates from other edges"""
        try:
            sender_id = message.sender_id
            
            # Handle different types of queue updates
            if 'event' in message.data:
                await self._handle_queue_event(message.data['event'], sender_id)
            elif 'edge_data' in message.data:
                await self._handle_edge_data_update(message.data, sender_id)
            elif 'global_queues' in message.data:
                await self._handle_global_queue_sync(message.data, sender_id)
            
        except Exception as e:
            logger.error(f"Error handling queue update from {message.sender_id}: {e}")
    
    async def _handle_queue_event(self, event_data: Dict[str, Any], sender_id: str):
        """Handle queue event from another edge"""
        event_id = event_data['event_id']
        
        # Check if we've already processed this event
        for existing_event in self.queue_events:
            if existing_event.event_id == event_id:
                existing_event.processed_by.add(sender_id)
                return
        
        # Create new event
        event = QueueEvent(
            event_id=event_id,
            queue_id=event_data['queue_id'],
            event_type=QueueEventType(event_data['event_type']),
            edge_id=sender_id,
            timestamp=event_data['timestamp'],
            data=event_data['data'],
            confidence=event_data['confidence'],
            processed_by={sender_id, self.edge_id}
        )
        
        self.queue_events.append(event)
        
        # Process event for correlation and fusion
        await self._process_cross_edge_event(event)
        
        logger.info(f"Processed queue event {event.event_type.value} from {sender_id}")
    
    async def _handle_edge_data_update(self, data: Dict[str, Any], sender_id: str):
        """Handle edge queue data updates"""
        edge_data_dict = data['edge_data']
        
        # Convert to EdgeQueueData object
        edge_data = EdgeQueueData(
            edge_id=edge_data_dict['edge_id'],
            camera_id=edge_data_dict['camera_id'],
            local_queues=edge_data_dict['local_queues'],
            traffic_density=edge_data_dict['traffic_density'],
            flow_rate=edge_data_dict['flow_rate'],
            timestamp=edge_data_dict['timestamp'],
            camera_position=tuple(edge_data_dict['camera_position']),
            camera_orientation=edge_data_dict['camera_orientation'],
            coverage_area=edge_data_dict['coverage_area']
        )
        
        # Store data
        self.local_queue_data[sender_id] = edge_data
        
        # Update coverage map
        self.coverage_map[sender_id] = edge_data.coverage_area
        
        # Trigger queue fusion analysis
        await self._analyze_queue_correlations()
    
    async def _process_cross_edge_event(self, event: QueueEvent):
        """Process events from other edges for correlation"""
        # Check if this event correlates with our local queues
        correlations = await self._find_queue_correlations(event)
        
        if correlations:
            # Update global queue state
            await self._update_global_queue_from_correlation(event, correlations)
        
        # Check for optimization opportunities
        if event.event_type == QueueEventType.CONGESTION_DETECTED:
            await self._analyze_congestion_optimization(event)
    
    async def _find_queue_correlations(self, event: QueueEvent) -> List[str]:
        """Find correlations between queue event and local queues"""
        correlations = []
        
        if self.edge_id not in self.local_queue_data:
            return correlations
        
        local_data = self.local_queue_data[self.edge_id]
        event_location = event.data.get('location')
        
        if not event_location:
            return correlations
        
        # Check spatial correlation
        for local_queue in local_data.local_queues:
            local_location = local_queue.get('center')
            if local_location:
                distance = self._calculate_distance(event_location, local_location)
                if distance < 50.0:  # Within 50 units (meters/pixels)
                    correlations.append(local_queue.get('id', ''))
        
        return correlations
    
    async def _update_global_queue_from_correlation(self, event: QueueEvent, correlations: List[str]):
        """Update global queue state based on correlations"""
        queue_id = event.queue_id
        
        # Create or update distributed queue
        if queue_id not in self.global_queues:
            # Create new distributed queue
            distributed_queue = DistributedQueue(
                queue_id=queue_id,
                primary_edge=event.edge_id,
                contributing_edges=[self.edge_id] if correlations else [],
                queue_type=event.data.get('type', 'unknown'),
                location=event.data.get('location', (0.0, 0.0)),
                length=event.data.get('length', 0.0),
                average_wait_time=event.data.get('wait_time', 0.0),
                density=event.data.get('density', 0.0),
                direction=event.data.get('direction', (0.0, 0.0)),
                confidence=event.confidence,
                last_updated=event.timestamp,
                metadata={}
            )
            
            self.global_queues[queue_id] = distributed_queue
        else:
            # Update existing queue
            queue = self.global_queues[queue_id]
            if self.edge_id not in queue.contributing_edges and correlations:
                queue.contributing_edges.append(self.edge_id)
            
            # Merge data using weighted average based on confidence
            total_confidence = queue.confidence + event.confidence
            if total_confidence > 0:
                weight = event.confidence / total_confidence
                queue.length = queue.length * (1 - weight) + event.data.get('length', 0) * weight
                queue.average_wait_time = (queue.average_wait_time * (1 - weight) + 
                                         event.data.get('wait_time', 0) * weight)
                queue.density = queue.density * (1 - weight) + event.data.get('density', 0) * weight
            
            queue.confidence = min(1.0, total_confidence / 2.0)
            queue.last_updated = event.timestamp
    
    async def _analyze_queue_correlations(self):
        """Analyze correlations between queues from different edges"""
        if len(self.local_queue_data) < 2:
            return
        
        # Find overlapping coverage areas
        edge_ids = list(self.local_queue_data.keys())
        
        for i, edge1 in enumerate(edge_ids):
            for edge2 in edge_ids[i+1:]:
                overlap = self._calculate_coverage_overlap(edge1, edge2)
                if overlap > 0.1:  # 10% overlap threshold
                    await self._correlate_queues_between_edges(edge1, edge2)
    
    def _calculate_coverage_overlap(self, edge1: str, edge2: str) -> float:
        """Calculate coverage area overlap between two edges"""
        if edge1 not in self.coverage_map or edge2 not in self.coverage_map:
            return 0.0
        
        # Simplified overlap calculation (in real implementation, use polygon intersection)
        area1 = self.coverage_map[edge1]
        area2 = self.coverage_map[edge2]
        
        # Simple bounding box overlap calculation
        if len(area1) >= 2 and len(area2) >= 2:
            # Assume rectangular areas for simplification
            return 0.2  # Simulated overlap
        
        return 0.0
    
    async def _correlate_queues_between_edges(self, edge1: str, edge2: str):
        """Correlate queues between two edge devices"""
        if edge1 not in self.local_queue_data or edge2 not in self.local_queue_data:
            return
        
        data1 = self.local_queue_data[edge1]
        data2 = self.local_queue_data[edge2]
        
        # Find queue pairs that might be the same queue seen from different angles
        for queue1 in data1.local_queues:
            for queue2 in data2.local_queues:
                correlation_score = self._calculate_queue_correlation(queue1, queue2)
                if correlation_score > 0.7:  # High correlation threshold
                    await self._merge_correlated_queues(queue1, queue2, edge1, edge2)
    
    def _calculate_queue_correlation(self, queue1: Dict[str, Any], queue2: Dict[str, Any]) -> float:
        """Calculate correlation score between two queue observations"""
        # Spatial correlation
        loc1 = queue1.get('center', (0, 0))
        loc2 = queue2.get('center', (0, 0))
        distance = self._calculate_distance(loc1, loc2)
        spatial_score = max(0, 1 - distance / 100.0)  # Normalize by 100 units
        
        # Temporal correlation
        time1 = queue1.get('timestamp', 0)
        time2 = queue2.get('timestamp', 0)
        time_diff = abs(time1 - time2)
        temporal_score = max(0, 1 - time_diff / 60.0)  # Normalize by 1 minute
        
        # Direction correlation
        dir1 = queue1.get('direction', (0, 0))
        dir2 = queue2.get('direction', (0, 0))
        direction_score = self._calculate_direction_similarity(dir1, dir2)
        
        # Combined score
        return (spatial_score * 0.4 + temporal_score * 0.3 + direction_score * 0.3)
    
    async def _merge_correlated_queues(self, queue1: Dict[str, Any], queue2: Dict[str, Any],
                                     edge1: str, edge2: str):
        """Merge two correlated queue observations into a global queue"""
        # Create merged queue ID
        merged_id = f"global_{min(edge1, edge2)}_{max(edge1, edge2)}_{int(time.time())}"
        
        # Calculate merged properties
        confidence1 = queue1.get('confidence', 0.5)
        confidence2 = queue2.get('confidence', 0.5)
        total_confidence = confidence1 + confidence2
        
        if total_confidence > 0:
            w1, w2 = confidence1 / total_confidence, confidence2 / total_confidence
            
            merged_location = (
                queue1.get('center', (0, 0))[0] * w1 + queue2.get('center', (0, 0))[0] * w2,
                queue1.get('center', (0, 0))[1] * w1 + queue2.get('center', (0, 0))[1] * w2
            )
            
            merged_length = queue1.get('length', 0) * w1 + queue2.get('length', 0) * w2
            merged_wait_time = queue1.get('wait_time', 0) * w1 + queue2.get('wait_time', 0) * w2
        else:
            merged_location = queue1.get('center', (0, 0))
            merged_length = queue1.get('length', 0)
            merged_wait_time = queue1.get('wait_time', 0)
        
        # Create distributed queue
        distributed_queue = DistributedQueue(
            queue_id=merged_id,
            primary_edge=edge1,  # First edge is primary
            contributing_edges=[edge2],
            queue_type=queue1.get('type', 'unknown'),
            location=merged_location,
            length=merged_length,
            average_wait_time=merged_wait_time,
            density=(queue1.get('density', 0) + queue2.get('density', 0)) / 2,
            direction=queue1.get('direction', (0, 0)),
            confidence=min(1.0, total_confidence / 2),
            last_updated=time.time(),
            metadata={'merged_from': [queue1.get('id'), queue2.get('id')]}
        )
        
        self.global_queues[merged_id] = distributed_queue
        logger.info(f"Merged queues from {edge1} and {edge2} into {merged_id}")
    
    async def _analyze_congestion_optimization(self, event: QueueEvent):
        """Analyze congestion events for optimization opportunities"""
        if event.event_type != QueueEventType.CONGESTION_DETECTED:
            return
        
        # Check if we should propose signal timing changes
        location = event.data.get('location')
        congestion_level = event.data.get('congestion_level', 0.5)
        
        if congestion_level > 0.7:  # High congestion
            # Propose signal timing optimization through consensus
            optimization_data = {
                'intersection_id': f"intersection_{location}",
                'current_congestion': congestion_level,
                'proposed_timing': self._calculate_optimal_timing(event.data),
                'expected_improvement': 0.2  # 20% improvement estimate
            }
            
            try:
                result = await propose_traffic_signal_change(
                    self.consensus,
                    optimization_data['intersection_id'],
                    optimization_data['proposed_timing'],
                    congestion_level,
                    optimization_data['expected_improvement']
                )
                
                if result.decision:
                    logger.info(f"Consensus reached for signal optimization at {location}")
                    await self._implement_signal_optimization(optimization_data)
                
            except Exception as e:
                logger.error(f"Error proposing signal optimization: {e}")
    
    def _calculate_optimal_timing(self, congestion_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate optimal signal timing based on congestion data"""
        # Simplified timing calculation
        base_timing = {'green': 30.0, 'yellow': 3.0, 'red': 27.0}
        
        congestion_level = congestion_data.get('congestion_level', 0.5)
        if congestion_level > 0.8:
            # Increase green time for congested direction
            base_timing['green'] = 45.0
            base_timing['red'] = 15.0
        
        return base_timing
    
    async def _implement_signal_optimization(self, optimization_data: Dict[str, Any]):
        """Implement signal timing optimization"""
        # In real implementation, this would interface with traffic control systems
        logger.info(f"Implementing signal optimization: {optimization_data}")
    
    # Utility methods
    def _calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two points"""
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def _calculate_direction_similarity(self, dir1: Tuple[float, float], dir2: Tuple[float, float]) -> float:
        """Calculate similarity between two direction vectors"""
        if not dir1 or not dir2:
            return 0.0
        
        # Normalize vectors
        norm1 = np.linalg.norm(dir1)
        norm2 = np.linalg.norm(dir2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        dir1_norm = np.array(dir1) / norm1
        dir2_norm = np.array(dir2) / norm2
        
        # Calculate cosine similarity
        similarity = np.dot(dir1_norm, dir2_norm)
        return max(0, similarity)  # Only positive similarity
    
    def _calculate_traffic_density(self, queue_data: List[Dict[str, Any]]) -> float:
        """Calculate overall traffic density from queue data"""
        if not queue_data:
            return 0.0
        
        total_length = sum(q.get('length', 0) for q in queue_data)
        total_area = 1000.0  # Assume fixed coverage area
        return min(1.0, total_length / total_area)
    
    def _calculate_flow_rate(self, queue_data: List[Dict[str, Any]]) -> float:
        """Calculate traffic flow rate from queue data"""
        if not queue_data:
            return 0.0
        
        # Simplified flow rate calculation
        return sum(1 / max(q.get('wait_time', 1), 1) for q in queue_data) / len(queue_data)
    
    def _get_coverage_area(self) -> List[Tuple[float, float]]:
        """Get camera coverage area as polygon"""
        # Simplified rectangular coverage area
        x, y = self.camera_position
        return [(x-50, y-50), (x+50, y-50), (x+50, y+50), (x-50, y+50)]
    
    def _has_significant_change(self, prev_queue: DistributedQueue, new_data: Dict[str, Any]) -> bool:
        """Check if queue has changed significantly"""
        length_change = abs(prev_queue.length - new_data.get('length', 0)) / max(prev_queue.length, 1)
        wait_time_change = abs(prev_queue.average_wait_time - new_data.get('wait_time', 0)) / max(prev_queue.average_wait_time, 1)
        
        return length_change > 0.2 or wait_time_change > 0.3  # 20% length or 30% wait time change
    
    # Service methods
    async def _sync_service(self):
        """Background service for synchronizing queue data"""
        while True:
            try:
                current_time = time.time()
                
                if current_time - self.last_sync_time > self.sync_interval:
                    await self._synchronize_global_state()
                    self.last_sync_time = current_time
                
                await asyncio.sleep(5.0)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"Error in sync service: {e}")
                await asyncio.sleep(10.0)
    
    async def _analytics_service(self):
        """Background service for queue analytics"""
        while True:
            try:
                await self._update_analytics()
                await asyncio.sleep(30.0)  # Update analytics every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in analytics service: {e}")
                await asyncio.sleep(60.0)
    
    async def _optimization_service(self):
        """Background service for optimization recommendations"""
        while True:
            try:
                await self._generate_optimization_recommendations()
                await asyncio.sleep(60.0)  # Check for optimizations every minute
                
            except Exception as e:
                logger.error(f"Error in optimization service: {e}")
                await asyncio.sleep(120.0)
    
    async def _synchronize_global_state(self):
        """Synchronize global queue state across edges"""
        # Send pending updates
        for edge_id, update_data in self.pending_updates.items():
            message = create_queue_update_message(
                self.edge_id,
                "broadcast",
                update_data
            )
            await self.communication.send_message(message)
        
        self.pending_updates.clear()
        
        # Request updates from other edges if needed
        if len(self.local_queue_data) < len(self.communication.connected_edges):
            # Request missing data
            pass
    
    async def _update_analytics(self):
        """Update queue analytics"""
        active_queues = [q for q in self.global_queues.values() 
                        if time.time() - q.last_updated < 60.0]
        
        self.queue_analytics['total_queues'] = len(active_queues)
        
        if active_queues:
            self.queue_analytics['average_wait_time'] = np.mean([q.average_wait_time for q in active_queues])
            
            # Calculate efficiency score
            total_wait_time = sum(q.average_wait_time for q in active_queues)
            optimal_wait_time = len(active_queues) * 30.0  # 30 seconds optimal
            self.queue_analytics['efficiency_score'] = max(0.1, optimal_wait_time / max(total_wait_time, 1))
        
        logger.debug(f"Updated analytics: {self.queue_analytics}")
    
    async def _generate_optimization_recommendations(self):
        """Generate optimization recommendations"""
        recommendations = []
        
        # Find long queues
        long_queues = [q for q in self.global_queues.values() 
                      if q.average_wait_time > 180.0]  # 3 minutes
        
        for queue in long_queues:
            recommendations.append({
                'type': 'reduce_wait_time',
                'queue_id': queue.queue_id,
                'current_wait_time': queue.average_wait_time,
                'suggested_action': 'optimize_signal_timing'
            })
        
        # Find underutilized areas
        edge_loads = {edge_id: data.traffic_density 
                     for edge_id, data in self.local_queue_data.items()}
        
        if edge_loads:
            avg_load = np.mean(list(edge_loads.values()))
            for edge_id, load in edge_loads.items():
                if load < avg_load * 0.5:  # Less than 50% of average
                    recommendations.append({
                        'type': 'load_balancing',
                        'edge_id': edge_id,
                        'current_load': load,
                        'suggested_action': 'redirect_traffic'
                    })
        
        self.queue_analytics['optimization_opportunities'] = recommendations
    
    # Public interface methods
    def get_global_queues(self) -> List[DistributedQueue]:
        """Get all global queues"""
        return list(self.global_queues.values())
    
    def get_queue_events(self, limit: int = 50) -> List[QueueEvent]:
        """Get recent queue events"""
        return list(self.queue_events)[-limit:]
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get queue analytics"""
        return self.queue_analytics.copy()
    
    def get_edge_data(self) -> Dict[str, EdgeQueueData]:
        """Get queue data from all edges"""
        return self.local_queue_data.copy()
    
    def get_coverage_map(self) -> Dict[str, List[Tuple[float, float]]]:
        """Get coverage map of all edges"""
        return self.coverage_map.copy()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get distributed queue manager statistics"""
        return {
            'global_queues': len(self.global_queues),
            'connected_edges': len(self.local_queue_data),
            'recent_events': len(self.queue_events),
            'sync_interval': self.sync_interval,
            'last_sync': self.last_sync_time,
            'analytics': self.queue_analytics
        }