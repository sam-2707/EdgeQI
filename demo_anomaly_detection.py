"""
EDGE-QI Anomaly Detection Demo

Demonstration script showing queue anomaly detection capabilities
including statistical, ML-based, and behavioral pattern analysis.
"""

import time
import random
import numpy as np
from datetime import datetime, timedelta
from typing import List

from Core.anomaly import (
    QueueAnomalyDetector, QueueAnomalyIntegrator, AnomalyAlertManager,
    QueueMetrics, QueueData, AnomalyType, AnomalySeverity,
    create_default_anomaly_callback
)

def generate_normal_queue_data(queue_id: str, base_time: float) -> QueueData:
    """Generate normal queue data for baseline"""
    return QueueData(
        queue_id=queue_id,
        timestamp=base_time,
        queue_length=random.uniform(8, 15),
        estimated_wait_time=random.uniform(60, 180),
        queue_density=random.uniform(0.3, 0.7),
        trajectory_points=None,
        historical_lengths=[random.uniform(8, 15) for _ in range(10)],
        average_speed=random.uniform(0.8, 1.5),
        length_change_rate=random.uniform(0.3, 0.8),
        abandonment_rate=random.uniform(0.05, 0.15),
        object_count=random.randint(8, 15)
    )

def generate_anomalous_queue_data(queue_id: str, base_time: float, anomaly_type: str) -> QueueData:
    """Generate anomalous queue data for testing"""
    if anomaly_type == "overcrowding":
        return QueueData(
            queue_id=queue_id,
            timestamp=base_time,
            queue_length=random.uniform(30, 50),  # Much longer queue
            estimated_wait_time=random.uniform(400, 800),  # Much longer wait
            queue_density=random.uniform(0.8, 1.0),  # High density
            trajectory_points=None,
            historical_lengths=[random.uniform(8, 15) for _ in range(10)],
            average_speed=random.uniform(0.1, 0.3),  # Slow movement
            length_change_rate=random.uniform(2.0, 4.0),  # Rapid formation
            abandonment_rate=random.uniform(0.05, 0.15),
            object_count=random.randint(30, 50)
        )
    
    elif anomaly_type == "abandonment":
        return QueueData(
            queue_id=queue_id,
            timestamp=base_time,
            queue_length=random.uniform(10, 20),
            estimated_wait_time=random.uniform(300, 600),  # Long wait time
            queue_density=random.uniform(0.4, 0.8),
            trajectory_points=None,
            historical_lengths=[random.uniform(8, 15) for _ in range(10)],
            average_speed=random.uniform(0.5, 1.0),
            length_change_rate=random.uniform(0.3, 0.8),
            abandonment_rate=random.uniform(0.6, 0.9),  # High abandonment
            object_count=random.randint(10, 20)
        )
    
    elif anomaly_type == "bottleneck":
        return QueueData(
            queue_id=queue_id,
            timestamp=base_time,
            queue_length=random.uniform(15, 25),
            estimated_wait_time=random.uniform(200, 400),
            queue_density=random.uniform(0.6, 0.9),
            trajectory_points=None,
            historical_lengths=[random.uniform(8, 15) for _ in range(10)],
            average_speed=random.uniform(0.05, 0.1),  # Very slow movement
            length_change_rate=random.uniform(0.1, 0.3),  # Slow formation
            abandonment_rate=random.uniform(0.2, 0.4),
            object_count=random.randint(15, 25)
        )
    
    else:  # Default to normal data
        return generate_normal_queue_data(queue_id, base_time)

