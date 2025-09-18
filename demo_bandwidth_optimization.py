"""
Bandwidth Optimization Demo for EDGE-QI Framework

Demonstrates the complete bandwidth optimization system including:
- Data compression with adaptive quality control
- Adaptive bitrate streaming
- Priority-based data transfer with QoS
- Real-time bandwidth monitoring
"""

import time
import numpy as np
import threading
from typing import Dict, Any
import json
import cv2

from Core.bandwidth import (
    DataCompressor, CompressionMethod,
    AdaptiveStreamer, StreamingProfile,
    PriorityTransferManager, DataPriority,
    BandwidthMonitor, NetworkCondition
)


def demo_data_compression():
    """Demonstrate data compression capabilities"""
    print("=" * 60)
    print("DATA COMPRESSION DEMO")
    print("=" * 60)
    
    compressor = DataCompressor()
    
    # Test different data types
    test_data = {
        'image': np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8),
        'numerical': np.random.randn(1000, 100).astype(np.float32),
        'text': json.dumps({"sensor_data": [{"id": i, "value": np.random.randn()} for i in range(100)]}).encode('utf-8'),
        'mixed': {"queue_data": list(range(500)), "metrics": np.random.randn(50).tolist()}
    }
    
    print("Testing compression on different data types:")
    print("-" * 50)
    
    for data_type, data in test_data.items():
        print(f"\n{data_type.upper()} DATA:")
        
        # Test multiple compression methods
        methods = [CompressionMethod.ADAPTIVE, CompressionMethod.GZIP, CompressionMethod.LZMA]
        if data_type == 'image':
            methods.extend([CompressionMethod.JPEG, CompressionMethod.WEBP])
        
        for method in methods:
            try:
                result = compressor.compress_data(data, method)
                
                print(f"  {method.value:12} - "
                      f"Ratio: {result.compression_ratio:.2f}x, "
                      f"Size: {result.original_size:6d} -> {result.compressed_size:6d} bytes, "
                      f"Time: {result.compression_time:.3f}s")
                
                if result.quality_score:
                    print(f"{'':15} Quality: {result.quality_score:.2f}")
                    
            except Exception as e:
                print(f"  {method.value:12} - Error: {e}")
    
    # Demonstrate adaptive compression
    print(f"\n{'ADAPTIVE COMPRESSION RECOMMENDATIONS:':^50}")
    print("-" * 50)
    
    for data_type in ['image', 'numerical', 'text', 'mixed']:
        optimal_method = compressor.get_optimal_method_for_target(
            data_type, target_ratio=3.0, max_time=0.1
        )
        estimated_ratio = compressor.estimate_compression_ratio(
            10000, optimal_method, data_type
        )
        
        print(f"{data_type:10} -> {optimal_method.value:12} "
              f"(Est. ratio: {estimated_ratio:.1f}x)")


def demo_adaptive_streaming():
    """Demonstrate adaptive streaming capabilities"""
    print("\n" + "=" * 60)
    print("ADAPTIVE STREAMING DEMO")
    print("=" * 60)
    
    # Create sample video frames
    def frame_generator():
        """Generate sample video frames"""
        frame = np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)
        # Add some simple patterns to make it more realistic
        cv2.rectangle(frame, (100, 100), (300, 200), (0, 255, 0), 2)
        cv2.circle(frame, (640, 360), 50, (255, 0, 0), -1)
        return frame
    
    # Output callback for encoded frames
    transmitted_data = {'total_bytes': 0, 'frame_count': 0}
    
    def output_callback(encoded_data: bytes, metadata: Dict):
        transmitted_data['total_bytes'] += len(encoded_data)
        transmitted_data['frame_count'] += 1
        
        if transmitted_data['frame_count'] % 10 == 0:  # Print every 10th frame
            print(f"Frame {transmitted_data['frame_count']:3d}: "
                  f"{len(encoded_data):5d} bytes, "
                  f"Profile: {metadata['profile']:10s}, "
                  f"Quality: {metadata['quality_factor']:.2f}, "
                  f"Est. bitrate: {metadata['estimated_bitrate']:4d} kbps")
    
    # Initialize adaptive streamer
    streamer = AdaptiveStreamer(
        initial_profile=StreamingProfile.MEDIUM,
        adaptation_interval=2.0
    )
    
    # Setup profile change callback
    def on_profile_change(old_profile, new_profile, settings):
        print(f"\n>>> PROFILE CHANGED: {old_profile.value} -> {new_profile.value}")
        print(f"    New settings: {settings.resolution}, "
              f"{settings.target_bitrate} kbps, "
              f"Quality: {settings.quality_factor:.2f}")
    
    streamer.on_profile_change = on_profile_change
    
    print("Starting adaptive streaming...")
    print("Profile changes will be triggered by simulated network conditions")
    print("-" * 60)
    
    # Start streaming
    streamer.start_streaming(frame_generator, output_callback)
    
    # Simulate different network conditions
    conditions = [
        ("Good network", 2.0),
        ("Congested network", 3.0),
        ("Poor network", 3.0),
        ("Recovering network", 4.0)
    ]
    
    for condition_name, duration in conditions:
        print(f"\n{condition_name} ({duration}s)...")
        
        # Simulate network condition by adjusting streamer state
        if "poor" in condition_name.lower():
            # Simulate poor conditions
            streamer.metrics.buffer_health = 0.2
            streamer.metrics.packet_loss_rate = 0.08
        elif "congested" in condition_name.lower():
            # Simulate congestion
            streamer.metrics.buffer_health = 0.4
            streamer.metrics.packet_loss_rate = 0.03
        else:
            # Simulate good conditions
            streamer.metrics.buffer_health = 0.9
            streamer.metrics.packet_loss_rate = 0.005
        
        time.sleep(duration)
    
    # Stop streaming
    streamer.stop_streaming()
    
    print(f"\nStreaming completed:")
    print(f"Total frames: {transmitted_data['frame_count']}")
    print(f"Total data transmitted: {transmitted_data['total_bytes'] / 1024:.1f} KB")
    
    # Show final metrics
    metrics = streamer.get_metrics()
    print(f"Final metrics:")
    print(f"  Adaptations: {metrics.adaptation_count}")
    print(f"  Final profile: {streamer.current_profile.value}")
    print(f"  Buffer health: {metrics.buffer_health:.2f}")


