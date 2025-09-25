# 🚀 Real-Time Data Integration Guide

## Overview

This guide shows you how to integrate **real-time data** into your EDGE-QI system **without requiring physical hardware**. We've created a comprehensive simulation system that generates realistic traffic scenarios, camera feeds, and sensor data.

## 🎯 What You Get

### ✅ **Real-Time Simulation Features:**
- **Live Camera Feeds**: Simulated video streams with moving vehicles, traffic lights
- **Realistic Traffic Patterns**: Rush hour, congestion, different vehicle types
- **Object Detection**: Real-time vehicle detection and tracking
- **Queue Formation**: Automatic queue detection at traffic lights
- **Traffic Analysis**: Flow monitoring, speed analysis, congestion detection
- **Sensor Data**: CPU, memory, temperature, network monitoring
- **Bandwidth Optimization**: Adaptive streaming based on network conditions
- **Anomaly Detection**: Unusual traffic patterns and system alerts

## 🚀 Quick Start

### **Option 1: Interactive Real-Time Demo (Recommended)**

```bash
# Activate your environment
.\.venv\Scripts\Activate.ps1

# Run the interactive demo with live video
python demo_realtime_integration.py
```

**Features:**
- Live video display with vehicle tracking
- Real-time queue detection visualization
- Traffic flow analytics
- Performance monitoring
- Interactive controls (pause, save frames)

### **Option 2: Enhanced Real-Time Dashboard**

```bash
# Run the enhanced dashboard
streamlit run run_realtime_dashboard.py
```

**Features:**
- Web-based real-time dashboard
- Live camera feed with overlays
- Real-time metrics and charts
- Interactive traffic density controls
- System performance monitoring

### **Option 3: Basic Real-Time Processing**

```python
from Core.simulation.realtime_integrator import RealTimeDataIntegrator

# Initialize real-time processing
integrator = RealTimeDataIntegrator()

# Start processing
integrator.start_real_time_processing()

# Get live data
frame = integrator.get_current_frame()
detections = integrator.get_current_detections()
queues = integrator.get_current_queue_data()
traffic = integrator.get_current_traffic_data()

# Stop when done
integrator.stop_real_time_processing()
```

## 🎛️ Configuration Options

### **Traffic Simulation Settings:**

```python
from Core.simulation.realtime_integrator import RealTimeConfig

config = RealTimeConfig(
    frame_width=1280,           # Video resolution
    frame_height=720,
    fps=30,                     # Frames per second
    traffic_density=0.7,        # 0.1 (light) to 1.0 (heavy)
    detection_confidence_threshold=0.7,
    enable_queue_detection=True,
    enable_traffic_analysis=True,
    enable_anomaly_detection=True,
    enable_bandwidth_optimization=True
)
```

### **Dynamic Controls:**

```python
# Adjust traffic in real-time
integrator.set_traffic_density(0.8)  # Heavy traffic

# Change detection sensitivity
integrator.set_detection_threshold(0.6)  # More sensitive

# Add congestion zones
integrator.add_congestion_zone(640, 360, 100)  # Center intersection
```

## 📊 Data Integration Examples

### **Real-Time Frame Processing:**

```python
def process_live_data():
    integrator = RealTimeDataIntegrator()
    integrator.start_real_time_processing()
    
    # Register callbacks for real-time updates
    integrator.register_frame_callback(on_frame_update)
    integrator.register_detection_callback(on_detection_update)
    integrator.register_queue_callback(on_queue_update)
    
    # Process for 60 seconds
    time.sleep(60)
    integrator.stop_real_time_processing()

def on_frame_update(frame_data):
    frame = frame_data['frame']
    timestamp = frame_data['timestamp']
    camera_id = frame_data['camera_id']
    
    # Your custom frame processing here
    print(f"New frame from {camera_id} at {timestamp}")

def on_detection_update(detections):
    for detection in detections:
        print(f"Detected: {detection['class']} at {detection['center']}")

def on_queue_update(queue_data):
    for queue in queue_data:
        print(f"Queue {queue['id']}: {queue['vehicle_count']} vehicles")
```

### **Traffic Analytics Integration:**

