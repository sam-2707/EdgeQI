"""
Tests for Multi-Edge Collaboration System

Tests the distributed edge computing capabilities including:
- Edge communication protocols
- Consensus mechanisms  
- Distributed queue management
- Edge coordination
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, List

from Core.edge.edge_communication import (
    EdgeCommunication, EdgeMessage, MessageType, 
    create_queue_update_message, create_emergency_alert_message
)
from Core.edge.consensus_protocol import (
    ConsensusProtocol, ConsensusType, ConsensusProposal, ConsensusVote,
    propose_traffic_signal_change, propose_emergency_protocol
)
from Core.edge.distributed_queue_manager import (
    DistributedQueueManager, DistributedQueue, QueueEvent, QueueEventType
)
from Core.edge.edge_coordinator import (
    EdgeCoordinator, EdgeRole, CoordinationMode, EdgeNodeInfo
)

class TestEdgeCommunication:
    """Test edge communication protocols"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.edge_comm1 = EdgeCommunication("edge_001", 8765)
        self.edge_comm2 = EdgeCommunication("edge_002", 8766)
    
    def test_edge_communication_creation(self):
        """Test edge communication initialization"""
        assert self.edge_comm1.edge_id == "edge_001"
        assert self.edge_comm1.listen_port == 8765
        assert len(self.edge_comm1.connected_edges) == 0
        assert not self.edge_comm1.is_running
    
    def test_message_creation_and_validation(self):
        """Test EdgeMessage creation and validation"""
        message = EdgeMessage(
            message_id="test_001",
            sender_id="edge_001",
            receiver_id="edge_002",
            message_type=MessageType.QUEUE_UPDATE,
            timestamp=time.time(),
            data={"queue_length": 5, "wait_time": 120}
        )
        
        assert message.is_valid()
        assert not message.is_expired()
        assert message.message_type == MessageType.QUEUE_UPDATE
    
    def test_message_serialization(self):
        """Test message serialization and deserialization"""
        original_message = EdgeMessage(
            message_id="test_002",
            sender_id="edge_001", 
            receiver_id="edge_002",
            message_type=MessageType.HEARTBEAT,
            timestamp=time.time(),
            data={"status": "alive"}
        )
        
        # Serialize to JSON
        json_str = original_message.to_json()
        
        # Deserialize back
        restored_message = EdgeMessage.from_json(json_str)
        
        assert restored_message.message_id == original_message.message_id
        assert restored_message.sender_id == original_message.sender_id
        assert restored_message.message_type == original_message.message_type
        assert restored_message.data == original_message.data
    
    @pytest.mark.asyncio
    async def test_edge_communication_lifecycle(self):
        """Test edge communication service lifecycle"""
        # Start communication
        await self.edge_comm1.start()
        assert self.edge_comm1.is_running
        
        # Stop communication
        await self.edge_comm1.stop()
        assert not self.edge_comm1.is_running
    
    @pytest.mark.asyncio
    async def test_message_handler_registration(self):
        """Test message handler registration"""
        handler_called = False
        
        async def test_handler(message: EdgeMessage):
            nonlocal handler_called
            handler_called = True
        
        self.edge_comm1.register_handler(MessageType.QUEUE_UPDATE, test_handler)
        
        # Create test message
        test_message = EdgeMessage(
            message_id="test_003",
            sender_id="edge_002",
            receiver_id="edge_001", 
            message_type=MessageType.QUEUE_UPDATE,
            timestamp=time.time(),
            data={"test": "data"}
        )
        
        # Process message
        await self.edge_comm1.receive_message(test_message)
        assert handler_called
    
    def test_utility_message_creation(self):
        """Test utility functions for message creation"""
        # Test queue update message
        queue_msg = create_queue_update_message(
            "edge_001", "edge_002", 
            {"queues": [{"id": 1, "length": 10}]}
        )
        assert queue_msg.message_type == MessageType.QUEUE_UPDATE
        assert queue_msg.sender_id == "edge_001"
        
        # Test emergency alert message
        emergency_msg = create_emergency_alert_message(
            "edge_001",
            {"type": "fire", "location": (100, 200), "severity": 5}
        )
        assert emergency_msg.message_type == MessageType.EMERGENCY_ALERT
        assert emergency_msg.receiver_id == "broadcast"
        assert emergency_msg.priority == 10

