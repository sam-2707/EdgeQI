"""
EDGE-QI Enhanced Stable Dashboard

Production-ready dashboard with comprehensive error handling,
performance optimization, and deprecation fixes.
"""

import streamlit as st
import numpy as np
import pandas as pd
import time
import threading
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from Core.simulation.realtime_integrator import RealTimeDataIntegrator, RealTimeConfig
    from Core.simulation.realtime_simulator import RealTimeDataSimulator
    SIMULATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Simulation modules not available: {e}")
    SIMULATION_AVAILABLE = False

# Configure Streamlit page
st.set_page_config(
    page_title="EDGE-QI Enhanced Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False
if 'integrator' not in st.session_state:
    st.session_state.integrator = None
if 'simulator' not in st.session_state:
    st.session_state.simulator = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()
if 'data_cache' not in st.session_state:
    st.session_state.data_cache = {
        'frames': [],
        'detections': [],
        'queues': [],
        'metrics': {}
    }

def safe_initialize_components():
    """Safely initialize EDGE-QI components with error handling"""
    try:
        if not SIMULATION_AVAILABLE:
            st.error("❌ Simulation components not available. Please check installation.")
            return False
            
        if st.session_state.integrator is None:
            config = RealTimeConfig(
                fps=8,
                frame_width=1280,
                frame_height=720,  
                enable_queue_detection=True,
                enable_anomaly_detection=True,
                enable_bandwidth_optimization=True
            )
            st.session_state.integrator = RealTimeDataIntegrator(config)
            
        if st.session_state.simulator is None:
            st.session_state.simulator = RealTimeDataSimulator(
                fps=8, width=1280, height=720
            )
            
        return True
        
    except Exception as e:
        st.error(f"❌ Component initialization failed: {e}")
        return False

def start_simulation():
    """Start real-time simulation with robust error handling"""
    if not safe_initialize_components():
        return False
        
    try:
        if not st.session_state.simulation_running:
            st.session_state.integrator.start_real_time_processing()
            st.session_state.simulator.start_simulation()
            st.session_state.simulation_running = True
            st.success("✅ Real-time simulation started successfully!")
            return True
    except Exception as e:
        st.error(f"❌ Failed to start simulation: {e}")
        st.session_state.simulation_running = False
        return False

def stop_simulation():
    """Stop simulation with cleanup"""
    try:
        if st.session_state.simulation_running:
            if st.session_state.integrator:
                st.session_state.integrator.stop_real_time_processing()
            if st.session_state.simulator:
                st.session_state.simulator.stop_simulation()
            st.session_state.simulation_running = False
            st.success("⏹️ Simulation stopped successfully!")
    except Exception as e:
        st.error(f"❌ Error stopping simulation: {e}")
        st.session_state.simulation_running = False

def get_simulation_data():
    """Get latest simulation data with error handling"""
    try:
        if not st.session_state.simulation_running or not st.session_state.integrator:
            return None, [], [], {}
            
        # Get latest frame
        frame_data = st.session_state.simulator.get_latest_frame()
        frame = frame_data['frame'] if frame_data else None
        
        # Get detections and queues
        detections = st.session_state.integrator.get_current_detections()
        queues = st.session_state.integrator.get_current_queue_data()
        
        # Get performance metrics
        metrics = st.session_state.integrator.get_processing_stats()
        
        # Update cache
        st.session_state.data_cache.update({
            'frames': [frame] if frame is not None else [],
            'detections': detections,
            'queues': queues,
            'metrics': metrics
        })
        
        st.session_state.last_update = time.time()
        
        return frame, detections, queues, metrics
        
    except Exception as e:
        st.warning(f"⚠️ Data retrieval error: {e}")
        # Return cached data
        cache = st.session_state.data_cache
        return (
            cache['frames'][0] if cache['frames'] else None,
            cache['detections'],
            cache['queues'], 
            cache['metrics']
        )

def create_enhanced_metrics_chart(metrics):
    """Create comprehensive metrics visualization"""
    if not metrics:
        return go.Figure().add_annotation(text="No metrics available", showarrow=False)
        
    # Create subplot with gauges
    fig = go.Figure()
    
    # Add FPS gauge
    fps = metrics.get('fps', 0)
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=fps,
        domain={'x': [0, 0.48], 'y': [0.5, 1]},
        title={'text': "FPS"},
        delta={'reference': 8},
        gauge={
            'axis': {'range': [None, 15]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 5], 'color': "lightgray"},
                {'range': [5, 10], 'color': "yellow"},
                {'range': [10, 15], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 8
            }
        }
    ))
    
    # Add processing time gauge  
    processing_time = metrics.get('processing_time', 0)
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=processing_time * 1000,  # Convert to ms
        domain={'x': [0.52, 1], 'y': [0.5, 1]},
        title={'text': "Processing Time (ms)"},
        gauge={
            'axis': {'range': [None, 500]},
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, 100], 'color': "lightgreen"},
                {'range': [100, 250], 'color': "yellow"},
                {'range': [250, 500], 'color': "red"}
            ]
        }
    ))
    
    # Add statistics
    detections_count = metrics.get('total_detections', 0)
    queues_count = metrics.get('total_queues', 0)
    
    fig.add_trace(go.Bar(
        x=['Detections', 'Queues'],
        y=[detections_count, queues_count],
        xaxis='x2', yaxis='y2',
        name='Counts',
        marker_color=['blue', 'orange']
    ))
    
    # Update layout
    fig.update_layout(
        grid={'rows': 2, 'columns': 2},
        template='plotly_white',
        height=400,
        title="Enhanced System Metrics",
        xaxis2={'domain': [0, 1], 'anchor': 'y2'},
        yaxis2={'domain': [0, 0.4], 'anchor': 'x2'}
    )
    
    return fig

