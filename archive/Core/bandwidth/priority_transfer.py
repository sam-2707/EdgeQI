"""
Priority Transfer Manager for EDGE-QI Framework

Manages priority-based data transfer with QoS guarantees for efficient
edge-to-cloud communication in distributed surveillance systems.
"""

import time
import threading
import heapq
from enum import Enum
from typing import Dict, List, Optional, Callable, Any, Tuple
from dataclasses import dataclass, field
import uuid
import json
import numpy as np


class DataPriority(Enum):
    """Data transfer priority levels"""
    CRITICAL = 0      # Emergency alerts, security incidents
    HIGH = 1         # Real-time analytics, anomaly detection
    MEDIUM = 2       # Normal surveillance data, queue metrics
    LOW = 3          # Historical data, system logs
    BACKGROUND = 4   # Bulk transfers, backups


@dataclass
class TransferRequest:
    """Data transfer request with priority and metadata"""
    id: str
    priority: DataPriority
    data: bytes
    metadata: Dict[str, Any]
    timestamp: float
    deadline: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 3
    callback: Optional[Callable] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = time.time()
    
    def __lt__(self, other):
        """Priority queue comparison - lower priority value = higher priority"""
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.timestamp < other.timestamp


@dataclass
class TransferMetrics:
    """Transfer performance metrics"""
    total_requests: int = 0
    completed_transfers: int = 0
    failed_transfers: int = 0
    average_latency: float = 0.0
    throughput_mbps: float = 0.0
    queue_depth: int = 0
    priority_distribution: Dict[str, int] = field(default_factory=dict)
    bandwidth_utilization: float = 0.0


class QoSPolicy:
    """Quality of Service policy configuration"""
    
    def __init__(self):
        # Bandwidth allocation by priority (percentage)
        self.bandwidth_allocation = {
            DataPriority.CRITICAL: 0.4,     # 40% for critical
            DataPriority.HIGH: 0.3,         # 30% for high
            DataPriority.MEDIUM: 0.2,       # 20% for medium
            DataPriority.LOW: 0.08,         # 8% for low
            DataPriority.BACKGROUND: 0.02   # 2% for background
        }
        
        # Maximum queue sizes by priority
        self.max_queue_sizes = {
            DataPriority.CRITICAL: 100,
            DataPriority.HIGH: 200,
            DataPriority.MEDIUM: 500,
            DataPriority.LOW: 1000,
            DataPriority.BACKGROUND: 2000
        }
        
        # Timeout values by priority (seconds)
        self.timeout_values = {
            DataPriority.CRITICAL: 1.0,
            DataPriority.HIGH: 5.0,
            DataPriority.MEDIUM: 30.0,
            DataPriority.LOW: 300.0,
            DataPriority.BACKGROUND: 3600.0
        }


