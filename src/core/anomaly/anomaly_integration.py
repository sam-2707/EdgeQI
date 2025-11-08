"""
Queue Anomaly Integration

Integration layer that connects queue anomaly detection with the existing
EDGE-QI queue detection and monitoring systems. Provides seamless anomaly
detection capabilities within the queue intelligence framework.
"""

import time
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

from Core.anomaly.queue_anomaly_detector import (
    QueueAnomalyDetector, QueueMetrics, QueueAnomaly, AnomalyType, AnomalySeverity
)

@dataclass
class QueueData:
    """Data structure for queue detection results"""
    queue_id: str
    timestamp: float
    queue_length: float
    estimated_wait_time: float
    queue_density: float
    trajectory_points: Optional[List] = None
    historical_lengths: Optional[List] = None
    average_speed: Optional[float] = None
    length_change_rate: Optional[float] = None
    abandonment_rate: Optional[float] = None
    object_count: Optional[int] = None
    
    @classmethod
    def from_detection_result(cls, queue_id: str, detection_result: Dict) -> 'QueueData':
        """Create QueueData from queue detection result dictionary"""
        metrics = detection_result.get('queue_metrics', {})
        
        return cls(
            queue_id=queue_id,
            timestamp=time.time(),
            queue_length=metrics.get('total_queue_length', 0.0),
            estimated_wait_time=metrics.get('estimated_wait_time', 0.0),
            queue_density=metrics.get('queue_density', 0.0),
            object_count=metrics.get('total_people', 0)
        )

