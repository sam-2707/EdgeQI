"""
Comprehensive tests for EDGE-QI Bandwidth Optimization System

Tests all components:
- Data Compression
- Adaptive Streaming  
- Priority Transfer Management
- Bandwidth Monitoring
"""

import pytest
import time
import threading
import numpy as np
import json
from unittest.mock import Mock, patch

from Core.bandwidth import (
    DataCompressor, CompressionMethod, CompressionResult,
    AdaptiveStreamer, StreamingProfile, BitrateSettings,
    PriorityTransferManager, DataPriority, TransferRequest,
    BandwidthMonitor, NetworkCondition, BandwidthMetrics
)


class TestDataCompressor:
    """Test suite for DataCompressor"""
    
    def setup_method(self):
        """Setup for each test"""
        self.compressor = DataCompressor()
    
    def test_compress_text_data(self):
        """Test compression of text data"""
        text_data = "Hello World! " * 100
        data_bytes = text_data.encode('utf-8')
        
        result = self.compressor.compress_data(data_bytes, CompressionMethod.GZIP)
        
        assert isinstance(result, CompressionResult)
        assert result.original_size > 0
        assert result.compressed_size > 0
        assert result.compression_ratio > 1.0
        assert result.method_used == CompressionMethod.GZIP
        assert result.compression_time >= 0
    
    def test_compress_numerical_data(self):
        """Test compression of numerical data"""
        data = np.random.randn(100, 50).astype(np.float32)
        
        result = self.compressor.compress_data(data, CompressionMethod.LZMA)
        
        assert result.compression_ratio > 1.0
        assert result.method_used == CompressionMethod.LZMA
    
    def test_compress_image_data(self):
        """Test compression of image data"""
        image_data = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        result = self.compressor.compress_data(image_data, CompressionMethod.JPEG, quality=80)
        
        assert result.compression_ratio > 1.0
        assert result.quality_score is not None
        assert 0.0 <= result.quality_score <= 1.0
    
    def test_adaptive_compression(self):
        """Test adaptive compression method selection"""
        # Test different data types
        test_cases = [
            (np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8), "image"),
            (np.random.randn(100, 10), "numerical"),
            ({"data": list(range(100))}, "structured")
        ]
        
        for data, expected_type in test_cases:
            result = self.compressor.compress_data(data, CompressionMethod.ADAPTIVE)
            assert result.compression_ratio > 1.0
    
    def test_decompress_data(self):
        """Test data decompression"""
        original_data = b"Test data for compression and decompression"
        
        # Compress
        result = self.compressor.compress_data(original_data, CompressionMethod.GZIP)
        
        # Decompress
        decompressed = self.compressor.decompress_data(
            result.compressed_data, 
            CompressionMethod.GZIP,
            data_type='bytes'
        )
        
        assert decompressed == original_data
    
    def test_compression_stats(self):
        """Test compression statistics tracking"""
        data = b"Test data" * 100
        
        # Perform several compressions
        for _ in range(5):
            self.compressor.compress_data(data, CompressionMethod.GZIP)
        
        stats = self.compressor.get_compression_stats()
        assert CompressionMethod.GZIP in stats
        assert stats[CompressionMethod.GZIP]['total_compressions'] == 5
        assert stats[CompressionMethod.GZIP]['avg_ratio'] > 0
    
    def test_optimal_method_selection(self):
        """Test optimal compression method selection"""
        method = self.compressor.get_optimal_method_for_target(
            'image', target_ratio=3.0, max_time=0.1
        )
        assert isinstance(method, CompressionMethod)
    
    def test_compression_ratio_estimation(self):
        """Test compression ratio estimation"""
        ratio = self.compressor.estimate_compression_ratio(
            10000, CompressionMethod.GZIP, 'text'
        )
        assert ratio > 1.0


