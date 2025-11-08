"""
Bandwidth Monitor for EDGE-QI Framework

Provides real-time bandwidth monitoring and network condition assessment
for intelligent bandwidth management in edge computing environments.
"""

import time
import threading
import statistics
from enum import Enum
from typing import Dict, List, Optional, Callable, Tuple
from dataclasses import dataclass
import numpy as np


class NetworkCondition(Enum):
    """Network condition assessment"""
    EXCELLENT = "excellent"    # > 90% available, low latency
    GOOD = "good"             # 70-90% available, moderate latency  
    FAIR = "fair"             # 50-70% available, higher latency
    POOR = "poor"             # 30-50% available, high latency
    CRITICAL = "critical"     # < 30% available, very high latency


@dataclass
class BandwidthMetrics:
    """Real-time bandwidth and network metrics"""
    timestamp: float
    
    # Bandwidth measurements
    available_bandwidth_mbps: float
    used_bandwidth_mbps: float
    utilization_percentage: float
    
    # Latency measurements
    latency_ms: float
    jitter_ms: float
    
    # Quality metrics
    packet_loss_percentage: float
    throughput_mbps: float
    
    # Network condition
    condition: NetworkCondition
    stability_score: float  # 0.0-1.0
    
    # Historical context
    trend_direction: str    # "improving", "stable", "degrading"
    congestion_level: float # 0.0-1.0