class TestConsensusProtocol:
    """Test consensus mechanisms"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.comm1 = EdgeCommunication("edge_001", 8765)
        self.comm2 = EdgeCommunication("edge_002", 8766)
        
        self.consensus1 = ConsensusProtocol("edge_001", self.comm1)
        self.consensus2 = ConsensusProtocol("edge_002", self.comm2)
    
    def test_consensus_protocol_creation(self):
        """Test consensus protocol initialization"""
        assert self.consensus1.edge_id == "edge_001"
        assert self.consensus1.consensus_type == ConsensusType.SIMPLE_MAJORITY
        assert len(self.consensus1.active_proposals) == 0
    
    def test_proposal_evaluation(self):
        """Test proposal evaluation logic"""
        # Test traffic signal timing proposal
        signal_proposal = ConsensusProposal(
            proposal_id="test_signal_001",
            proposer_id="edge_001",
            proposal_type="traffic_signal_timing",
            proposal_data={
                "timing": {"green": 45, "red": 15},
                "traffic_load": 0.8,
                "expected_improvement": 0.3
            },
            timestamp=time.time(),
            deadline=time.time() + 30
        )
        
        # Should vote yes for high load and good improvement
        vote = self.consensus1._evaluate_proposal(signal_proposal)
        assert vote == True
        
        # Test emergency proposal
        emergency_proposal = ConsensusProposal(
            proposal_id="test_emergency_001", 
            proposer_id="edge_001",
            proposal_type="emergency_protocol",
            proposal_data={
                "emergency_level": 4,
                "confidence": 0.9
            },
            timestamp=time.time(),
            deadline=time.time() + 10
        )
        
        vote = self.consensus1._evaluate_proposal(emergency_proposal)
        assert vote == True
    
    def test_edge_weight_management(self):
        """Test edge voting weight management"""
        # Set custom weights
        self.consensus1.set_edge_weight("edge_002", 2.0)
        self.consensus1.set_edge_weight("edge_003", 0.5)
        
        assert self.consensus1._get_edge_weight("edge_002") == 2.0
        assert self.consensus1._get_edge_weight("edge_003") == 0.5
        assert self.consensus1._get_edge_weight("edge_001") == 1.0  # Self weight
    
    @pytest.mark.asyncio
    async def test_consensus_message_handling(self):
        """Test consensus message handling"""
        # Start both consensus protocols
        await self.comm1.start()
        await self.comm2.start()
        
        # Create a consensus request message
        proposal_data = {
            'proposal': {
                'proposal_id': 'test_consensus_001',
                'proposer_id': 'edge_001',
                'proposal_type': 'queue_priority',
                'proposal_data': {'queue_length': 15, 'priority_change': 2},
                'deadline': time.time() + 30,
                'priority': 3
            },
            'consensus_type': 'simple_majority'
        }
        
        request_message = EdgeMessage(
            message_id="consensus_req_001",
            sender_id="edge_001",
            receiver_id="edge_002",
            message_type=MessageType.CONSENSUS_REQUEST,
            timestamp=time.time(),
            data=proposal_data
        )
        
        # Handle the message
        await self.consensus2._handle_consensus_request(request_message)
        
        # Check that proposal was stored
        assert 'test_consensus_001' in self.consensus2.active_proposals
        
        # Clean up
        await self.comm1.stop()
        await self.comm2.stop()
    
    @pytest.mark.asyncio
    async def test_utility_consensus_functions(self):
        """Test utility functions for common consensus scenarios"""
        await self.comm1.start()
        
        # Test traffic signal change proposal
        with patch.object(self.consensus1, 'propose_decision') as mock_propose:
            mock_propose.return_value = Mock(decision=True, confidence=0.8)
            
            result = await propose_traffic_signal_change(
                self.consensus1,
                "intersection_001",
                {"green": 40, "red": 20},
                0.7,
                0.2
            )
            
            mock_propose.assert_called_once()
            args = mock_propose.call_args[0]
            assert args[0] == "traffic_signal_timing"
        
        # Test emergency protocol proposal
        with patch.object(self.consensus1, 'propose_decision') as mock_propose:
            mock_propose.return_value = Mock(decision=True, confidence=0.9)
            
            result = await propose_emergency_protocol(
                self.consensus1,
                "fire",
                (100.0, 200.0),
                5,
                0.95
            )
            
            mock_propose.assert_called_once()
            args = mock_propose.call_args[0]
            assert args[0] == "emergency_protocol"
        
        await self.comm1.stop()

class TestDistributedQueueManager:
    """Test distributed queue management"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.comm1 = EdgeCommunication("edge_001", 8765)
        self.comm2 = EdgeCommunication("edge_002", 8766)
        
        self.consensus1 = ConsensusProtocol("edge_001", self.comm1)
        self.consensus2 = ConsensusProtocol("edge_002", self.comm2)
        
        self.queue_mgr1 = DistributedQueueManager(
            "edge_001", self.comm1, self.consensus1, (100.0, 100.0)
        )
        self.queue_mgr2 = DistributedQueueManager(
            "edge_002", self.comm2, self.consensus2, (200.0, 200.0)
        )
    
    def test_distributed_queue_manager_creation(self):
        """Test distributed queue manager initialization"""
        assert self.queue_mgr1.edge_id == "edge_001"
        assert self.queue_mgr1.camera_position == (100.0, 100.0)
        assert len(self.queue_mgr1.global_queues) == 0
        assert len(self.queue_mgr1.local_queue_data) == 0
    
    @pytest.mark.asyncio
    async def test_local_queue_update(self):
        """Test local queue data updates"""
        queue_data = [
            {
                'id': 'queue_001',
                'type': 'vehicle',
                'center': (150, 150),
                'length': 25.0,
                'wait_time': 180.0,
                'density': 0.7,
                'confidence': 0.85
            },
            {
                'id': 'queue_002',
                'type': 'pedestrian',
                'center': (170, 130),
                'length': 15.0,
                'wait_time': 90.0,
                'density': 0.4,
                'confidence': 0.75
            }
        ]
        
        await self.queue_mgr1.update_local_queues(queue_data, "camera_001")
        
        # Check that local data was stored
        assert "edge_001" in self.queue_mgr1.local_queue_data
        edge_data = self.queue_mgr1.local_queue_data["edge_001"]
        assert len(edge_data.local_queues) == 2
        assert edge_data.camera_id == "camera_001"
        assert edge_data.traffic_density > 0
    
    def test_queue_correlation_calculation(self):
        """Test queue correlation calculations"""
        queue1 = {
            'center': (100, 100),
            'timestamp': time.time(),
            'direction': (1.0, 0.0),
            'confidence': 0.8
        }
        
        queue2 = {
            'center': (105, 102),  # Close to queue1
            'timestamp': time.time(),
            'direction': (0.9, 0.1),  # Similar direction
            'confidence': 0.7
        }
        
        correlation = self.queue_mgr1._calculate_queue_correlation(queue1, queue2)
        assert correlation > 0.5  # Should be correlated
        
        queue3 = {
            'center': (500, 500),  # Far from queue1
            'timestamp': time.time() - 300,  # Old timestamp
            'direction': (-1.0, 0.0),  # Opposite direction
            'confidence': 0.6
        }
        
        correlation = self.queue_mgr1._calculate_queue_correlation(queue1, queue3)
        assert correlation < 0.3  # Should not be correlated
    
    @pytest.mark.asyncio
    async def test_queue_event_creation(self):
        """Test queue event creation and processing"""
        queue_data = {
            'id': 'queue_test',
            'type': 'vehicle',
            'location': (120, 120),
            'length': 30.0,
            'confidence': 0.9
        }
        
        await self.queue_mgr1._create_queue_event(
            "queue_test_001",
            QueueEventType.QUEUE_FORMED,
            queue_data
        )
        
        # Check that event was created
        assert len(self.queue_mgr1.queue_events) > 0
        last_event = self.queue_mgr1.queue_events[-1]
        assert last_event.event_type == QueueEventType.QUEUE_FORMED
        assert last_event.queue_id == "queue_test_001"
        assert last_event.edge_id == "edge_001"
    
    def test_analytics_calculations(self):
        """Test queue analytics calculations"""
        # Test traffic density calculation
        queue_data = [
            {'length': 20.0, 'density': 0.6},
            {'length': 15.0, 'density': 0.4},
            {'length': 30.0, 'density': 0.8}
        ]
        
        density = self.queue_mgr1._calculate_traffic_density(queue_data)
        assert 0.0 <= density <= 1.0
        
        # Test flow rate calculation
        flow_rate = self.queue_mgr1._calculate_flow_rate(queue_data)
        assert flow_rate >= 0.0
    
    def test_coverage_area_calculation(self):
        """Test camera coverage area calculation"""
        coverage = self.queue_mgr1._get_coverage_area()
        assert len(coverage) == 4  # Rectangular area
        assert all(isinstance(point, tuple) and len(point) == 2 for point in coverage)
    
    @pytest.mark.asyncio
    async def test_queue_message_handling(self):
        """Test queue update message handling"""
        await self.comm1.start()
        
        # Create queue update message with event data
        event_data = {
            'event_id': 'event_001',
            'queue_id': 'queue_remote_001',
            'event_type': 'queue_formed',
            'timestamp': time.time(),
            'data': {'length': 20, 'location': (180, 180)},
            'confidence': 0.8
        }
        
        message = EdgeMessage(
            message_id="queue_update_001",
            sender_id="edge_002",
            receiver_id="edge_001",
            message_type=MessageType.QUEUE_UPDATE,
            timestamp=time.time(),
            data={'event': event_data}
        )
        
        await self.queue_mgr1._handle_queue_update(message)
        
        # Check that event was processed
        assert len(self.queue_mgr1.queue_events) > 0
        
        await self.comm1.stop()

