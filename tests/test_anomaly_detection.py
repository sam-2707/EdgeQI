"""
Test suite for Queue Anomaly Detection System

Comprehensive tests for anomaly detection capabilities including
statistical methods, machine learning algorithms, behavior pattern
analysis, and integration with queue detection systems.
"""

import pytest
import numpy as np
import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from typing import List

from Core.anomaly.queue_anomaly_detector import (
    QueueAnomalyDetector, QueueMetrics, QueueAnomaly, AnomalyType, AnomalySeverity,
    StatisticalAnomalyDetector, MLAnomalyDetector, BehaviorPatternDetector
)
from Core.anomaly.anomaly_integration import (
    QueueAnomalyIntegrator, AnomalyAlertManager, QueueData, create_default_anomaly_callback
)

class TestQueueMetrics:
    """Test QueueMetrics data structure"""
    
    def test_queue_metrics_creation(self):
        """Test QueueMetrics object creation"""
        metrics = QueueMetrics(
            queue_id="test_queue",
            timestamp=datetime.now(),
            length=15.5,
            wait_time=120.0,
            density=0.75,
            movement_speed=1.2,
            formation_rate=0.8,
            abandonment_rate=0.1,
            spatial_distribution=[(100, 200), (150, 220)],
            temporal_pattern=[1.0, 1.2, 1.1, 0.9],
            interaction_count=12
        )
        
        assert metrics.queue_id == "test_queue"
        assert metrics.length == 15.5
        assert metrics.wait_time == 120.0
        assert metrics.density == 0.75
        assert len(metrics.spatial_distribution) == 2
        assert len(metrics.temporal_pattern) == 4
        assert metrics.interaction_count == 12

class TestQueueAnomaly:
    """Test QueueAnomaly data structure"""
    
    def test_queue_anomaly_creation(self):
        """Test QueueAnomaly object creation"""
        anomaly = QueueAnomaly(
            id="anomaly_001",
            type=AnomalyType.OVERCROWDING,
            severity=AnomalySeverity.HIGH,
            confidence=0.85,
            timestamp=datetime.now(),
            location=(100.0, 200.0),
            description="Test anomaly",
            affected_queue_ids=["queue_1", "queue_2"],
            metrics={"length": 25.0, "density": 0.9},
            recommendations=["Add service points", "Deploy staff"]
        )
        
        assert anomaly.id == "anomaly_001"
        assert anomaly.type == AnomalyType.OVERCROWDING
        assert anomaly.severity == AnomalySeverity.HIGH
        assert anomaly.confidence == 0.85
        assert len(anomaly.affected_queue_ids) == 2
        assert len(anomaly.recommendations) == 2
    
    def test_anomaly_to_dict(self):
        """Test anomaly conversion to dictionary"""
        anomaly = QueueAnomaly(
            id="anomaly_001",
            type=AnomalyType.OVERCROWDING,
            severity=AnomalySeverity.HIGH,
            confidence=0.85,
            timestamp=datetime.now(),
            location=(100.0, 200.0),
            description="Test anomaly",
            affected_queue_ids=["queue_1"],
            metrics={"length": 25.0},
            recommendations=["Test recommendation"]
        )
        
        anomaly_dict = anomaly.to_dict()
        
        assert anomaly_dict['id'] == "anomaly_001"
        assert anomaly_dict['type'] == "overcrowding"
        assert anomaly_dict['severity'] == "high"
        assert anomaly_dict['confidence'] == 0.85
        assert isinstance(anomaly_dict['timestamp'], str)
        assert anomaly_dict['location'] == (100.0, 200.0)