class BandwidthMonitor:
    """
    Real-time bandwidth monitoring and network condition assessment
    """
    
    def __init__(self, 
                 monitoring_interval: float = 1.0,
                 history_size: int = 300):
        """
        Initialize bandwidth monitor
        
        Args:
            monitoring_interval: How often to measure (seconds)
            history_size: Number of historical measurements to keep
        """
        self.monitoring_interval = monitoring_interval
        self.history_size = history_size
        
        # Monitoring state
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Historical data
        self.bandwidth_history: List[BandwidthMetrics] = []
        self.history_lock = threading.Lock()
        
        # Current metrics
        self.current_metrics: Optional[BandwidthMetrics] = None
        
        # Network configuration
        self.max_bandwidth_mbps = 10.0  # Assume 10 Mbps connection
        self.baseline_latency_ms = 20.0
        
        # Callbacks
        self.on_metrics_update: Optional[Callable] = None
        self.on_condition_change: Optional[Callable] = None
        
        # Simulated network state for demonstration
        self.simulated_conditions = {
            'base_bandwidth': 10.0,
            'congestion_factor': 1.0,
            'latency_factor': 1.0,
            'stability': 0.9
        }
    
    def start_monitoring(self):
        """Start bandwidth monitoring"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        print("Bandwidth monitoring started")
    
    def stop_monitoring(self):
        """Stop bandwidth monitoring"""
        self.is_monitoring = False
        
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2.0)
        
        print("Bandwidth monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Measure current network conditions
                metrics = self._measure_network_conditions()
                
                # Store metrics
                with self.history_lock:
                    self.bandwidth_history.append(metrics)
                    
                    # Maintain history size
                    if len(self.bandwidth_history) > self.history_size:
                        self.bandwidth_history.pop(0)
                    
                    self.current_metrics = metrics
                
                # Check for condition changes
                self._check_condition_changes(metrics)
                
                # Notify callbacks
                if self.on_metrics_update:
                    try:
                        self.on_metrics_update(metrics)
                    except Exception as e:
                        print(f"Metrics callback error: {e}")
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                print(f"Monitoring loop error: {e}")
                time.sleep(5.0)
    
    def _measure_network_conditions(self) -> BandwidthMetrics:
        """Measure current network conditions"""
        current_time = time.time()
        
        # Simulate realistic network measurements
        # In real implementation, this would use actual network probing
        
        # Bandwidth measurement
        available_bandwidth = self._measure_bandwidth()
        used_bandwidth = self._estimate_current_usage()
        utilization = (used_bandwidth / max(available_bandwidth, 0.1)) * 100
        
        # Latency measurement
        latency = self._measure_latency()
        jitter = self._measure_jitter()
        
        # Quality measurement
        packet_loss = self._measure_packet_loss()
        throughput = self._measure_throughput()
        
        # Network condition assessment
        condition = self._assess_network_condition(
            available_bandwidth, utilization, latency, packet_loss
        )
        
        # Stability and trend analysis
        stability_score = self._calculate_stability_score()
        trend_direction = self._analyze_trend()
        congestion_level = self._estimate_congestion_level(utilization, latency)
        
        return BandwidthMetrics(
            timestamp=current_time,
            available_bandwidth_mbps=available_bandwidth,
            used_bandwidth_mbps=used_bandwidth,
            utilization_percentage=utilization,
            latency_ms=latency,
            jitter_ms=jitter,
            packet_loss_percentage=packet_loss,
            throughput_mbps=throughput,
            condition=condition,
            stability_score=stability_score,
            trend_direction=trend_direction,
            congestion_level=congestion_level
        )
    
    def _measure_bandwidth(self) -> float:
        """Measure available bandwidth (simulated)"""
        # Simulate bandwidth measurement with realistic variations
        base_bandwidth = self.simulated_conditions['base_bandwidth']
        congestion = self.simulated_conditions['congestion_factor']
        
        # Add time-based variations (peak hours, etc.)
        hour = time.localtime().tm_hour
        time_factor = 1.0
        
        if 9 <= hour <= 17:  # Business hours
            time_factor = 0.7
        elif 19 <= hour <= 23:  # Evening peak
            time_factor = 0.5
        
        # Add random variations
        variation = np.random.normal(1.0, 0.1)
        
        available_bandwidth = base_bandwidth * congestion * time_factor * variation
        return max(0.1, available_bandwidth)
    
    def _estimate_current_usage(self) -> float:
        """Estimate current bandwidth usage"""
        # Simulate current usage based on system activity
        base_usage = 0.5  # Base system usage
        
        # Add random usage spikes
        if np.random.random() < 0.1:  # 10% chance of usage spike
            spike = np.random.uniform(2.0, 5.0)
            return min(self.max_bandwidth_mbps * 0.9, base_usage + spike)
        
        # Normal usage with variations
        usage_variation = np.random.uniform(0.1, 2.0)
        return base_usage + usage_variation
    
    def _measure_latency(self) -> float:
        """Measure network latency (simulated)"""
        base_latency = self.baseline_latency_ms
        latency_factor = self.simulated_conditions['latency_factor']
        
        # Add congestion-based latency
        if hasattr(self, 'current_metrics') and self.current_metrics:
            congestion_latency = self.current_metrics.utilization_percentage * 0.5
        else:
            congestion_latency = 0
        
        # Add random variations
        variation = np.random.normal(1.0, 0.2)
        
        latency = (base_latency * latency_factor + congestion_latency) * variation
        return max(1.0, latency)
    
    def _measure_jitter(self) -> float:
        """Measure network jitter (simulated)"""
        # Jitter typically correlates with latency and congestion
        base_jitter = 2.0
        
        if hasattr(self, 'current_metrics') and self.current_metrics:
            latency_jitter = self.current_metrics.latency_ms * 0.1
            congestion_jitter = self.current_metrics.utilization_percentage * 0.05
        else:
            latency_jitter = congestion_jitter = 0
        
        total_jitter = base_jitter + latency_jitter + congestion_jitter
        return max(0.1, total_jitter + np.random.normal(0, 0.5))
    
    def _measure_packet_loss(self) -> float:
        """Measure packet loss percentage (simulated)"""
        base_loss = 0.1  # 0.1% base loss
        
        # Loss increases with utilization and latency
        if hasattr(self, 'current_metrics') and self.current_metrics:
            utilization_loss = max(0, (self.current_metrics.utilization_percentage - 70) * 0.01)
            latency_loss = max(0, (self.current_metrics.latency_ms - 50) * 0.005)
        else:
            utilization_loss = latency_loss = 0
        
        total_loss = base_loss + utilization_loss + latency_loss
        return min(10.0, max(0.0, total_loss + np.random.normal(0, 0.02)))
    
    def _measure_throughput(self) -> float:
        """Measure actual throughput (simulated)"""
        # Throughput is affected by packet loss and congestion
        available_bandwidth = getattr(self, '_last_bandwidth', 10.0)
        
        if hasattr(self, 'current_metrics') and self.current_metrics:
            loss_factor = 1.0 - (self.current_metrics.packet_loss_percentage / 100)
            congestion_factor = 1.0 - (self.current_metrics.utilization_percentage / 200)
        else:
            loss_factor = congestion_factor = 0.9
        
        throughput = available_bandwidth * loss_factor * congestion_factor
        return max(0.1, throughput)
    
    def _assess_network_condition(self, 
                                 bandwidth: float,
                                 utilization: float,
                                 latency: float,
                                 packet_loss: float) -> NetworkCondition:
        """Assess overall network condition"""
        # Calculate condition score based on multiple factors
        bandwidth_score = min(1.0, bandwidth / self.max_bandwidth_mbps)
        utilization_score = max(0.0, (100 - utilization) / 100)
        latency_score = max(0.0, (100 - latency) / 100)
        loss_score = max(0.0, (5.0 - packet_loss) / 5.0)
        
        # Weighted overall score
        overall_score = (
            bandwidth_score * 0.3 +
            utilization_score * 0.3 +
            latency_score * 0.2 +
            loss_score * 0.2
        )
        
        # Map score to condition
        if overall_score >= 0.9:
            return NetworkCondition.EXCELLENT
        elif overall_score >= 0.7:
            return NetworkCondition.GOOD
        elif overall_score >= 0.5:
            return NetworkCondition.FAIR
        elif overall_score >= 0.3:
            return NetworkCondition.POOR
        else:
            return NetworkCondition.CRITICAL
    
    def _calculate_stability_score(self) -> float:
        """Calculate network stability score based on recent history"""
        with self.history_lock:
            if len(self.bandwidth_history) < 10:
                return 0.5  # Not enough data
            
            # Get recent measurements
            recent_metrics = self.bandwidth_history[-10:]
            
            # Calculate coefficient of variation for key metrics
            bandwidths = [m.available_bandwidth_mbps for m in recent_metrics]
            latencies = [m.latency_ms for m in recent_metrics]
            
            bandwidth_cv = statistics.stdev(bandwidths) / max(statistics.mean(bandwidths), 0.1)
            latency_cv = statistics.stdev(latencies) / max(statistics.mean(latencies), 0.1)
            
            # Lower coefficient of variation = higher stability
            stability = max(0.0, 1.0 - (bandwidth_cv + latency_cv) / 2)
            return min(1.0, stability)
    
    def _analyze_trend(self) -> str:
        """Analyze trend direction for key metrics"""
        with self.history_lock:
            if len(self.bandwidth_history) < 5:
                return "stable"
            
            # Get recent measurements
            recent_metrics = self.bandwidth_history[-5:]
            
            # Analyze bandwidth trend
            bandwidths = [m.available_bandwidth_mbps for m in recent_metrics]
            latencies = [m.latency_ms for m in recent_metrics]
            
            # Simple linear trend analysis
            bandwidth_trend = np.polyfit(range(len(bandwidths)), bandwidths, 1)[0]
            latency_trend = np.polyfit(range(len(latencies)), latencies, 1)[0]
            
            # Determine overall trend
            if bandwidth_trend > 0.1 and latency_trend < -1.0:
                return "improving"
            elif bandwidth_trend < -0.1 or latency_trend > 1.0:
                return "degrading"
            else:
                return "stable"
    
    def _estimate_congestion_level(self, utilization: float, latency: float) -> float:
        """Estimate network congestion level"""
        # Congestion based on utilization and latency
        utilization_congestion = min(1.0, utilization / 100)
        latency_congestion = min(1.0, max(0.0, (latency - self.baseline_latency_ms) / 100))
        
        # Combined congestion level
        congestion = (utilization_congestion * 0.7 + latency_congestion * 0.3)
        return min(1.0, max(0.0, congestion))
    
    def _check_condition_changes(self, metrics: BandwidthMetrics):
        """Check for significant condition changes"""
        if self.current_metrics is None:
            return
        
        # Check for condition change
        if metrics.condition != self.current_metrics.condition:
            if self.on_condition_change:
                try:
                    self.on_condition_change(
                        self.current_metrics.condition,
                        metrics.condition,
                        metrics
                    )
                except Exception as e:
                    print(f"Condition change callback error: {e}")
    
    def get_current_metrics(self) -> Optional[BandwidthMetrics]:
        """Get current bandwidth metrics"""
        return self.current_metrics
    
    def get_historical_metrics(self, 
                             duration_seconds: Optional[int] = None) -> List[BandwidthMetrics]:
        """
        Get historical bandwidth metrics
        
        Args:
            duration_seconds: How far back to look (None for all history)
            
        Returns:
            List of historical metrics
        """
        with self.history_lock:
            if duration_seconds is None:
                return list(self.bandwidth_history)
            
            cutoff_time = time.time() - duration_seconds
            return [
                m for m in self.bandwidth_history 
                if m.timestamp >= cutoff_time
            ]
    
    def get_network_summary(self) -> Dict[str, any]:
        """Get summary of current network conditions"""
        if self.current_metrics is None:
            return {"status": "No data available"}
        
        metrics = self.current_metrics
        
        # Calculate averages from recent history
        recent_metrics = self.get_historical_metrics(300)  # Last 5 minutes
        
        if recent_metrics:
            avg_bandwidth = statistics.mean([m.available_bandwidth_mbps for m in recent_metrics])
            avg_latency = statistics.mean([m.latency_ms for m in recent_metrics])
            avg_loss = statistics.mean([m.packet_loss_percentage for m in recent_metrics])
        else:
            avg_bandwidth = metrics.available_bandwidth_mbps
            avg_latency = metrics.latency_ms
            avg_loss = metrics.packet_loss_percentage
        
        return {
            "current_condition": metrics.condition.value,
            "stability_score": metrics.stability_score,
            "trend": metrics.trend_direction,
            "current_bandwidth_mbps": metrics.available_bandwidth_mbps,
            "average_bandwidth_mbps": avg_bandwidth,
            "current_utilization": metrics.utilization_percentage,
            "current_latency_ms": metrics.latency_ms,
            "average_latency_ms": avg_latency,
            "packet_loss_percentage": avg_loss,
            "congestion_level": metrics.congestion_level,
            "last_updated": metrics.timestamp
        }
    
    def predict_bandwidth_availability(self, 
                                     future_seconds: int = 60) -> Dict[str, float]:
        """
        Predict bandwidth availability for near future
        
        Args:
            future_seconds: How far into future to predict
            
        Returns:
            Prediction results
        """
        recent_metrics = self.get_historical_metrics(300)  # Last 5 minutes
        
        if len(recent_metrics) < 10:
            # Not enough data for prediction
            current = self.current_metrics
            if current:
                return {
                    "predicted_bandwidth_mbps": current.available_bandwidth_mbps,
                    "confidence": 0.3,
                    "prediction_method": "current_value"
                }
            else:
                return {
                    "predicted_bandwidth_mbps": self.max_bandwidth_mbps * 0.5,
                    "confidence": 0.1,
                    "prediction_method": "default"
                }
        
        # Simple trend-based prediction
        bandwidths = [m.available_bandwidth_mbps for m in recent_metrics]
        times = [m.timestamp for m in recent_metrics]
        
        # Linear regression for trend
        if len(bandwidths) >= 2:
            trend_slope = np.polyfit(
                [t - times[0] for t in times], 
                bandwidths, 
                1
            )[0]
            
            current_bandwidth = bandwidths[-1]
            predicted_bandwidth = current_bandwidth + (trend_slope * future_seconds)
            
            # Bound prediction within reasonable limits
            predicted_bandwidth = max(0.1, min(self.max_bandwidth_mbps, predicted_bandwidth))
            
            # Calculate confidence based on trend consistency
            trend_consistency = 1.0 - (statistics.stdev(bandwidths) / max(statistics.mean(bandwidths), 0.1))
            confidence = max(0.1, min(0.9, trend_consistency))
            
            return {
                "predicted_bandwidth_mbps": predicted_bandwidth,
                "confidence": confidence,
                "prediction_method": "linear_trend",
                "trend_slope": trend_slope
            }
        
        # Fallback to average
        avg_bandwidth = statistics.mean(bandwidths)
        return {
            "predicted_bandwidth_mbps": avg_bandwidth,
            "confidence": 0.6,
            "prediction_method": "historical_average"
        }
    
    def set_network_configuration(self, 
                                max_bandwidth_mbps: float,
                                baseline_latency_ms: float = 20.0):
        """
        Update network configuration parameters
        
        Args:
            max_bandwidth_mbps: Maximum available bandwidth
            baseline_latency_ms: Expected baseline latency
        """
        self.max_bandwidth_mbps = max_bandwidth_mbps
        self.baseline_latency_ms = baseline_latency_ms
    
    def simulate_network_conditions(self, 
                                  congestion_factor: float = 1.0,
                                  latency_factor: float = 1.0,
                                  stability: float = 0.9):
        """
        Simulate specific network conditions for testing
        
        Args:
            congestion_factor: Network congestion multiplier (0.1-1.0)
            latency_factor: Latency multiplier (1.0-5.0) 
            stability: Network stability score (0.0-1.0)
        """
        self.simulated_conditions.update({
            'congestion_factor': max(0.1, min(1.0, congestion_factor)),
            'latency_factor': max(1.0, min(5.0, latency_factor)),
            'stability': max(0.0, min(1.0, stability))
        })
        
        print(f"Simulated network conditions updated: "
              f"congestion={congestion_factor:.1f}, "
              f"latency={latency_factor:.1f}, "
              f"stability={stability:.1f}")
    
    def export_metrics(self, 
                      duration_seconds: Optional[int] = None) -> List[Dict[str, any]]:
        """
        Export metrics data for analysis
        
        Args:
            duration_seconds: How far back to export (None for all)
            
        Returns:
            List of metric dictionaries
        """
        metrics = self.get_historical_metrics(duration_seconds)
        
        return [
            {
                "timestamp": m.timestamp,
                "available_bandwidth_mbps": m.available_bandwidth_mbps,
                "used_bandwidth_mbps": m.used_bandwidth_mbps,
                "utilization_percentage": m.utilization_percentage,
                "latency_ms": m.latency_ms,
                "jitter_ms": m.jitter_ms,
                "packet_loss_percentage": m.packet_loss_percentage,
                "throughput_mbps": m.throughput_mbps,
                "condition": m.condition.value,
                "stability_score": m.stability_score,
                "trend_direction": m.trend_direction,
                "congestion_level": m.congestion_level
            }
            for m in metrics
        ]