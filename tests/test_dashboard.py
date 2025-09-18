"""
Test suite for EDGE-QI Real-time Dashboard

Tests dashboard functionality, data generation, visualization components,
and integration with EDGE-QI framework components.
"""

import pytest
import numpy as np
import time
import threading
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import dashboard components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from App.dashboard import (
    DashboardState,
    generate_simulation_data,
    create_queue_heatmap,
    create_traffic_flow_chart,
    create_edge_network_topology,
    create_performance_metrics_chart,
    init_dashboard_components
)

class TestDashboardState:
    """Test DashboardState class functionality"""
    
    def test_dashboard_state_initialization(self):
        """Test DashboardState initialization"""
        state = DashboardState()
        
        assert state.queue_data == []
        assert state.traffic_data == []
        assert state.edge_network_data == {}
        assert state.alerts == []
        assert state.performance_metrics == {}
        assert state.historical_data == []
        assert state.simulation_active == False
        assert state.simulation_thread is None
        
        # Component initialization
        assert state.edge_coordinator is None
        assert state.traffic_analyzer is None
        assert state.surveillance_task is None
        assert state.mqtt_client is None
    
    def test_dashboard_state_data_storage(self):
        """Test dashboard state data storage and retrieval"""
        state = DashboardState()
        
        # Test queue data storage
        queue_data = [
            {
                'id': 'test_queue',
                'type': 'vehicle',
                'location': (100, 200),
                'length': 15.5,
                'wait_time': 120.0,
                'density': 0.75,
                'confidence': 0.92,
                'timestamp': time.time()
            }
        ]
        state.queue_data = queue_data
        assert len(state.queue_data) == 1
        assert state.queue_data[0]['id'] == 'test_queue'
        
        # Test traffic data storage
        traffic_data = {
            'timestamp': time.time(),
            'total_vehicles': 45,
            'average_speed': 32.5,
            'congestion_level': 0.6,
            'flow_rate': 1.2
        }
        state.traffic_data.append(traffic_data)
        assert len(state.traffic_data) == 1
        assert state.traffic_data[0]['total_vehicles'] == 45
        
        # Test alerts storage
        alert = {
            'id': 'test_alert',
            'type': 'congestion',
            'severity': 'high',
            'message': 'Test alert message',
            'timestamp': time.time(),
            'location': (300, 400)
        }
        state.alerts.append(alert)
        assert len(state.alerts) == 1
        assert state.alerts[0]['type'] == 'congestion'