class TestStatisticalAnomalyDetector:
    """Test statistical anomaly detection methods"""
    
    def test_statistical_detector_initialization(self):
        """Test statistical detector initialization"""
        detector = StatisticalAnomalyDetector(window_size=30, sensitivity=2.0)
        
        assert detector.window_size == 30
        assert detector.sensitivity == 2.0
        assert detector.historical_data == {}
    
    def test_statistical_anomaly_detection_insufficient_data(self):
        """Test statistical detection with insufficient historical data"""
        detector = StatisticalAnomalyDetector(window_size=50)
        
        metrics = QueueMetrics(
            queue_id="test_queue",
            timestamp=datetime.now(),
            length=15.0,
            wait_time=120.0,
            density=0.75,
            movement_speed=1.0,
            formation_rate=0.5,
            abandonment_rate=0.1,
            spatial_distribution=[],
            temporal_pattern=[],
            interaction_count=10
        )
        
        anomalies = detector.detect_statistical_anomalies(metrics)
        assert len(anomalies) == 0  # Not enough historical data
    
    def test_statistical_anomaly_detection_with_data(self):
        """Test statistical detection with sufficient historical data"""
        detector = StatisticalAnomalyDetector(window_size=10, sensitivity=2.0)
        
        # Create normal baseline data
        normal_metrics = []
        for i in range(15):
            metrics = QueueMetrics(
                queue_id="test_queue",
                timestamp=datetime.now(),
                length=10.0 + np.random.normal(0, 1),  # Normal around 10
                wait_time=100.0 + np.random.normal(0, 10),  # Normal around 100
                density=0.5 + np.random.normal(0, 0.1),  # Normal around 0.5
                movement_speed=1.0,
                formation_rate=0.5,
                abandonment_rate=0.1,
                spatial_distribution=[],
                temporal_pattern=[],
                interaction_count=10
            )
            normal_metrics.append(metrics)
            detector.detect_statistical_anomalies(metrics)
        
        # Create anomalous data
        anomalous_metrics = QueueMetrics(
            queue_id="test_queue",
            timestamp=datetime.now(),
            length=25.0,  # Significantly higher than normal
            wait_time=300.0,  # Significantly higher than normal
            density=0.95,  # Significantly higher than normal
            movement_speed=1.0,
            formation_rate=0.5,
            abandonment_rate=0.5,  # Higher abandonment
            spatial_distribution=[],
            temporal_pattern=[],
            interaction_count=10
        )
        
        anomalies = detector.detect_statistical_anomalies(anomalous_metrics)
        
        # Should detect multiple anomalies
        assert len(anomalies) > 0
        anomaly_types = [a[0] for a in anomalies]
        assert AnomalyType.OVERCROWDING in anomaly_types

class TestMLAnomalyDetector:
    """Test machine learning anomaly detection"""
    
    def test_ml_detector_initialization(self):
        """Test ML detector initialization"""
        detector = MLAnomalyDetector(contamination=0.1)
        
        assert detector.contamination == 0.1
        assert not detector.is_trained
        assert detector.feature_history == []
    
    def test_prepare_features(self):
        """Test feature preparation from metrics"""
        detector = MLAnomalyDetector()
        
        metrics = QueueMetrics(
            queue_id="test_queue",
            timestamp=datetime.now(),
            length=15.0,
            wait_time=120.0,
            density=0.75,
            movement_speed=1.2,
            formation_rate=0.8,
            abandonment_rate=0.1,
            spatial_distribution=[(100, 200), (150, 220)],
            temporal_pattern=[1.0, 1.2, 1.1, 0.9],
            interaction_count=12
        )
        
        features = detector.prepare_features(metrics)
        
        assert features.shape == (1, 10)  # 10 features
        assert features[0, 0] == 15.0  # length
        assert features[0, 1] == 120.0  # wait_time
        assert features[0, 2] == 0.75  # density
    
    def test_ml_training_insufficient_data(self):
        """Test ML training with insufficient data"""
        detector = MLAnomalyDetector()
        
        # Create small dataset
        metrics_list = []
        for i in range(10):  # Less than required 50
            metrics = QueueMetrics(
                queue_id=f"queue_{i}",
                timestamp=datetime.now(),
                length=10.0,
                wait_time=100.0,
                density=0.5,
                movement_speed=1.0,
                formation_rate=0.5,
                abandonment_rate=0.1,
                spatial_distribution=[],
                temporal_pattern=[],
                interaction_count=10
            )
            metrics_list.append(metrics)
        
        result = detector.train(metrics_list)
        
        assert not result
        assert not detector.is_trained
    
    def test_ml_training_sufficient_data(self):
        """Test ML training with sufficient data"""
        detector = MLAnomalyDetector()
        
        # Create sufficient dataset
        metrics_list = []
        for i in range(60):  # More than required 50
            metrics = QueueMetrics(
                queue_id=f"queue_{i}",
                timestamp=datetime.now(),
                length=10.0 + np.random.normal(0, 2),
                wait_time=100.0 + np.random.normal(0, 20),
                density=0.5 + np.random.normal(0, 0.1),
                movement_speed=1.0 + np.random.normal(0, 0.2),
                formation_rate=0.5 + np.random.normal(0, 0.1),
                abandonment_rate=0.1 + np.random.normal(0, 0.05),
                spatial_distribution=[],
                temporal_pattern=[],
                interaction_count=10
            )
            metrics_list.append(metrics)
        
        result = detector.train(metrics_list)
        
        assert result
        assert detector.is_trained
    
    def test_ml_anomaly_detection_untrained(self):
        """Test ML detection without training"""
        detector = MLAnomalyDetector()
        
        metrics = QueueMetrics(
            queue_id="test_queue",
            timestamp=datetime.now(),
            length=15.0,
            wait_time=120.0,
            density=0.75,
            movement_speed=1.0,
            formation_rate=0.5,
            abandonment_rate=0.1,
            spatial_distribution=[],
            temporal_pattern=[],
            interaction_count=10
        )
        
        anomalies = detector.detect_ml_anomalies(metrics)
        
        assert len(anomalies) == 0  # Should return empty list when not trained