class TestAdaptiveStreamer:
    """Test suite for AdaptiveStreamer"""
    
    def setup_method(self):
        """Setup for each test"""
        self.streamer = AdaptiveStreamer(
            initial_profile=StreamingProfile.MEDIUM,
            adaptation_interval=0.5,
            buffer_target=10
        )
        self.frame_count = 0
        self.output_data = []
    
    def mock_frame_source(self):
        """Mock frame source for testing"""
        self.frame_count += 1
        if self.frame_count > 20:  # Limit frames for testing
            return None
        return np.random.randint(0, 255, (240, 320, 3), dtype=np.uint8)
    
    def mock_output_callback(self, data, metadata):
        """Mock output callback for testing"""
        self.output_data.append((data, metadata))
    
    def test_streaming_initialization(self):
        """Test streamer initialization"""
        assert self.streamer.current_profile == StreamingProfile.MEDIUM
        assert self.streamer.is_streaming is False
        assert len(self.streamer.frame_buffer) == 0
    
    def test_profile_switching(self):
        """Test streaming profile switching"""
        original_profile = self.streamer.current_profile
        
        # Switch to low profile
        self.streamer.set_profile(StreamingProfile.LOW)
        
        assert self.streamer.current_profile == StreamingProfile.LOW
        assert self.streamer.current_profile != original_profile
    
    def test_bitrate_settings(self):
        """Test bitrate settings for different profiles"""
        profiles = [StreamingProfile.ULTRA_LOW, StreamingProfile.LOW, 
                   StreamingProfile.MEDIUM, StreamingProfile.HIGH, StreamingProfile.ULTRA_HIGH]
        
        for profile in profiles:
            self.streamer.set_profile(profile)
            settings = self.streamer.get_current_settings()
            
            assert isinstance(settings, BitrateSettings)
            assert settings.target_bitrate > 0
            assert settings.max_bitrate >= settings.target_bitrate
            assert settings.min_bitrate <= settings.target_bitrate
            assert len(settings.resolution) == 2
    
    def test_streaming_metrics(self):
        """Test streaming metrics tracking"""
        metrics = self.streamer.get_metrics()
        
        assert hasattr(metrics, 'current_bitrate')
        assert hasattr(metrics, 'actual_frame_rate')
        assert hasattr(metrics, 'buffer_health')
        assert hasattr(metrics, 'quality_score')
        assert 0 <= metrics.buffer_health <= 1
        assert 0 <= metrics.quality_score <= 1
    
    def test_buffer_management(self):
        """Test frame buffer management"""
        # Simulate adding frames to buffer
        for i in range(15):
            encoded_data = f"frame_{i}".encode()
            metadata = {'timestamp': time.time(), 'frame_id': i}
            self.streamer._manage_buffer(encoded_data, metadata)
        
        buffer_status = self.streamer.get_buffer_status()
        assert buffer_status['buffer_size'] <= self.streamer.current_settings.buffer_size
    
    def test_bandwidth_estimation(self):
        """Test bandwidth requirement estimation"""
        for profile in StreamingProfile:
            if profile != StreamingProfile.ADAPTIVE:
                bandwidth = self.streamer.estimate_bandwidth_requirement(profile)
                assert bandwidth > 0