class TestEdgeCoordinator:
    """Test edge coordination functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.coordinator1 = EdgeCoordinator(
            "edge_001", EdgeRole.LEADER, CoordinationMode.DISTRIBUTED, 8765, (100.0, 100.0)
        )
        self.coordinator2 = EdgeCoordinator(
            "edge_002", EdgeRole.FOLLOWER, CoordinationMode.DISTRIBUTED, 8766, (200.0, 200.0)  
        )
    
    def test_edge_coordinator_creation(self):
        """Test edge coordinator initialization"""
        assert self.coordinator1.edge_id == "edge_001"
        assert self.coordinator1.role == EdgeRole.LEADER
        assert self.coordinator1.coordination_mode == CoordinationMode.DISTRIBUTED
        assert self.coordinator1.camera_position == (100.0, 100.0)
        assert not self.coordinator1.is_running
    
    def test_capability_initialization(self):
        """Test edge capability initialization"""
        capabilities = self.coordinator1.edge_capabilities
        
        assert capabilities['queue_detection'] == True
        assert capabilities['traffic_analysis'] == True
        assert capabilities['consensus_participation'] == True
        assert 'max_concurrent_streams' in capabilities
        assert 'compute_power' in capabilities
    
    @pytest.mark.asyncio
    async def test_coordinator_lifecycle(self):
        """Test coordinator service lifecycle"""
        # Start coordinator
        await self.coordinator1.start()
        assert self.coordinator1.is_running
        assert len(self.coordinator1.coordination_tasks) > 0
        
        # Stop coordinator
        await self.coordinator1.stop()
        assert not self.coordinator1.is_running
    
    def test_load_calculation(self):
        """Test system load calculation"""
        # Set some performance metrics
        self.coordinator1.performance_metrics.update({
            'cpu_usage': 0.4,
            'memory_usage': 0.3
        })
        
        load = self.coordinator1._get_current_load()
        assert 0.0 <= load <= 1.0
    
    def test_distance_calculation(self):
        """Test distance calculation utility"""
        point1 = (0.0, 0.0)
        point2 = (3.0, 4.0)
        
        distance = self.coordinator1._calculate_distance(point1, point2)
        assert distance == 5.0  # 3-4-5 triangle
    
    @pytest.mark.asyncio
    async def test_coordination_request_processing(self):
        """Test coordination request processing"""
        # Test load balancing request
        load_data = {'requested_load': 0.3}
        response = await self.coordinator1._handle_load_balancing_request(
            load_data, "edge_002"
        )
        
        assert 'status' in response
        assert 'current_load' in response
        assert 'available_capacity' in response
        
        # Test capability exchange request
        cap_data = {
            'capabilities': {
                'queue_detection': True,
                'compute_power': 'high'
            }
        }
        response = await self.coordinator1._handle_capability_exchange_request(
            cap_data, "edge_002"
        )
        
        assert response['status'] == 'capabilities_shared'
        assert 'capabilities_data' in response
    
    @pytest.mark.asyncio
    async def test_emergency_response_handling(self):
        """Test emergency response coordination"""
        emergency_data = {
            'emergency_type': 'fire',
            'location': (150.0, 150.0),  # Near coordinator1
            'severity': 4
        }
        
        response = await self.coordinator1._handle_emergency_response_request(
            emergency_data, "edge_002"
        )
        
        assert response['status'] == 'acknowledged'
        assert 'can_assist' in response
        assert 'distance' in response
        assert 'estimated_response_time' in response
    
    def test_topology_management(self):
        """Test network topology management"""
        # Add edge node info
        node_info = EdgeNodeInfo(
            edge_id="edge_002",
            role=EdgeRole.FOLLOWER,
            capabilities={'queue_detection': True},
            location=(200.0, 200.0),
            status="active",
            load=0.3,
            last_seen=time.time(),
            performance_metrics={}
        )
        
        self.coordinator1.network_topology.nodes["edge_002"] = node_info
        
        # Test topology access
        topology = self.coordinator1.get_network_topology()
        assert "edge_002" in topology.nodes
        assert topology.nodes["edge_002"].load == 0.3
    
    def test_statistics_collection(self):
        """Test statistics collection"""
        stats = self.coordinator1.get_statistics()
        
        assert 'role' in stats
        assert 'connected_edges' in stats
        assert 'current_load' in stats
        assert 'uptime' in stats
        assert stats['role'] == 'leader'
    
    @pytest.mark.asyncio
    async def test_queue_data_processing(self):
        """Test queue data processing through coordinator"""
        queue_data = [
            {
                'id': 'coord_queue_001',
                'type': 'vehicle',
                'center': (120, 120),
                'length': 20.0,
                'wait_time': 150.0,
                'confidence': 0.8
            }
        ]
        
        await self.coordinator1.process_queue_data(queue_data, "camera_001")
        
        # Check that queue manager was updated
        local_data = self.coordinator1.queue_manager.local_queue_data
        assert "edge_001" in local_data
        assert len(local_data["edge_001"].local_queues) == 1

class TestMultiEdgeIntegration:
    """Integration tests for multi-edge scenarios"""
    
    def setup_method(self):
        """Set up test fixtures for integration testing"""
        self.coordinators = []
        
        # Create multiple edge coordinators
        for i in range(3):
            edge_id = f"edge_{i+1:03d}"
            coordinator = EdgeCoordinator(
                edge_id, 
                EdgeRole.FOLLOWER,
                CoordinationMode.DISTRIBUTED,
                8765 + i,
                (100.0 * (i+1), 100.0)
            )
            self.coordinators.append(coordinator)
    
    @pytest.mark.asyncio
    async def test_multi_edge_communication(self):
        """Test communication between multiple edge devices"""
        # Start all coordinators
        for coordinator in self.coordinators:
            await coordinator.start()
        
        # Simulate connections (in real scenario, would use actual networking)
        comm1 = self.coordinators[0].communication
        comm2 = self.coordinators[1].communication
        
        # Test message exchange
        test_message = EdgeMessage(
            message_id="integration_test_001",
            sender_id="edge_001",
            receiver_id="edge_002", 
            message_type=MessageType.HEARTBEAT,
            timestamp=time.time(),
            data={"status": "alive", "load": 0.3}
        )
        
        # Simulate message reception
        await comm2.receive_message(test_message)
        
        # Stop all coordinators
        for coordinator in self.coordinators:
            await coordinator.stop()
    
    @pytest.mark.asyncio
    async def test_distributed_consensus_scenario(self):
        """Test distributed consensus across multiple edges"""
        # Start coordinators
        for coordinator in self.coordinators[:2]:  # Use first 2
            await coordinator.start()
        
        consensus1 = self.coordinators[0].consensus
        consensus2 = self.coordinators[1].consensus
        
        # Set up voting weights
        consensus1.set_edge_weight("edge_002", 1.5)
        consensus2.set_edge_weight("edge_001", 1.2)
        
        # Create a test proposal
        proposal_data = {
            'intersection_id': 'test_intersection',
            'timing': {'green': 40, 'red': 20},
            'traffic_load': 0.8,
            'expected_improvement': 0.25
        }
        
        # Mock the consensus process
        with patch.object(consensus1, '_wait_for_consensus') as mock_wait:
            mock_result = Mock()
            mock_result.decision = True
            mock_result.confidence = 0.8
            mock_wait.return_value = mock_result
            
            result = await consensus1.propose_decision(
                "traffic_signal_timing",
                proposal_data,
                timeout=10.0
            )
            
            assert result.decision == True
        
        # Stop coordinators
        for coordinator in self.coordinators[:2]:
            await coordinator.stop()
    
    @pytest.mark.asyncio 
    async def test_queue_data_propagation(self):
        """Test queue data propagation across multiple edges"""
        # Start coordinators
        for coordinator in self.coordinators:
            await coordinator.start()
        
        # Simulate queue detection on edge 1
        queue_data = [
            {
                'id': 'propagation_test_queue',
                'type': 'vehicle',
                'center': (150, 100),
                'length': 35.0,
                'wait_time': 200.0,
                'density': 0.8,
                'confidence': 0.9
            }
        ]
        
        await self.coordinators[0].process_queue_data(queue_data)
        
        # Check that queue manager has the data
        queue_mgr = self.coordinators[0].queue_manager
        assert len(queue_mgr.local_queue_data) > 0
        
        # Stop coordinators
        for coordinator in self.coordinators:
            await coordinator.stop()
    
    def test_network_topology_formation(self):
        """Test network topology formation with multiple edges"""
        # Simulate network discovery
        for i, coordinator in enumerate(self.coordinators):
            for j, other_coordinator in enumerate(self.coordinators):
                if i != j:
                    # Add other edges to topology
                    node_info = EdgeNodeInfo(
                        edge_id=other_coordinator.edge_id,
                        role=EdgeRole.FOLLOWER,
                        capabilities=other_coordinator.edge_capabilities,
                        location=other_coordinator.camera_position,
                        status="active",
                        load=0.3,
                        last_seen=time.time(),
                        performance_metrics={}
                    )
                    coordinator.network_topology.nodes[other_coordinator.edge_id] = node_info
        
        # Verify topology
        for coordinator in self.coordinators:
            topology = coordinator.get_network_topology()
            assert len(topology.nodes) == len(self.coordinators) - 1  # All others
    
    def test_load_balancing_scenarios(self):
        """Test load balancing scenarios across edges"""
        # Set different loads for coordinators
        loads = [0.9, 0.3, 0.5]  # High, low, medium
        
        for coordinator, load in zip(self.coordinators, loads):
            coordinator.performance_metrics.update({
                'cpu_usage': load,
                'memory_usage': load * 0.8
            })
        
        # Check load calculations
        calculated_loads = [coord._get_current_load() for coord in self.coordinators]
        
        # Highest load should be from first coordinator
        assert calculated_loads[0] > calculated_loads[1]
        assert calculated_loads[0] > calculated_loads[2]
        
        # Lowest load should be from second coordinator
        assert calculated_loads[1] < calculated_loads[2]

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])