class TestBehaviorPatternDetector:
    """Test behavior pattern anomaly detection"""
    
    def test_behavior_detector_initialization(self):
        """Test behavior detector initialization"""
        detector = BehaviorPatternDetector()
        
        assert detector.behavior_history == {}
        assert detector.pattern_threshold == 0.7
    
    def test_spatial_pattern_analysis(self):
        """Test spatial pattern anomaly detection"""
        detector = BehaviorPatternDetector()
        
        # Create metrics with clustered spatial distribution
        clustered_positions = [(100, 100), (102, 101), (300, 300), (302, 301), (500, 500)]
        
        metrics = QueueMetrics(
            queue_id="test_queue",
            timestamp=datetime.now(),
            length=15.0,
            wait_time=120.0,
            density=0.75,
            movement_speed=1.0,
            formation_rate=0.5,
            abandonment_rate=0.1,
            spatial_distribution=clustered_positions,
            temporal_pattern=[],
            interaction_count=5
        )
        
        anomalies = detector.detect_behavior_anomalies(metrics)
        
        # May detect spatial clustering as suspicious behavior
        assert isinstance(anomalies, list)
    
    def test_temporal_pattern_analysis(self):
        """Test temporal pattern anomaly detection"""
        detector = BehaviorPatternDetector()
        
        # Create metrics with highly variable temporal pattern
        variable_pattern = [1.0, 5.0, 0.5, 8.0, 0.2, 10.0]
        
        metrics = QueueMetrics(
            queue_id="test_queue",
            timestamp=datetime.now(),
            length=15.0,
            wait_time=120.0,
            density=0.75,
            movement_speed=1.0,
            formation_rate=0.5,
            abandonment_rate=0.1,
            spatial_distribution=[],
            temporal_pattern=variable_pattern,
            interaction_count=10
        )
        
        anomalies = detector.detect_behavior_anomalies(metrics)
        
        # Should detect temporal variability
        assert isinstance(anomalies, list)
    
    def test_formation_pattern_analysis(self):
        """Test queue formation pattern analysis"""
        detector = BehaviorPatternDetector()
        
        # Create metrics with rapid formation
        metrics = QueueMetrics(
            queue_id="test_queue",
            timestamp=datetime.now(),
            length=15.0,
            wait_time=120.0,
            density=0.75,
            movement_speed=1.0,
            formation_rate=3.0,  # Very rapid formation
            abandonment_rate=0.1,
            spatial_distribution=[],
            temporal_pattern=[],
            interaction_count=10
        )
        
        anomalies = detector.detect_behavior_anomalies(metrics)
        
        # Should detect rapid formation anomaly
        anomaly_types = [a[0] for a in anomalies]
        assert AnomalyType.QUEUE_FORMATION in anomaly_types

