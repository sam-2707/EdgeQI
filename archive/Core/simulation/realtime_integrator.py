"""
Real-Time Data Integration for EDGE-QI Framework

Integrates simulated real-time data with the EDGE-QI system, allowing
the framework to process live data streams without requiring physical hardware.
"""

import cv2
import numpy as np
import asyncio
import threading
import time
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass

from .realtime_simulator import RealTimeDataSimulator

# Import EDGE-QI components with error handling
try:
    from Core.queue.queue_detector import QueueDetector
    from Core.traffic.traffic_analyzer import TrafficFlowAnalyzer
    from Core.video.video_stream import VideoStreamProcessor
    from Core.bandwidth.bandwidth_monitor import BandwidthMonitor
    from Core.bandwidth.adaptive_streaming import AdaptiveStreamer
    from Core.anomaly import QueueAnomalyDetector
    from ML.tasks.surveillance_task import SurveillanceTask
except ImportError as e:
    # Create mock classes for missing components
    print(f"Warning: Some components not available: {e}")
    
    class QueueDetector:
        def __init__(self): pass
    
    class TrafficFlowAnalyzer:
        def __init__(self, frame_width, frame_height): pass
    
    class VideoStreamProcessor:
        def __init__(self, config=None): pass
    
    class BandwidthMonitor:
        def __init__(self): pass
        def update_bandwidth_measurement(self, bandwidth): pass
    
    class AdaptiveStreamer:
        def __init__(self): pass
    
    class QueueAnomalyDetector:
        def __init__(self): pass
    
    class SurveillanceTask:
        def __init__(self): pass

@dataclass
class RealTimeConfig:
    """Configuration for real-time data integration"""
    frame_width: int = 1280
    frame_height: int = 720
    fps: int = 30
    enable_queue_detection: bool = True
    enable_traffic_analysis: bool = True
    enable_anomaly_detection: bool = True
    enable_bandwidth_optimization: bool = True
    traffic_density: float = 0.5
    detection_confidence_threshold: float = 0.6

