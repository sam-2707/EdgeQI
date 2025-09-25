"""
Stable Real-Time Dashboard for EDGE-QI

A more stable version of the real-time dashboard that handles
Streamlit's refresh cycles properly without crashing.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import time
import cv2
from PIL import Image
import sys
import os
from typing import Dict, List, Optional
import threading

# Add path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import real-time components
try:
    from Core.simulation.realtime_integrator import RealTimeDataIntegrator, RealTimeConfig
    REALTIME_AVAILABLE = True
except ImportError as e:
    REALTIME_AVAILABLE = False
    st.error(f"Real-time components not available: {e}")

def init_session_state():
    """Initialize Streamlit session state"""
    if "rt_integrator" not in st.session_state:
        st.session_state.rt_integrator = None
    if "rt_running" not in st.session_state:
        st.session_state.rt_running = False
    if "rt_data" not in st.session_state:
        st.session_state.rt_data = {}
    if "last_update" not in st.session_state:
        st.session_state.last_update = 0
    if "refresh_rate" not in st.session_state:
        st.session_state.refresh_rate = 3.0  # Refresh every 3 seconds

@st.cache_resource
def get_realtime_integrator():
    """Get or create real-time integrator (cached)"""
    if not REALTIME_AVAILABLE:
        return None
    
    config = RealTimeConfig(
        frame_width=1280,
        frame_height=720,
        fps=8,  # Lower FPS for stability
        traffic_density=0.5,
        detection_confidence_threshold=0.7
    )
    return RealTimeDataIntegrator(config)

def start_realtime_processing():
    """Start real-time processing"""
    if not REALTIME_AVAILABLE:
        st.error("Real-time components not available")
        return
    
    integrator = get_realtime_integrator()
    if integrator and not st.session_state.rt_running:
        try:
            integrator.start_real_time_processing()
            st.session_state.rt_integrator = integrator
            st.session_state.rt_running = True
            st.success("✅ Real-time processing started")
        except Exception as e:
            st.error(f"Failed to start real-time processing: {e}")

def stop_realtime_processing():
    """Stop real-time processing"""
    if st.session_state.rt_integrator and st.session_state.rt_running:
        try:
            st.session_state.rt_integrator.stop_real_time_processing()
            st.session_state.rt_running = False
            st.info("⏹️ Real-time processing stopped")
        except Exception as e:
            st.error(f"Failed to stop real-time processing: {e}")

def update_realtime_data():
    """Update real-time data at controlled intervals"""
    current_time = time.time()
    
    if (current_time - st.session_state.last_update > st.session_state.refresh_rate and 
        st.session_state.rt_integrator and st.session_state.rt_running):
        
        try:
            # Get latest data
            st.session_state.rt_data = {
                'frame': st.session_state.rt_integrator.get_current_frame(),
                'detections': st.session_state.rt_integrator.get_current_detections(),
                'queues': st.session_state.rt_integrator.get_current_queue_data(),
                'traffic': st.session_state.rt_integrator.get_current_traffic_data(),
                'sensors': st.session_state.rt_integrator.get_current_sensor_data(),
                'stats': st.session_state.rt_integrator.get_processing_stats()
            }
            st.session_state.last_update = current_time
        except Exception as e:
            st.error(f"Error updating data: {e}")

def create_annotated_frame(frame, data):
    """Create annotated frame with detections"""
    if frame is None:
        return None
    
    try:
        annotated = frame.copy()
        detections = data.get('detections', [])
        
        # Draw detections
        for detection in detections:
            if detection.get('confidence', 0) > 0.6:
                bbox = detection.get('bbox', [0, 0, 0, 0])
                x, y, w, h = bbox
                
                # Draw bounding box
                color = (0, 255, 0) if detection.get('speed', 0) > 10 else (255, 0, 0)
                cv2.rectangle(annotated, (int(x), int(y)), (int(x + w), int(y + h)), color, 2)
                
                # Draw label
                label = f"{detection.get('class', 'unknown')} ({detection.get('confidence', 0):.2f})"
                cv2.putText(annotated, label, (int(x), int(y - 5)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Draw queues
        queues = data.get('queues', [])
        for queue in queues:
            center = queue.get('location', (0, 0))
            radius = int(queue.get('length', 0) / 4)
            if radius > 0:
                cv2.circle(annotated, (int(center[0]), int(center[1])), radius, (255, 0, 255), 2)
        
        return annotated
    except Exception as e:
        st.error(f"Error creating annotated frame: {e}")
        return frame

def main():
    """Main dashboard function"""
    st.set_page_config(
        page_title="EDGE-QI Stable Real-Time Dashboard",
        page_icon="🚦",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Update data at controlled intervals
    update_realtime_data()
    
    # Header
    st.title("🚦 EDGE-QI Stable Real-Time Dashboard")
    st.markdown("**Edge-based Queue Intelligence Framework - Stable Version**")
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Real-Time Controls")
        
        if not REALTIME_AVAILABLE:
            st.error("❌ Real-time integration not available")
            st.markdown("Please check the installation and imports.")
            return
        
        # Status display
        status = "🟢 Running" if st.session_state.rt_running else "🔴 Stopped"
        st.markdown(f"**Status:** {status}")
        
        # Control buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Start", disabled=st.session_state.rt_running):
                start_realtime_processing()
        with col2:
            if st.button("⏹️ Stop", disabled=not st.session_state.rt_running):
                stop_realtime_processing()
        
        # Settings
        st.markdown("---")
        st.subheader("⚙️ Settings")
        
        refresh_rate = st.slider("Refresh Rate (seconds)", 1.0, 10.0, 3.0, 0.5)
        st.session_state.refresh_rate = refresh_rate
        
        traffic_density = st.slider("Traffic Density", 0.1, 1.0, 0.5, 0.1)
        detection_threshold = st.slider("Detection Threshold", 0.1, 1.0, 0.7, 0.05)
        
        if st.button("🔄 Update Settings"):
            if st.session_state.rt_integrator:
                st.session_state.rt_integrator.set_traffic_density(traffic_density)
                st.session_state.rt_integrator.set_detection_threshold(detection_threshold)
                st.success("Settings updated!")
        
        # Force refresh button
        if st.button("🔄 Force Refresh"):
            st.session_state.last_update = 0
            st.rerun()
        
        # Stats
        if st.session_state.rt_data:
            st.markdown("---")
            st.subheader("📊 Stats")
            stats = st.session_state.rt_data.get('stats', {})
            st.metric("FPS", f"{stats.get('fps', 0):.1f}")
            st.metric("Frames", stats.get('frames_processed', 0))
            st.metric("Detections", len(st.session_state.rt_data.get('detections', [])))
    
    # Main content
    if not st.session_state.rt_running:
        st.info("🎬 Click 'Start' to begin real-time processing")
        st.markdown("""
        ### 🚀 Stable Real-Time Features:
        - **Controlled Refresh Rate**: Prevents dashboard crashes
        - **Session State Management**: Maintains stability across refreshes  
        - **Error Handling**: Graceful error recovery
        - **Live Camera Simulation**: Realistic traffic patterns
        - **Real-Time Analytics**: Queue detection and traffic monitoring
        - **Interactive Controls**: Adjust settings in real-time
        """)
        return
    
    # Display real-time data
    data = st.session_state.rt_data
    
    if not data:
        st.info("⏳ Loading real-time data...")
        return
    
    # Video feed and metrics
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📹 Live Camera Feed")
        frame = data.get('frame')
        
        if frame is not None:
            try:
                # Convert BGR to RGB for display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                annotated_frame = create_annotated_frame(frame_rgb, data)
                
                if annotated_frame is not None:
                    st.image(annotated_frame, channels="RGB", width="stretch")
                else:
                    st.image(frame_rgb, channels="RGB", width="stretch")
            except Exception as e:
                st.error(f"Error displaying frame: {e}")
        else:
            st.info("📷 Waiting for camera feed...")
    
    with col2:
        st.subheader("📊 Live Metrics")
        
        # Current metrics
        detections = data.get('detections', [])
        queues = data.get('queues', [])
        traffic = data.get('traffic', {})
        sensors = data.get('sensors', {})
        
        st.metric("Live Detections", len(detections))
        st.metric("Active Queues", len(queues))
        
        if traffic:
            st.metric("Avg Speed", f"{traffic.get('average_speed', 0):.1f} km/h")
            st.metric("Condition", traffic.get('condition', 'Unknown').replace('_', ' ').title())
            st.metric("Vehicles", traffic.get('vehicle_count', 0))
        
        if sensors:
            st.metric("CPU", f"{sensors.get('cpu_usage', 0):.1f}%")
            st.metric("Memory", f"{sensors.get('memory_usage', 0):.1f}%")
            st.metric("Temp", f"{sensors.get('temperature', 0):.1f}°C")
    
    # Analytics
    if traffic or detections:
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚗 Traffic Analysis")
            if traffic:
                metrics = ['Vehicles', 'Speed', 'Density', 'Throughput']
                values = [
                    traffic.get('vehicle_count', 0),
                    traffic.get('average_speed', 0),
                    traffic.get('density', 0) * 100,
                    traffic.get('throughput', 0) * 10
                ]
                
                fig = go.Figure(data=go.Bar(x=metrics, y=values))
                fig.update_layout(title="Traffic Metrics", height=300)
                st.plotly_chart(fig, width="stretch")
        
        with col2:
            st.subheader("🔍 Detection Types")
            if detections:
                detection_types = {}
                for d in detections:
                    vehicle_type = d.get('class', 'unknown')
                    detection_types[vehicle_type] = detection_types.get(vehicle_type, 0) + 1
                
                if detection_types:
                    fig = px.pie(values=list(detection_types.values()), 
                                names=list(detection_types.keys()))
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, width="stretch")
    
    # Queue analysis
    if queues:
        st.markdown("---")
        st.subheader("📋 Queue Analysis")
        
        queue_df = pd.DataFrame([
            {
                'Queue ID': q.get('id', 'N/A'),
                'Vehicles': q.get('vehicle_count', 0),
                'Wait Time (s)': f"{q.get('wait_time', 0):.0f}",
                'Length': f"{q.get('length', 0)/10:.1f}m",
                'Confidence': f"{q.get('confidence', 0):.2f}"
            }
            for q in queues
        ])
        
        st.dataframe(queue_df, width="stretch")
    
    # Last update time
    st.markdown("---")
    st.caption(f"Last updated: {time.strftime('%H:%M:%S', time.localtime(st.session_state.last_update))}")
    
    # Auto-refresh trigger (only if enough time has passed)
    current_time = time.time()
    if current_time - st.session_state.last_update > st.session_state.refresh_rate:
        st.rerun()

if __name__ == "__main__":
    main()