def demo_priority_transfer():
    """Demonstrate priority-based transfer management"""
    print("\n" + "=" * 60)
    print("PRIORITY TRANSFER DEMO")
    print("=" * 60)
    
    # Initialize transfer manager
    transfer_manager = PriorityTransferManager(max_bandwidth_mbps=5.0)
    
    # Setup callbacks
    completed_transfers = []
    failed_transfers = []
    
    def on_complete(request):
        completed_transfers.append(request)
        print(f"✓ Completed: {request.priority.name:10s} transfer {request.id[:8]}")
    
    def on_failed(request, error):
        failed_transfers.append((request, error))
        print(f"✗ Failed: {request.priority.name:10s} transfer {request.id[:8]} - {error}")
    
    transfer_manager.on_transfer_complete = on_complete
    transfer_manager.on_transfer_failed = on_failed
    
    # Start transfer manager
    transfer_manager.start(num_workers=2)
    
    print("Submitting transfers with different priorities...")
    print("-" * 60)
    
    # Submit various transfers
    transfers = []
    
    # Critical alerts
    for i in range(3):
        data = json.dumps({
            "alert_type": "security_incident",
            "location": f"camera_{i+1}",
            "timestamp": time.time(),
            "severity": "critical"
        }).encode('utf-8')
        
        transfer_id = transfer_manager.submit_transfer(
            data=data,
            priority=DataPriority.CRITICAL,
            metadata={"type": "security_alert", "camera_id": i+1}
        )
        transfers.append(transfer_id)
        print(f"Submitted CRITICAL transfer: {transfer_id[:8]}")
    
    # High priority analytics
    for i in range(5):
        # Simulate queue detection data
        queue_data = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        
        transfer_id = transfer_manager.submit_transfer(
            data=queue_data.tobytes(),
            priority=DataPriority.HIGH,
            metadata={"type": "queue_detection", "frame": i}
        )
        transfers.append(transfer_id)
        print(f"Submitted HIGH priority transfer: {transfer_id[:8]}")
    
    # Medium priority surveillance data
    for i in range(8):
        surveillance_data = {
            "camera_id": f"cam_{i%4 + 1}",
            "detections": [{"type": "person", "confidence": 0.85 + np.random.uniform(-0.1, 0.1)}],
            "timestamp": time.time()
        }
        
        transfer_id = transfer_manager.submit_transfer(
            data=json.dumps(surveillance_data).encode('utf-8'),
            priority=DataPriority.MEDIUM,
            metadata={"type": "surveillance_data"}
        )
        transfers.append(transfer_id)
        print(f"Submitted MEDIUM priority transfer: {transfer_id[:8]}")
    
    # Low priority system logs
    for i in range(10):
        log_data = {
            "level": "INFO",
            "message": f"System status update #{i}",
            "component": "edge_node_1",
            "timestamp": time.time()
        }
        
        transfer_id = transfer_manager.submit_transfer(
            data=json.dumps(log_data).encode('utf-8'),
            priority=DataPriority.LOW,
            metadata={"type": "system_log"}
        )
        transfers.append(transfer_id)
        print(f"Submitted LOW priority transfer: {transfer_id[:8]}")
    
    # Monitor progress
    print(f"\nMonitoring transfer progress...")
    print("-" * 60)
    
    start_time = time.time()
    while time.time() - start_time < 15:  # Monitor for 15 seconds
        # Print queue status
        queue_status = transfer_manager.get_queue_status()
        total_queued = sum(status['queue_size'] for status in queue_status.values())
        
        if total_queued > 0:
            print(f"Queued transfers: ", end="")
            for priority, status in queue_status.items():
                if status['queue_size'] > 0:
                    print(f"{priority}: {status['queue_size']} ", end="")
            print()
        
        # Print metrics
        metrics = transfer_manager.get_metrics()
        print(f"Completed: {metrics.completed_transfers}, "
              f"Failed: {metrics.failed_transfers}, "
              f"Bandwidth usage: {metrics.bandwidth_utilization:.1%}")
        
        time.sleep(2)
        
        # Break if all transfers completed
        if total_queued == 0 and len(transfer_manager.active_transfers) == 0:
            break
    
    # Final statistics
    transfer_manager.stop()
    
    print(f"\nTransfer Summary:")
    print("-" * 30)
    print(f"Total submitted: {len(transfers)}")
    print(f"Completed: {len(completed_transfers)}")
    print(f"Failed: {len(failed_transfers)}")
    
    # Show completion by priority
    priority_completion = {}
    for request in completed_transfers:
        priority = request.priority.name
        priority_completion[priority] = priority_completion.get(priority, 0) + 1
    
    print("\nCompletion by priority:")
    for priority, count in priority_completion.items():
        print(f"  {priority:10s}: {count}")


