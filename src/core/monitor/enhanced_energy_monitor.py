"""
Enhanced Energy Monitor with Realistic Energy Calculations
Implements distributed systems concepts for energy management
"""

import time
import threading
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class PowerMode(Enum):
    HIGH_PERFORMANCE = "high_performance"
    BALANCED = "balanced"
    POWER_SAVING = "power_saving"
    EMERGENCY = "emergency"

@dataclass
class EnergyConsumption:
    cpu_watts: float
    gpu_watts: float
    network_watts: float
    storage_watts: float
    idle_watts: float
    total_watts: float
    timestamp: float

@dataclass
class EnergyConstraints:
    max_continuous_watts: float = 150.0
    emergency_threshold_percent: float = 5.0
    power_saving_threshold_percent: float = 20.0
    critical_task_energy_reserve: float = 10.0  # Watts reserved for critical tasks

class EnhancedEnergyMonitor:
    """
    Advanced energy monitoring with distributed systems concepts:
    - Mutual Exclusion: Atomic energy allocation for tasks
    - Deadlock Prevention: Priority-based energy budgeting
    - Leader Election: Coordination for energy load balancing
    """
    
    def __init__(self, 
                 initial_battery_kwh: float = 2.5,
                 max_power_watts: float = 150.0):
        """
        Initialize enhanced energy monitor
        
        Args:
            initial_battery_kwh: Initial battery capacity in kWh
            max_power_watts: Maximum power consumption allowed
        """
        self.initial_battery_kwh = initial_battery_kwh
        self.current_battery_kwh = initial_battery_kwh
        self.max_power_watts = max_power_watts
        
        # Energy consumption tracking
        self.consumption_history: List[EnergyConsumption] = []
        self.current_consumption = EnergyConsumption(0, 0, 0, 0, 25.0, 25.0, time.time())
        
        # Power mode management
        self.current_mode = PowerMode.BALANCED
        self.constraints = EnergyConstraints()
        
        # Distributed systems components
        self.energy_lock = threading.Lock()  # Mutual exclusion for energy allocation
        self.allocated_energy: Dict[str, float] = {}  # Task ID -> Allocated watts
        self.energy_waitqueue: List[tuple] = []  # (task_id, required_watts, priority, callback)
        
        # Monitoring state
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Callbacks for energy events
        self.on_power_mode_change: Optional[Callable] = None
        self.on_critical_energy: Optional[Callable] = None
        
    def start_monitoring(self):
        """Start energy monitoring service"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.info("Enhanced energy monitoring started")
    
    def stop_monitoring(self):
        """Stop energy monitoring service"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        logger.info("Enhanced energy monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop - implements distributed coordination"""
        while self.is_monitoring:
            try:
                # Update energy consumption
                self._update_energy_consumption()
                
                # Process energy allocation requests (deadlock prevention)
                self._process_energy_requests()
                
                # Check for power mode changes
                self._evaluate_power_mode()
                
                # Update battery level
                self._update_battery_level()
                
                # Detect energy anomalies
                self._detect_energy_anomalies()
                
                time.sleep(1.0)  # Update every second
                
            except Exception as e:
                logger.error(f"Error in energy monitoring loop: {e}")
    
    def _update_energy_consumption(self):
        """Calculate real-time energy consumption"""
        timestamp = time.time()
        
        # Base consumption calculations
        cpu_usage = self._get_cpu_usage()  # 0-100%
        gpu_usage = self._get_gpu_usage()  # 0-100%
        network_usage = self._get_network_usage()  # Mbps
        storage_usage = self._get_storage_usage()  # Operations/sec
        
        # Calculate power consumption by component
        cpu_watts = (cpu_usage / 100.0) * 45.0  # Max 45W for CPU
        gpu_watts = (gpu_usage / 100.0) * 75.0  # Max 75W for GPU
        network_watts = network_usage * 0.1  # 0.1W per Mbps
        storage_watts = storage_usage * 0.001  # 0.001W per operation
        idle_watts = 25.0  # Base idle consumption
        
        # Apply power mode adjustments
        mode_multiplier = self._get_power_mode_multiplier()
        cpu_watts *= mode_multiplier
        gpu_watts *= mode_multiplier
        
        total_watts = cpu_watts + gpu_watts + network_watts + storage_watts + idle_watts
        
        # Update current consumption
        with self.energy_lock:  # Mutual exclusion
            self.current_consumption = EnergyConsumption(
                cpu_watts=cpu_watts,
                gpu_watts=gpu_watts,
                network_watts=network_watts,
                storage_watts=storage_watts,
                idle_watts=idle_watts,
                total_watts=total_watts,
                timestamp=timestamp
            )
            
            # Add to history
            self.consumption_history.append(self.current_consumption)
            
            # Keep history limited to last hour
            if len(self.consumption_history) > 3600:
                self.consumption_history.pop(0)
    
    def _process_energy_requests(self):
        """
        Process pending energy allocation requests
        Implements deadlock prevention through priority ordering
        """
        if not self.energy_waitqueue:
            return
            
        with self.energy_lock:
            # Sort by priority (higher priority first)
            self.energy_waitqueue.sort(key=lambda x: x[2], reverse=True)
            
            available_watts = self._get_available_energy()
            processed_requests = []
            
            for i, (task_id, required_watts, priority, callback) in enumerate(self.energy_waitqueue):
                if available_watts >= required_watts:
                    # Allocate energy
                    self.allocated_energy[task_id] = required_watts
                    available_watts -= required_watts
                    
                    # Notify task
                    if callback:
                        try:
                            callback(True, required_watts)
                        except Exception as e:
                            logger.error(f"Error in energy allocation callback: {e}")
                    
                    processed_requests.append(i)
                else:
                    # Cannot allocate - check if we should defer or deny
                    if priority < 3:  # Low priority - deny request
                        if callback:
                            try:
                                callback(False, 0)
                            except Exception as e:
                                logger.error(f"Error in energy denial callback: {e}")
                        processed_requests.append(i)
            
            # Remove processed requests
            for i in reversed(processed_requests):
                self.energy_waitqueue.pop(i)
    
    def request_energy_allocation(self, 
                                task_id: str, 
                                required_watts: float, 
                                priority: int = 1,
                                callback: Optional[Callable] = None) -> bool:
        """
        Request energy allocation for a task (implements distributed locking)
        
        Args:
            task_id: Unique identifier for the task
            required_watts: Power requirement in watts
            priority: Task priority (1=low, 5=critical)
            callback: Function to call when allocation is decided
            
        Returns:
            True if immediately allocated, False if queued or denied
        """
        with self.energy_lock:
            available_watts = self._get_available_energy()
            
            # Immediate allocation for critical tasks or if energy available
            if priority >= 4 or available_watts >= required_watts:
                self.allocated_energy[task_id] = required_watts
                if callback:
                    callback(True, required_watts)
                return True
            else:
                # Queue the request
                self.energy_waitqueue.append((task_id, required_watts, priority, callback))
                return False
    
    def release_energy_allocation(self, task_id: str):
        """Release energy allocation for a completed task"""
        with self.energy_lock:
            if task_id in self.allocated_energy:
                del self.allocated_energy[task_id]
                logger.debug(f"Released energy allocation for task {task_id}")
    
    def _get_available_energy(self) -> float:
        """Calculate available energy for new allocations"""
        total_allocated = sum(self.allocated_energy.values())
        reserved_energy = self.constraints.critical_task_energy_reserve
        
        if self.current_mode == PowerMode.EMERGENCY:
            max_available = 30.0  # Emergency mode - very limited power
        elif self.current_mode == PowerMode.POWER_SAVING:
            max_available = 60.0  # Power saving mode
        else:
            max_available = self.max_power_watts - reserved_energy
        
        return max(0, max_available - total_allocated)
    
    def _evaluate_power_mode(self):
        """Evaluate and update power mode based on battery level"""
        battery_percent = self.get_battery_percentage()
        
        new_mode = self.current_mode
        
        if battery_percent <= self.constraints.emergency_threshold_percent:
            new_mode = PowerMode.EMERGENCY
        elif battery_percent <= self.constraints.power_saving_threshold_percent:
            new_mode = PowerMode.POWER_SAVING
        elif battery_percent > 50:
            new_mode = PowerMode.BALANCED
        elif battery_percent > 80:
            new_mode = PowerMode.HIGH_PERFORMANCE
        
        if new_mode != self.current_mode:
            old_mode = self.current_mode
            self.current_mode = new_mode
            logger.info(f"Power mode changed: {old_mode.value} -> {new_mode.value}")
            
            if self.on_power_mode_change:
                self.on_power_mode_change(old_mode, new_mode)
    
    def _update_battery_level(self):
        """Update battery level based on power consumption"""
        if not self.consumption_history:
            return
        
        # Calculate energy consumed in last second (Wh)
        current_watts = self.current_consumption.total_watts
        energy_consumed_wh = current_watts / 3600.0  # Watts to Watt-hours
        energy_consumed_kwh = energy_consumed_wh / 1000.0
        
        # Update battery
        self.current_battery_kwh = max(0, self.current_battery_kwh - energy_consumed_kwh)
        
        # Check for critical energy levels
        if self.get_battery_percentage() <= 5.0 and self.on_critical_energy:
            self.on_critical_energy(self.current_battery_kwh, self.get_battery_percentage())
    
    def _detect_energy_anomalies(self):
        """Detect unusual energy consumption patterns"""
        if len(self.consumption_history) < 10:
            return
        
        recent_consumption = [c.total_watts for c in self.consumption_history[-10:]]
        mean_consumption = np.mean(recent_consumption)
        std_consumption = np.std(recent_consumption)
        
        current_consumption = self.current_consumption.total_watts
        
        if std_consumption > 0:
            z_score = abs(current_consumption - mean_consumption) / std_consumption
            if z_score > 3.0:  # Significant anomaly
                logger.warning(f"Energy consumption anomaly detected: {current_consumption:.1f}W "
                             f"(mean: {mean_consumption:.1f}W, z-score: {z_score:.2f})")
    
    def _get_power_mode_multiplier(self) -> float:
        """Get power consumption multiplier based on current mode"""
        multipliers = {
            PowerMode.HIGH_PERFORMANCE: 1.2,
            PowerMode.BALANCED: 1.0,
            PowerMode.POWER_SAVING: 0.7,
            PowerMode.EMERGENCY: 0.4
        }
        return multipliers.get(self.current_mode, 1.0)
    
    def _get_cpu_usage(self) -> float:
        """Simulate CPU usage - replace with actual monitoring"""
        import random
        base_usage = 30 + len(self.allocated_energy) * 15  # More tasks = higher usage
        return min(100, base_usage + random.uniform(-10, 20))
    
    def _get_gpu_usage(self) -> float:
        """Simulate GPU usage - replace with actual monitoring"""
        import random
        # GPU used primarily for ML inference tasks
        ml_tasks = sum(1 for task_id in self.allocated_energy.keys() 
                      if 'ml' in task_id.lower() or 'vision' in task_id.lower())
        base_usage = ml_tasks * 25
        return min(100, base_usage + random.uniform(-5, 15))
    
    def _get_network_usage(self) -> float:
        """Simulate network usage - replace with actual monitoring"""
        import random
        network_tasks = sum(1 for task_id in self.allocated_energy.keys() 
                           if 'transmit' in task_id.lower() or 'sync' in task_id.lower())
        return network_tasks * 2 + random.uniform(0, 5)  # Mbps
    
    def _get_storage_usage(self) -> float:
        """Simulate storage operations - replace with actual monitoring"""
        import random
        return len(self.allocated_energy) * 10 + random.uniform(0, 50)
    
    # Public API methods
    def get_current_consumption(self) -> EnergyConsumption:
        """Get current energy consumption"""
        with self.energy_lock:
            return self.current_consumption
    
    def get_battery_percentage(self) -> float:
        """Get current battery percentage"""
        return (self.current_battery_kwh / self.initial_battery_kwh) * 100.0
    
    def get_estimated_runtime_hours(self) -> float:
        """Estimate remaining runtime based on current consumption"""
        if self.current_consumption.total_watts <= 0:
            return float('inf')
        
        remaining_wh = self.current_battery_kwh * 1000  # Convert to Wh
        return remaining_wh / self.current_consumption.total_watts
    
    def get_power_efficiency_score(self) -> float:
        """Calculate power efficiency score (0-100)"""
        if not self.consumption_history:
            return 50.0
        
        # Base efficiency on how well we're managing power vs. task load
        avg_consumption = np.mean([c.total_watts for c in self.consumption_history[-60:]])
        task_load = len(self.allocated_energy)
        
        if task_load == 0:
            return 100.0 if avg_consumption < 30 else 50.0
        
        # Efficiency = tasks per watt * 100
        efficiency = min(100.0, (task_load / (avg_consumption / 100.0)) * 20)
        return efficiency
    
    def get_statistics(self) -> Dict:
        """Get comprehensive energy statistics"""
        with self.energy_lock:
            return {
                'battery_percentage': self.get_battery_percentage(),
                'battery_kwh': self.current_battery_kwh,
                'current_watts': self.current_consumption.total_watts,
                'allocated_tasks': len(self.allocated_energy),
                'pending_requests': len(self.energy_waitqueue),
                'power_mode': self.current_mode.value,
                'efficiency_score': self.get_power_efficiency_score(),
                'estimated_runtime_hours': self.get_estimated_runtime_hours(),
                'component_breakdown': {
                    'cpu_watts': self.current_consumption.cpu_watts,
                    'gpu_watts': self.current_consumption.gpu_watts,
                    'network_watts': self.current_consumption.network_watts,
                    'storage_watts': self.current_consumption.storage_watts,
                    'idle_watts': self.current_consumption.idle_watts
                }
            }

# Distributed Energy Coordination Class
class DistributedEnergyCoordinator:
    """
    Coordinates energy usage across multiple edge nodes
    Implements leader election and distributed energy balancing
    """
    
    def __init__(self, node_id: str, energy_monitor: EnhancedEnergyMonitor):
        self.node_id = node_id
        self.energy_monitor = energy_monitor
        self.peer_nodes: List[str] = []
        self.is_energy_leader = False
        self.energy_term = 0
        self.global_energy_budget = 500.0  # Watts across all nodes
        
    async def elect_energy_leader(self) -> bool:
        """
        Implement RAFT-style leader election for energy coordination
        Returns True if this node becomes the leader
        """
        self.energy_term += 1
        votes_received = 1  # Vote for self
        
        # Request votes from peers
        for peer_id in self.peer_nodes:
            # In real implementation, send network messages
            # For now, simulate based on energy levels
            peer_energy = self._get_peer_energy_level(peer_id)
            my_energy = self.energy_monitor.get_battery_percentage()
            
            # Vote for the node with higher energy
            if my_energy >= peer_energy:
                votes_received += 1
        
        # Become leader if majority votes
        if votes_received > len(self.peer_nodes) / 2:
            self.is_energy_leader = True
            logger.info(f"Node {self.node_id} elected as energy leader for term {self.energy_term}")
            return True
        
        return False
    
    async def coordinate_energy_load_balancing(self):
        """
        Coordinate energy load balancing across nodes (leader only)
        """
        if not self.is_energy_leader:
            return
        
        # Collect energy status from all nodes
        node_energy_status = {}
        for peer_id in self.peer_nodes:
            node_energy_status[peer_id] = self._get_peer_energy_status(peer_id)
        
        # Add own status
        node_energy_status[self.node_id] = self.energy_monitor.get_statistics()
        
        # Calculate optimal load distribution
        total_capacity = sum(status['battery_percentage'] for status in node_energy_status.values())
        
        for node_id, status in node_energy_status.items():
            # Calculate recommended load based on energy level
            recommended_load = (status['battery_percentage'] / total_capacity) * 100
            
            # Send load balancing recommendations
            await self._send_load_recommendation(node_id, recommended_load)
    
    def _get_peer_energy_level(self, peer_id: str) -> float:
        """Simulate getting peer energy level"""
        import random
        return random.uniform(20, 80)  # Simulate peer energy levels
    
    def _get_peer_energy_status(self, peer_id: str) -> Dict:
        """Simulate getting peer energy status"""
        import random
        return {
            'battery_percentage': random.uniform(20, 80),
            'current_watts': random.uniform(40, 120),
            'allocated_tasks': random.randint(1, 5)
        }
    
    async def _send_load_recommendation(self, node_id: str, recommended_load: float):
        """Send load balancing recommendation to peer node"""
        logger.info(f"Recommending {recommended_load:.1f}% load for node {node_id}")
        # In real implementation, send network message