class RealTimeDataIntegrator:
    """
    Integrates simulated real-time data with EDGE-QI processing pipeline
    
    This class creates a complete real-time processing pipeline:
    1. Simulated camera feeds with moving vehicles
    2. Real-time object detection and tracking
    3. Queue detection and analysis
    4. Traffic flow monitoring
    5. Anomaly detection
    6. Bandwidth optimization
    7. Data streaming and visualization
    """
    
    def __init__(self, config: RealTimeConfig = None):
        self.config = config or RealTimeConfig()
        
        # Initialize simulator
        self.simulator = RealTimeDataSimulator(
            width=self.config.frame_width,
            height=self.config.frame_height,
            fps=self.config.fps
        )
        self.simulator.set_traffic_density(self.config.traffic_density)
        
        # Initialize EDGE-QI components
        self.queue_detector = None
        self.traffic_analyzer = None
        self.video_processor = None
        self.anomaly_detector = None
        self.bandwidth_monitor = None
        self.adaptive_streamer = None
        
        # Processing state
        self.is_processing = False
        self.processing_stats = {
            'frames_processed': 0,
            'detections_made': 0,
            'queues_detected': 0,
            'anomalies_found': 0,
            'start_time': None
        }
        
        # Real-time data storage
        self.latest_frame = None
        self.latest_detections = []
        self.latest_queue_data = []
        self.latest_traffic_data = {}
        self.latest_sensor_data = {}
        
        # Callbacks for external systems
        self.frame_callbacks = []
        self.detection_callbacks = []
        self.queue_callbacks = []
        self.traffic_callbacks = []
        self.anomaly_callbacks = []
        
        self._setup_components()
    
    def _setup_components(self):
        """Initialize EDGE-QI processing components"""
        try:
            # Queue detection
            if self.config.enable_queue_detection:
                self.queue_detector = QueueDetector()
            
            # Traffic analysis
            if self.config.enable_traffic_analysis:
                self.traffic_analyzer = TrafficFlowAnalyzer(
                    frame_width=self.config.frame_width,
                    frame_height=self.config.frame_height
                )
            
            # Video processing
            try:
                # Try with mock config for compatibility
                mock_config = type('Config', (), {'frame_width': 1920, 'frame_height': 1080})()
                self.video_processor = VideoStreamProcessor(mock_config)
            except:
                # Fallback to mock class
                self.video_processor = type('VideoStreamProcessor', (), {})()
                self.video_processor.process_frame = lambda x: x
            
            # Anomaly detection
            if self.config.enable_anomaly_detection:
                self.anomaly_detector = QueueAnomalyDetector()
            
            # Bandwidth optimization
            if self.config.enable_bandwidth_optimization:
                self.bandwidth_monitor = BandwidthMonitor()
                self.adaptive_streamer = AdaptiveStreamer()
            
            print("✅ EDGE-QI components initialized for real-time processing")
            
        except Exception as e:
            print(f"⚠️ Error initializing components: {e}")
    
    def start_real_time_processing(self):
        """Start real-time data processing pipeline"""
        if self.is_processing:
            print("🔄 Real-time processing already running")
            return
        
        print("🚀 Starting Real-Time Data Processing Pipeline...")
        
        # Start simulator
        self.simulator.start_simulation()
        
        # Start processing
        self.is_processing = True
        self.processing_stats['start_time'] = time.time()
        
        # Start processing threads
        self.processing_thread = threading.Thread(target=self._processing_loop)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        print("✅ Real-time processing pipeline started")
        print(f"📹 Simulating {self.config.fps} FPS video stream")
        print(f"🚗 Traffic density: {self.config.traffic_density}")
        print(f"🎯 Detection threshold: {self.config.detection_confidence_threshold}")
    
    def stop_real_time_processing(self):
        """Stop real-time data processing"""
        print("⏹️ Stopping real-time processing...")
        
        self.is_processing = False
        self.simulator.stop_simulation()
        
        # Print final stats
        duration = time.time() - self.processing_stats['start_time']
        print(f"📊 Processing Statistics:")
        print(f"   Duration: {duration:.1f} seconds")
        print(f"   Frames processed: {self.processing_stats['frames_processed']}")
        print(f"   Detections made: {self.processing_stats['detections_made']}")
        print(f"   Queues detected: {self.processing_stats['queues_detected']}")
        print(f"   Anomalies found: {self.processing_stats['anomalies_found']}")
        if duration > 0:
            fps = self.processing_stats['frames_processed'] / duration
            print(f"   Average FPS: {fps:.1f}")
    
    def _processing_loop(self):
        """Main real-time processing loop"""
        while self.is_processing:
            try:
                # Get latest frame
                frame_data = self.simulator.get_latest_frame()
                if frame_data is None:
                    time.sleep(0.01)
                    continue
                
                frame = frame_data['frame']
                camera_id = frame_data['camera_id']
                timestamp = frame_data['timestamp']
                
                self.latest_frame = frame_data
                
                # Process frame through EDGE-QI pipeline
                self._process_frame(frame, camera_id, timestamp)
                
                # Get sensor data
                sensor_data = self.simulator.get_latest_sensor_data()
                if sensor_data:
                    self.latest_sensor_data = sensor_data
                    self._process_sensor_data(sensor_data)
                
                self.processing_stats['frames_processed'] += 1
                
                # Notify callbacks
                self._notify_callbacks()
                
            except Exception as e:
                print(f"⚠️ Processing error: {e}")
                time.sleep(0.1)
    
    def _process_frame(self, frame: np.ndarray, camera_id: str, timestamp: float):
        """Process individual frame through EDGE-QI pipeline"""
        
        # 1. Object Detection (simulated detections from simulator)
        detection_data = self.simulator.get_latest_detections()
        if detection_data and detection_data.get('camera_id') == camera_id:
            detections = detection_data['detections']
            self.latest_detections = detections
            self.processing_stats['detections_made'] += len(detections)
        
        # 2. Queue Detection
        if self.queue_detector and self.latest_detections:
            try:
                queue_data = self._detect_queues(self.latest_detections, timestamp)
                if queue_data:
                    self.latest_queue_data = queue_data
                    self.processing_stats['queues_detected'] += len(queue_data)
            except Exception as e:
                pass  # Continue processing even if queue detection fails
        
        # 3. Traffic Analysis
        if self.traffic_analyzer and self.latest_detections:
            try:
                traffic_data = self._analyze_traffic(self.latest_detections, timestamp)
                self.latest_traffic_data = traffic_data
            except Exception as e:
                pass
        
        # 4. Anomaly Detection
        if self.anomaly_detector and self.latest_queue_data:
            try:
                anomalies = self._detect_anomalies(self.latest_queue_data, timestamp)
                if anomalies:
                    self.processing_stats['anomalies_found'] += len(anomalies)
            except Exception as e:
                pass
        
        # 5. Bandwidth Optimization
        if self.bandwidth_monitor:
            try:
                self._optimize_bandwidth(frame, timestamp)
            except Exception as e:
                pass
    
    def _detect_queues(self, detections: List[Dict], timestamp: float) -> List[Dict]:
        """Convert detections to queue data"""
        queue_data = []
        
        # Group nearby vehicles to form potential queues
        vehicle_positions = []
        for detection in detections:
            if detection['confidence'] > self.config.detection_confidence_threshold:
                center = detection['center']
                vehicle_positions.append({
                    'x': center[0],
                    'y': center[1],
                    'type': detection['class'],
                    'speed': detection.get('speed', 0)
                })
        
        # Simple queue detection: find clusters of slow/stopped vehicles
        if len(vehicle_positions) >= 3:
            slow_vehicles = [v for v in vehicle_positions if v['speed'] < 10]
            
            if len(slow_vehicles) >= 3:
                # Calculate queue properties
                positions = [(v['x'], v['y']) for v in slow_vehicles]
                center_x = sum(p[0] for p in positions) / len(positions)
                center_y = sum(p[1] for p in positions) / len(positions)
                
                # Estimate queue length
                distances = [np.sqrt((p[0] - center_x)**2 + (p[1] - center_y)**2) for p in positions]
                queue_length = max(distances) * 2  # Approximate queue length
                
                queue_data.append({
                    'id': f'queue_{int(timestamp)}',
                    'type': 'vehicle',
                    'location': (center_x, center_y),
                    'length': queue_length,
                    'vehicle_count': len(slow_vehicles),
                    'wait_time': np.random.uniform(30, 300),  # Simulated wait time
                    'density': len(slow_vehicles) / max(1, queue_length / 20),
                    'confidence': 0.8,
                    'timestamp': timestamp
                })
        
        return queue_data
    
    def _analyze_traffic(self, detections: List[Dict], timestamp: float) -> Dict:
        """Analyze traffic flow from detections"""
        vehicle_count = len([d for d in detections if d['confidence'] > self.config.detection_confidence_threshold])
        
        speeds = [d.get('speed', 0) for d in detections]
        avg_speed = sum(speeds) / len(speeds) if speeds else 0
        
        # Calculate traffic density (vehicles per area)
        area = self.config.frame_width * self.config.frame_height
        density = vehicle_count / (area / 10000)  # vehicles per 100x100 pixel area
        
        # Determine traffic condition
        if avg_speed > 25 and density < 0.3:
            condition = 'free_flow'
        elif avg_speed > 15 and density < 0.6:
            condition = 'moderate'
        elif avg_speed > 5:
            condition = 'congested'
        else:
            condition = 'jammed'
        
        return {
            'timestamp': timestamp,
            'vehicle_count': vehicle_count,
            'average_speed': avg_speed,
            'density': density,
            'condition': condition,
            'throughput': vehicle_count * avg_speed / 60,  # vehicles per minute
        }
    
    def _detect_anomalies(self, queue_data: List[Dict], timestamp: float) -> List[Dict]:
        """Detect anomalies in queue behavior"""
        anomalies = []
        
        for queue in queue_data:
            # Check for unusually long queues
            if queue['length'] > 200:  # Threshold for long queue
                anomalies.append({
                    'type': 'long_queue',
                    'severity': 'high',
                    'queue_id': queue['id'],
                    'description': f"Unusually long queue detected: {queue['length']:.1f} pixels",
                    'timestamp': timestamp
                })
            
            # Check for high density queues
            if queue['density'] > 0.8:
                anomalies.append({
                    'type': 'high_density',
                    'severity': 'medium',
                    'queue_id': queue['id'],
                    'description': f"High density queue: {queue['density']:.2f}",
                    'timestamp': timestamp
                })
        
        return anomalies
    
    def _process_sensor_data(self, sensor_data: Dict):
        """Process sensor data for monitoring"""
        # Check for high temperature
        if sensor_data['temperature'] > 45:
            print(f"🌡️ High temperature warning: {sensor_data['temperature']:.1f}°C")
        
        # Check for high resource usage
        if sensor_data['cpu_usage'] > 80:
            print(f"💻 High CPU usage: {sensor_data['cpu_usage']:.1f}%")
        
        if sensor_data['memory_usage'] > 85:
            print(f"🧠 High memory usage: {sensor_data['memory_usage']:.1f}%")
    
    def _optimize_bandwidth(self, frame: np.ndarray, timestamp: float):
        """Apply bandwidth optimization to frame"""
        if self.bandwidth_monitor:
            # Simulate bandwidth monitoring
            current_bandwidth = np.random.uniform(1000000, 10000000)  # 1-10 Mbps
            self.bandwidth_monitor.update_bandwidth_measurement(current_bandwidth)
    
    def _notify_callbacks(self):
        """Notify registered callbacks with latest data"""
        try:
            for callback in self.frame_callbacks:
                callback(self.latest_frame)
        except:
            pass
        
        try:
            for callback in self.detection_callbacks:
                callback(self.latest_detections)
        except:
            pass
        
        try:
            for callback in self.queue_callbacks:
                callback(self.latest_queue_data)
        except:
            pass
        
        try:
            for callback in self.traffic_callbacks:
                callback(self.latest_traffic_data)
        except:
            pass
    
    # Public API methods
    def get_current_frame(self) -> Optional[np.ndarray]:
        """Get the current processed frame"""
        return self.latest_frame['frame'] if self.latest_frame else None
    
    def get_current_detections(self) -> List[Dict]:
        """Get current object detections"""
        return self.latest_detections.copy()
    
    def get_current_queue_data(self) -> List[Dict]:
        """Get current queue detection results"""
        return self.latest_queue_data.copy()
    
    def get_current_traffic_data(self) -> Dict:
        """Get current traffic analysis results"""
        return self.latest_traffic_data.copy()
    
    def get_current_sensor_data(self) -> Dict:
        """Get current sensor readings"""
        return self.latest_sensor_data.copy()
    
    def get_processing_stats(self) -> Dict:
        """Get processing performance statistics"""
        stats = self.processing_stats.copy()
        if stats['start_time']:
            stats['runtime'] = time.time() - stats['start_time']
            if stats['runtime'] > 0:
                stats['fps'] = stats['frames_processed'] / stats['runtime']
        return stats
    
    # Callback registration
    def register_frame_callback(self, callback: Callable):
        """Register callback for frame updates"""
        self.frame_callbacks.append(callback)
    
    def register_detection_callback(self, callback: Callable):
        """Register callback for detection updates"""
        self.detection_callbacks.append(callback)
    
    def register_queue_callback(self, callback: Callable):
        """Register callback for queue detection updates"""
        self.queue_callbacks.append(callback)
    
    def register_traffic_callback(self, callback: Callable):
        """Register callback for traffic analysis updates"""
        self.traffic_callbacks.append(callback)
    
    def register_anomaly_callback(self, callback: Callable):
        """Register callback for anomaly detection updates"""
        self.anomaly_callbacks.append(callback)
    
    # Configuration methods
    def set_traffic_density(self, density: float):
        """Adjust simulated traffic density"""
        self.config.traffic_density = density
        self.simulator.set_traffic_density(density)
    
    def set_detection_threshold(self, threshold: float):
        """Adjust detection confidence threshold"""
        self.config.detection_confidence_threshold = threshold
    
    def add_congestion_zone(self, x: int, y: int, radius: int):
        """Add congestion zone to simulation"""
        self.simulator.add_congestion_zone(x, y, radius)