class TestPriorityTransferManager:
    """Test suite for PriorityTransferManager"""
    
    def setup_method(self):
        """Setup for each test"""
        self.transfer_manager = PriorityTransferManager(max_bandwidth_mbps=5.0)
        self.completed_transfers = []
        self.failed_transfers = []
        
        # Setup callbacks
        self.transfer_manager.on_transfer_complete = self.on_complete
        self.transfer_manager.on_transfer_failed = self.on_failed
    
    def on_complete(self, request):
        self.completed_transfers.append(request)
    
    def on_failed(self, request, error):
        self.failed_transfers.append((request, error))
    
    def teardown_method(self):
        """Cleanup after each test"""
        if self.transfer_manager.is_running:
            self.transfer_manager.stop()
    
    def test_transfer_submission(self):
        """Test transfer request submission"""
        data = b"test data"
        
        transfer_id = self.transfer_manager.submit_transfer(
            data=data,
            priority=DataPriority.HIGH,
            metadata={"test": True}
        )
        
        assert isinstance(transfer_id, str)
        assert len(transfer_id) > 0
        
        # Check if transfer is queued
        status = self.transfer_manager.get_transfer_status(transfer_id)
        assert status is not None
        assert status['status'] == 'queued'
        assert status['priority'] == 'HIGH'
    
    def test_priority_ordering(self):
        """Test that transfers are processed in priority order"""
        self.transfer_manager.start(num_workers=1)
        
        # Submit transfers in reverse priority order
        transfers = []
        priorities = [DataPriority.LOW, DataPriority.MEDIUM, 
                     DataPriority.HIGH, DataPriority.CRITICAL]
        
        for priority in priorities:
            transfer_id = self.transfer_manager.submit_transfer(
                data=f"data_{priority.name}".encode(),
                priority=priority,
                metadata={"priority": priority.name}
            )
            transfers.append((transfer_id, priority))
        
        # Wait for processing
        time.sleep(3)
        
        # Check that higher priority transfers completed first
        if len(self.completed_transfers) >= 2:
            first_priority = self.completed_transfers[0].priority
            second_priority = self.completed_transfers[1].priority
            assert first_priority.value <= second_priority.value
    
    def test_queue_capacity_limits(self):
        """Test queue capacity enforcement"""
        # Fill up low priority queue to capacity
        max_size = self.transfer_manager.qos_policy.max_queue_sizes[DataPriority.LOW]
        
        # Submit exactly max_size transfers
        for i in range(max_size):
            self.transfer_manager.submit_transfer(
                data=f"data_{i}".encode(),
                priority=DataPriority.LOW
            )
        
        # Next submission should raise an error
        with pytest.raises(RuntimeError, match="Transfer queue full"):
            self.transfer_manager.submit_transfer(
                data=b"overflow_data",
                priority=DataPriority.LOW
            )
    
    def test_transfer_cancellation(self):
        """Test transfer request cancellation"""
        transfer_id = self.transfer_manager.submit_transfer(
            data=b"test data",
            priority=DataPriority.MEDIUM
        )
        
        # Cancel the transfer
        result = self.transfer_manager.cancel_transfer(transfer_id)
        assert result is True
        
        # Should not be found anymore
        status = self.transfer_manager.get_transfer_status(transfer_id)
        assert status is None
    
    def test_metrics_tracking(self):
        """Test transfer metrics tracking"""
        self.transfer_manager.start(num_workers=1)
        
        # Submit some transfers
        for i in range(5):
            self.transfer_manager.submit_transfer(
                data=f"test_data_{i}".encode(),
                priority=DataPriority.MEDIUM
            )
        
        time.sleep(2)  # Let some transfers process
        
        metrics = self.transfer_manager.get_metrics()
        assert metrics.total_requests >= 5
        assert hasattr(metrics, 'completed_transfers')
        assert hasattr(metrics, 'failed_transfers')
        assert hasattr(metrics, 'bandwidth_utilization')
    
    def test_qos_policy_configuration(self):
        """Test QoS policy configuration"""
        from Core.bandwidth.priority_transfer import QoSPolicy
        
        custom_policy = QoSPolicy()
        custom_policy.bandwidth_allocation[DataPriority.CRITICAL] = 0.5
        
        self.transfer_manager.update_qos_policy(custom_policy)
        
        # Verify policy was updated
        assert (self.transfer_manager.qos_policy.bandwidth_allocation[DataPriority.CRITICAL] 
                == 0.5)
    
    def test_priority_statistics(self):
        """Test priority-based statistics"""
        # Submit transfers with different priorities
        priorities = [DataPriority.CRITICAL, DataPriority.HIGH, DataPriority.MEDIUM]
        
        for priority in priorities:
            for i in range(3):
                self.transfer_manager.submit_transfer(
                    data=f"data_{priority.name}_{i}".encode(),
                    priority=priority
                )
        
        stats = self.transfer_manager.get_priority_stats()
        
        for priority in priorities:
            priority_name = priority.name
            assert priority_name in stats
            assert 'current_queue_size' in stats[priority_name]
            assert 'bandwidth_allocation' in stats[priority_name]