class TestQueueAnomalyDetector:
    """Test main queue anomaly detection system"""
    
    def test_detector_initialization(self):
        """Test detector initialization"""
        detector = QueueAnomalyDetector()
        
        assert detector.statistical_detector is not None
        assert detector.ml_detector is not None
        assert detector.behavior_detector is not None
        assert detector.anomaly_counter == 0
        assert detector.detection_history == []
    
    def test_detector_initialization_no_ml(self):
        """Test detector initialization without ML"""
        detector = QueueAnomalyDetector(enable_ml=False)
        
        assert detector.statistical_detector is not None
        assert detector.ml_detector is None
        assert detector.behavior_detector is not None
    
    def test_severity_determination(self):
        """Test anomaly severity determination"""
        detector = QueueAnomalyDetector()
        
        assert detector._determine_severity(0.2) == AnomalySeverity.LOW
        assert detector._determine_severity(0.5) == AnomalySeverity.LOW  # Below 0.6 threshold
        assert detector._determine_severity(0.7) == AnomalySeverity.MEDIUM  # Above 0.6 threshold
        assert detector._determine_severity(0.85) == AnomalySeverity.HIGH  # Above 0.8 threshold
        assert detector._determine_severity(0.98) == AnomalySeverity.CRITICAL  # Above 0.95 threshold
    
    def test_description_generation(self):
        """Test anomaly description generation"""
        detector = QueueAnomalyDetector()
        
        metrics = QueueMetrics(
            queue_id="test_queue",
            timestamp=datetime.now(),
            length=15.0,
            wait_time=120.0,
            density=0.75,
            movement_speed=1.0,
            formation_rate=0.5,
            abandonment_rate=0.1,
            spatial_distribution=[],
            temporal_pattern=[],
            interaction_count=10
        )
        
        description = detector._generate_description(AnomalyType.OVERCROWDING, metrics)
        
        assert "overcrowding" in description.lower()
        assert "15.0" in description
        assert "0.75" in description
    
    def test_recommendations_generation(self):
        """Test anomaly recommendations generation"""
        detector = QueueAnomalyDetector()
        
        recommendations = detector._generate_recommendations(
            AnomalyType.OVERCROWDING, 
            AnomalySeverity.HIGH
        )
        
        assert len(recommendations) <= 4
        assert any("service" in rec.lower() for rec in recommendations)
    
    def test_anomaly_detection_integration(self):
        """Test integrated anomaly detection"""
        detector = QueueAnomalyDetector()
        
        metrics = QueueMetrics(
            queue_id="test_queue",
            timestamp=datetime.now(),
            length=15.0,
            wait_time=120.0,
            density=0.75,
            movement_speed=1.0,
            formation_rate=0.5,
            abandonment_rate=0.1,
            spatial_distribution=[],
            temporal_pattern=[],
            interaction_count=10
        )
        
        anomalies = detector.detect_anomalies(metrics)
        
        # Should return list of anomalies (may be empty for normal data)
        assert isinstance(anomalies, list)
        assert detector.anomaly_counter >= 0
        assert len(detector.detection_history) > 0
    
    def test_detection_statistics(self):
        """Test detection statistics collection"""
        detector = QueueAnomalyDetector()
        
        # Process some metrics
        for i in range(5):
            metrics = QueueMetrics(
                queue_id=f"queue_{i}",
                timestamp=datetime.now(),
                length=15.0,
                wait_time=120.0,
                density=0.75,
                movement_speed=1.0,
                formation_rate=0.5,
                abandonment_rate=0.1,
                spatial_distribution=[],
                temporal_pattern=[],
                interaction_count=10
            )
            detector.detect_anomalies(metrics)
        
        stats = detector.get_detection_statistics()
        
        assert 'detection_sessions' in stats
        assert stats['detection_sessions'] == 5

