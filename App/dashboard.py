"""
EDGE-QI Real-time Dashboard

Advanced dashboard for real-time queue intelligence visualization, monitoring,
and management. Provides comprehensive insights into queue detection, traffic
analysis, multi-edge coordination, and system performance.

Features:
- Real-time queue visualizations and heatmaps
- Traffic flow analytics and signal optimization
- Multi-edge network topology and collaboration status
- Alert management and historical analytics
- Performance monitoring and system health
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import asyncio
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import threading
from dataclasses import asdict

# Import EDGE-QI components
try:
    from Core.queue.queue_detector import QueueDetector
    from Core.traffic.traffic_analyzer import TrafficFlowAnalyzer
    from Core.video.video_stream import VideoStreamProcessor
    from Core.edge.edge_coordinator import EdgeCoordinator, EdgeRole
    from Core.communication.mqtt_client import MqttClient
    from ML.models.vision.object_detector import YOLODetector
    from ML.tasks.surveillance_task import SurveillanceTask
    from Core.anomaly import QueueAnomalyDetector, AnomalyType, AnomalySeverity, QueueAnomaly
except ImportError as e:
    # For testing environment - create mock classes
    class QueueDetector: pass
    class TrafficFlowAnalyzer: 
        def __init__(self, width, height): pass
    class VideoStreamProcessor: pass
    class EdgeCoordinator: 
        def __init__(self, node_id, role, camera_position): pass
    class EdgeRole:
        COORDINATOR = "coordinator"
    class MqttClient: pass
    class YOLODetector: pass
    class SurveillanceTask:
        def __init__(self, detector_type, stream_sources): pass
    class QueueAnomalyDetector:
        def __init__(self): pass
    class AnomalyType:
        OVERCROWDING = "overcrowding"
        ABNORMAL_WAIT_TIME = "abnormal_wait_time"
        SUSPICIOUS_BEHAVIOR = "suspicious_behavior"
    class AnomalySeverity:
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        CRITICAL = "critical"
    class QueueAnomaly:
        def __init__(self, **kwargs): pass

# Dashboard configuration
st.set_page_config(
    page_title="EDGE-QI Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DashboardState:
    """Manages dashboard state and data"""
    
    def __init__(self):
        self.queue_data = []
        self.traffic_data = []
        self.edge_network_data = {}
        self.alerts = []
        self.anomalies = []  # New: Store detected anomalies
        self.performance_metrics = {}
        self.historical_data = []
        self.last_update = time.time()
        
        # System components
        self.edge_coordinator = None
        self.traffic_analyzer = None
        self.anomaly_detector = None  # New: Anomaly detection component
        self.surveillance_task = None
        self.mqtt_client = None
        
        # Simulation data for demo
        self.simulation_active = False
        self.simulation_thread = None

# Initialize dashboard state
if 'dashboard_state' not in st.session_state:
    st.session_state.dashboard_state = DashboardState()

dashboard_state = st.session_state.dashboard_state

def init_dashboard_components():
    """Initialize EDGE-QI components for the dashboard"""
    try:
        # Initialize edge coordinator
        if not dashboard_state.edge_coordinator:
            dashboard_state.edge_coordinator = EdgeCoordinator(
                node_id="dashboard_node",
                role=EdgeRole.COORDINATOR,
                camera_position=(500, 300)
            )
        
        # Initialize traffic analyzer
        if not dashboard_state.traffic_analyzer:
            dashboard_state.traffic_analyzer = TrafficFlowAnalyzer(
                width=1000, height=600
            )
        
        # Initialize anomaly detector
        if not dashboard_state.anomaly_detector:
            dashboard_state.anomaly_detector = QueueAnomalyDetector()
            
        return True
    except Exception as e:
        st.error(f"Error initializing components: {e}")
        return False

def generate_simulation_data():
    """Generate simulation data for dashboard demonstration"""
    current_time = time.time()
    
    # Generate queue data
    num_queues = np.random.randint(3, 8)
    queue_data = []
    
    for i in range(num_queues):
        queue_data.append({
            'id': f'queue_{i+1}',
            'type': np.random.choice(['vehicle', 'pedestrian', 'mixed']),
            'location': (
                np.random.uniform(50, 950),
                np.random.uniform(50, 550)
            ),
            'length': np.random.uniform(5, 50),
            'wait_time': np.random.uniform(30, 600),
            'density': np.random.uniform(0.1, 1.0),
            'confidence': np.random.uniform(0.6, 0.95),
            'timestamp': current_time
        })
    
    dashboard_state.queue_data = queue_data
    
    # Generate traffic data
    traffic_data = {
        'timestamp': current_time,
        'total_vehicles': np.random.randint(20, 100),
        'average_speed': np.random.uniform(15, 45),
        'congestion_level': np.random.uniform(0.1, 0.9),
        'flow_rate': np.random.uniform(0.5, 2.0),
        'intersections': {
            'intersection_1': {
                'queue_length': np.random.uniform(5, 30),
                'signal_phase': np.random.choice(['green_ns', 'green_ew', 'red']),
                'efficiency': np.random.uniform(0.6, 0.95)
            },
            'intersection_2': {
                'queue_length': np.random.uniform(3, 25),
                'signal_phase': np.random.choice(['green_ns', 'green_ew', 'red']),
                'efficiency': np.random.uniform(0.6, 0.95)
            }
        }
    }
    
    dashboard_state.traffic_data.append(traffic_data)
    
    # Keep only last 100 data points
    if len(dashboard_state.traffic_data) > 100:
        dashboard_state.traffic_data.pop(0)
    
    # Generate edge network data
    dashboard_state.edge_network_data = {
        'edges': {
            'edge_001': {
                'status': 'active',
                'load': np.random.uniform(0.2, 0.8),
                'queues_detected': len([q for q in queue_data if q['type'] == 'vehicle']),
                'last_seen': current_time,
                'location': (100, 100)
            },
            'edge_002': {
                'status': 'active',
                'load': np.random.uniform(0.1, 0.7),
                'queues_detected': len([q for q in queue_data if q['type'] == 'pedestrian']),
                'last_seen': current_time,
                'location': (300, 200)
            },
            'edge_003': {
                'status': np.random.choice(['active', 'warning', 'error']),
                'load': np.random.uniform(0.3, 0.9),
                'queues_detected': len([q for q in queue_data if q['type'] == 'mixed']),
                'last_seen': current_time - np.random.uniform(0, 30),
                'location': (500, 150)
            }
        },
        'network_health': np.random.uniform(0.7, 1.0),
        'total_edges': 3,
        'active_edges': 3
    }
    
    # Generate alerts
    if np.random.random() < 0.1:  # 10% chance of new alert
        alert_types = ['congestion', 'anomaly', 'system_warning', 'optimization']
        alert = {
            'id': f'alert_{int(current_time)}',
            'type': np.random.choice(alert_types),
            'severity': np.random.choice(['low', 'medium', 'high', 'critical']),
            'message': f"Sample alert generated at {datetime.fromtimestamp(current_time).strftime('%H:%M:%S')}",
            'timestamp': current_time,
            'location': (np.random.uniform(0, 1000), np.random.uniform(0, 600))
        }
        dashboard_state.alerts.append(alert)
        
        # Keep only last 20 alerts
        if len(dashboard_state.alerts) > 20:
            dashboard_state.alerts.pop(0)
    
    # Generate anomalies (15% chance of new anomaly)
    if np.random.random() < 0.15:
        anomaly_types = ['overcrowding', 'abnormal_wait_time', 'queue_abandonment', 
                        'suspicious_behavior', 'flow_disruption']
        severities = ['low', 'medium', 'high', 'critical']
        weights = [0.5, 0.3, 0.15, 0.05]  # Most anomalies are low/medium severity
        
        anomaly = {
            'id': f'anomaly_{int(current_time)}',
            'type': np.random.choice(anomaly_types),
            'severity': np.random.choice(severities, p=weights),
            'queue_id': f'queue_{np.random.randint(1, 8)}',
            'confidence': np.random.uniform(0.7, 0.95),
            'timestamp': current_time,
            'location': (np.random.uniform(0, 1000), np.random.uniform(0, 600)),
            'description': f"Anomaly detected in queue monitoring system"
        }
        dashboard_state.anomalies.append(anomaly)
        
        # Keep only last 50 anomalies
        if len(dashboard_state.anomalies) > 50:
            dashboard_state.anomalies.pop(0)
    
    # Generate performance metrics
    dashboard_state.performance_metrics = {
        'system_load': np.random.uniform(0.2, 0.8),
        'memory_usage': np.random.uniform(0.3, 0.7),
        'network_latency': np.random.uniform(10, 100),
        'processing_rate': np.random.uniform(5, 15),
        'queue_detection_accuracy': np.random.uniform(0.85, 0.98),
        'consensus_success_rate': np.random.uniform(0.9, 1.0)
    }
    
    dashboard_state.last_update = current_time

def start_simulation():
    """Start data simulation in background thread"""
    def simulation_loop():
        while dashboard_state.simulation_active:
            generate_simulation_data()
            time.sleep(2)  # Update every 2 seconds
    
    if not dashboard_state.simulation_active:
        dashboard_state.simulation_active = True
        dashboard_state.simulation_thread = threading.Thread(target=simulation_loop)
        dashboard_state.simulation_thread.daemon = True
        dashboard_state.simulation_thread.start()

def stop_simulation():
    """Stop data simulation"""
    dashboard_state.simulation_active = False

def create_queue_heatmap():
    """Create heatmap visualization of queue densities"""
    if not dashboard_state.queue_data:
        return go.Figure()
    
    # Create grid for heatmap
    x_coords = [q['location'][0] for q in dashboard_state.queue_data]
    y_coords = [q['location'][1] for q in dashboard_state.queue_data]
    densities = [q['density'] for q in dashboard_state.queue_data]
    
    fig = go.Figure(data=go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers',
        marker=dict(
            size=[d * 30 + 10 for d in densities],
            color=densities,
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="Queue Density"),
            line=dict(width=2, color='black')
        ),
        text=[f"Queue {q['id']}<br>Type: {q['type']}<br>Length: {q['length']:.1f}<br>Wait: {q['wait_time']:.0f}s"
              for q in dashboard_state.queue_data],
        hovertemplate='%{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Queue Density Heatmap",
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate",
        height=400,
        showlegend=False
    )
    
    return fig

def create_traffic_flow_chart():
    """Create traffic flow analysis chart"""
    if len(dashboard_state.traffic_data) < 2:
        return go.Figure()
    
    timestamps = [datetime.fromtimestamp(d['timestamp']) for d in dashboard_state.traffic_data]
    vehicle_counts = [d['total_vehicles'] for d in dashboard_state.traffic_data]
    avg_speeds = [d['average_speed'] for d in dashboard_state.traffic_data]
    congestion_levels = [d['congestion_level'] for d in dashboard_state.traffic_data]
    
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Vehicle Count', 'Average Speed (km/h)', 'Congestion Level'),
        vertical_spacing=0.08
    )
    
    fig.add_trace(
        go.Scatter(x=timestamps, y=vehicle_counts, name='Vehicles', line=dict(color='blue')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=timestamps, y=avg_speeds, name='Speed', line=dict(color='green')),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=timestamps, y=congestion_levels, name='Congestion', line=dict(color='red')),
        row=3, col=1
    )
    
    fig.update_layout(height=500, showlegend=False, title="Traffic Flow Analytics")
    return fig

def create_edge_network_topology():
    """Create edge network topology visualization"""
    if not dashboard_state.edge_network_data.get('edges'):
        return go.Figure()
    
    edges = dashboard_state.edge_network_data['edges']
    
    # Node positions
    x_coords = [info['location'][0] for info in edges.values()]
    y_coords = [info['location'][1] for info in edges.values()]
    
    # Node colors based on status
    status_colors = {'active': 'green', 'warning': 'orange', 'error': 'red'}
    colors = [status_colors.get(info['status'], 'gray') for info in edges.values()]
    
    # Node sizes based on load
    sizes = [info['load'] * 50 + 20 for info in edges.values()]
    
    fig = go.Figure(data=go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(width=2, color='black')
        ),
        text=list(edges.keys()),
        textposition="middle center",
        textfont=dict(color='white', size=10),
        hovertemplate='<b>%{text}</b><br>' +
                      'Load: %{customdata[0]:.1%}<br>' +
                      'Status: %{customdata[1]}<br>' +
                      'Queues: %{customdata[2]}<extra></extra>',
        customdata=[[info['load'], info['status'], info['queues_detected']] 
                   for info in edges.values()]
    ))
    
    # Add connections between edges (simplified)
    for i, edge1 in enumerate(edges.keys()):
        for j, edge2 in enumerate(edges.keys()):
            if i < j:  # Avoid duplicate connections
                fig.add_trace(go.Scatter(
                    x=[x_coords[i], x_coords[j]],
                    y=[y_coords[i], y_coords[j]],
                    mode='lines',
                    line=dict(color='gray', width=1, dash='dot'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
    
    fig.update_layout(
        title="Edge Network Topology",
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate",
        height=400,
        showlegend=False
    )
    
    return fig

def create_anomaly_detection_chart():
    """Create anomaly detection visualization"""
    anomalies = dashboard_state.anomalies
    
    if not anomalies:
        # Create empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="No anomalies detected",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font_size=20, font_color="gray"
        )
        fig.update_layout(
            height=400,
            title="Anomaly Detection Timeline",
            xaxis_title="Time",
            yaxis_title="Anomaly Count"
        )
        return fig
    
    # Group anomalies by time periods (last 24 hours, 1-hour bins)
    current_time = time.time()
    time_bins = []
    anomaly_counts = []
    severity_data = {'low': [], 'medium': [], 'high': [], 'critical': []}
    
    for i in range(24):
        bin_start = current_time - (24 - i) * 3600
        bin_end = bin_start + 3600
        
        # Count anomalies in this time bin
        bin_anomalies = [a for a in anomalies 
                        if bin_start <= a.get('timestamp', 0) < bin_end]
        
        time_bins.append(time.strftime('%H:00', time.localtime(bin_start)))
        anomaly_counts.append(len(bin_anomalies))
        
        # Count by severity
        for severity in ['low', 'medium', 'high', 'critical']:
            count = len([a for a in bin_anomalies 
                        if a.get('severity', '').lower() == severity])
            severity_data[severity].append(count)
    
    # Create stacked bar chart
    fig = go.Figure()
    
    colors = {
        'critical': '#FF0000',
        'high': '#FF8C00', 
        'medium': '#FFD700',
        'low': '#90EE90'
    }
    
    for severity, data in severity_data.items():
        fig.add_trace(go.Bar(
            name=severity.title(),
            x=time_bins,
            y=data,
            marker_color=colors[severity]
        ))
    
    fig.update_layout(
        height=400,
        title="Anomaly Detection Timeline (Last 24 Hours)",
        xaxis_title="Time (Hour)",
        yaxis_title="Anomaly Count",
        barmode='stack',
        showlegend=True
    )
    
    return fig

def create_performance_metrics_chart():
    """Create performance metrics dashboard"""
    metrics = dashboard_state.performance_metrics
    
    if not metrics:
        return go.Figure()
    
    # Create gauge charts for key metrics
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=('System Load', 'Memory Usage', 'Processing Rate',
                       'Detection Accuracy', 'Network Health', 'Consensus Rate'),
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
               [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]]
    )
    
    # System Load
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=metrics.get('system_load', 0) * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "System Load (%)"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "darkblue"},
               'steps': [{'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 85], 'color': "yellow"},
                        {'range': [85, 100], 'color': "red"}],
               'threshold': {'line': {'color': "red", 'width': 4},
                           'thickness': 0.75, 'value': 90}}
    ), row=1, col=1)
    
    # Memory Usage
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=metrics.get('memory_usage', 0) * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Memory (%)"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "green"}}
    ), row=1, col=2)
    
    # Processing Rate
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=metrics.get('processing_rate', 0),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Processing Rate (FPS)"},
        gauge={'axis': {'range': [None, 20]},
               'bar': {'color': "orange"}}
    ), row=1, col=3)
    
    # Detection Accuracy
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=metrics.get('queue_detection_accuracy', 0) * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Detection Accuracy (%)"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "purple"}}
    ), row=2, col=1)
    
    # Network Health
    network_health = dashboard_state.edge_network_data.get('network_health', 0) * 100
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=network_health,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Network Health (%)"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "cyan"}}
    ), row=2, col=2)
    
    # Consensus Success Rate
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=metrics.get('consensus_success_rate', 0) * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Consensus Success (%)"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "magenta"}}
    ), row=2, col=3)
    
    fig.update_layout(height=500, title="System Performance Metrics")
    return fig

def display_alerts_panel():
    """Display alerts and notifications panel"""
    st.subheader("🚨 Alerts & Notifications")
    
    if not dashboard_state.alerts:
        st.info("No active alerts")
        return
    
    # Sort alerts by timestamp (newest first)
    sorted_alerts = sorted(dashboard_state.alerts, key=lambda x: x['timestamp'], reverse=True)
    
    for alert in sorted_alerts[:10]:  # Show last 10 alerts
        severity_colors = {
            'critical': '🔴',
            'high': '🟠', 
            'medium': '🟡',
            'low': '🟢'
        }
        
        icon = severity_colors.get(alert['severity'], '⚪')
        timestamp = datetime.fromtimestamp(alert['timestamp']).strftime('%H:%M:%S')
        
        with st.expander(f"{icon} {alert['type'].title()} - {timestamp}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Message:** {alert['message']}")
                st.write(f"**Severity:** {alert['severity']}")
                st.write(f"**Location:** ({alert['location'][0]:.0f}, {alert['location'][1]:.0f})")
            with col2:
                if st.button(f"Dismiss", key=f"dismiss_{alert['id']}"):
                    dashboard_state.alerts.remove(alert)
                    st.rerun()

def display_queue_statistics():
    """Display queue statistics summary"""
    if not dashboard_state.queue_data:
        return
    
    total_queues = len(dashboard_state.queue_data)
    avg_wait_time = np.mean([q['wait_time'] for q in dashboard_state.queue_data])
    max_queue_length = max([q['length'] for q in dashboard_state.queue_data])
    avg_density = np.mean([q['density'] for q in dashboard_state.queue_data])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Queues", total_queues)
    
    with col2:
        st.metric("Avg Wait Time", f"{avg_wait_time:.1f}s")
    
    with col3:
        st.metric("Max Queue Length", f"{max_queue_length:.1f}")
    
    with col4:
        st.metric("Avg Density", f"{avg_density:.2f}")

def main_dashboard():
    """Main dashboard interface"""
    
    # Header
    st.title("🚦 EDGE-QI Real-time Dashboard")
    st.markdown("**Edge-based Queue Intelligence Framework for Smart Surveillance and Traffic Management**")
    
    # Sidebar controls
    st.sidebar.title("Dashboard Controls")
    
    # Simulation controls
    st.sidebar.subheader("Data Simulation")
    if st.sidebar.button("Start Simulation"):
        start_simulation()
        st.sidebar.success("Simulation started")
    
    if st.sidebar.button("Stop Simulation"):
        stop_simulation()
        st.sidebar.success("Simulation stopped")
    
    # Auto-refresh
    auto_refresh = st.sidebar.checkbox("Auto Refresh (2s)", value=True)
    
    if auto_refresh and dashboard_state.simulation_active:
        time.sleep(2)
        st.rerun()
    
    # Manual refresh
    if st.sidebar.button("Manual Refresh"):
        st.rerun()
    
    # Status indicators
    st.sidebar.subheader("System Status")
    simulation_status = "🟢 Running" if dashboard_state.simulation_active else "🔴 Stopped"
    st.sidebar.write(f"Simulation: {simulation_status}")
    
    last_update = datetime.fromtimestamp(dashboard_state.last_update).strftime('%H:%M:%S')
    st.sidebar.write(f"Last Update: {last_update}")
    
    # Main content area
    if not dashboard_state.simulation_active and not dashboard_state.queue_data:
        st.warning("Start simulation to see dashboard data")
        return
    
    # Queue Analytics Section
    st.header("📊 Queue Analytics")
    
    # Queue statistics
    display_queue_statistics()
    
    # Queue visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_queue_heatmap(), use_container_width=True)
    
    with col2:
        # Queue types distribution
        if dashboard_state.queue_data:
            queue_types = [q['type'] for q in dashboard_state.queue_data]
            type_counts = pd.Series(queue_types).value_counts()
            
            fig = px.pie(values=type_counts.values, names=type_counts.index, 
                        title="Queue Types Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    # Traffic Analytics Section
    st.header("🚗 Traffic Analytics")
    st.plotly_chart(create_traffic_flow_chart(), use_container_width=True)
    
    # Anomaly Detection Section
    st.header("🚨 Anomaly Detection")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(create_anomaly_detection_chart(), use_container_width=True)
    
    with col2:
        # Anomaly statistics
        anomalies = dashboard_state.anomalies
        if anomalies:
            # Recent anomalies count
            recent_anomalies = [a for a in anomalies if time.time() - a.get('timestamp', 0) < 3600]  # Last hour
            st.metric("Recent Anomalies", len(recent_anomalies))
            
            # Severity distribution
            severity_counts = {}
            for anomaly in recent_anomalies:
                severity = anomaly.get('severity', 'unknown')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            if severity_counts:
                st.subheader("Severity Distribution")
                for severity, count in severity_counts.items():
                    severity_icon = {
                        'low': '🟢',
                        'medium': '🟡', 
                        'high': '🟠',
                        'critical': '🔴'
                    }.get(severity.lower(), '⚪')
                    st.write(f"{severity_icon} {severity.title()}: {count}")
            
            # Latest anomalies
            st.subheader("Latest Anomalies")
            for anomaly in sorted(anomalies, key=lambda x: x.get('timestamp', 0), reverse=True)[:5]:
                severity_color = {
                    'low': 'green',
                    'medium': 'orange',
                    'high': 'red',
                    'critical': 'red'
                }.get(anomaly.get('severity', '').lower(), 'gray')
                
                st.markdown(f":{severity_color}[{anomaly.get('type', 'Unknown')} - {anomaly.get('severity', 'Unknown')}]")
                st.caption(f"Queue {anomaly.get('queue_id', 'N/A')} - {time.strftime('%H:%M:%S', time.localtime(anomaly.get('timestamp', 0)))}")
        else:
            st.info("No anomalies detected")
    
    # Multi-Edge Network Section
    st.header("🌐 Multi-Edge Network")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(create_edge_network_topology(), use_container_width=True)
    
    with col2:
        # Edge network statistics
        if dashboard_state.edge_network_data:
            network_data = dashboard_state.edge_network_data
            st.metric("Active Edges", network_data.get('active_edges', 0))
            st.metric("Network Health", f"{network_data.get('network_health', 0)*100:.1f}%")
            
            # Edge status list
            st.subheader("Edge Status")
            for edge_id, info in network_data.get('edges', {}).items():
                status_icon = {'active': '🟢', 'warning': '🟡', 'error': '🔴'}.get(info['status'], '⚪')
                st.write(f"{status_icon} {edge_id}: {info['load']*100:.1f}% load")
    
    # Performance Metrics Section
    st.header("⚡ Performance Metrics")
    st.plotly_chart(create_performance_metrics_chart(), use_container_width=True)
    
    # Alerts Section
    display_alerts_panel()
    
    # Additional Information
    with st.expander("📋 System Information"):
        st.subheader("Component Status")
        
        components_status = {
            "Edge Coordinator": "✅ Active" if dashboard_state.edge_coordinator else "❌ Inactive",
            "Traffic Analyzer": "✅ Active" if dashboard_state.traffic_analyzer else "❌ Inactive", 
            "Surveillance Task": "✅ Active" if dashboard_state.surveillance_task else "❌ Inactive",
            "Data Simulation": "✅ Running" if dashboard_state.simulation_active else "🔴 Stopped"
        }
        
        for component, status in components_status.items():
            st.write(f"**{component}:** {status}")
        
        st.subheader("Recent Queue Data")
        if dashboard_state.queue_data:
            df = pd.DataFrame(dashboard_state.queue_data)
            st.dataframe(df, use_container_width=True)

def create_dashboard():
    """Main entry point for the dashboard"""
    # Initialize components
    init_dashboard_components()
    
    # Run main dashboard
    main_dashboard()

if __name__ == "__main__":
    create_dashboard()