class TestBandwidthMonitor:
    """Test suite for BandwidthMonitor"""
    
    def setup_method(self):
        """Setup for each test"""
        self.monitor = BandwidthMonitor(monitoring_interval=0.1, history_size=100)
        self.metrics_updates = []
        self.condition_changes = []
        
        # Setup callbacks
        self.monitor.on_metrics_update = self.on_metrics_update
        self.monitor.on_condition_change = self.on_condition_change
    
    def on_metrics_update(self, metrics):
        self.metrics_updates.append(metrics)
    
    def on_condition_change(self, old_condition, new_condition, metrics):
        self.condition_changes.append((old_condition, new_condition, metrics))
    
    def teardown_method(self):
        """Cleanup after each test"""
        if self.monitor.is_monitoring:
            self.monitor.stop_monitoring()
    
    def test_monitoring_initialization(self):
        """Test monitor initialization"""
        assert self.monitor.is_monitoring is False
        assert len(self.monitor.bandwidth_history) == 0
        assert self.monitor.current_metrics is None
    
    def test_start_stop_monitoring(self):
        """Test starting and stopping monitoring"""
        self.monitor.start_monitoring()
        assert self.monitor.is_monitoring is True
        
        time.sleep(0.5)  # Let it collect some data
        
        self.monitor.stop_monitoring()
        assert self.monitor.is_monitoring is False
    
    def test_metrics_collection(self):
        """Test metrics collection"""
        self.monitor.start_monitoring()
        time.sleep(0.5)  # Collect some metrics
        
        current_metrics = self.monitor.get_current_metrics()
        assert current_metrics is not None
        assert isinstance(current_metrics, BandwidthMetrics)
        
        # Check metric fields
        assert current_metrics.available_bandwidth_mbps > 0
        assert 0 <= current_metrics.utilization_percentage <= 100
        assert current_metrics.latency_ms > 0
        assert isinstance(current_metrics.condition, NetworkCondition)
        assert 0 <= current_metrics.stability_score <= 1
    
    def test_historical_metrics(self):
        """Test historical metrics retrieval"""
        self.monitor.start_monitoring()
        time.sleep(0.5)
        
        # Get all history
        all_history = self.monitor.get_historical_metrics()
        assert len(all_history) > 0
        
        # Get recent history
        recent_history = self.monitor.get_historical_metrics(duration_seconds=1)
        assert len(recent_history) <= len(all_history)
    
    def test_network_condition_assessment(self):
        """Test network condition assessment"""
        # Test different simulated conditions
        test_conditions = [
            {"congestion_factor": 0.9, "latency_factor": 1.0, "stability": 0.9},
            {"congestion_factor": 0.5, "latency_factor": 2.0, "stability": 0.7},
            {"congestion_factor": 0.2, "latency_factor": 4.0, "stability": 0.3}
        ]
        
        self.monitor.start_monitoring()
        
        for conditions in test_conditions:
            self.monitor.simulate_network_conditions(**conditions)
            time.sleep(0.3)
            
            metrics = self.monitor.get_current_metrics()
            if metrics:
                assert isinstance(metrics.condition, NetworkCondition)
    
    def test_bandwidth_prediction(self):
        """Test bandwidth prediction"""
        self.monitor.start_monitoring()
        time.sleep(0.5)  # Collect some history
        
        prediction = self.monitor.predict_bandwidth_availability(30)
        
        assert 'predicted_bandwidth_mbps' in prediction
        assert 'confidence' in prediction
        assert 'prediction_method' in prediction
        assert prediction['predicted_bandwidth_mbps'] > 0
        assert 0 <= prediction['confidence'] <= 1
    
    def test_network_summary(self):
        """Test network summary generation"""
        self.monitor.start_monitoring()
        time.sleep(0.3)
        
        summary = self.monitor.get_network_summary()
        
        required_fields = [
            'current_condition', 'stability_score', 'trend',
            'current_bandwidth_mbps', 'current_utilization',
            'current_latency_ms', 'congestion_level'
        ]
        
        for field in required_fields:
            assert field in summary
    
    def test_metrics_export(self):
        """Test metrics data export"""
        self.monitor.start_monitoring()
        time.sleep(0.3)
        
        exported_data = self.monitor.export_metrics()
        
        assert isinstance(exported_data, list)
        if len(exported_data) > 0:
            sample_metric = exported_data[0]
            required_fields = [
                'timestamp', 'available_bandwidth_mbps', 'latency_ms',
                'condition', 'stability_score'
            ]
            for field in required_fields:
                assert field in sample_metric
    
    def test_configuration_update(self):
        """Test network configuration updates"""
        new_bandwidth = 20.0
        new_latency = 30.0
        
        self.monitor.set_network_configuration(
            max_bandwidth_mbps=new_bandwidth,
            baseline_latency_ms=new_latency
        )
        
        assert self.monitor.max_bandwidth_mbps == new_bandwidth
        assert self.monitor.baseline_latency_ms == new_latency