class TestSimulationData:
    """Test simulation data generation"""
    
    def test_generate_simulation_data_structure(self):
        """Test simulation data generation produces correct structure"""
        state = DashboardState()
        
        # Patch the global dashboard_state
        with patch('App.dashboard.dashboard_state', state):
            generate_simulation_data()
        
        # Check queue data structure
        assert len(state.queue_data) >= 3
        assert len(state.queue_data) <= 8
        
        for queue in state.queue_data:
            assert 'id' in queue
            assert 'type' in queue
            assert 'location' in queue
            assert 'length' in queue
            assert 'wait_time' in queue
            assert 'density' in queue
            assert 'confidence' in queue
            assert 'timestamp' in queue
            
            assert queue['type'] in ['vehicle', 'pedestrian', 'mixed']
            assert 0 <= queue['density'] <= 1
            assert 0.6 <= queue['confidence'] <= 0.95
    
    def test_generate_simulation_data_traffic(self):
        """Test traffic data generation"""
        state = DashboardState()
        
        with patch('App.dashboard.dashboard_state', state):
            generate_simulation_data()
        
        # Check traffic data structure
        assert len(state.traffic_data) == 1
        traffic = state.traffic_data[0]
        
        assert 'timestamp' in traffic
        assert 'total_vehicles' in traffic
        assert 'average_speed' in traffic
        assert 'congestion_level' in traffic
        assert 'flow_rate' in traffic
        assert 'intersections' in traffic
        
        assert 20 <= traffic['total_vehicles'] <= 100
        assert 15 <= traffic['average_speed'] <= 45
        assert 0.1 <= traffic['congestion_level'] <= 0.9
        
        # Check intersections data
        intersections = traffic['intersections']
        assert 'intersection_1' in intersections
        assert 'intersection_2' in intersections
        
        for intersection in intersections.values():
            assert 'queue_length' in intersection
            assert 'signal_phase' in intersection
            assert 'efficiency' in intersection
            assert intersection['signal_phase'] in ['green_ns', 'green_ew', 'red']
    
    def test_generate_simulation_data_edge_network(self):
        """Test edge network data generation"""
        state = DashboardState()
        
        with patch('App.dashboard.dashboard_state', state):
            generate_simulation_data()
        
        # Check edge network data structure
        network_data = state.edge_network_data
        assert 'edges' in network_data
        assert 'network_health' in network_data
        assert 'total_edges' in network_data
        assert 'active_edges' in network_data
        
        edges = network_data['edges']
        assert len(edges) == 3
        
        for edge_id, edge_info in edges.items():
            assert edge_id.startswith('edge_')
            assert 'status' in edge_info
            assert 'load' in edge_info
            assert 'queues_detected' in edge_info
            assert 'last_seen' in edge_info
            assert 'location' in edge_info
            
            assert edge_info['status'] in ['active', 'warning', 'error']
            assert 0 <= edge_info['load'] <= 1
    
    def test_generate_simulation_data_performance_metrics(self):
        """Test performance metrics generation"""
        state = DashboardState()
        
        with patch('App.dashboard.dashboard_state', state):
            generate_simulation_data()
        
        # Check performance metrics
        metrics = state.performance_metrics
        
        required_metrics = [
            'system_load', 'memory_usage', 'network_latency',
            'processing_rate', 'queue_detection_accuracy', 'consensus_success_rate'
        ]
        
        for metric in required_metrics:
            assert metric in metrics
        
        # Check metric ranges
        assert 0.2 <= metrics['system_load'] <= 0.8
        assert 0.3 <= metrics['memory_usage'] <= 0.7
        assert 10 <= metrics['network_latency'] <= 100
        assert 5 <= metrics['processing_rate'] <= 15
        assert 0.85 <= metrics['queue_detection_accuracy'] <= 0.98
        assert 0.9 <= metrics['consensus_success_rate'] <= 1.0

