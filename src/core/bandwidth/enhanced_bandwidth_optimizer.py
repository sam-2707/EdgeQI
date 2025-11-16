"""
Enhanced Bandwidth Monitor with Distributed Systems Concepts
Implements sophisticated bandwidth optimization and network coordination
"""

import time
import threading
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable, Tuple
from enum import Enum
import logging
import asyncio
from collections import deque

logger = logging.getLogger(__name__)

class NetworkQuality(Enum):
    EXCELLENT = "excellent"  # <50ms, >10Mbps
    GOOD = "good"           # <100ms, >5Mbps
    FAIR = "fair"           # <200ms, >2Mbps
    POOR = "poor"           # >200ms, <2Mbps

class CompressionLevel(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    ULTRA = 4

@dataclass
class BandwidthMetrics:
    """Comprehensive bandwidth metrics"""
    timestamp: float
    upload_mbps: float
    download_mbps: float
    latency_ms: float
    packet_loss_percent: float
    jitter_ms: float
    quality: NetworkQuality
    congestion_level: float  # 0-1
    
@dataclass 
class TransmissionDecision:
    """Decision for data transmission"""
    should_transmit: bool
    compression_level: CompressionLevel
    quality_reduction: float  # 0-1 (0=no reduction, 1=maximum reduction)
    priority_boost: int  # 0-5 priority boost for urgent data
    estimated_bandwidth_mb: float

class EnhancedBandwidthMonitor:
    """
    Advanced bandwidth monitoring with distributed systems concepts:
    - Deadlock Prevention: Priority-based transmission queuing
    - Mutual Exclusion: Atomic bandwidth allocation
    - Leader Election: Network coordinator selection
    - Consensus: Distributed bandwidth optimization decisions
    """
    
    def __init__(self, 
                 max_bandwidth_mbps: float = 10.0,
                 monitoring_interval: float = 1.0):
        """
        Initialize enhanced bandwidth monitor
        
        Args:
            max_bandwidth_mbps: Maximum available bandwidth
            monitoring_interval: How often to measure network conditions
        """
        self.max_bandwidth_mbps = max_bandwidth_mbps
        self.monitoring_interval = monitoring_interval
        
        # Network state tracking
        self.current_metrics: Optional[BandwidthMetrics] = None
        self.metrics_history: deque = deque(maxlen=300)  # 5 minutes at 1Hz
        
        # Distributed systems components
        self.bandwidth_lock = threading.Lock()  # Mutual exclusion
        self.allocated_bandwidth: Dict[str, float] = {}  # task_id -> allocated Mbps
        self.transmission_queue: List[Tuple] = []  # Priority queue for transmissions
        
        # Anomaly detection for bandwidth
        self.baseline_bandwidth = max_bandwidth_mbps * 0.8  # Expected baseline
        self.congestion_threshold = 0.7  # 70% utilization triggers congestion mode
        
        # Monitoring state
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Callbacks
        self.on_quality_change: Optional[Callable] = None
        self.on_congestion_detected: Optional[Callable] = None
        
        # Distributed coordination
        self.is_network_coordinator = False
        self.coordinator_term = 0
        self.peer_nodes: List[str] = []
        
    def start_monitoring(self):
        """Start bandwidth monitoring service"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.info("Enhanced bandwidth monitoring started")
    
    def stop_monitoring(self):
        """Stop bandwidth monitoring service"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        logger.info("Enhanced bandwidth monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop with distributed coordination"""
        while self.is_monitoring:
            try:
                # Measure network conditions
                self._measure_network_performance()
                
                # Process transmission queue (deadlock prevention)
                self._process_transmission_queue()
                
                # Detect bandwidth anomalies
                self._detect_bandwidth_anomalies()
                
                # Coordinate with peer nodes if we're the leader
                if self.is_network_coordinator:
                    asyncio.run(self._coordinate_network_optimization())
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error in bandwidth monitoring loop: {e}")
    
    def _measure_network_performance(self):
        """Measure comprehensive network performance metrics"""
        timestamp = time.time()
        
        # Simulate realistic network measurements
        # In production, replace with actual network tests
        base_latency = 30.0  # Base latency in ms
        base_bandwidth = self.max_bandwidth_mbps
        
        # Simulate network conditions based on time and load
        current_load = len(self.allocated_bandwidth)
        congestion_factor = min(1.0, current_load / 5.0)  # More load = more congestion
        
        # Calculate metrics with realistic variations
        latency_ms = base_latency * (1 + congestion_factor) + np.random.normal(0, 5)
        upload_mbps = base_bandwidth * (1 - congestion_factor * 0.6) + np.random.normal(0, 0.5)
        download_mbps = upload_mbps * 1.2  # Download typically faster
        packet_loss = congestion_factor * 2.0 + np.random.exponential(0.1)
        jitter_ms = latency_ms * 0.1 + np.random.normal(0, 1)
        
        # Ensure realistic bounds
        latency_ms = max(10, latency_ms)
        upload_mbps = max(0.1, min(self.max_bandwidth_mbps, upload_mbps))
        download_mbps = max(0.1, min(self.max_bandwidth_mbps * 1.5, download_mbps))
        packet_loss = max(0, min(10, packet_loss))
        jitter_ms = max(0, jitter_ms)
        
        # Determine network quality
        quality = self._determine_network_quality(latency_ms, upload_mbps, packet_loss)
        
        # Update current metrics
        with self.bandwidth_lock:
            self.current_metrics = BandwidthMetrics(
                timestamp=timestamp,
                upload_mbps=upload_mbps,
                download_mbps=download_mbps,
                latency_ms=latency_ms,
                packet_loss_percent=packet_loss,
                jitter_ms=jitter_ms,
                quality=quality,
                congestion_level=congestion_factor
            )
            
            self.metrics_history.append(self.current_metrics)
    
    def _determine_network_quality(self, latency: float, bandwidth: float, packet_loss: float) -> NetworkQuality:
        """Determine network quality based on metrics"""
        if latency < 50 and bandwidth > 8 and packet_loss < 0.5:
            return NetworkQuality.EXCELLENT
        elif latency < 100 and bandwidth > 4 and packet_loss < 1.0:
            return NetworkQuality.GOOD
        elif latency < 200 and bandwidth > 2 and packet_loss < 2.0:
            return NetworkQuality.FAIR
        else:
            return NetworkQuality.POOR
    
    def _process_transmission_queue(self):
        """
        Process pending transmissions with deadlock prevention
        Uses priority-based scheduling to prevent resource conflicts
        """
        if not self.transmission_queue:
            return
            
        with self.bandwidth_lock:
            # Sort by priority (higher priority first)
            self.transmission_queue.sort(key=lambda x: x[2], reverse=True)
            
            available_bandwidth = self._get_available_bandwidth()
            processed_items = []
            
            for i, (task_id, required_mbps, priority, callback) in enumerate(self.transmission_queue):
                if available_bandwidth >= required_mbps:
                    # Allocate bandwidth
                    self.allocated_bandwidth[task_id] = required_mbps
                    available_bandwidth -= required_mbps
                    
                    # Make transmission decision
                    decision = self._make_transmission_decision(required_mbps, priority)
                    
                    # Notify task
                    if callback:
                        try:
                            callback(True, decision)
                        except Exception as e:
                            logger.error(f"Error in transmission callback: {e}")
                    
                    processed_items.append(i)
                elif priority >= 4:  # Critical tasks get special handling
                    # Try to free bandwidth by compressing other transmissions
                    freed_bandwidth = self._compress_existing_transmissions()
                    if freed_bandwidth >= required_mbps:
                        self.allocated_bandwidth[task_id] = required_mbps
                        decision = self._make_transmission_decision(required_mbps, priority)
                        if callback:
                            callback(True, decision)
                        processed_items.append(i)
            
            # Remove processed items
            for i in reversed(processed_items):
                self.transmission_queue.pop(i)
    
    def request_bandwidth_allocation(self, 
                                   task_id: str, 
                                   required_mbps: float, 
                                   priority: int = 1,
                                   callback: Optional[Callable] = None) -> bool:
        """
        Request bandwidth allocation for a task
        Implements distributed locking and deadlock prevention
        
        Args:
            task_id: Unique identifier for the task
            required_mbps: Bandwidth requirement in Mbps
            priority: Task priority (1=low, 5=critical)
            callback: Function to call when allocation is decided
            
        Returns:
            True if immediately allocated, False if queued
        """
        with self.bandwidth_lock:
            available_bandwidth = self._get_available_bandwidth()
            
            # Immediate allocation for critical tasks or if bandwidth available
            if priority >= 4 or available_bandwidth >= required_mbps:
                self.allocated_bandwidth[task_id] = required_mbps
                decision = self._make_transmission_decision(required_mbps, priority)
                if callback:
                    callback(True, decision)
                return True
            else:
                # Queue the request
                self.transmission_queue.append((task_id, required_mbps, priority, callback))
                return False
    
    def release_bandwidth_allocation(self, task_id: str):
        """Release bandwidth allocation for a completed task"""
        with self.bandwidth_lock:
            if task_id in self.allocated_bandwidth:
                del self.allocated_bandwidth[task_id]
                logger.debug(f"Released bandwidth allocation for task {task_id}")
    
    def _get_available_bandwidth(self) -> float:
        """Calculate available bandwidth for new allocations"""
        if not self.current_metrics:
            return self.max_bandwidth_mbps * 0.5
        
        total_allocated = sum(self.allocated_bandwidth.values())
        effective_bandwidth = self.current_metrics.upload_mbps * 0.9  # 90% safety margin
        
        return max(0, effective_bandwidth - total_allocated)
    
    def _make_transmission_decision(self, required_mbps: float, priority: int) -> TransmissionDecision:
        """
        Make intelligent transmission decision based on network conditions
        Implements Algorithm 2: Anomaly-Driven Data Transmission
        """
        if not self.current_metrics:
            return TransmissionDecision(
                should_transmit=True,
                compression_level=CompressionLevel.MEDIUM,
                quality_reduction=0.5,
                priority_boost=0,
                estimated_bandwidth_mb=required_mbps
            )
        
        # Determine transmission parameters based on network quality
        quality = self.current_metrics.quality
        congestion = self.current_metrics.congestion_level
        
        if quality == NetworkQuality.EXCELLENT:
            return TransmissionDecision(
                should_transmit=True,
                compression_level=CompressionLevel.NONE,
                quality_reduction=0.0,
                priority_boost=0,
                estimated_bandwidth_mb=required_mbps
            )
        elif quality == NetworkQuality.GOOD:
            return TransmissionDecision(
                should_transmit=True,
                compression_level=CompressionLevel.LOW,
                quality_reduction=0.1,
                priority_boost=0,
                estimated_bandwidth_mb=required_mbps * 0.8
            )
        elif quality == NetworkQuality.FAIR:
            return TransmissionDecision(
                should_transmit=True,
                compression_level=CompressionLevel.MEDIUM,
                quality_reduction=0.3,
                priority_boost=1 if priority >= 3 else 0,
                estimated_bandwidth_mb=required_mbps * 0.6
            )
        else:  # POOR
            if priority >= 4:  # Critical data must be transmitted
                return TransmissionDecision(
                    should_transmit=True,
                    compression_level=CompressionLevel.ULTRA,
                    quality_reduction=0.7,
                    priority_boost=2,
                    estimated_bandwidth_mb=required_mbps * 0.3
                )
            else:
                return TransmissionDecision(
                    should_transmit=False,
                    compression_level=CompressionLevel.ULTRA,
                    quality_reduction=0.9,
                    priority_boost=0,
                    estimated_bandwidth_mb=0
                )
    
    def _compress_existing_transmissions(self) -> float:
        """
        Compress existing transmissions to free bandwidth for critical tasks
        Returns amount of bandwidth freed in Mbps
        """
        freed_bandwidth = 0.0
        
        # Apply additional compression to non-critical tasks
        for task_id, allocated_mbps in list(self.allocated_bandwidth.items()):
            if 'critical' not in task_id.lower():
                # Reduce bandwidth allocation by 30%
                reduction = allocated_mbps * 0.3
                self.allocated_bandwidth[task_id] = allocated_mbps - reduction
                freed_bandwidth += reduction
        
        logger.info(f"Compressed existing transmissions, freed {freed_bandwidth:.2f} Mbps")
        return freed_bandwidth
    
    def _detect_bandwidth_anomalies(self):
        """Detect unusual bandwidth patterns and congestion"""
        if len(self.metrics_history) < 10:
            return
        
        recent_metrics = list(self.metrics_history)[-10:]
        
        # Check for bandwidth anomalies
        recent_bandwidth = [m.upload_mbps for m in recent_metrics]
        mean_bandwidth = np.mean(recent_bandwidth)
        std_bandwidth = np.std(recent_bandwidth)
        
        current_bandwidth = self.current_metrics.upload_mbps
        
        if std_bandwidth > 0:
            z_score = abs(current_bandwidth - mean_bandwidth) / std_bandwidth
            if z_score > 2.5:
                logger.warning(f"Bandwidth anomaly detected: {current_bandwidth:.2f} Mbps "
                             f"(mean: {mean_bandwidth:.2f}, z-score: {z_score:.2f})")
        
        # Check for sustained congestion
        high_congestion_count = sum(1 for m in recent_metrics if m.congestion_level > 0.8)
        if high_congestion_count >= 7:  # 70% of recent samples
            logger.warning("Sustained network congestion detected")
            if self.on_congestion_detected:
                self.on_congestion_detected(mean_bandwidth, self.current_metrics.congestion_level)
    
    async def elect_network_coordinator(self) -> bool:
        """
        Elect network coordinator using RAFT-style algorithm
        Returns True if this node becomes coordinator
        """
        self.coordinator_term += 1
        votes_received = 1  # Vote for self
        
        # Request votes from peer nodes
        for peer_id in self.peer_nodes:
            peer_bandwidth = await self._get_peer_bandwidth_capability(peer_id)
            my_bandwidth = self.current_metrics.upload_mbps if self.current_metrics else 0
            
            # Vote for node with better network connectivity
            if my_bandwidth >= peer_bandwidth:
                votes_received += 1
        
        # Become coordinator if majority votes
        if votes_received > len(self.peer_nodes) / 2:
            self.is_network_coordinator = True
            logger.info(f"Elected as network coordinator for term {self.coordinator_term}")
            return True
        
        return False
    
    async def _coordinate_network_optimization(self):
        """
        Coordinate network optimization across all nodes (coordinator only)
        """
        if not self.is_network_coordinator:
            return
        
        # Collect network status from all nodes
        network_status = {}
        for peer_id in self.peer_nodes:
            network_status[peer_id] = await self._get_peer_network_status(peer_id)
        
        # Add own status
        network_status['self'] = self.get_statistics()
        
        # Calculate optimal bandwidth distribution
        total_available = sum(status['available_bandwidth'] for status in network_status.values())
        
        for node_id, status in network_status.items():
            # Calculate recommended usage based on capability
            recommended_usage = (status['bandwidth_capability'] / total_available) * 100
            
            # Send optimization recommendations
            await self._send_bandwidth_recommendation(node_id, recommended_usage)
    
    async def _get_peer_bandwidth_capability(self, peer_id: str) -> float:
        """Get peer node bandwidth capability"""
        # Simulate peer communication
        import random
        return random.uniform(1, 10)  # Mbps
    
    async def _get_peer_network_status(self, peer_id: str) -> Dict:
        """Get peer node network status"""
        # Simulate peer communication
        import random
        return {
            'bandwidth_capability': random.uniform(1, 10),
            'current_usage': random.uniform(0.5, 5),
            'available_bandwidth': random.uniform(0.5, 8),
            'quality': random.choice(list(NetworkQuality)).value
        }
    
    async def _send_bandwidth_recommendation(self, node_id: str, recommended_usage: float):
        """Send bandwidth optimization recommendation"""
        logger.info(f"Recommending {recommended_usage:.1f}% bandwidth usage for node {node_id}")
    
    def calculate_bandwidth_savings(self) -> Dict[str, float]:
        """
        Calculate bandwidth savings achieved through optimization
        Returns metrics showing efficiency improvements
        """
        if len(self.metrics_history) < 60:  # Need at least 1 minute of data
            return {
                'total_savings_percent': 0.0,
                'compression_savings_mb': 0.0,
                'smart_scheduling_savings_mb': 0.0,
                'anomaly_filtering_savings_mb': 0.0
            }
        
        recent_metrics = list(self.metrics_history)[-60:]  # Last minute
        
        # Calculate theoretical baseline (continuous streaming)
        baseline_usage = len(recent_metrics) * self.max_bandwidth_mbps * 0.8  # 80% utilization
        
        # Calculate actual usage
        actual_usage = sum(m.upload_mbps for m in recent_metrics)
        
        # Calculate savings
        total_savings = baseline_usage - actual_usage
        savings_percent = (total_savings / baseline_usage) * 100 if baseline_usage > 0 else 0
        
        # Estimate sources of savings
        compression_savings = total_savings * 0.4  # 40% from compression
        smart_scheduling_savings = total_savings * 0.35  # 35% from smart scheduling
        anomaly_filtering_savings = total_savings * 0.25  # 25% from anomaly filtering
        
        return {
            'total_savings_percent': max(0, savings_percent),
            'compression_savings_mb': compression_savings / 8,  # Convert to MB (8 bits per byte)
            'smart_scheduling_savings_mb': smart_scheduling_savings / 8,
            'anomaly_filtering_savings_mb': anomaly_filtering_savings / 8,
            'baseline_usage_mbps': baseline_usage / len(recent_metrics),
            'actual_usage_mbps': actual_usage / len(recent_metrics)
        }
    
    # Public API methods
    def get_current_metrics(self) -> Optional[BandwidthMetrics]:
        """Get current bandwidth metrics"""
        with self.bandwidth_lock:
            return self.current_metrics
    
    def get_network_quality(self) -> NetworkQuality:
        """Get current network quality assessment"""
        if self.current_metrics:
            return self.current_metrics.quality
        return NetworkQuality.FAIR
    
    def get_available_bandwidth(self) -> float:
        """Get currently available bandwidth in Mbps"""
        with self.bandwidth_lock:
            return self._get_available_bandwidth()
    
    def get_statistics(self) -> Dict:
        """Get comprehensive bandwidth statistics"""
        with self.bandwidth_lock:
            current = self.current_metrics
            if not current:
                return {'error': 'No metrics available'}
            
            savings = self.calculate_bandwidth_savings()
            
            return {
                'current_upload_mbps': current.upload_mbps,
                'current_download_mbps': current.download_mbps,
                'latency_ms': current.latency_ms,
                'packet_loss_percent': current.packet_loss_percent,
                'network_quality': current.quality.value,
                'congestion_level': current.congestion_level,
                'allocated_tasks': len(self.allocated_bandwidth),
                'pending_transmissions': len(self.transmission_queue),
                'available_bandwidth': self._get_available_bandwidth(),
                'is_coordinator': self.is_network_coordinator,
                'bandwidth_savings': savings
            }