def demo_bandwidth_monitoring():
    """Demonstrate bandwidth monitoring capabilities"""
    print("\n" + "=" * 60)
    print("BANDWIDTH MONITORING DEMO")
    print("=" * 60)
    
    monitor = BandwidthMonitor(monitoring_interval=0.5)
    
    # Setup callbacks
    def on_metrics_update(metrics):
        if metrics.timestamp % 2 < 0.5:  # Print every ~2 seconds
            print(f"Bandwidth: {metrics.available_bandwidth_mbps:.1f} Mbps, "
                  f"Utilization: {metrics.utilization_percentage:.1f}%, "
                  f"Latency: {metrics.latency_ms:.1f}ms, "
                  f"Condition: {metrics.condition.value}")
    
    def on_condition_change(old_condition, new_condition, metrics):
        print(f"\n>>> NETWORK CONDITION CHANGED: {old_condition.value} -> {new_condition.value}")
        print(f"    Bandwidth: {metrics.available_bandwidth_mbps:.1f} Mbps, "
              f"Stability: {metrics.stability_score:.2f}")
    
    monitor.on_metrics_update = on_metrics_update
    monitor.on_condition_change = on_condition_change
    
    # Start monitoring
    monitor.start_monitoring()
    
    print("Starting bandwidth monitoring...")
    print("Simulating various network conditions...")
    print("-" * 60)
    
    # Simulate different network scenarios
    scenarios = [
        ("Good network conditions", {"congestion_factor": 0.9, "latency_factor": 1.0, "stability": 0.95}),
        ("Peak hour congestion", {"congestion_factor": 0.5, "latency_factor": 2.0, "stability": 0.7}),
        ("Network instability", {"congestion_factor": 0.8, "latency_factor": 1.5, "stability": 0.4}),
        ("Poor connectivity", {"congestion_factor": 0.3, "latency_factor": 3.0, "stability": 0.6}),
        ("Recovery period", {"congestion_factor": 0.8, "latency_factor": 1.2, "stability": 0.9})
    ]
    
    for scenario_name, conditions in scenarios:
        print(f"\n{scenario_name}...")
        monitor.simulate_network_conditions(**conditions)
        time.sleep(4)
    
    # Show prediction capabilities
    print(f"\nBandwidth prediction:")
    prediction = monitor.predict_bandwidth_availability(60)
    print(f"Predicted bandwidth (60s): {prediction['predicted_bandwidth_mbps']:.1f} Mbps")
    print(f"Confidence: {prediction['confidence']:.1%}")
    print(f"Method: {prediction['prediction_method']}")
    
    # Show network summary
    summary = monitor.get_network_summary()
    print(f"\nNetwork Summary:")
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    # Stop monitoring
    monitor.stop_monitoring()


