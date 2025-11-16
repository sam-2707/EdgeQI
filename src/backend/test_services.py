"""
Quick Test Script for EDGE-QI Enhanced Backend
Tests the 3 new services independently
"""

import sys
import asyncio

print("=" * 70)
print("🧪 EDGE-QI Service Tests")
print("=" * 70)

# Test 1: System Monitor
print("\n📊 Test 1: System Monitor")
print("-" * 70)
try:
    from system_monitor import SystemMonitor
    
    monitor = SystemMonitor()
    metrics = monitor.get_all_metrics()
    
    print(f"✅ System Monitor Working!")
    print(f"   CPU: {metrics['cpu']['usage_percent']}%")
    print(f"   Memory: {metrics['memory']['percent']}%")
    print(f"   GPU: {'Available' if metrics['gpu']['available'] else 'Not available'}")
    print(f"   Battery: {'Present' if metrics['battery']['present'] else 'Not present'}")
    
except Exception as e:
    print(f"❌ System Monitor Error: {e}")

# Test 2: Anomaly Transmitter
print("\n🚨 Test 2: Anomaly Transmitter")
print("-" * 70)
try:
    from anomaly_transmitter import AnomalyDrivenTransmitter
    
    transmitter = AnomalyDrivenTransmitter(window_size=20, anomaly_threshold=2.0)
    
    # Simulate some detections
    import random
    for i in range(25):
        vehicle_count = random.randint(5, 15) if i < 20 else random.randint(25, 35)
        detections = [{'class_name': 'car'} for _ in range(vehicle_count)]
        should_send, reason, metadata = transmitter.should_transmit(detections)
    
    stats = transmitter.get_stats()
    print(f"✅ Anomaly Transmitter Working!")
    print(f"   Frames processed: {stats['total_frames']}")
    print(f"   Bandwidth saved: {stats['bandwidth_saved_percent']:.1f}%")
    print(f"   Anomalies detected: {stats['anomalies_detected']}")
    
except Exception as e:
    print(f"❌ Anomaly Transmitter Error: {e}")

# Test 3: Detection Service
print("\n🎯 Test 3: YOLOv8 Detection Service")
print("-" * 70)
try:
    from detection_service import YOLODetectionService
    import numpy as np
    
    detector = YOLODetectionService(device="auto")
    
    # Create dummy frame
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Run detection
    detections = detector.detect_frame(dummy_frame)
    stats = detector.get_stats()
    
    print(f"✅ Detection Service Working!")
    print(f"   Model loaded: {stats['model_loaded']}")
    print(f"   Device: {stats['device']}")
    print(f"   Detections in test frame: {len(detections)}")
    print(f"   FPS: {stats['fps']:.2f}")
    
    if not stats['model_loaded']:
        print("\n   ⚠️  Note: YOLOv8 model not loaded (using mock mode)")
        print("      Install with: pip install ultralytics")
    
except Exception as e:
    print(f"❌ Detection Service Error: {e}")

# Summary
print("\n" + "=" * 70)
print("📝 Summary")
print("=" * 70)
print("""
✅ If all 3 tests passed, your backend is ready!

Next steps:
1. cd src/backend
2. python server.py
3. Open http://localhost:8000/docs to see API
4. Check http://localhost:8000/health for service status

Dashboard endpoints:
- /api/system/metrics/real  - Real CPU/GPU/memory metrics
- /api/detection/stats      - Detection statistics  
- /api/anomaly/stats        - Bandwidth savings

Frontend: cd src/frontend && npm start
""")