class TestQueueAnomalyIntegrator:
    """Test anomaly integration with queue detection"""
    
    def test_integrator_initialization(self):
        """Test integrator initialization"""
        integrator = QueueAnomalyIntegrator()
        
        assert integrator.anomaly_detector is not None
        assert integrator.queue_history == {}
        assert integrator.anomaly_callbacks == []
        assert not integrator.ml_trained
    
    def test_callback_registration(self):
        """Test callback registration"""
        integrator = QueueAnomalyIntegrator()
        
        callback = Mock()
        integrator.register_anomaly_callback(callback)
        
        assert len(integrator.anomaly_callbacks) == 1
        assert callback in integrator.anomaly_callbacks
    
    def test_queue_data_conversion(self):
        """Test QueueData to QueueMetrics conversion"""
        integrator = QueueAnomalyIntegrator()
        
        # Create mock QueueData
        queue_data = Mock(spec=QueueData)
        queue_data.queue_id = "test_queue"
        queue_data.timestamp = time.time()
        queue_data.queue_length = 15.0
        queue_data.estimated_wait_time = 120.0
        queue_data.queue_density = 0.75
        queue_data.trajectory_points = None  # Explicitly set to None
        queue_data.historical_lengths = None
        queue_data.average_speed = None
        queue_data.length_change_rate = None
        queue_data.abandonment_rate = None
        queue_data.object_count = None
        
        metrics = integrator._convert_to_metrics(queue_data)
        
        assert metrics.queue_id == "test_queue"
        assert metrics.length == 15.0
        assert metrics.wait_time == 120.0
        assert metrics.density == 0.75
        assert metrics.spatial_distribution == []  # Should be empty when trajectory_points is None
    
    def test_historical_data_storage(self):
        """Test historical data storage and management"""
        integrator = QueueAnomalyIntegrator(training_window=5)
        
        # Add data beyond training window
        for i in range(10):
            metrics = QueueMetrics(
                queue_id="test_queue",
                timestamp=datetime.now(),
                length=15.0,
                wait_time=120.0,
                density=0.75,
                movement_speed=1.0,
                formation_rate=0.5,
                abandonment_rate=0.1,
                spatial_distribution=[],
                temporal_pattern=[],
                interaction_count=10
            )
            integrator._store_historical_data(metrics)
        
        # Should maintain only training_window samples
        assert len(integrator.queue_history["test_queue"]) == 5
    
    def test_ml_training_trigger(self):
        """Test ML training trigger conditions"""
        integrator = QueueAnomalyIntegrator(training_window=60)
        integrator.min_training_samples = 10
        
        # Add insufficient data
        for i in range(5):
            metrics = QueueMetrics(
                queue_id="test_queue",
                timestamp=datetime.now(),
                length=15.0,
                wait_time=120.0,
                density=0.75,
                movement_speed=1.0,
                formation_rate=0.5,
                abandonment_rate=0.1,
                spatial_distribution=[],
                temporal_pattern=[],
                interaction_count=10
            )
            integrator._store_historical_data(metrics)
        
        assert not integrator._should_train_ml()
        
        # Add sufficient data
        for i in range(10):
            metrics = QueueMetrics(
                queue_id=f"queue_{i}",
                timestamp=datetime.now(),
                length=15.0,
                wait_time=120.0,
                density=0.75,
                movement_speed=1.0,
                formation_rate=0.5,
                abandonment_rate=0.1,
                spatial_distribution=[],
                temporal_pattern=[],
                interaction_count=10
            )
            integrator._store_historical_data(metrics)
        
        assert integrator._should_train_ml()