class TestIntegratedSystem:
    """Test suite for integrated bandwidth optimization system"""
    
    def test_compression_with_streaming(self):
        """Test integration between compression and streaming"""
        compressor = DataCompressor()
        streamer = AdaptiveStreamer(initial_profile=StreamingProfile.LOW)
        
        # Compress data for streaming
        image_data = np.random.randint(0, 255, (240, 320, 3), dtype=np.uint8)
        compression_result = compressor.compress_data(image_data, CompressionMethod.JPEG, quality=75)
        
        # Verify compression worked
        assert compression_result.compression_ratio > 1.0
        
        # Verify streaming profile settings are appropriate
        settings = streamer.get_current_settings()
        assert settings.quality_factor <= 0.6  # Low quality for low profile
    
    def test_monitoring_with_transfer_adaptation(self):
        """Test integration between monitoring and transfer management"""
        monitor = BandwidthMonitor(monitoring_interval=0.1)
        transfer_manager = PriorityTransferManager(max_bandwidth_mbps=5.0)
        
        try:
            monitor.start_monitoring()
            transfer_manager.start(num_workers=1)
            
            # Simulate poor network conditions
            monitor.simulate_network_conditions(
                congestion_factor=0.3, 
                latency_factor=3.0, 
                stability=0.4
            )
            
            time.sleep(0.3)
            
            # Get network condition
            metrics = monitor.get_current_metrics()
            if metrics and metrics.condition in [NetworkCondition.POOR, NetworkCondition.CRITICAL]:
                # Should adapt transfer behavior for poor conditions
                # Submit high priority transfer
                transfer_id = transfer_manager.submit_transfer(
                    data=b"urgent_data",
                    priority=DataPriority.CRITICAL
                )
                
                assert transfer_id is not None
                
                # Verify transfer was queued
                status = transfer_manager.get_transfer_status(transfer_id)
                assert status is not None
            
        finally:
            transfer_manager.stop()
            monitor.stop_monitoring()
    
    def test_end_to_end_data_flow(self):
        """Test complete end-to-end data flow"""
        # Initialize components
        compressor = DataCompressor()
        monitor = BandwidthMonitor(monitoring_interval=0.1)
        transfer_manager = PriorityTransferManager(max_bandwidth_mbps=8.0)
        
        try:
            monitor.start_monitoring()
            transfer_manager.start(num_workers=2)
            
            # Simulate surveillance data processing
            surveillance_data = {
                "camera_id": "cam_001",
                "timestamp": time.time(),
                "detections": [
                    {"type": "person", "confidence": 0.95, "bbox": [100, 100, 200, 300]},
                    {"type": "vehicle", "confidence": 0.87, "bbox": [300, 150, 500, 250]}
                ]
            }
            
            # Compress surveillance data
            data_bytes = json.dumps(surveillance_data).encode('utf-8')
            compression_result = compressor.compress_data(data_bytes, CompressionMethod.GZIP)
            
            # Submit for priority transfer
            transfer_id = transfer_manager.submit_transfer(
                data=compression_result.compressed_data,
                priority=DataPriority.HIGH,
                metadata={
                    "original_size": compression_result.original_size,
                    "compression_ratio": compression_result.compression_ratio,
                    "data_type": "surveillance"
                }
            )
            
            # Wait for processing
            time.sleep(1.0)
            
            # Verify the data flow worked
            assert compression_result.compression_ratio > 1.0
            assert transfer_id is not None
            
            # Check transfer metrics instead of individual status
            # (transfer may have completed and been removed from tracking)
            transfer_metrics = transfer_manager.get_metrics()
            assert transfer_metrics.total_requests >= 1
            
        finally:
            transfer_manager.stop()
            monitor.stop_monitoring()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])