class QueueAnomalyIntegrator:
    """Integrates anomaly detection with existing queue detection system"""
    
    def __init__(self, 
                 sensitivity: float = 2.5,
                 enable_ml: bool = True,
                 training_window: int = 100):
        """
        Initialize anomaly integrator
        
        Args:
            sensitivity: Statistical anomaly detection sensitivity
            enable_ml: Whether to enable ML-based detection
            training_window: Number of samples for ML training
        """
        self.anomaly_detector = QueueAnomalyDetector(
            statistical_sensitivity=sensitivity,
            enable_ml=enable_ml
        )
        
        self.training_window = training_window
        self.queue_history = {}
        self.anomaly_callbacks = []
        
        # Configuration
        self.min_training_samples = 50
        self.ml_trained = False
        
        self.logger = logging.getLogger(__name__)
    
    def register_anomaly_callback(self, callback):
        """Register callback function for anomaly notifications"""
        self.anomaly_callbacks.append(callback)
    
    def process_queue_data(self, queue_data: QueueData) -> List[QueueAnomaly]:
        """
        Process queue data and detect anomalies
        
        Args:
            queue_data: Queue detection results
            
        Returns:
            List of detected anomalies
        """
        # Convert QueueData to QueueMetrics
        metrics = self._convert_to_metrics(queue_data)
        
        # Store historical data
        self._store_historical_data(metrics)
        
        # Train ML detector if enough data available
        if not self.ml_trained and self._should_train_ml():
            self._train_ml_detector()
        
        # Detect anomalies
        anomalies = self.anomaly_detector.detect_anomalies(metrics)
        
        # Notify callbacks
        for anomaly in anomalies:
            self._notify_callbacks(anomaly)
        
        return anomalies
    
    def _convert_to_metrics(self, queue_data: QueueData) -> QueueMetrics:
        """Convert QueueData to QueueMetrics format"""
        # Calculate additional metrics from queue data
        spatial_distribution = []
        if hasattr(queue_data, 'trajectory_points') and queue_data.trajectory_points:
            spatial_distribution = [(p.x, p.y) for p in queue_data.trajectory_points]
        
        # Calculate temporal pattern (simplified)
        temporal_pattern = []
        if hasattr(queue_data, 'historical_lengths') and queue_data.historical_lengths:
            temporal_pattern = queue_data.historical_lengths[-10:]  # Last 10 measurements
        
        # Calculate movement speed
        movement_speed = 0.0
        if hasattr(queue_data, 'average_speed') and queue_data.average_speed is not None:
            movement_speed = queue_data.average_speed
        elif spatial_distribution and len(spatial_distribution) > 1:
            # Estimate based on spatial changes
            distances = []
            for i in range(1, len(spatial_distribution)):
                p1, p2 = spatial_distribution[i-1], spatial_distribution[i]
                dist = ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5
                distances.append(dist)
            movement_speed = sum(distances) / len(distances) if distances else 0.0
        
        # Calculate formation rate (queue length change rate)
        formation_rate = 0.0
        if hasattr(queue_data, 'length_change_rate') and queue_data.length_change_rate is not None:
            formation_rate = queue_data.length_change_rate
        
        # Calculate abandonment rate (estimated)
        abandonment_rate = 0.0
        if hasattr(queue_data, 'abandonment_rate') and queue_data.abandonment_rate is not None:
            abandonment_rate = queue_data.abandonment_rate
        elif queue_data.queue_length > 0:
            # Simple estimation based on wait time
            abandonment_rate = min(queue_data.estimated_wait_time / 600.0, 1.0)  # Normalize by 10 minutes
        
        # Interaction count (number of people/objects in queue)
        interaction_count = 0
        if hasattr(queue_data, 'object_count') and queue_data.object_count is not None:
            interaction_count = queue_data.object_count
        elif spatial_distribution:
            interaction_count = len(spatial_distribution)
        
        return QueueMetrics(
            queue_id=queue_data.queue_id,
            timestamp=datetime.fromtimestamp(queue_data.timestamp),
            length=queue_data.queue_length,
            wait_time=queue_data.estimated_wait_time,
            density=queue_data.queue_density,
            movement_speed=movement_speed,
            formation_rate=formation_rate,
            abandonment_rate=abandonment_rate,
            spatial_distribution=spatial_distribution,
            temporal_pattern=temporal_pattern,
            interaction_count=interaction_count
        )
    
    def _store_historical_data(self, metrics: QueueMetrics):
        """Store historical data for training and analysis"""
        if metrics.queue_id not in self.queue_history:
            self.queue_history[metrics.queue_id] = []
        
        self.queue_history[metrics.queue_id].append(metrics)
        
        # Keep only recent data within training window
        if len(self.queue_history[metrics.queue_id]) > self.training_window:
            self.queue_history[metrics.queue_id].pop(0)
    
    def _should_train_ml(self) -> bool:
        """Check if ML detector should be trained"""
        total_samples = sum(len(history) for history in self.queue_history.values())
        return total_samples >= self.min_training_samples
    
    def _train_ml_detector(self):
        """Train the ML anomaly detector"""
        all_metrics = []
        for history in self.queue_history.values():
            all_metrics.extend(history)
        
        if len(all_metrics) >= self.min_training_samples:
            success = self.anomaly_detector.train_ml_detector(all_metrics)
            if success:
                self.ml_trained = True
                self.logger.info(f"ML anomaly detector trained with {len(all_metrics)} samples")
            else:
                self.logger.warning("Failed to train ML anomaly detector")
    
    def _notify_callbacks(self, anomaly: QueueAnomaly):
        """Notify registered callbacks about anomaly"""
        for callback in self.anomaly_callbacks:
            try:
                callback(anomaly)
            except Exception as e:
                self.logger.error(f"Error in anomaly callback: {e}")
    
    def get_anomaly_statistics(self) -> Dict[str, Any]:
        """Get comprehensive anomaly detection statistics"""
        detector_stats = self.anomaly_detector.get_detection_statistics()
        
        # Add integration-specific statistics
        integration_stats = {
            'ml_trained': self.ml_trained,
            'total_queues_monitored': len(self.queue_history),
            'total_samples_collected': sum(len(h) for h in self.queue_history.values()),
            'callbacks_registered': len(self.anomaly_callbacks),
            'queue_histories': {
                queue_id: len(history) for queue_id, history in self.queue_history.items()
            }
        }
        
        return {**detector_stats, **integration_stats}
    
    def force_ml_training(self) -> bool:
        """Force ML training if sufficient data is available"""
        if self._should_train_ml():
            self._train_ml_detector()
            return self.ml_trained
        return False
    
    def reset_detector(self):
        """Reset the anomaly detector state"""
        self.anomaly_detector = QueueAnomalyDetector(
            statistical_sensitivity=self.anomaly_detector.statistical_detector.sensitivity,
            enable_ml=self.anomaly_detector.ml_detector is not None
        )
        self.ml_trained = False
        self.logger.info("Anomaly detector reset")

