"""
Enhanced Dashboard with Real-Time Data Integration

Updates the EDGE-QI dashboard to use simulated real-time data
instead of static simulation data.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import time
import cv2
from PIL import Image
import threading
from typing import Dict, List, Optional

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Core.simulation.realtime_integrator import RealTimeDataIntegrator, RealTimeConfig

class RealTimeDashboard:
    """Enhanced dashboard with real-time data integration"""
    
    def __init__(self):
        self.integrator = None
        self.is_running = False
        self.latest_data = {
            'frame': None,
            'detections': [],
            'queues': [],
            'traffic': {},
            'sensors': {},
            'stats': {}
        }
        
        # Dashboard configuration
        self.config = RealTimeConfig(
            frame_width=1280,
            frame_height=720,
            fps=10,  # Lower FPS for dashboard display
            traffic_density=0.5,
            detection_confidence_threshold=0.7
        )
    
    def initialize_realtime_processing(self):
        """Initialize real-time data processing"""
        if self.integrator is None:
            self.integrator = RealTimeDataIntegrator(self.config)
            
            # Register callbacks
            self.integrator.register_frame_callback(self._update_frame_data)
            self.integrator.register_detection_callback(self._update_detection_data)
            self.integrator.register_queue_callback(self._update_queue_data)
            self.integrator.register_traffic_callback(self._update_traffic_data)
            
            st.success("✅ Real-time processing initialized")
        return self.integrator is not None
    
    def start_realtime_processing(self):
        """Start real-time data processing"""
        if not self.integrator:
            self.initialize_realtime_processing()
        
        if not self.is_running:
            self.integrator.start_real_time_processing()
            self.is_running = True
            st.success("🚀 Real-time processing started")
    
    def stop_realtime_processing(self):
        """Stop real-time data processing"""
        if self.is_running and self.integrator:
            self.integrator.stop_real_time_processing()
            self.is_running = False
            st.info("⏹️ Real-time processing stopped")
    
    def get_realtime_frame(self) -> Optional[np.ndarray]:
        """Get current real-time frame"""
        if self.integrator and self.is_running:
            return self.integrator.get_current_frame()
        return None
    
    def get_realtime_data(self) -> Dict:
        """Get all current real-time data"""
        if not self.integrator or not self.is_running:
            return self.latest_data
        
        return {
            'frame': self.integrator.get_current_frame(),
            'detections': self.integrator.get_current_detections(),
            'queues': self.integrator.get_current_queue_data(),
            'traffic': self.integrator.get_current_traffic_data(),
            'sensors': self.integrator.get_current_sensor_data(),
            'stats': self.integrator.get_processing_stats()
        }
    
    def update_traffic_density(self, density: float):
        """Update traffic density in real-time"""
        if self.integrator:
            self.integrator.set_traffic_density(density)
            st.info(f"🚗 Traffic density updated to {density:.1f}")
    
    def update_detection_threshold(self, threshold: float):
        """Update detection threshold in real-time"""
        if self.integrator:
            self.integrator.set_detection_threshold(threshold)
            st.info(f"🎯 Detection threshold updated to {threshold:.2f}")
    
    # Callback methods
    def _update_frame_data(self, frame_data):
        """Update frame data"""
        self.latest_data['frame'] = frame_data
    
    def _update_detection_data(self, detections):
        """Update detection data"""
        self.latest_data['detections'] = detections
    
    def _update_queue_data(self, queue_data):
        """Update queue data"""
        self.latest_data['queues'] = queue_data
    
    def _update_traffic_data(self, traffic_data):
        """Update traffic data"""
        self.latest_data['traffic'] = traffic_data

# Global dashboard instance
realtime_dashboard = RealTimeDashboard()

def create_realtime_dashboard():
    """Create enhanced dashboard with real-time data"""
    
    st.set_page_config(
        page_title="EDGE-QI Real-Time Dashboard",
        page_icon="🚦",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if "dashboard_initialized" not in st.session_state:
        st.session_state.dashboard_initialized = True
        st.session_state.refresh_counter = 0
    
    # Main title
    st.title("🚦 EDGE-QI Real-Time Dashboard")
    st.markdown("**Edge-based Queue Intelligence Framework for Smart Surveillance and Traffic Management**")
    st.markdown("---")
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Real-Time Controls")
        
        # Start/Stop controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Start Real-Time", key="start_rt"):
                realtime_dashboard.start_realtime_processing()
        
        with col2:
            if st.button("⏹️ Stop Real-Time", key="stop_rt"):
                realtime_dashboard.stop_realtime_processing()
        
        st.markdown("---")
        
        # Configuration controls
        st.subheader("⚙️ Configuration")
        
        traffic_density = st.slider(
            "Traffic Density",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1,
            key="traffic_density"
        )
        
        detection_threshold = st.slider(
            "Detection Threshold",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.05,
            key="detection_threshold"
        )
        
        # Update settings
        if st.button("Update Settings"):
            realtime_dashboard.update_traffic_density(traffic_density)
            realtime_dashboard.update_detection_threshold(detection_threshold)
        
        # Manual refresh button
        if st.button("🔄 Refresh Data"):
            st.session_state.last_refresh = 0  # Force refresh
        
        st.markdown("---")
        
        # System status
        st.subheader("📊 System Status")
        status = "🟢 Running" if realtime_dashboard.is_running else "🔴 Stopped"
        st.markdown(f"**Status:** {status}")
        
        # Display current stats
        data = realtime_dashboard.get_realtime_data()
        stats = data.get('stats', {})
        
        if stats:
            st.metric("Frames Processed", stats.get('frames_processed', 0))
            st.metric("Processing FPS", f"{stats.get('fps', 0):.1f}")
            st.metric("Detections Made", stats.get('detections_made', 0))
            st.metric("Queues Detected", stats.get('queues_detected', 0))
    
    # Main content
    if not realtime_dashboard.is_running:
        st.info("🎬 Click 'Start Real-Time' to begin processing simulated camera feeds")
        st.markdown("""
        ### 🚀 Real-Time Features:
        - **Live Camera Simulation**: Realistic traffic patterns with moving vehicles
        - **Real-Time Detection**: Object detection and tracking at 10 FPS
        - **Queue Analysis**: Automatic queue detection and wait time estimation
        - **Traffic Monitoring**: Flow analysis and congestion detection
        - **System Monitoring**: Resource usage and performance metrics
        - **Interactive Controls**: Adjust traffic density and detection settings in real-time
        """)
        return
    
    # Get real-time data
    data = realtime_dashboard.get_realtime_data()
    
    # Video feed section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📹 Live Camera Feed")
        
        frame = data.get('frame')
        if frame is not None:
            # Convert frame for display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Create annotated frame
            annotated_frame = create_annotated_frame(frame_rgb, data)
            
            st.image(annotated_frame, channels="RGB", use_column_width=True)
        else:
            st.info("📷 Waiting for camera feed...")
    
    with col2:
        st.subheader("📊 Live Metrics")
        
        # Current detections
        detections = data.get('detections', [])
        st.metric("Current Detections", len(detections))
        
        # Current queues
        queues = data.get('queues', [])
        st.metric("Active Queues", len(queues))
        
        # Traffic data
        traffic = data.get('traffic', {})
        if traffic:
            st.metric("Average Speed", f"{traffic.get('average_speed', 0):.1f} km/h")
            st.metric("Traffic Condition", traffic.get('condition', 'Unknown').title())
            st.metric("Vehicle Count", traffic.get('vehicle_count', 0))
        
        # Sensor data
        sensors = data.get('sensors', {})
        if sensors:
            st.metric("CPU Usage", f"{sensors.get('cpu_usage', 0):.1f}%")
            st.metric("Temperature", f"{sensors.get('temperature', 0):.1f}°C")
            st.metric("Memory Usage", f"{sensors.get('memory_usage', 0):.1f}%")
    
    # Analytics section
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚗 Traffic Analysis")
        
        if traffic:
            # Create traffic flow chart
            fig = go.Figure()
            
            # Add traffic metrics
            metrics = ['Vehicle Count', 'Average Speed', 'Density', 'Throughput']
            values = [
                traffic.get('vehicle_count', 0),
                traffic.get('average_speed', 0),
                traffic.get('density', 0) * 100,  # Scale density
                traffic.get('throughput', 0) * 10  # Scale throughput
            ]
            
            fig.add_trace(go.Bar(
                x=metrics,
                y=values,
                marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
            ))
            
            fig.update_layout(
                title="Real-Time Traffic Metrics",
                yaxis_title="Value",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⏳ Waiting for traffic data...")
    
    with col2:
        st.subheader("🔍 Detection Details")
        
        if detections:
            # Create detection summary
            detection_types = {}
            for detection in detections:
                vehicle_type = detection.get('class', 'unknown')
                detection_types[vehicle_type] = detection_types.get(vehicle_type, 0) + 1
            
            # Create pie chart
            fig = px.pie(
                values=list(detection_types.values()),
                names=list(detection_types.keys()),
                title="Vehicle Type Distribution"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⏳ Waiting for detection data...")
    
    # Queue analysis section
    if queues:
        st.markdown("---")
        st.subheader("📋 Queue Analysis")
        
        # Queue data table
        queue_df = pd.DataFrame([
            {
                'Queue ID': q['id'],
                'Vehicle Count': q['vehicle_count'],
                'Length (m)': f"{q['length']/10:.1f}",  # Convert pixels to meters
                'Wait Time (s)': f"{q['wait_time']:.0f}",
                'Density': f"{q['density']:.2f}",
                'Confidence': f"{q['confidence']:.2f}"
            }
            for q in queues
        ])
        
        st.dataframe(queue_df, use_container_width=True)
    
    # Controlled auto-refresh to prevent dashboard crashes
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    # Only refresh every 2 seconds to prevent overwhelming Streamlit
    current_time = time.time()
    if current_time - st.session_state.last_refresh > 2.0:
        st.session_state.last_refresh = current_time
        st.rerun()

def create_annotated_frame(frame: np.ndarray, data: Dict) -> np.ndarray:
    """Create annotated frame with detections and queues"""
    annotated = frame.copy()
    
    # Draw detections
    detections = data.get('detections', [])
    for detection in detections:
        bbox = detection['bbox']
        x, y, w, h = bbox
        confidence = detection['confidence']
        
        if confidence > 0.6:
            # Draw bounding box
            color = (0, 255, 0) if detection.get('speed', 0) > 10 else (255, 0, 0)
            cv2.rectangle(annotated, (int(x), int(y)), (int(x + w), int(y + h)), color, 2)
            
            # Draw label
            label = f"{detection['class']} ({confidence:.2f})"
            cv2.putText(annotated, label, (int(x), int(y - 5)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    # Draw queues
    queues = data.get('queues', [])
    for queue in queues:
        center = queue['location']
        radius = int(queue['length'] / 4)
        
        # Draw queue circle
        cv2.circle(annotated, (int(center[0]), int(center[1])), radius, (255, 0, 255), 2)
        
        # Draw queue label
        queue_label = f"Q: {queue['vehicle_count']} vehicles"
        cv2.putText(annotated, queue_label, (int(center[0] - 50), int(center[1] - radius - 10)),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
    
    return annotated

if __name__ == "__main__":
    create_realtime_dashboard()