```python
def analyze_traffic_patterns():
    integrator = RealTimeDataIntegrator()
    integrator.start_real_time_processing()
    
    # Collect data for analysis
    traffic_history = []
    
    for _ in range(100):  # Collect 100 data points
        traffic_data = integrator.get_current_traffic_data()
        if traffic_data:
            traffic_history.append(traffic_data)
        time.sleep(1)
    
    # Analyze patterns
    avg_speed = sum(t['average_speed'] for t in traffic_history) / len(traffic_history)
    congestion_events = len([t for t in traffic_history if t['condition'] == 'jammed'])
    
    print(f"Average speed: {avg_speed:.1f} km/h")
    print(f"Congestion events: {congestion_events}")
    
    integrator.stop_real_time_processing()
```

### **Custom Dashboard Integration:**

```python
import streamlit as st
from Core.simulation.realtime_integrator import RealTimeDataIntegrator

# Initialize in Streamlit
@st.cache_resource
def get_integrator():
    return RealTimeDataIntegrator()

def create_custom_dashboard():
    integrator = get_integrator()
    
    # Controls
    if st.button("Start Processing"):
        integrator.start_real_time_processing()
    
    # Display live data
    frame = integrator.get_current_frame()
    if frame is not None:
        st.image(frame, channels="BGR")
    
    # Live metrics
    stats = integrator.get_processing_stats()
    st.metric("FPS", stats.get('fps', 0))
    st.metric("Detections", stats.get('detections_made', 0))
    
    # Auto-refresh
    time.sleep(0.1)
    st.rerun()
```

## 🎨 Advanced Features

### **Multi-Camera Simulation:**

```python
# The simulator supports multiple camera views
cameras = integrator.simulator.cameras
for camera_id, camera in cameras.items():
    print(f"Camera {camera_id}: {camera.position}")
    
# Get specific camera feed
main_feed = integrator.simulator.get_latest_frame('main_intersection')
north_feed = integrator.simulator.get_latest_frame('north_approach')
```

### **Network Condition Simulation:**

```python
# Simulate varying network conditions
import random

def simulate_network_conditions():
    while processing:
        # Simulate network changes
        if random.random() < 0.1:  # 10% chance every iteration
            new_density = random.uniform(0.2, 0.9)
            integrator.set_traffic_density(new_density)
            print(f"Network condition changed - new density: {new_density}")
        
        time.sleep(1)
```

### **Data Export and Logging:**

```python
import json
import csv

def log_processing_data():
    integrator = RealTimeDataIntegrator()
    integrator.start_real_time_processing()
    
    log_data = []
    
    try:
        for i in range(300):  # 5 minutes of data
            data_point = {
                'timestamp': time.time(),
                'detections': len(integrator.get_current_detections()),
                'queues': len(integrator.get_current_queue_data()),
                'traffic': integrator.get_current_traffic_data(),
                'sensors': integrator.get_current_sensor_data()
            }
            log_data.append(data_point)
            time.sleep(1)
    
    finally:
        # Save data
        with open('edge_qi_data.json', 'w') as f:
            json.dump(log_data, f, indent=2)
        
        integrator.stop_real_time_processing()
        print("Data exported to edge_qi_data.json")
```

## 🚦 Use Cases

### **1. Smart Traffic Management**
- Monitor intersection queues in real-time
- Optimize traffic light timing
- Detect congestion and suggest alternative routes

### **2. Emergency Response**
- Detect unusual traffic patterns
- Monitor queue lengths during emergencies
- Prioritize emergency vehicle routing

### **3. Urban Planning**
- Analyze traffic flow patterns
- Identify bottlenecks and problem areas
- Simulate infrastructure changes

### **4. Performance Testing**
- Test system under various load conditions
- Validate bandwidth optimization
- Benchmark processing performance

## 🎯 Next Steps

1. **Start with the Interactive Demo** to see everything working
2. **Try the Real-Time Dashboard** for web-based monitoring
3. **Integrate with your existing systems** using the API
4. **Customize traffic patterns** for your specific use case
5. **Add your own processing logic** using callbacks

## 🔧 Troubleshooting

### **Common Issues:**

**Q: Demo window not showing video**
```bash
# Install OpenCV with GUI support
pip install opencv-python-headless
# or
pip install opencv-contrib-python
```

**Q: Low FPS performance**
```python
# Reduce simulation complexity
config = RealTimeConfig(
    frame_width=640,    # Lower resolution
    frame_height=480,
    fps=15,             # Lower FPS
    traffic_density=0.3 # Less traffic
)
```

**Q: Memory usage high**
```python
# Limit queue sizes in simulator
simulator.frame_queue = Queue(maxsize=30)  # Reduce buffer
```

This real-time integration system gives you all the benefits of live data processing without requiring any physical hardware! 🚀