"""
Real-Time Data Integration Demo for EDGE-QI Framework

Demonstrates how to integrate simulated real-time data with EDGE-QI
processing pipeline without requiring physical hardware.
"""

import cv2
import numpy as np
import time
import asyncio
import sys
import os
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Core.simulation.realtime_integrator import RealTimeDataIntegrator, RealTimeConfig

class RealTimeDemo:
    """
    Interactive demo of real-time data processing
    """
    
    def __init__(self):
        # Configure real-time processing
        config = RealTimeConfig(
            frame_width=1280,
            frame_height=720,
            fps=30,
            enable_queue_detection=True,
            enable_traffic_analysis=True,
            enable_anomaly_detection=True,
            enable_bandwidth_optimization=True,
            traffic_density=0.6,
            detection_confidence_threshold=0.7
        )
        
        # Initialize integrator
        self.integrator = RealTimeDataIntegrator(config)
        
        # Register callbacks for real-time updates
        self.integrator.register_frame_callback(self._on_frame_update)
        self.integrator.register_detection_callback(self._on_detection_update)
        self.integrator.register_queue_callback(self._on_queue_update)
        self.integrator.register_traffic_callback(self._on_traffic_update)
        
        # Demo state
        self.show_video = True
        self.save_frames = False
        self.frame_count = 0
        
        print("🎬 Real-Time EDGE-QI Demo Initialized")
        print("=" * 60)
    
    def start_demo(self, duration: int = 60):
        """Start real-time demo for specified duration"""
        print(f"🚀 Starting {duration}-second real-time processing demo...")
        print("\nFeatures enabled:")
        print("✅ Simulated camera feeds with moving vehicles")
        print("✅ Real-time object detection and tracking")
        print("✅ Queue detection and analysis")
        print("✅ Traffic flow monitoring")
        print("✅ Anomaly detection")
        print("✅ Bandwidth optimization")
        print("✅ Live video display")
        print("\n" + "=" * 60)
        
        # Start processing
        self.integrator.start_real_time_processing()
        
        try:
            # Run demo
            if self.show_video:
                self._run_video_demo(duration)
            else:
                self._run_headless_demo(duration)
                
        except KeyboardInterrupt:
            print("\n🛑 Demo interrupted by user")
        
        finally:
            # Stop processing
            self.integrator.stop_real_time_processing()
            print("\n✅ Demo completed")
    
    def _run_video_demo(self, duration: int):
        """Run demo with live video display"""
        try:
            print("🎥 Starting live video display...")
            print("Press 'q' to quit, 's' to save frame, 'SPACE' to pause")
            
            start_time = time.time()
            paused = False
            
            while time.time() - start_time < duration:
                # Get current frame
                frame = self.integrator.get_current_frame()

                if frame is not None:
                    # Create display frame with overlays
                    display_frame = self._create_display_frame(frame)

                    # Show frame
                    cv2.imshow('EDGE-QI Real-Time Processing', display_frame)

                    self.frame_count += 1

                    # Handle keyboard input
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    elif key == ord('s'):
                        filename = f'edge_qi_frame_{int(time.time())}.jpg'
                        cv2.imwrite(filename, display_frame)
                        print(f"💾 Frame saved as {filename}")
                    elif key == ord(' '):
                        paused = not paused
                        print(f"⏸️ {'Paused' if paused else 'Resumed'}")

                    if paused:
                        time.sleep(0.1)
                else:
                    time.sleep(0.01)

            cv2.destroyAllWindows()
            
        except Exception as e:
            print(f"⚠️ Video display error (OpenCV GUI not available): {e}")
            print("🔄 Switching to headless mode...")
            self._run_headless_demo(duration)
    
    def _run_headless_demo(self, duration: int):
        """Run demo without video display"""
        print("📊 Running headless demo - monitoring metrics...")
        
        start_time = time.time()
        last_stats_time = start_time
        
        while time.time() - start_time < duration:
            current_time = time.time()
            
            # Print stats every 10 seconds
            if current_time - last_stats_time >= 10:
                self._print_current_stats()
                last_stats_time = current_time
            
            time.sleep(1)
    
    def _create_display_frame(self, frame: np.ndarray) -> np.ndarray:
        """Create display frame with overlays and information"""
        display_frame = frame.copy()
        
        # Get current data
        detections = self.integrator.get_current_detections()
        queue_data = self.integrator.get_current_queue_data()
        traffic_data = self.integrator.get_current_traffic_data()
        sensor_data = self.integrator.get_current_sensor_data()
        stats = self.integrator.get_processing_stats()
        
        # Draw vehicle detections
        for detection in detections:
            if detection['confidence'] > 0.6:
                bbox = detection['bbox']
                x, y, w, h = bbox
                
                # Draw bounding box
                color = (0, 255, 0) if detection['speed'] > 10 else (0, 0, 255)
                cv2.rectangle(display_frame, (int(x), int(y)), (int(x + w), int(y + h)), color, 2)
                
                # Draw label
                label = f"{detection['class']} ({detection['confidence']:.2f}) {detection['speed']:.1f}km/h"
                cv2.putText(display_frame, label, (int(x), int(y - 5)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Draw queue zones
        for queue in queue_data:
            center = queue['location']
            radius = int(queue['length'] / 4)
            
            # Draw queue circle
            cv2.circle(display_frame, (int(center[0]), int(center[1])), radius, (255, 0, 255), 2)
            
            # Draw queue info
            queue_label = f"Queue: {queue['vehicle_count']} vehicles, {queue['wait_time']:.0f}s wait"
            cv2.putText(display_frame, queue_label, (int(center[0] - 50), int(center[1] - radius - 10)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
        
        # Add information overlay
        self._add_info_overlay(display_frame, detections, queue_data, traffic_data, sensor_data, stats)
        
        return display_frame
    
    def _add_info_overlay(self, frame: np.ndarray, detections: List, queue_data: List,
                         traffic_data: Dict, sensor_data: Dict, stats: Dict):
        """Add information overlay to frame"""
        height = frame.shape[0]
        
        # Background for text
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, height - 200), (400, height - 10), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Text information
        y_pos = height - 180
        line_height = 20
        
        info_lines = [
            f"Detections: {len(detections)}",
            f"Queues: {len(queue_data)}",
            f"Avg Speed: {traffic_data.get('average_speed', 0):.1f} km/h",
            f"Traffic: {traffic_data.get('condition', 'unknown')}",
            f"FPS: {stats.get('fps', 0):.1f}",
            f"Frames: {stats.get('frames_processed', 0)}",
            f"CPU: {sensor_data.get('cpu_usage', 0):.1f}%",
            f"Temp: {sensor_data.get('temperature', 0):.1f}°C"
        ]
        
        for i, line in enumerate(info_lines):
            cv2.putText(frame, line, (20, y_pos + i * line_height),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def _print_current_stats(self):
        """Print current processing statistics"""
        stats = self.integrator.get_processing_stats()
        traffic_data = self.integrator.get_current_traffic_data()
        sensor_data = self.integrator.get_current_sensor_data()
        
        print(f"\n📊 Current Stats (Runtime: {stats.get('runtime', 0):.1f}s)")
        print(f"   🎬 Frames processed: {stats.get('frames_processed', 0)}")
        print(f"   🎯 Detections made: {stats.get('detections_made', 0)}")
        print(f"   🚗 Queues detected: {stats.get('queues_detected', 0)}")
        print(f"   ⚠️ Anomalies found: {stats.get('anomalies_found', 0)}")
        print(f"   📺 Processing FPS: {stats.get('fps', 0):.1f}")
        print(f"   🚦 Traffic condition: {traffic_data.get('condition', 'unknown')}")
        print(f"   💻 CPU usage: {sensor_data.get('cpu_usage', 0):.1f}%")
        print(f"   🌡️ Temperature: {sensor_data.get('temperature', 0):.1f}°C")
    
    # Callback methods
    def _on_frame_update(self, frame_data):
        """Handle frame updates"""
        pass  # Frame processing is handled in main loop
    
    def _on_detection_update(self, detections):
        """Handle detection updates"""
        # You can add custom detection processing here
        pass
    
    def _on_queue_update(self, queue_data):
        """Handle queue detection updates"""
        if queue_data:
            for queue in queue_data:
                if queue['wait_time'] > 180:  # Alert for long waits
                    print(f"⚠️ Long wait detected: Queue {queue['id']} - {queue['wait_time']:.0f}s")
    
    def _on_traffic_update(self, traffic_data):
        """Handle traffic analysis updates"""
        if traffic_data.get('condition') == 'jammed':
            print(f"🚨 Traffic jam detected! Avg speed: {traffic_data.get('average_speed', 0):.1f} km/h")

def main():
    """Main demo function"""
    print("EDGE-QI Real-Time Data Integration Demo")
    print("=" * 60)
    print("This demo shows how to process real-time data without hardware:")
    print("• Simulated camera feeds with realistic traffic")
    print("• Real-time object detection and tracking")
    print("• Queue detection and traffic analysis")
    print("• Anomaly detection and system monitoring")
    print("• Bandwidth optimization")
    print("=" * 60)
    
    demo = RealTimeDemo()
    
    # Ask user for demo preferences
    print("\nDemo Options:")
    print("1. Live video display (recommended)")
    print("2. Headless mode (statistics only)")
    
    try:
        choice = input("Choose option (1 or 2): ").strip()
        if choice == '2':
            demo.show_video = False
        
        duration = input("Demo duration in seconds (default 60): ").strip()
        duration = int(duration) if duration.isdigit() else 60
        
        print(f"\n🚀 Starting demo...")
        demo.start_demo(duration)
        
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    main()