class TestVisualizationComponents:
    """Test dashboard visualization components"""
    
    def test_create_queue_heatmap_empty_data(self):
        """Test queue heatmap with empty data"""
        state = DashboardState()
        
        with patch('App.dashboard.dashboard_state', state):
            fig = create_queue_heatmap()
        
        # Should return empty figure without errors
        assert fig is not None
        assert hasattr(fig, 'data')
    
    def test_create_queue_heatmap_with_data(self):
        """Test queue heatmap with simulation data"""
        state = DashboardState()
        
        # Add sample queue data
        state.queue_data = [
            {
                'id': 'queue_1',
                'type': 'vehicle',
                'location': (100, 200),
                'length': 15.0,
                'wait_time': 120.0,
                'density': 0.75,
                'confidence': 0.92,
                'timestamp': time.time()
            },
            {
                'id': 'queue_2',
                'type': 'pedestrian',
                'location': (300, 400),
                'length': 8.0,
                'wait_time': 60.0,
                'density': 0.45,
                'confidence': 0.88,
                'timestamp': time.time()
            }
        ]
        
        with patch('App.dashboard.dashboard_state', state):
            fig = create_queue_heatmap()
        
        assert fig is not None
        assert len(fig.data) > 0
        
        # Check if scatter plot data is correct
        scatter_data = fig.data[0]
        assert len(scatter_data.x) == 2
        assert len(scatter_data.y) == 2
        assert scatter_data.x[0] == 100
        assert scatter_data.y[0] == 200
    
    def test_create_traffic_flow_chart_empty_data(self):
        """Test traffic flow chart with insufficient data"""
        state = DashboardState()
        
        with patch('App.dashboard.dashboard_state', state):
            fig = create_traffic_flow_chart()
        
        # Should return empty figure without errors
        assert fig is not None
        assert hasattr(fig, 'data')
    
    def test_create_traffic_flow_chart_with_data(self):
        """Test traffic flow chart with simulation data"""
        state = DashboardState()
        
        # Add sample traffic data
        current_time = time.time()
        for i in range(5):
            state.traffic_data.append({
                'timestamp': current_time - (4-i) * 10,
                'total_vehicles': 30 + i * 5,
                'average_speed': 25 + i * 2,
                'congestion_level': 0.3 + i * 0.1,
                'flow_rate': 1.0 + i * 0.1,
                'intersections': {}
            })
        
        with patch('App.dashboard.dashboard_state', state):
            fig = create_traffic_flow_chart()
        
        assert fig is not None
        assert len(fig.data) == 3  # Three subplots
        
        # Check if data is properly structured
        for trace in fig.data:
            assert len(trace.x) == 5
            assert len(trace.y) == 5
    
    def test_create_edge_network_topology_empty_data(self):
        """Test edge network topology with empty data"""
        state = DashboardState()
        
        with patch('App.dashboard.dashboard_state', state):
            fig = create_edge_network_topology()
        
        # Should return empty figure without errors
        assert fig is not None
        assert hasattr(fig, 'data')
    
    def test_create_edge_network_topology_with_data(self):
        """Test edge network topology with simulation data"""
        state = DashboardState()
        
        # Add sample edge network data
        state.edge_network_data = {
            'edges': {
                'edge_001': {
                    'status': 'active',
                    'load': 0.6,
                    'queues_detected': 3,
                    'last_seen': time.time(),
                    'location': (100, 100)
                },
                'edge_002': {
                    'status': 'warning',
                    'load': 0.8,
                    'queues_detected': 5,
                    'last_seen': time.time(),
                    'location': (300, 200)
                }
            },
            'network_health': 0.85,
            'total_edges': 2,
            'active_edges': 2
        }
        
        with patch('App.dashboard.dashboard_state', state):
            fig = create_edge_network_topology()
        
        assert fig is not None
        assert len(fig.data) >= 2  # At least node data + connections
        
        # Check node data
        node_data = fig.data[0]
        assert len(node_data.x) == 2
        assert len(node_data.y) == 2
        assert node_data.x[0] == 100
        assert node_data.y[0] == 100
    
    def test_create_performance_metrics_chart_empty_data(self):
        """Test performance metrics chart with empty data"""
        state = DashboardState()
        
        with patch('App.dashboard.dashboard_state', state):
            fig = create_performance_metrics_chart()
        
        # Should return empty figure without errors
        assert fig is not None
        assert hasattr(fig, 'data')
    
    def test_create_performance_metrics_chart_with_data(self):
        """Test performance metrics chart with simulation data"""
        state = DashboardState()
        
        # Add sample performance metrics
        state.performance_metrics = {
            'system_load': 0.65,
            'memory_usage': 0.45,
            'network_latency': 25.5,
            'processing_rate': 12.0,
            'queue_detection_accuracy': 0.92,
            'consensus_success_rate': 0.95
        }
        
        state.edge_network_data = {
            'network_health': 0.88
        }
        
        with patch('App.dashboard.dashboard_state', state):
            fig = create_performance_metrics_chart()
        
        assert fig is not None
        assert len(fig.data) == 6  # Six gauge charts
        
        # Check gauge values
        for i, trace in enumerate(fig.data):
            assert hasattr(trace, 'value')
            assert trace.value is not None