class TestAnomalyAlertManager:
    """Test anomaly alert management"""
    
    def test_alert_manager_initialization(self):
        """Test alert manager initialization"""
        manager = AnomalyAlertManager()
        
        assert manager.alert_threshold == AnomalySeverity.MEDIUM
        assert manager.active_alerts == {}
        assert manager.alert_history == []
        assert manager.suppression_window == 300
    
    def test_alert_threshold_filtering(self):
        """Test alert filtering based on severity threshold"""
        manager = AnomalyAlertManager(alert_threshold=AnomalySeverity.HIGH)
        
        # Create low severity anomaly
        low_anomaly = QueueAnomaly(
            id="anomaly_001",
            type=AnomalyType.OVERCROWDING,
            severity=AnomalySeverity.LOW,
            confidence=0.4,
            timestamp=datetime.now(),
            location=(100.0, 200.0),
            description="Low severity anomaly",
            affected_queue_ids=["queue_1"],
            metrics={}
        )
        
        # Should not trigger alert
        result = manager.process_anomaly(low_anomaly)
        assert not result
        
        # Create high severity anomaly
        high_anomaly = QueueAnomaly(
            id="anomaly_002",
            type=AnomalyType.OVERCROWDING,
            severity=AnomalySeverity.HIGH,
            confidence=0.85,
            timestamp=datetime.now(),
            location=(100.0, 200.0),
            description="High severity anomaly",
            affected_queue_ids=["queue_1"],
            metrics={}
        )
        
        # Should trigger alert
        result = manager.process_anomaly(high_anomaly)
        assert result
    
    def test_alert_suppression(self):
        """Test alert suppression to prevent spam"""
        manager = AnomalyAlertManager(alert_threshold=AnomalySeverity.LOW)
        manager.suppression_window = 60  # 1 minute
        
        # Create similar anomalies
        anomaly1 = QueueAnomaly(
            id="anomaly_001",
            type=AnomalyType.OVERCROWDING,
            severity=AnomalySeverity.MEDIUM,
            confidence=0.6,
            timestamp=datetime.now(),
            location=(100.0, 200.0),
            description="First anomaly",
            affected_queue_ids=["queue_1"],
            metrics={}
        )
        
        anomaly2 = QueueAnomaly(
            id="anomaly_002",
            type=AnomalyType.OVERCROWDING,
            severity=AnomalySeverity.MEDIUM,
            confidence=0.7,
            timestamp=datetime.now(),
            location=(100.0, 200.0),
            description="Second anomaly",
            affected_queue_ids=["queue_1"],
            metrics={}
        )
        
        # First should trigger
        result1 = manager.process_anomaly(anomaly1)
        assert result1
        
        # Second should be suppressed
        result2 = manager.process_anomaly(anomaly2)
        assert not result2
    
    def test_active_alerts_retrieval(self):
        """Test active alerts retrieval"""
        manager = AnomalyAlertManager()
        
        # Trigger some alerts
        anomaly = QueueAnomaly(
            id="anomaly_001",
            type=AnomalyType.OVERCROWDING,
            severity=AnomalySeverity.HIGH,
            confidence=0.85,
            timestamp=datetime.now(),
            location=(100.0, 200.0),
            description="Test anomaly",
            affected_queue_ids=["queue_1"],
            metrics={}
        )
        
        manager.process_anomaly(anomaly)
        
        active_alerts = manager.get_active_alerts()
        
        assert len(active_alerts) == 1
        assert active_alerts[0]['anomaly_id'] == "anomaly_001"
    
    def test_alert_clearing(self):
        """Test alert clearing functionality"""
        manager = AnomalyAlertManager()
        
        # Add some alerts
        manager.active_alerts = {
            "overcrowding_queue_1": time.time(),
            "traffic_flow_queue_2": time.time()
        }
        
        # Clear specific type
        manager.clear_alerts(AnomalyType.OVERCROWDING)
        
        assert "overcrowding_queue_1" not in manager.active_alerts
        assert "traffic_flow_queue_2" in manager.active_alerts
        
        # Clear all
        manager.clear_alerts()
        
        assert len(manager.active_alerts) == 0

class TestAnomalyCallbacks:
    """Test anomaly callback functionality"""
    
    def test_default_callback_creation(self):
        """Test default callback creation"""
        alert_manager = AnomalyAlertManager()
        callback = create_default_anomaly_callback(alert_manager)
        
        assert callable(callback)
        
        # Test callback execution
        anomaly = QueueAnomaly(
            id="anomaly_001",
            type=AnomalyType.OVERCROWDING,
            severity=AnomalySeverity.HIGH,
            confidence=0.85,
            timestamp=datetime.now(),
            location=(100.0, 200.0),
            description="Test anomaly",
            affected_queue_ids=["queue_1"],
            metrics={}
        )
        
        # Should not raise exception
        callback(anomaly)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])