def demo_integrated_system():
    """Demonstrate the integrated bandwidth optimization system"""
    print("\n" + "=" * 60)
    print("INTEGRATED BANDWIDTH OPTIMIZATION DEMO")
    print("=" * 60)
    
    # Initialize all components
    compressor = DataCompressor()
    monitor = BandwidthMonitor(monitoring_interval=1.0)
    transfer_manager = PriorityTransferManager(max_bandwidth_mbps=10.0)
    
    # Start monitoring and transfer manager
    monitor.start_monitoring()
    transfer_manager.start(num_workers=3)
    
    print("Integrated system started...")
    print("Demonstrating adaptive compression and transfer based on network conditions")
    print("-" * 60)
    
    # Simulate edge device data processing
    for scenario in range(3):
        print(f"\nScenario {scenario + 1}: Processing surveillance data batch")
        
        # Simulate different network conditions
        if scenario == 0:
            monitor.simulate_network_conditions(congestion_factor=0.9, latency_factor=1.0)
            print("Network condition: GOOD")
        elif scenario == 1:
            monitor.simulate_network_conditions(congestion_factor=0.6, latency_factor=1.8)
            print("Network condition: CONGESTED")
        else:
            monitor.simulate_network_conditions(congestion_factor=0.3, latency_factor=3.0)
            print("Network condition: POOR")
        
        time.sleep(1)  # Let network condition stabilize
        
        # Get current network metrics
        metrics = monitor.get_current_metrics()
        if metrics:
            # Adapt compression based on network condition
            if metrics.condition in [NetworkCondition.EXCELLENT, NetworkCondition.GOOD]:
                compression_quality = 90
                stream_profile = StreamingProfile.HIGH
            elif metrics.condition == NetworkCondition.FAIR:
                compression_quality = 70
                stream_profile = StreamingProfile.MEDIUM
            else:
                compression_quality = 50
                stream_profile = StreamingProfile.LOW
            
            print(f"Adapting to network: Quality={compression_quality}%, Profile={stream_profile.value}")
            
            # Process different types of data
            data_types = [
                ("Critical Alert", DataPriority.CRITICAL, np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)),
                ("Queue Detection", DataPriority.HIGH, np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)),
                ("Surveillance Frame", DataPriority.MEDIUM, np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)),
                ("System Log", DataPriority.LOW, json.dumps({"log": "status update"}).encode('utf-8'))
            ]
            
            for data_name, priority, data in data_types:
                # Compress data based on network conditions
                if isinstance(data, np.ndarray):
                    compression_result = compressor.compress_data(
                        data, 
                        CompressionMethod.WEBP,
                        quality=compression_quality
                    )
                else:
                    compression_result = compressor.compress_data(data)
                
                # Submit for transfer
                transfer_id = transfer_manager.submit_transfer(
                    data=compression_result.compressed_data,
                    priority=priority,
                    metadata={
                        "original_size": compression_result.original_size,
                        "compression_ratio": compression_result.compression_ratio,
                        "quality": compression_result.quality_score,
                        "type": data_name
                    }
                )
                
                print(f"  {data_name:15s}: {compression_result.compression_ratio:.1f}x compression, "
                      f"{priority.name:8s} priority, ID: {transfer_id[:8]}")
        
        time.sleep(3)  # Wait between scenarios
    
    # Monitor final results
    print(f"\nFinal system status:")
    time.sleep(2)
    
    # Transfer metrics
    transfer_metrics = transfer_manager.get_metrics()
    print(f"Transfers - Completed: {transfer_metrics.completed_transfers}, "
          f"Failed: {transfer_metrics.failed_transfers}")
    
    # Compression stats
    compression_stats = compressor.get_compression_stats()
    if compression_stats:
        print("Compression efficiency:")
        for method, stats in compression_stats.items():
            print(f"  {method}: {stats['avg_ratio']:.1f}x ratio, "
                  f"{stats['total_compressions']} uses")
    
    # Network summary
    network_summary = monitor.get_network_summary()
    print(f"Network: {network_summary['current_condition']} "
          f"({network_summary['current_bandwidth_mbps']:.1f} Mbps available)")
    
    # Cleanup
    transfer_manager.stop()
    monitor.stop_monitoring()
    
    print("\nIntegrated system demo completed!")


def main():
    """Run all bandwidth optimization demos"""
    print("EDGE-QI Bandwidth Optimization System Demo")
    print("=" * 60)
    
    try:
        # Individual component demos
        demo_data_compression()
        demo_adaptive_streaming()
        demo_priority_transfer()
        demo_bandwidth_monitoring()
        
        # Integrated system demo
        demo_integrated_system()
        
        print("\n" + "=" * 60)
        print("All demos completed successfully!")
        print("Bandwidth optimization system is ready for production use.")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nDemo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()