class TestComponentIntegration:
    """Test dashboard integration with EDGE-QI components"""
    
    @patch('App.dashboard.EdgeCoordinator')
    @patch('App.dashboard.TrafficFlowAnalyzer')
    @patch('App.dashboard.SurveillanceTask')
    def test_init_dashboard_components_success(self, mock_surveillance, mock_traffic, mock_coordinator):
        """Test successful component initialization"""
        state = DashboardState()
        
        # Mock successful initialization
        mock_coordinator.return_value = Mock()
        mock_traffic.return_value = Mock()
        mock_surveillance.return_value = Mock()
        
        with patch('App.dashboard.dashboard_state', state):
            result = init_dashboard_components()
        
        assert result == True
        assert state.edge_coordinator is not None
        assert state.traffic_analyzer is not None
        assert state.surveillance_task is not None
    
    @patch('App.dashboard.EdgeCoordinator')
    def test_init_dashboard_components_failure(self, mock_coordinator):
        """Test component initialization failure handling"""
        state = DashboardState()
        
        # Mock initialization failure
        mock_coordinator.side_effect = Exception("Initialization failed")
        
        with patch('App.dashboard.dashboard_state', state):
            result = init_dashboard_components()
        
        assert result == False
    
    def test_dashboard_state_component_reuse(self):
        """Test that components are reused if already initialized"""
        state = DashboardState()
        
        # Pre-initialize components
        mock_coordinator = Mock()
        mock_traffic = Mock()
        mock_surveillance = Mock()
        
        state.edge_coordinator = mock_coordinator
        state.traffic_analyzer = mock_traffic
        state.surveillance_task = mock_surveillance
        
        with patch('App.dashboard.dashboard_state', state):
            result = init_dashboard_components()
        
        assert result == True
        assert state.edge_coordinator is mock_coordinator
        assert state.traffic_analyzer is mock_traffic
        assert state.surveillance_task is mock_surveillance

class TestDataManagement:
    """Test dashboard data management features"""
    
    def test_traffic_data_limit(self):
        """Test traffic data is limited to 100 entries"""
        state = DashboardState()
        
        # Add exactly 100 entries
        current_time = time.time()
        for i in range(100):
            state.traffic_data.append({
                'timestamp': current_time - i,
                'total_vehicles': 30,
                'average_speed': 25,
                'congestion_level': 0.5,
                'flow_rate': 1.0,
                'intersections': {}
            })
        
        with patch('App.dashboard.dashboard_state', state):
            generate_simulation_data()
        
        # Should maintain only 100 entries after adding new one
        assert len(state.traffic_data) <= 100
    
    def test_alerts_limit(self):
        """Test alerts are limited to 20 entries"""
        state = DashboardState()
        
        # Add exactly 20 alerts
        current_time = time.time()
        for i in range(20):
            state.alerts.append({
                'id': f'alert_{i}',
                'type': 'test',
                'severity': 'low',
                'message': f'Test alert {i}',
                'timestamp': current_time - i,
                'location': (100, 200)
            })
        
        with patch('App.dashboard.dashboard_state', state):
            # Simulate alert generation (will add new alert if random condition met)
            with patch('numpy.random.random', return_value=0.05):  # Force alert generation
                generate_simulation_data()
        
        # Should maintain only 20 alerts
        assert len(state.alerts) <= 20

class TestDashboardFunctionality:
    """Test overall dashboard functionality"""
    
    def test_simulation_timing(self):
        """Test simulation data generation timing"""
        state = DashboardState()
        
        initial_time = state.last_update
        
        with patch('App.dashboard.dashboard_state', state):
            generate_simulation_data()
        
        # Should update last_update timestamp
        assert state.last_update > initial_time
    
    def test_data_consistency(self):
        """Test data consistency across components"""
        state = DashboardState()
        
        with patch('App.dashboard.dashboard_state', state):
            generate_simulation_data()
        
        # Check data consistency
        assert len(state.queue_data) >= 0
        assert len(state.traffic_data) >= 0
        assert isinstance(state.edge_network_data, dict)
        assert isinstance(state.performance_metrics, dict)
        
        # All timestamps should be recent
        current_time = time.time()
        for queue in state.queue_data:
            assert abs(queue['timestamp'] - current_time) < 5  # Within 5 seconds
    
    def test_edge_network_health_calculation(self):
        """Test edge network health calculation"""
        state = DashboardState()
        
        with patch('App.dashboard.dashboard_state', state):
            generate_simulation_data()
        
        network_data = state.edge_network_data
        
        if 'network_health' in network_data:
            assert 0.0 <= network_data['network_health'] <= 1.0
        
        if 'edges' in network_data:
            for edge_info in network_data['edges'].values():
                assert 0.0 <= edge_info['load'] <= 1.0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])