def demo_statistical_detection():
    """Demonstrate statistical anomaly detection"""
    print("\n" + "="*60)
    print("STATISTICAL ANOMALY DETECTION DEMO")
    print("="*60)
    
    detector = QueueAnomalyDetector(enable_ml=False)
    
    print("🔍 Training with normal queue data...")
    
    # Generate baseline normal data
    base_time = time.time()
    for i in range(30):  # Generate enough baseline data
        queue_data = generate_normal_queue_data("demo_queue_1", base_time + i)
        metrics = QueueMetrics(
            queue_id=queue_data.queue_id,
            timestamp=datetime.fromtimestamp(queue_data.timestamp),
            length=queue_data.queue_length,
            wait_time=queue_data.estimated_wait_time,
            density=queue_data.queue_density,
            movement_speed=queue_data.average_speed or 1.0,
            formation_rate=queue_data.length_change_rate or 0.5,
            abandonment_rate=queue_data.abandonment_rate or 0.1,
            spatial_distribution=[],
            temporal_pattern=queue_data.historical_lengths or [],
            interaction_count=queue_data.object_count or 10
        )
        
        anomalies = detector.detect_anomalies(metrics)
        if i % 10 == 0:
            print(f"   Processed {i+1}/30 baseline samples...")
    
    print("✅ Baseline established")
    
    # Test with anomalous data
    print("\n🚨 Testing with anomalous queue data...")
    
    anomaly_types = ["overcrowding", "abandonment", "bottleneck"]
    
    for anomaly_type in anomaly_types:
        print(f"\n--- Testing {anomaly_type.upper()} ---")
        
        anomalous_data = generate_anomalous_queue_data("demo_queue_1", time.time(), anomaly_type)
        metrics = QueueMetrics(
            queue_id=anomalous_data.queue_id,
            timestamp=datetime.fromtimestamp(anomalous_data.timestamp),
            length=anomalous_data.queue_length,
            wait_time=anomalous_data.estimated_wait_time,
            density=anomalous_data.queue_density,
            movement_speed=anomalous_data.average_speed or 1.0,
            formation_rate=anomalous_data.length_change_rate or 0.5,
            abandonment_rate=anomalous_data.abandonment_rate or 0.1,
            spatial_distribution=[],
            temporal_pattern=anomalous_data.historical_lengths or [],
            interaction_count=anomalous_data.object_count or 10
        )
        
        anomalies = detector.detect_anomalies(metrics)
        
        if anomalies:
            for anomaly in anomalies:
                print(f"   🔴 ANOMALY DETECTED: {anomaly.type.value}")
                print(f"      Severity: {anomaly.severity.value}")
                print(f"      Confidence: {anomaly.confidence:.2f}")
                print(f"      Description: {anomaly.description}")
                print(f"      Recommendations: {', '.join(anomaly.recommendations[:2])}")
        else:
            print(f"   ✅ No anomalies detected")

def demo_ml_detection():
    """Demonstrate ML-based anomaly detection"""
    print("\n" + "="*60)
    print("MACHINE LEARNING ANOMALY DETECTION DEMO")
    print("="*60)
    
    detector = QueueAnomalyDetector(enable_ml=True)
    
    print("🧠 Training ML model with historical data...")
    
    # Generate training data
    training_metrics = []
    base_time = time.time()
    
    for i in range(60):  # Need at least 50 samples for ML training
        queue_data = generate_normal_queue_data(f"training_queue_{i%3}", base_time + i)
        
        # Add some variability
        if random.random() < 0.1:  # 10% slightly anomalous data
            queue_data.queue_length *= random.uniform(1.2, 1.5)
            queue_data.estimated_wait_time *= random.uniform(1.3, 1.7)
        
        metrics = QueueMetrics(
            queue_id=queue_data.queue_id,
            timestamp=datetime.fromtimestamp(queue_data.timestamp),
            length=queue_data.queue_length,
            wait_time=queue_data.estimated_wait_time,
            density=queue_data.queue_density,
            movement_speed=queue_data.average_speed or 1.0,
            formation_rate=queue_data.length_change_rate or 0.5,
            abandonment_rate=queue_data.abandonment_rate or 0.1,
            spatial_distribution=[],
            temporal_pattern=queue_data.historical_lengths or [],
            interaction_count=queue_data.object_count or 10
        )
        
        training_metrics.append(metrics)
        
        if i % 20 == 0:
            print(f"   Generated {i+1}/60 training samples...")
    
    # Train the ML model
    success = detector.train_ml_detector(training_metrics)
    
    if success:
        print("✅ ML model trained successfully")
        
        print("\n🔍 Testing ML anomaly detection...")
        
        # Test with clearly anomalous data
        anomalous_data = generate_anomalous_queue_data("ml_test_queue", time.time(), "overcrowding")
        metrics = QueueMetrics(
            queue_id=anomalous_data.queue_id,
            timestamp=datetime.fromtimestamp(anomalous_data.timestamp),
            length=anomalous_data.queue_length,
            wait_time=anomalous_data.estimated_wait_time,
            density=anomalous_data.queue_density,
            movement_speed=anomalous_data.average_speed or 0.1,
            formation_rate=anomalous_data.length_change_rate or 3.0,
            abandonment_rate=anomalous_data.abandonment_rate or 0.1,
            spatial_distribution=[],
            temporal_pattern=anomalous_data.historical_lengths or [],
            interaction_count=anomalous_data.object_count or 10
        )
        
        anomalies = detector.detect_anomalies(metrics)
        
        if anomalies:
            for anomaly in anomalies:
                print(f"   🔴 ML ANOMALY DETECTED: {anomaly.type.value}")
                print(f"      Severity: {anomaly.severity.value}")
                print(f"      Confidence: {anomaly.confidence:.2f}")
                print(f"      Description: {anomaly.description}")
        else:
            print("   ℹ️ No ML anomalies detected (this may happen with random data)")
    else:
        print("❌ ML model training failed")

