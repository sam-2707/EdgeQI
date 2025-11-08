"""
Queue Anomaly Detection Module

Advanced anomaly detection system for queue intelligence that identifies:
- Overcrowding situations
- Abnormal waiting times
- Suspicious behavior patterns
- Queue formation anomalies
- Traffic flow irregularities

Uses statistical analysis, machine learning algorithms, and pattern recognition
to detect various types of queue-related anomalies in real-time.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging
from enum import Enum
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class AnomalyType(Enum):
    """Types of queue anomalies"""
    OVERCROWDING = "overcrowding"
    ABNORMAL_WAIT_TIME = "abnormal_wait_time"
    SUSPICIOUS_BEHAVIOR = "suspicious_behavior"
    QUEUE_FORMATION = "queue_formation"
    TRAFFIC_FLOW = "traffic_flow"
    DENSITY_SPIKE = "density_spike"
    ABANDONMENT_PATTERN = "abandonment_pattern"
    BOTTLENECK = "bottleneck"

class AnomalySeverity(Enum):
    """Severity levels for anomalies"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class QueueAnomaly:
    """Represents a detected queue anomaly"""
    id: str
    type: AnomalyType
    severity: AnomalySeverity
    confidence: float
    timestamp: datetime
    location: Tuple[float, float]
    description: str
    affected_queue_ids: List[str]
    metrics: Dict[str, float]
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert anomaly to dictionary format"""
        return {
            'id': self.id,
            'type': self.type.value,
            'severity': self.severity.value,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat(),
            'location': self.location,
            'description': self.description,
            'affected_queue_ids': self.affected_queue_ids,
            'metrics': self.metrics,
            'recommendations': self.recommendations
        }

@dataclass
class QueueMetrics:
    """Queue metrics for anomaly detection"""
    queue_id: str
    timestamp: datetime
    length: float
    wait_time: float
    density: float
    movement_speed: float
    formation_rate: float
    abandonment_rate: float
    spatial_distribution: List[Tuple[float, float]]
    temporal_pattern: List[float]
    interaction_count: int
    
class StatisticalAnomalyDetector:
    """Statistical methods for anomaly detection"""
    
    def __init__(self, window_size: int = 50, sensitivity: float = 2.5):
        self.window_size = window_size
        self.sensitivity = sensitivity
        self.historical_data = {}
        
    def detect_statistical_anomalies(self, metrics: QueueMetrics) -> List[Tuple[AnomalyType, float]]:
        """Detect anomalies using statistical methods"""
        anomalies = []
        
        # Initialize historical data for queue if not exists
        if metrics.queue_id not in self.historical_data:
            self.historical_data[metrics.queue_id] = {
                'length': [], 'wait_time': [], 'density': [],
                'movement_speed': [], 'formation_rate': [], 'abandonment_rate': []
            }
        
        history = self.historical_data[metrics.queue_id]
        
        # Check for length anomalies (overcrowding)
        if len(history['length']) >= self.window_size:
            length_mean = np.mean(history['length'])
            length_std = np.std(history['length'])
            
            if length_std > 0:
                z_score = abs(metrics.length - length_mean) / length_std
                if z_score > self.sensitivity:
                    confidence = min(z_score / self.sensitivity, 1.0)
                    if metrics.length > length_mean:
                        anomalies.append((AnomalyType.OVERCROWDING, confidence))
        
        # Check for wait time anomalies
        if len(history['wait_time']) >= self.window_size:
            wait_mean = np.mean(history['wait_time'])
            wait_std = np.std(history['wait_time'])
            
            if wait_std > 0:
                z_score = abs(metrics.wait_time - wait_mean) / wait_std
                if z_score > self.sensitivity:
                    confidence = min(z_score / self.sensitivity, 1.0)
                    anomalies.append((AnomalyType.ABNORMAL_WAIT_TIME, confidence))
        
        # Check for density spikes
        if len(history['density']) >= self.window_size:
            density_mean = np.mean(history['density'])
            density_std = np.std(history['density'])
            
            if density_std > 0:
                z_score = abs(metrics.density - density_mean) / density_std
                if z_score > self.sensitivity and metrics.density > density_mean:
                    confidence = min(z_score / self.sensitivity, 1.0)
                    anomalies.append((AnomalyType.DENSITY_SPIKE, confidence))
        
        # Check for abnormal abandonment patterns
        if len(history['abandonment_rate']) >= self.window_size:
            abandon_mean = np.mean(history['abandonment_rate'])
            abandon_std = np.std(history['abandonment_rate'])
            
            if abandon_std > 0:
                z_score = abs(metrics.abandonment_rate - abandon_mean) / abandon_std
                if z_score > self.sensitivity and metrics.abandonment_rate > abandon_mean:
                    confidence = min(z_score / self.sensitivity, 1.0)
                    anomalies.append((AnomalyType.ABANDONMENT_PATTERN, confidence))
        
        # Update historical data
        for key in history.keys():
            history[key].append(getattr(metrics, key))
            if len(history[key]) > self.window_size:
                history[key].pop(0)
        
        return anomalies

class MLAnomalyDetector:
    """Machine learning-based anomaly detection"""
    
    def __init__(self, contamination: float = 0.1):
        self.contamination = contamination
        self.isolation_forest = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_history = []
        
    def prepare_features(self, metrics: QueueMetrics) -> np.ndarray:
        """Prepare feature vector from queue metrics"""
        features = [
            metrics.length,
            metrics.wait_time,
            metrics.density,
            metrics.movement_speed,
            metrics.formation_rate,
            metrics.abandonment_rate,
            metrics.interaction_count,
            len(metrics.spatial_distribution),
            np.mean(metrics.temporal_pattern) if metrics.temporal_pattern else 0,
            np.std(metrics.temporal_pattern) if metrics.temporal_pattern else 0
        ]
        return np.array(features).reshape(1, -1)
    
    def train(self, historical_metrics: List[QueueMetrics]):
        """Train the ML model with historical data"""
        if len(historical_metrics) < 50:
            logging.warning("Insufficient data for ML training")
            return False
        
        features = []
        for metrics in historical_metrics:
            feature_vector = self.prepare_features(metrics).flatten()
            features.append(feature_vector)
        
        features_array = np.array(features)
        
        # Scale features
        self.scaler.fit(features_array)
        scaled_features = self.scaler.transform(features_array)
        
        # Train isolation forest
        self.isolation_forest.fit(scaled_features)
        self.is_trained = True
        
        return True
    
    def detect_ml_anomalies(self, metrics: QueueMetrics) -> List[Tuple[AnomalyType, float]]:
        """Detect anomalies using ML model"""
        if not self.is_trained:
            return []
        
        features = self.prepare_features(metrics)
        scaled_features = self.scaler.transform(features)
        
        # Get anomaly score
        anomaly_score = self.isolation_forest.decision_function(scaled_features)[0]
        is_anomaly = self.isolation_forest.predict(scaled_features)[0] == -1
        
        anomalies = []
        if is_anomaly:
            # Convert score to confidence (higher negative score = more anomalous)
            confidence = min(abs(anomaly_score) * 2, 1.0)
            
            # Determine anomaly type based on features
            if metrics.density > 0.8:
                anomalies.append((AnomalyType.OVERCROWDING, confidence))
            elif metrics.wait_time > 300:  # 5 minutes
                anomalies.append((AnomalyType.ABNORMAL_WAIT_TIME, confidence))
            elif metrics.movement_speed < 0.1:
                anomalies.append((AnomalyType.BOTTLENECK, confidence))
            else:
                anomalies.append((AnomalyType.SUSPICIOUS_BEHAVIOR, confidence))
        
        return anomalies

class BehaviorPatternDetector:
    """Detect suspicious behavior patterns in queues"""
    
    def __init__(self):
        self.behavior_history = {}
        self.pattern_threshold = 0.7
        
    def detect_behavior_anomalies(self, metrics: QueueMetrics) -> List[Tuple[AnomalyType, float]]:
        """Detect suspicious behavior patterns"""
        anomalies = []
        
        # Check for unusual spatial distribution patterns
        if len(metrics.spatial_distribution) > 0:
            spatial_anomaly = self._analyze_spatial_pattern(metrics)
            if spatial_anomaly:
                anomalies.append(spatial_anomaly)
        
        # Check for temporal pattern anomalies
        if len(metrics.temporal_pattern) > 0:
            temporal_anomaly = self._analyze_temporal_pattern(metrics)
            if temporal_anomaly:
                anomalies.append(temporal_anomaly)
        
        # Check for formation pattern anomalies
        formation_anomaly = self._analyze_formation_pattern(metrics)
        if formation_anomaly:
            anomalies.append(formation_anomaly)
        
        return anomalies
    
    def _analyze_spatial_pattern(self, metrics: QueueMetrics) -> Optional[Tuple[AnomalyType, float]]:
        """Analyze spatial distribution for anomalies"""
        positions = np.array(metrics.spatial_distribution)
        
        if len(positions) < 3:
            return None
        
        # Use DBSCAN to detect clustering anomalies
        clustering = DBSCAN(eps=5.0, min_samples=2).fit(positions)
        n_clusters = len(set(clustering.labels_)) - (1 if -1 in clustering.labels_ else 0)
        n_noise = list(clustering.labels_).count(-1)
        
        # Unusual clustering patterns might indicate suspicious behavior
        if n_clusters > 3 or n_noise > len(positions) * 0.3:
            confidence = min((n_clusters / 3.0) + (n_noise / len(positions)), 1.0)
            return (AnomalyType.SUSPICIOUS_BEHAVIOR, confidence)
        
        return None
    
    def _analyze_temporal_pattern(self, metrics: QueueMetrics) -> Optional[Tuple[AnomalyType, float]]:
        """Analyze temporal patterns for anomalies"""
        pattern = np.array(metrics.temporal_pattern)
        
        if len(pattern) < 5:
            return None
        
        # Check for unusual oscillations or spikes
        pattern_variance = np.var(pattern)
        pattern_mean = np.mean(pattern)
        
        if pattern_variance > pattern_mean * 2:
            confidence = min(pattern_variance / (pattern_mean * 2), 1.0)
            return (AnomalyType.TRAFFIC_FLOW, confidence)
        
        return None
    
    def _analyze_formation_pattern(self, metrics: QueueMetrics) -> Optional[Tuple[AnomalyType, float]]:
        """Analyze queue formation patterns"""
        # Check for rapid formation or dissolution
        if metrics.formation_rate > 2.0:  # Very rapid formation
            confidence = min(metrics.formation_rate / 2.0, 1.0)
            return (AnomalyType.QUEUE_FORMATION, confidence)
        
        # Check for unusual abandonment patterns
        if metrics.abandonment_rate > 0.5:  # High abandonment rate
            confidence = min(metrics.abandonment_rate, 1.0)
            return (AnomalyType.ABANDONMENT_PATTERN, confidence)
        
        return None

class QueueAnomalyDetector:
    """Main queue anomaly detection system"""
    
    def __init__(self, 
                 statistical_sensitivity: float = 2.5,
                 ml_contamination: float = 0.1,
                 enable_ml: bool = True):
        self.statistical_detector = StatisticalAnomalyDetector(sensitivity=statistical_sensitivity)
        self.ml_detector = MLAnomalyDetector(contamination=ml_contamination) if enable_ml else None
        self.behavior_detector = BehaviorPatternDetector()
        
        self.anomaly_counter = 0
        self.detection_history = []
        
        # Thresholds for severity classification
        self.severity_thresholds = {
            AnomalySeverity.LOW: 0.3,
            AnomalySeverity.MEDIUM: 0.6,
            AnomalySeverity.HIGH: 0.8,
            AnomalySeverity.CRITICAL: 0.95
        }
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def train_ml_detector(self, historical_metrics: List[QueueMetrics]) -> bool:
        """Train the ML anomaly detector"""
        if self.ml_detector:
            return self.ml_detector.train(historical_metrics)
        return False
    
    def detect_anomalies(self, metrics: QueueMetrics) -> List[QueueAnomaly]:
        """Detect all types of anomalies in queue metrics"""
        all_anomalies = []
        
        # Statistical anomaly detection
        statistical_anomalies = self.statistical_detector.detect_statistical_anomalies(metrics)
        
        # ML-based anomaly detection
        ml_anomalies = []
        if self.ml_detector:
            ml_anomalies = self.ml_detector.detect_ml_anomalies(metrics)
        
        # Behavior pattern anomaly detection
        behavior_anomalies = self.behavior_detector.detect_behavior_anomalies(metrics)
        
        # Combine and process all detected anomalies
        combined_anomalies = statistical_anomalies + ml_anomalies + behavior_anomalies
        
        # Remove duplicates and consolidate
        anomaly_dict = {}
        for anomaly_type, confidence in combined_anomalies:
            if anomaly_type in anomaly_dict:
                # Take the higher confidence score
                anomaly_dict[anomaly_type] = max(anomaly_dict[anomaly_type], confidence)
            else:
                anomaly_dict[anomaly_type] = confidence
        
        # Create QueueAnomaly objects
        for anomaly_type, confidence in anomaly_dict.items():
            severity = self._determine_severity(confidence)
            
            anomaly = QueueAnomaly(
                id=f"anomaly_{self.anomaly_counter}",
                type=anomaly_type,
                severity=severity,
                confidence=confidence,
                timestamp=metrics.timestamp,
                location=(0.0, 0.0),  # Would be derived from queue location
                description=self._generate_description(anomaly_type, metrics),
                affected_queue_ids=[metrics.queue_id],
                metrics=self._extract_relevant_metrics(anomaly_type, metrics),
                recommendations=self._generate_recommendations(anomaly_type, severity)
            )
            
            all_anomalies.append(anomaly)
            self.anomaly_counter += 1
        
        # Store detection history
        self.detection_history.append({
            'timestamp': metrics.timestamp,
            'queue_id': metrics.queue_id,
            'anomalies_detected': len(all_anomalies),
            'anomaly_types': [a.type.value for a in all_anomalies]
        })
        
        # Keep history limited
        if len(self.detection_history) > 1000:
            self.detection_history.pop(0)
        
        return all_anomalies
    
    def _determine_severity(self, confidence: float) -> AnomalySeverity:
        """Determine anomaly severity based on confidence"""
        if confidence >= self.severity_thresholds[AnomalySeverity.CRITICAL]:
            return AnomalySeverity.CRITICAL
        elif confidence >= self.severity_thresholds[AnomalySeverity.HIGH]:
            return AnomalySeverity.HIGH
        elif confidence >= self.severity_thresholds[AnomalySeverity.MEDIUM]:
            return AnomalySeverity.MEDIUM
        else:
            return AnomalySeverity.LOW
    
    def _generate_description(self, anomaly_type: AnomalyType, metrics: QueueMetrics) -> str:
        """Generate human-readable description for anomaly"""
        descriptions = {
            AnomalyType.OVERCROWDING: f"Queue overcrowding detected with length {metrics.length:.1f} and density {metrics.density:.2f}",
            AnomalyType.ABNORMAL_WAIT_TIME: f"Abnormal wait time of {metrics.wait_time:.1f} seconds detected",
            AnomalyType.SUSPICIOUS_BEHAVIOR: f"Suspicious behavior pattern detected with unusual spatial distribution",
            AnomalyType.QUEUE_FORMATION: f"Unusual queue formation rate of {metrics.formation_rate:.2f}",
            AnomalyType.TRAFFIC_FLOW: f"Traffic flow irregularity detected with movement speed {metrics.movement_speed:.2f}",
            AnomalyType.DENSITY_SPIKE: f"Queue density spike detected at {metrics.density:.2f}",
            AnomalyType.ABANDONMENT_PATTERN: f"High abandonment rate of {metrics.abandonment_rate:.2f} detected",
            AnomalyType.BOTTLENECK: f"Queue bottleneck detected with slow movement speed {metrics.movement_speed:.2f}"
        }
        
        return descriptions.get(anomaly_type, f"Anomaly of type {anomaly_type.value} detected")
    
    def _extract_relevant_metrics(self, anomaly_type: AnomalyType, metrics: QueueMetrics) -> Dict[str, float]:
        """Extract relevant metrics for the anomaly type"""
        base_metrics = {
            'queue_length': metrics.length,
            'wait_time': metrics.wait_time,
            'density': metrics.density
        }
        
        if anomaly_type == AnomalyType.OVERCROWDING:
            base_metrics.update({
                'formation_rate': metrics.formation_rate,
                'interaction_count': metrics.interaction_count
            })
        elif anomaly_type == AnomalyType.ABNORMAL_WAIT_TIME:
            base_metrics.update({
                'movement_speed': metrics.movement_speed,
                'abandonment_rate': metrics.abandonment_rate
            })
        elif anomaly_type in [AnomalyType.TRAFFIC_FLOW, AnomalyType.BOTTLENECK]:
            base_metrics.update({
                'movement_speed': metrics.movement_speed,
                'formation_rate': metrics.formation_rate
            })
        
        return base_metrics
    
    def _generate_recommendations(self, anomaly_type: AnomalyType, severity: AnomalySeverity) -> List[str]:
        """Generate recommendations based on anomaly type and severity"""
        recommendations = {
            AnomalyType.OVERCROWDING: [
                "Deploy additional service points",
                "Implement crowd control measures",
                "Consider queue management system",
                "Alert facility management"
            ],
            AnomalyType.ABNORMAL_WAIT_TIME: [
                "Optimize service efficiency",
                "Add temporary service staff",
                "Investigate service bottlenecks",
                "Implement priority queuing"
            ],
            AnomalyType.SUSPICIOUS_BEHAVIOR: [
                "Increase security monitoring",
                "Deploy security personnel",
                "Review CCTV footage",
                "Alert security team"
            ],
            AnomalyType.QUEUE_FORMATION: [
                "Monitor queue entry points",
                "Implement queue guidance systems",
                "Review facility layout",
                "Consider entry flow control"
            ],
            AnomalyType.TRAFFIC_FLOW: [
                "Optimize traffic signal timing",
                "Deploy traffic management personnel",
                "Review traffic flow patterns",
                "Consider alternative routing"
            ],
            AnomalyType.DENSITY_SPIKE: [
                "Implement immediate crowd dispersal",
                "Increase monitoring frequency",
                "Deploy emergency protocols",
                "Alert emergency services"
            ],
            AnomalyType.ABANDONMENT_PATTERN: [
                "Investigate service quality issues",
                "Improve queue information systems",
                "Review service wait times",
                "Implement customer feedback system"
            ],
            AnomalyType.BOTTLENECK: [
                "Identify and resolve bottleneck points",
                "Optimize service flow",
                "Add service capacity",
                "Review facility design"
            ]
        }
        
        base_recommendations = recommendations.get(anomaly_type, ["Monitor situation closely"])
        
        # Add severity-specific recommendations
        if severity in [AnomalySeverity.HIGH, AnomalySeverity.CRITICAL]:
            base_recommendations.extend([
                "Implement immediate intervention",
                "Escalate to management",
                "Consider emergency protocols"
            ])
        
        return base_recommendations[:4]  # Limit to top 4 recommendations
    
    def get_detection_statistics(self) -> Dict[str, Any]:
        """Get statistics about anomaly detection performance"""
        if not self.detection_history:
            return {}
        
        total_detections = sum(d['anomalies_detected'] for d in self.detection_history)
        anomaly_types_count = {}
        
        for detection in self.detection_history:
            for anomaly_type in detection['anomaly_types']:
                anomaly_types_count[anomaly_type] = anomaly_types_count.get(anomaly_type, 0) + 1
        
        return {
            'total_detections': total_detections,
            'detection_sessions': len(self.detection_history),
            'average_anomalies_per_session': total_detections / len(self.detection_history) if self.detection_history else 0,
            'anomaly_type_distribution': anomaly_types_count,
            'most_common_anomaly': max(anomaly_types_count.items(), key=lambda x: x[1])[0] if anomaly_types_count else None
        }