class AnomalyAlertManager:
    """Manages anomaly alerts and notifications"""
    
    def __init__(self, alert_threshold: AnomalySeverity = AnomalySeverity.MEDIUM):
        self.alert_threshold = alert_threshold
        self.active_alerts = {}
        self.alert_history = []
        self.suppression_window = 300  # 5 minutes in seconds
        
        self.logger = logging.getLogger(__name__)
    
    def process_anomaly(self, anomaly: QueueAnomaly) -> bool:
        """
        Process anomaly and determine if alert should be triggered
        
        Args:
            anomaly: Detected anomaly
            
        Returns:
            True if alert was triggered, False otherwise
        """
        # Check if anomaly severity meets threshold
        severity_order = [AnomalySeverity.LOW, AnomalySeverity.MEDIUM, 
                         AnomalySeverity.HIGH, AnomalySeverity.CRITICAL]
        
        if severity_order.index(anomaly.severity) < severity_order.index(self.alert_threshold):
            return False
        
        # Check for alert suppression (avoid spam)
        if self._is_suppressed(anomaly):
            return False
        
        # Trigger alert
        self._trigger_alert(anomaly)
        return True
    
    def _is_suppressed(self, anomaly: QueueAnomaly) -> bool:
        """Check if anomaly should be suppressed due to recent similar alerts"""
        current_time = time.time()
        anomaly_key = f"{anomaly.type.value}_{anomaly.affected_queue_ids[0] if anomaly.affected_queue_ids else 'unknown'}"
        
        if anomaly_key in self.active_alerts:
            last_alert_time = self.active_alerts[anomaly_key]
            if current_time - last_alert_time < self.suppression_window:
                return True
        
        return False
    
    def _trigger_alert(self, anomaly: QueueAnomaly):
        """Trigger alert for anomaly"""
        current_time = time.time()
        anomaly_key = f"{anomaly.type.value}_{anomaly.affected_queue_ids[0] if anomaly.affected_queue_ids else 'unknown'}"
        
        # Record alert
        self.active_alerts[anomaly_key] = current_time
        self.alert_history.append({
            'timestamp': current_time,
            'anomaly_id': anomaly.id,
            'type': anomaly.type.value,
            'severity': anomaly.severity.value,
            'confidence': anomaly.confidence,
            'description': anomaly.description
        })
        
        # Keep alert history limited
        if len(self.alert_history) > 1000:
            self.alert_history.pop(0)
        
        # Log alert
        self.logger.warning(
            f"ANOMALY ALERT: {anomaly.type.value} ({anomaly.severity.value}) - "
            f"{anomaly.description} [Confidence: {anomaly.confidence:.2f}]"
        )
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get currently active alerts"""
        current_time = time.time()
        active = []
        
        for alert in self.alert_history[-50:]:  # Last 50 alerts
            if current_time - alert['timestamp'] < self.suppression_window:
                active.append(alert)
        
        return active
    
    def clear_alerts(self, anomaly_type: Optional[AnomalyType] = None):
        """Clear alerts, optionally filtered by type"""
        if anomaly_type:
            # Clear specific type
            keys_to_remove = [k for k in self.active_alerts.keys() if k.startswith(anomaly_type.value)]
            for key in keys_to_remove:
                del self.active_alerts[key]
        else:
            # Clear all
            self.active_alerts.clear()
        
        self.logger.info(f"Cleared alerts{' for ' + anomaly_type.value if anomaly_type else ''}")

def create_default_anomaly_callback(alert_manager: AnomalyAlertManager):
    """Create default anomaly callback that uses alert manager"""
    def callback(anomaly: QueueAnomaly):
        alert_manager.process_anomaly(anomaly)
    
    return callback