def demo_integration_system():
    """Demonstrate the integrated anomaly detection system"""
    print("\n" + "="*60)
    print("INTEGRATED ANOMALY DETECTION SYSTEM DEMO")
    print("="*60)
    
    # Create integrated system
    integrator = QueueAnomalyIntegrator(sensitivity=2.0, enable_ml=True)
    alert_manager = AnomalyAlertManager(alert_threshold=AnomalySeverity.MEDIUM)
    
    # Register callback
    callback = create_default_anomaly_callback(alert_manager)
    integrator.register_anomaly_callback(callback)
    
    print("🔧 Integrated system initialized")
    print("📊 Processing queue data stream...")
    
    # Simulate data stream
    base_time = time.time()
    
    # Process normal data first
    for i in range(20):
        queue_data = generate_normal_queue_data("integrated_queue", base_time + i)
        anomalies = integrator.process_queue_data(queue_data)
        
        if i % 5 == 0:
            print(f"   Processed {i+1}/20 normal samples...")
    
    print("✅ Normal data processed, baseline established")
    
    # Introduce anomalies
    print("\n🚨 Introducing anomalies into data stream...")
    
    anomaly_scenarios = [
        ("overcrowding", "Sudden overcrowding event"),
        ("abandonment", "High abandonment rate event"),
        ("bottleneck", "Service bottleneck event")
    ]
    
    for anomaly_type, description in anomaly_scenarios:
        print(f"\n--- {description} ---")
        
        anomalous_data = generate_anomalous_queue_data("integrated_queue", time.time(), anomaly_type)
        anomalies = integrator.process_queue_data(anomalous_data)
        
        if anomalies:
            print(f"   🔴 {len(anomalies)} anomalies detected!")
            for anomaly in anomalies:
                print(f"      - {anomaly.type.value} ({anomaly.severity.value})")
        else:
            print("   ✅ No anomalies detected")
    
    # Show active alerts
    active_alerts = alert_manager.get_active_alerts()
    if active_alerts:
        print(f"\n📋 Active alerts: {len(active_alerts)}")
        for alert in active_alerts[-3:]:  # Show last 3
            print(f"   - {alert['type']} ({alert['severity']}): {alert['description']}")
    
    # Show system statistics
    stats = integrator.get_anomaly_statistics()
    print(f"\n📈 System Statistics:")
    print(f"   Total detections: {stats.get('total_detections', 0)}")
    print(f"   ML trained: {stats.get('ml_trained', False)}")
    print(f"   Queues monitored: {stats.get('total_queues_monitored', 0)}")
    print(f"   Samples collected: {stats.get('total_samples_collected', 0)}")

def main():
    """Main demo function"""
    print("🚦 EDGE-QI Queue Anomaly Detection System Demo")
    print("Advanced anomaly detection for intelligent queue management")
    
    try:
        # Run demonstrations
        demo_statistical_detection()
        demo_ml_detection()
        demo_integration_system()
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETED SUCCESSFULLY")
        print("="*60)
        print("\nThe EDGE-QI anomaly detection system demonstrated:")
        print("• Statistical anomaly detection using z-score analysis")
        print("• Machine learning anomaly detection using Isolation Forest")
        print("• Behavioral pattern analysis for suspicious activities")
        print("• Integrated alert management with severity classification")
        print("• Real-time processing and callback notifications")
        print("\nReady for integration with live queue detection systems!")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()