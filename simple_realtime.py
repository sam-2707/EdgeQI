"""
Simple Real-Time Integration for EDGE-QI Dashboard

Provides a simple, GUI-free way to integrate real-time data
with your EDGE-QI dashboard and applications.
"""

import sys
import os
import time
import threading
from typing import Dict, List, Optional, Callable

# Add path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Core.simulation.realtime_integrator import RealTimeDataIntegrator, RealTimeConfig

class SimpleRealTimeProvider:
    """
    Simple real-time data provider for dashboard integration
    No GUI dependencies, just pure data processing
    """
    
    def __init__(self, fps: int = 10, traffic_density: float = 0.5):
        # Configure for dashboard use
        config = RealTimeConfig(
            frame_width=1280,
            frame_height=720,
            fps=fps,
            enable_queue_detection=True,
            enable_traffic_analysis=True,
            enable_anomaly_detection=True,
            enable_bandwidth_optimization=True,
            traffic_density=traffic_density,
            detection_confidence_threshold=0.7
        )
        
        self.integrator = RealTimeDataIntegrator(config)
        self.is_running = False
        self._data_cache = {}
        self._update_thread = None
        
    def start(self):
        """Start real-time data generation"""
        if not self.is_running:
            self.integrator.start_real_time_processing()
            self.is_running = True
            
            # Start background data update thread
            self._update_thread = threading.Thread(target=self._update_cache)
            self._update_thread.daemon = True
            self._update_thread.start()
            
            print("✅ Real-time data provider started")
    
    def stop(self):
        """Stop real-time data generation"""
        if self.is_running:
            self.is_running = False
            self.integrator.stop_real_time_processing()
            print("⏹️ Real-time data provider stopped")
    
    def _update_cache(self):
        """Background thread to update data cache"""
        while self.is_running:
            try:
                self._data_cache = {
                    'timestamp': time.time(),
                    'frame': self.integrator.get_current_frame(),
                    'detections': self.integrator.get_current_detections(),
                    'queues': self.integrator.get_current_queue_data(),
                    'traffic': self.integrator.get_current_traffic_data(),
                    'sensors': self.integrator.get_current_sensor_data(),
                    'stats': self.integrator.get_processing_stats()
                }
                time.sleep(0.1)  # Update 10 times per second
            except Exception as e:
                print(f"⚠️ Data update error: {e}")
                time.sleep(1)
    
    def get_latest_data(self) -> Dict:
        """Get latest real-time data"""
        return self._data_cache.copy()
    
    def get_frame_as_bytes(self) -> Optional[bytes]:
        """Get current frame as bytes for dashboard display"""
        frame = self._data_cache.get('frame')
        if frame is not None:
            import cv2
            # Encode frame as JPEG bytes
            _, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()
        return None
    
    def set_traffic_density(self, density: float):
        """Adjust traffic density"""
        self.integrator.set_traffic_density(density)
    
    def set_detection_threshold(self, threshold: float):
        """Adjust detection threshold"""
        self.integrator.set_detection_threshold(threshold)
    
    def get_stats_summary(self) -> Dict:
        """Get simplified stats for dashboard"""
        stats = self._data_cache.get('stats', {})
        traffic = self._data_cache.get('traffic', {})
        sensors = self._data_cache.get('sensors', {})
        
        return {
            'fps': stats.get('fps', 0),
            'frames_processed': stats.get('frames_processed', 0),
            'detections_made': stats.get('detections_made', 0),
            'current_detections': len(self._data_cache.get('detections', [])),
            'current_queues': len(self._data_cache.get('queues', [])),
            'traffic_condition': traffic.get('condition', 'unknown'),
            'vehicle_count': traffic.get('vehicle_count', 0),
            'average_speed': traffic.get('average_speed', 0),
            'cpu_usage': sensors.get('cpu_usage', 0),
            'temperature': sensors.get('temperature', 0),
            'is_running': self.is_running
        }

# Global provider instance for easy dashboard integration
_global_provider = None

def get_realtime_provider() -> SimpleRealTimeProvider:
    """Get or create global real-time provider"""
    global _global_provider
    if _global_provider is None:
        _global_provider = SimpleRealTimeProvider()
    return _global_provider

def start_realtime_data():
    """Start real-time data generation"""
    provider = get_realtime_provider()
    provider.start()
    return provider

def stop_realtime_data():
    """Stop real-time data generation"""
    provider = get_realtime_provider()
    provider.stop()

def get_realtime_data() -> Dict:
    """Get latest real-time data"""
    provider = get_realtime_provider()
    return provider.get_latest_data()

def get_realtime_stats() -> Dict:
    """Get real-time stats summary"""
    provider = get_realtime_provider()
    return provider.get_stats_summary()

# Demo function
def demo_simple_integration():
    """Demonstrate simple real-time integration"""
    print("🚀 Starting Simple Real-Time Integration Demo")
    
    provider = SimpleRealTimeProvider(fps=5, traffic_density=0.4)  # Lower FPS for demo
    provider.start()
    
    try:
        print("📊 Monitoring for 15 seconds...")
        for i in range(15):
            stats = provider.get_stats_summary()
            print(f"[{i+1:2d}s] FPS: {stats['fps']:.1f}, "
                  f"Detections: {stats['current_detections']}, "
                  f"Traffic: {stats['traffic_condition']}, "
                  f"Speed: {stats['average_speed']:.1f} km/h")
            time.sleep(1)
    
    finally:
        provider.stop()
        print("✅ Demo completed")

if __name__ == "__main__":
    demo_simple_integration()