class PriorityTransferManager:
    """
    Priority-based data transfer manager with QoS guarantees
    """
    
    def __init__(self, 
                 max_bandwidth_mbps: float = 10.0,
                 qos_policy: Optional[QoSPolicy] = None):
        """
        Initialize priority transfer manager
        
        Args:
            max_bandwidth_mbps: Maximum available bandwidth in Mbps
            qos_policy: QoS policy configuration
        """
        self.max_bandwidth_mbps = max_bandwidth_mbps
        self.qos_policy = qos_policy or QoSPolicy()
        
        # Transfer queues by priority
        self.transfer_queues = {
            priority: [] for priority in DataPriority
        }
        
        # Active transfers
        self.active_transfers: Dict[str, TransferRequest] = {}
        
        # Transfer metrics
        self.metrics = TransferMetrics()
        
        # Control flags
        self.is_running = False
        self.transfer_lock = threading.Lock()
        
        # Bandwidth management
        self.current_bandwidth_usage = 0.0
        self.bandwidth_history = []
        
        # Callbacks
        self.on_transfer_complete: Optional[Callable] = None
        self.on_transfer_failed: Optional[Callable] = None
        self.on_queue_full: Optional[Callable] = None
        
        # Worker threads
        self.transfer_threads = []
        self.monitor_thread = None
    
    def start(self, num_workers: int = 3):
        """
        Start the priority transfer manager
        
        Args:
            num_workers: Number of worker threads for transfers
        """
        if self.is_running:
            return
        
        self.is_running = True
        
        # Start worker threads
        for i in range(num_workers):
            worker = threading.Thread(
                target=self._transfer_worker,
                name=f"TransferWorker-{i}"
            )
            worker.daemon = True
            worker.start()
            self.transfer_threads.append(worker)
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        print(f"Priority Transfer Manager started with {num_workers} workers")
    
    def stop(self):
        """Stop the priority transfer manager"""
        self.is_running = False
        
        # Wait for threads to finish
        for thread in self.transfer_threads:
            if thread.is_alive():
                thread.join(timeout=1.0)
        
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1.0)
        
        # Clear queues
        with self.transfer_lock:
            for queue in self.transfer_queues.values():
                queue.clear()
            self.active_transfers.clear()
        
        print("Priority Transfer Manager stopped")
    
    def submit_transfer(self, 
                       data: bytes,
                       priority: DataPriority,
                       metadata: Optional[Dict[str, Any]] = None,
                       deadline: Optional[float] = None,
                       callback: Optional[Callable] = None) -> str:
        """
        Submit data for priority transfer
        
        Args:
            data: Data to transfer
            priority: Transfer priority level
            metadata: Additional metadata
            deadline: Optional deadline timestamp
            callback: Optional completion callback
            
        Returns:
            Transfer request ID
        """
        request = TransferRequest(
            id=str(uuid.uuid4()),
            priority=priority,
            data=data,
            metadata=metadata or {},
            timestamp=time.time(),
            deadline=deadline,
            callback=callback
        )
        
        # Check queue capacity
        queue = self.transfer_queues[priority]
        max_size = self.qos_policy.max_queue_sizes[priority]
        
        with self.transfer_lock:
            if len(queue) >= max_size:
                # Queue full - handle based on priority
                if priority in [DataPriority.CRITICAL, DataPriority.HIGH]:
                    # Remove oldest low priority item
                    self._make_room_for_priority(priority)
                else:
                    # Reject request
                    if self.on_queue_full:
                        self.on_queue_full(request)
                    raise RuntimeError(f"Transfer queue full for priority {priority.name}")
            
            # Add to priority queue
            heapq.heappush(queue, request)
            self.metrics.total_requests += 1
            
            # Update priority distribution
            priority_name = priority.name
            if priority_name not in self.metrics.priority_distribution:
                self.metrics.priority_distribution[priority_name] = 0
            self.metrics.priority_distribution[priority_name] += 1
        
        return request.id
    
    def cancel_transfer(self, request_id: str) -> bool:
        """
        Cancel a pending transfer request
        
        Args:
            request_id: Transfer request ID
            
        Returns:
            True if cancelled successfully
        """
        with self.transfer_lock:
            # Check active transfers
            if request_id in self.active_transfers:
                # Cannot cancel active transfer
                return False
            
            # Search queues
            for priority, queue in self.transfer_queues.items():
                for i, request in enumerate(queue):
                    if request.id == request_id:
                        # Remove from queue
                        queue.pop(i)
                        heapq.heapify(queue)  # Restore heap property
                        return True
        
        return False
    
    def get_transfer_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a transfer request
        
        Args:
            request_id: Transfer request ID
            
        Returns:
            Transfer status information
        """
        with self.transfer_lock:
            # Check active transfers
            if request_id in self.active_transfers:
                request = self.active_transfers[request_id]
                return {
                    'id': request.id,
                    'status': 'active',
                    'priority': request.priority.name,
                    'progress': 0.5,  # Simplified progress
                    'started_at': request.timestamp
                }
            
            # Check queues
            for priority, queue in self.transfer_queues.items():
                for i, request in enumerate(queue):
                    if request.id == request_id:
                        return {
                            'id': request.id,
                            'status': 'queued',
                            'priority': request.priority.name,
                            'queue_position': i + 1,
                            'submitted_at': request.timestamp
                        }
        
        return None
    
    def _transfer_worker(self):
        """Worker thread for processing transfers"""
        while self.is_running:
            try:
                # Get next highest priority transfer
                request = self._get_next_transfer()
                
                if request is None:
                    time.sleep(0.1)  # No work available
                    continue
                
                # Check bandwidth availability
                if not self._check_bandwidth_availability(request):
                    # Put back in queue if bandwidth not available
                    self._requeue_transfer(request)
                    time.sleep(0.5)
                    continue
                
                # Execute transfer
                self._execute_transfer(request)
                
            except Exception as e:
                print(f"Transfer worker error: {e}")
                time.sleep(1.0)
    
    def _get_next_transfer(self) -> Optional[TransferRequest]:
        """Get next highest priority transfer from queues"""
        with self.transfer_lock:
            # Check each priority level
            for priority in DataPriority:
                queue = self.transfer_queues[priority]
                if queue:
                    # Check deadline constraints
                    while queue:
                        request = heapq.heappop(queue)
                        
                        # Check if expired
                        if (request.deadline and 
                            time.time() > request.deadline):
                            # Transfer expired
                            self._handle_transfer_failure(request, "Deadline exceeded")
                            continue
                        
                        # Valid request found
                        return request
        
        return None
    
    def _check_bandwidth_availability(self, request: TransferRequest) -> bool:
        """Check if bandwidth is available for transfer"""
        # Estimate transfer size and time
        data_size_mb = len(request.data) / (1024 * 1024)
        
        # Get allocated bandwidth for priority
        allocated_bandwidth = (
            self.max_bandwidth_mbps * 
            self.qos_policy.bandwidth_allocation[request.priority]
        )
        
        # Check current usage
        current_usage = self.current_bandwidth_usage
        available_bandwidth = self.max_bandwidth_mbps - current_usage
        
        # Ensure minimum bandwidth for critical/high priority
        if request.priority in [DataPriority.CRITICAL, DataPriority.HIGH]:
            min_required = min(allocated_bandwidth, available_bandwidth)
            return min_required > 0.1  # At least 0.1 Mbps
        
        # For other priorities, check allocation
        return available_bandwidth >= allocated_bandwidth * 0.5
    
    def _execute_transfer(self, request: TransferRequest):
        """Execute the transfer request"""
        start_time = time.time()
        
        try:
            # Mark as active
            with self.transfer_lock:
                self.active_transfers[request.id] = request
                self.metrics.queue_depth = sum(len(q) for q in self.transfer_queues.values())
            
            # Simulate transfer (in real implementation, this would be actual network transfer)
            transfer_success = self._simulate_transfer(request)
            
            if transfer_success:
                # Transfer completed successfully
                end_time = time.time()
                latency = end_time - start_time
                
                # Update metrics
                with self.transfer_lock:
                    self.metrics.completed_transfers += 1
                    # Update average latency
                    n = self.metrics.completed_transfers
                    self.metrics.average_latency = (
                        ((n - 1) * self.metrics.average_latency + latency) / n
                    )
                
                # Call completion callback
                if request.callback:
                    try:
                        request.callback(request, True, None)
                    except Exception as e:
                        print(f"Callback error: {e}")
                
                if self.on_transfer_complete:
                    self.on_transfer_complete(request)
                    
            else:
                # Transfer failed
                self._handle_transfer_failure(request, "Transfer simulation failed")
        
        except Exception as e:
            self._handle_transfer_failure(request, str(e))
        
        finally:
            # Remove from active transfers
            with self.transfer_lock:
                self.active_transfers.pop(request.id, None)
    
    def _simulate_transfer(self, request: TransferRequest) -> bool:
        """Simulate data transfer with realistic timing and failure rates"""
        data_size_mb = len(request.data) / (1024 * 1024)
        
        # Calculate transfer time based on allocated bandwidth
        allocated_bandwidth = (
            self.max_bandwidth_mbps * 
            self.qos_policy.bandwidth_allocation[request.priority]
        )
        
        # Add some realistic variation
        actual_bandwidth = allocated_bandwidth * np.random.uniform(0.7, 1.3)
        transfer_time = data_size_mb / max(actual_bandwidth, 0.1)
        
        # Update bandwidth usage
        self.current_bandwidth_usage += actual_bandwidth
        
        try:
            # Simulate transfer time
            time.sleep(min(transfer_time, 5.0))  # Cap at 5 seconds for simulation
            
            # Simulate failure rate based on priority
            failure_rates = {
                DataPriority.CRITICAL: 0.01,    # 1% failure
                DataPriority.HIGH: 0.02,        # 2% failure
                DataPriority.MEDIUM: 0.05,      # 5% failure
                DataPriority.LOW: 0.1,          # 10% failure
                DataPriority.BACKGROUND: 0.15   # 15% failure
            }
            
            failure_rate = failure_rates.get(request.priority, 0.05)
            return np.random.random() > failure_rate
            
        finally:
            # Release bandwidth
            self.current_bandwidth_usage = max(0, self.current_bandwidth_usage - actual_bandwidth)
    
    def _handle_transfer_failure(self, request: TransferRequest, error_message: str):
        """Handle transfer failure with retry logic"""
        request.retry_count += 1
        
        if request.retry_count <= request.max_retries:
            # Retry with exponential backoff
            delay = min(2 ** request.retry_count, 60)  # Max 60 seconds
            
            def retry_later():
                time.sleep(delay)
                if self.is_running:
                    self._requeue_transfer(request)
            
            retry_thread = threading.Thread(target=retry_later)
            retry_thread.daemon = True
            retry_thread.start()
            
        else:
            # Max retries exceeded
            with self.transfer_lock:
                self.metrics.failed_transfers += 1
            
            # Call failure callback
            if request.callback:
                try:
                    request.callback(request, False, error_message)
                except Exception as e:
                    print(f"Callback error: {e}")
            
            if self.on_transfer_failed:
                self.on_transfer_failed(request, error_message)
    
    def _requeue_transfer(self, request: TransferRequest):
        """Put transfer back in queue"""
        with self.transfer_lock:
            queue = self.transfer_queues[request.priority]
            heapq.heappush(queue, request)
    
    def _make_room_for_priority(self, priority: DataPriority):
        """Make room in queues for high priority transfer"""
        # Remove lowest priority items first
        for low_priority in reversed(list(DataPriority)):
            if low_priority.value <= priority.value:
                continue
            
            queue = self.transfer_queues[low_priority]
            if queue:
                removed_request = heapq.heappop(queue)
                print(f"Dropped {low_priority.name} transfer to make room for {priority.name}")
                return
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.is_running:
            try:
                self._update_metrics()
                self._cleanup_expired_transfers()
                time.sleep(1.0)
                
            except Exception as e:
                print(f"Monitor loop error: {e}")
                time.sleep(5.0)
    
    def _update_metrics(self):
        """Update transfer metrics"""
        current_time = time.time()
        
        with self.transfer_lock:
            # Update queue depth
            self.metrics.queue_depth = sum(len(q) for q in self.transfer_queues.values())
            
            # Calculate throughput
            if hasattr(self, 'last_metrics_update'):
                time_diff = current_time - self.last_metrics_update
                if time_diff > 0:
                    # Simplified throughput calculation
                    active_transfers = len(self.active_transfers)
                    self.metrics.throughput_mbps = active_transfers * 0.5  # Estimate
            
            self.last_metrics_update = current_time
            
            # Update bandwidth utilization
            self.metrics.bandwidth_utilization = (
                self.current_bandwidth_usage / max(self.max_bandwidth_mbps, 1)
            )
    
    def _cleanup_expired_transfers(self):
        """Remove expired transfers from queues"""
        current_time = time.time()
        
        with self.transfer_lock:
            for priority, queue in self.transfer_queues.items():
                # Check for expired items
                expired_items = []
                for i, request in enumerate(queue):
                    if (request.deadline and current_time > request.deadline):
                        expired_items.append(i)
                
                # Remove expired items (reverse order to maintain indices)
                for i in reversed(expired_items):
                    expired_request = queue.pop(i)
                    self._handle_transfer_failure(expired_request, "Transfer expired")
                
                # Restore heap property if items were removed
                if expired_items:
                    heapq.heapify(queue)
    
    def get_metrics(self) -> TransferMetrics:
        """Get current transfer metrics"""
        return self.metrics
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status for all priorities"""
        with self.transfer_lock:
            return {
                priority.name: {
                    'queue_size': len(queue),
                    'max_size': self.qos_policy.max_queue_sizes[priority],
                    'utilization': len(queue) / max(self.qos_policy.max_queue_sizes[priority], 1)
                }
                for priority, queue in self.transfer_queues.items()
            }
    
    def set_bandwidth_limit(self, max_bandwidth_mbps: float):
        """Update maximum bandwidth limit"""
        self.max_bandwidth_mbps = max_bandwidth_mbps
    
    def update_qos_policy(self, qos_policy: QoSPolicy):
        """Update QoS policy configuration"""
        self.qos_policy = qos_policy
    
    def get_priority_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics by priority level"""
        stats = {}
        
        with self.transfer_lock:
            for priority in DataPriority:
                priority_name = priority.name
                queue_size = len(self.transfer_queues[priority])
                
                stats[priority_name] = {
                    'current_queue_size': queue_size,
                    'max_queue_size': self.qos_policy.max_queue_sizes[priority],
                    'bandwidth_allocation': self.qos_policy.bandwidth_allocation[priority],
                    'timeout_seconds': self.qos_policy.timeout_values[priority],
                    'total_submitted': self.metrics.priority_distribution.get(priority_name, 0)
                }
        
        return stats