def main():
    """Enhanced main dashboard interface"""
    st.title("🚀 EDGE-QI Enhanced Real-time Dashboard")
    st.markdown("Production-ready intelligent edge computing framework with queue detection")
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Dashboard Controls")
        
        # System status
        if st.session_state.simulation_running:
            st.success("🟢 System: Running")
        else:
            st.warning("🟡 System: Stopped")
            
        # Control buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Start", disabled=st.session_state.simulation_running):
                start_simulation()
                st.rerun()
                
        with col2:
            if st.button("⏹️ Stop", disabled=not st.session_state.simulation_running):
                stop_simulation()
                st.rerun()
        
        # Settings
        st.markdown("---")
        st.subheader("⚙️ Settings")
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=True)
        refresh_interval = st.slider("Refresh interval (seconds)", 1, 10, 3)
        
        if auto_refresh and st.session_state.simulation_running:
            time.sleep(refresh_interval)
            st.rerun()
        
        # Manual refresh
        if st.button("🔄 Refresh Now"):
            st.rerun()
            
        # Statistics
        st.markdown("---")
        st.subheader("📊 Statistics")
        cache = st.session_state.data_cache
        st.metric("Detections", len(cache.get('detections', [])))
        st.metric("Queues", len(cache.get('queues', [])))
        st.metric("Last Update", 
                 time.strftime('%H:%M:%S', time.localtime(st.session_state.last_update)))
    
    # Main content
    if st.session_state.simulation_running or st.session_state.data_cache['frames']:
        
        # Get latest data
        frame, detections, queues, metrics = get_simulation_data()
        
        # Video display
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📹 Live Camera Feed")
            if frame is not None:
                # Convert BGR to RGB for display
                if len(frame.shape) == 3 and frame.shape[2] == 3:
                    frame_rgb = frame[:, :, ::-1]  # BGR to RGB
                    st.image(frame_rgb, channels="RGB", width="stretch")
                else:
                    st.image(frame, width="stretch")
            else:
                st.info("📷 Waiting for camera feed...")
                
        with col2:
            st.subheader("🎯 Detection Status")
            
            if detections:
                st.success(f"✅ {len(detections)} objects detected")
                
                # Show detection summary
                detection_types = {}
                for d in detections:
                    obj_type = d.get('class', 'unknown')
                    detection_types[obj_type] = detection_types.get(obj_type, 0) + 1
                
                for obj_type, count in detection_types.items():
                    st.metric(f"{obj_type.title()}", count)
            else:
                st.info("🔍 No objects detected")
                
            if queues:
                st.warning(f"🚦 {len(queues)} queues detected")
            else:
                st.success("✅ No queues detected")
        
        # Enhanced metrics
        st.markdown("---")
        st.subheader("📈 Enhanced Performance Metrics")
        
        if metrics:
            fig = create_enhanced_metrics_chart(metrics)
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("📊 Waiting for performance metrics...")
        
        # Detailed analytics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚗 Traffic Analytics")
            if detections:
                # Traffic density calculation
                total_vehicles = sum(1 for d in detections 
                                   if d.get('class', '').lower() in ['car', 'truck', 'bus', 'vehicle'])
                traffic_density = min(total_vehicles / 10.0, 1.0)  # Normalized
                
                st.metric("Traffic Density", f"{traffic_density:.1%}")
                st.metric("Total Vehicles", total_vehicles)
                
                # Confidence distribution
                confidences = [d.get('confidence', 0) for d in detections]
                if confidences:
                    avg_confidence = np.mean(confidences)
                    st.metric("Avg Confidence", f"{avg_confidence:.2%}")
        
        with col2:
            st.subheader("🔍 Detection Analysis")
            if detections:
                detection_df = pd.DataFrame([
                    {
                        'Type': d.get('class', 'unknown'),
                        'Confidence': f"{d.get('confidence', 0):.2%}",
                        'X': int(d.get('x', 0)),
                        'Y': int(d.get('y', 0))
                    }
                    for d in detections[:10]  # Show top 10
                ])
                
                st.dataframe(detection_df, width="stretch")
            else:
                st.info("No detection data available")
        
        # Queue analysis
        if queues:
            st.markdown("---")
            st.subheader("📋 Queue Analysis")
            
            queue_df = pd.DataFrame([
                {
                    'Queue ID': f"Q{i+1}",
                    'Length': q.get('length', 0),
                    'Position': f"({int(q.get('x', 0))}, {int(q.get('y', 0))})",
                    'Confidence': f"{q.get('confidence', 0):.2%}"
                }
                for i, q in enumerate(queues)
            ])
            
            st.dataframe(queue_df, width="stretch")
    
    else:
        # Welcome screen
        st.markdown("---")
        st.info("👋 Welcome to EDGE-QI Enhanced Dashboard! Click '▶️ Start' to begin real-time processing.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🎯 Features")
            st.markdown("""
            - **Real-time Queue Detection**
            - **Traffic Flow Analysis**  
            - **Object Detection & Tracking**
            - **Performance Monitoring**
            - **Enhanced Error Handling**
            """)
            
        with col2:
            st.subheader("🔧 Components")
            st.markdown("""
            - **Video Stream Processing**
            - **ML-based Analytics**
            - **Bandwidth Optimization**
            - **Multi-camera Support**
            - **Anomaly Detection**
            """)
            
        with col3:
            st.subheader("📊 Analytics")
            st.markdown("""
            - **Interactive Visualizations**
            - **Real-time Metrics**
            - **Performance Gauges**
            - **Detection Statistics**
            - **System Health Monitoring**
            """)

if __name__ == "__main__":
    main()