"""
Headless Real-Time Data Integration Demo for EDGE-QI Framework

Demonstrates real-time data processing without GUI dependencies.
Perfect for systems without OpenCV GUI support or headless environments.
"""

import numpy as np
import time
import asyncio
import sys
import os
from typing import Dict, List, Any
import json

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Core.simulation.realtime_integrator import RealTimeDataIntegrator, RealTimeConfig

class HeadlessRealTimeDemo:
    """
    Headless demo of real-time data processing (no GUI required)
    """
    
    def __init__(self):
        # Configure real-time processing
        config = RealTimeConfig(
            frame_width=1280,
            frame_height=720,
            fps=15,  # Lower FPS for better performance
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
        self.integrator.register_detection_callback(self._on_detection_update)
        self.integrator.register_queue_callback(self._on_queue_update)
        self.integrator.register_traffic_callback(self._on_traffic_update)
        
        # Demo state
        self.frame_count = 0
        self.detection_history = []
        self.queue_history = []
        self.traffic_history = []
        self.alerts_shown = set()
        
        print("🎬 Headless Real-Time EDGE-QI Demo Initialized")
        print("=" * 60)
    
    def start_demo(self, duration: int = 60):
        """Start headless real-time demo for specified duration"""
        print(f"🚀 Starting {duration}-second headless real-time processing demo...")
        print("\nFeatures enabled:")
        print("✅ Simulated camera feeds with moving vehicles")
        print("✅ Real-time object detection and tracking")
        print("✅ Queue detection and analysis")
        print("✅ Traffic flow monitoring")
        print("✅ Anomaly detection")
        print("✅ Bandwidth optimization")
        print("✅ Performance monitoring")
        print("✅ Data logging and export")
        print("\n" + "=" * 60)
        
        # Start processing
        self.integrator.start_real_time_processing()
        
        try:
            self._run_headless_demo(duration)
        except KeyboardInterrupt:
            print("\n🛑 Demo interrupted by user")
        finally:
            # Stop processing and show results
            self.integrator.stop_real_time_processing()
            self._show_final_results()
            print("\n✅ Demo completed")
    
    def _run_headless_demo(self, duration: int):
        """Run headless demo with comprehensive monitoring"""
        print("📊 Starting comprehensive monitoring...")
        print("🔍 Real-time analysis in progress...")
        print("-" * 60)
        
        start_time = time.time()
        last_stats_time = start_time
        last_frame_save_time = start_time
        
        while time.time() - start_time < duration:
            current_time = time.time()
            
            # Print stats every 10 seconds
            if current_time - last_stats_time >= 10:
                self._print_detailed_stats()
                last_stats_time = current_time
            
            # Save frame data every 5 seconds
            if current_time - last_frame_save_time >= 5:
                self._save_current_frame_data()
                last_frame_save_time = current_time
            
            # Check for interesting events
            self._check_for_events()
            
            time.sleep(1)
        
        print("\n" + "=" * 60)
        print("🏁 Demo completed - generating final report...")
    
    def _print_detailed_stats(self):
        """Print comprehensive processing statistics"""
        stats = self.integrator.get_processing_stats()
        traffic_data = self.integrator.get_current_traffic_data()
        sensor_data = self.integrator.get_current_sensor_data()
        detections = self.integrator.get_current_detections()
        queues = self.integrator.get_current_queue_data()
        
        print(f"\n📊 Current Stats (Runtime: {stats.get('runtime', 0):.1f}s)")
        print(f"   🎬 Frames processed: {stats.get('frames_processed', 0)}")
        print(f"   🎯 Total detections: {stats.get('detections_made', 0)}")
        print(f"   🚗 Total queues detected: {stats.get('queues_detected', 0)}")
        print(f"   ⚠️ Anomalies found: {stats.get('anomalies_found', 0)}")
        print(f"   📺 Processing FPS: {stats.get('fps', 0):.1f}")
        
        if traffic_data:
            print(f"   🚦 Current traffic:")
            print(f"      • Condition: {traffic_data.get('condition', 'unknown').title()}")
            print(f"      • Vehicle count: {traffic_data.get('vehicle_count', 0)}")
            print(f"      • Average speed: {traffic_data.get('average_speed', 0):.1f} km/h")
            print(f"      • Density: {traffic_data.get('density', 0):.2f}")
            print(f"      • Throughput: {traffic_data.get('throughput', 0):.1f} vehicles/min")
        
        if sensor_data:
            print(f"   🖥️ System resources:")
            print(f"      • CPU usage: {sensor_data.get('cpu_usage', 0):.1f}%")
            print(f"      • Memory usage: {sensor_data.get('memory_usage', 0):.1f}%")
            print(f"      • Temperature: {sensor_data.get('temperature', 0):.1f}°C")
            print(f"      • Network latency: {sensor_data.get('network_latency', 0):.1f}ms")
        
        print(f"   📋 Current detections: {len(detections)} objects")
        print(f"   🚶 Active queues: {len(queues)}")
        
        if queues:
            for i, queue in enumerate(queues[:3]):  # Show first 3 queues
                print(f"      • Queue {i+1}: {queue['vehicle_count']} vehicles, {queue['wait_time']:.0f}s wait")
    
    def _save_current_frame_data(self):
        """Save current frame data for analysis"""
        current_data = {
            'timestamp': time.time(),
            'detections': self.integrator.get_current_detections(),
            'queues': self.integrator.get_current_queue_data(),
            'traffic': self.integrator.get_current_traffic_data(),
            'sensors': self.integrator.get_current_sensor_data(),
            'stats': self.integrator.get_processing_stats()
        }
        
        # Store in history for final analysis
        if current_data['detections']:
            self.detection_history.append(len(current_data['detections']))
        if current_data['queues']:
            self.queue_history.extend(current_data['queues'])
        if current_data['traffic']:
            self.traffic_history.append(current_data['traffic'])
        
        self.frame_count += 1
    
    def _check_for_events(self):
        """Check for interesting events and alert"""
        traffic_data = self.integrator.get_current_traffic_data()
        sensor_data = self.integrator.get_current_sensor_data()
        queues = self.integrator.get_current_queue_data()
        
        # Traffic congestion alert
        if traffic_data and traffic_data.get('condition') == 'jammed':
            alert_key = f"traffic_jam_{int(time.time() // 30)}"  # Alert every 30s max
            if alert_key not in self.alerts_shown:
                print(f"🚨 TRAFFIC JAM DETECTED!")
                print(f"   • Average speed: {traffic_data.get('average_speed', 0):.1f} km/h")
                print(f"   • Vehicle density: {traffic_data.get('density', 0):.2f}")
                self.alerts_shown.add(alert_key)
        
        # High resource usage alert
        if sensor_data:
            if sensor_data.get('cpu_usage', 0) > 80:
                alert_key = f"high_cpu_{int(time.time() // 30)}"
                if alert_key not in self.alerts_shown:
                    print(f"⚠️ HIGH CPU USAGE: {sensor_data['cpu_usage']:.1f}%")
                    self.alerts_shown.add(alert_key)
            
            if sensor_data.get('temperature', 0) > 50:
                alert_key = f"high_temp_{int(time.time() // 30)}"
                if alert_key not in self.alerts_shown:
                    print(f"🌡️ HIGH TEMPERATURE: {sensor_data['temperature']:.1f}°C")
                    self.alerts_shown.add(alert_key)
        
        # Long queue alert
        for queue in queues:
            if queue['wait_time'] > 180:  # 3 minutes
                alert_key = f"long_queue_{queue['id']}"
                if alert_key not in self.alerts_shown:
                    print(f"⏰ LONG QUEUE DETECTED!")
                    print(f"   • Queue {queue['id']}: {queue['wait_time']:.0f}s wait time")
                    print(f"   • {queue['vehicle_count']} vehicles waiting")
                    self.alerts_shown.add(alert_key)
    
    def _show_final_results(self):
        """Show comprehensive final results and analysis"""
        stats = self.integrator.get_processing_stats()
        
        print("\n" + "=" * 60)
        print("📈 FINAL PROCESSING REPORT")
        print("=" * 60)
        
        # Performance metrics
        print("🎯 Performance Metrics:")
        print(f"   • Total runtime: {stats.get('runtime', 0):.1f} seconds")
        print(f"   • Frames processed: {stats.get('frames_processed', 0)}")
        print(f"   • Average FPS: {stats.get('fps', 0):.1f}")
        print(f"   • Total detections: {stats.get('detections_made', 0)}")
        print(f"   • Total queues detected: {stats.get('queues_detected', 0)}")
        print(f"   • Anomalies found: {stats.get('anomalies_found', 0)}")
        
        # Detection analysis
        if self.detection_history:
            avg_detections = sum(self.detection_history) / len(self.detection_history)
            max_detections = max(self.detection_history)
            min_detections = min(self.detection_history)
            
            print(f"\n🔍 Detection Analysis:")
            print(f"   • Average detections per frame: {avg_detections:.1f}")
            print(f"   • Peak detections: {max_detections}")
            print(f"   • Minimum detections: {min_detections}")
        
        # Traffic analysis
        if self.traffic_history:
            conditions = [t.get('condition', 'unknown') for t in self.traffic_history]
            speeds = [t.get('average_speed', 0) for t in self.traffic_history]
            
            print(f"\n🚦 Traffic Analysis:")
            print(f"   • Average speed: {sum(speeds)/len(speeds):.1f} km/h")
            print(f"   • Peak speed: {max(speeds):.1f} km/h")
            print(f"   • Traffic conditions observed:")
            
            condition_counts = {}
            for condition in conditions:
                condition_counts[condition] = condition_counts.get(condition, 0) + 1
            
            for condition, count in condition_counts.items():
                percentage = (count / len(conditions)) * 100
                print(f"      • {condition.title()}: {count} times ({percentage:.1f}%)")
        
        # Queue analysis
        if self.queue_history:
            wait_times = [q['wait_time'] for q in self.queue_history]
            vehicle_counts = [q['vehicle_count'] for q in self.queue_history]
            
            print(f"\n🚶 Queue Analysis:")
            print(f"   • Total queue instances: {len(self.queue_history)}")
            print(f"   • Average wait time: {sum(wait_times)/len(wait_times):.1f} seconds")
            print(f"   • Maximum wait time: {max(wait_times):.1f} seconds")
            print(f"   • Average queue size: {sum(vehicle_counts)/len(vehicle_counts):.1f} vehicles")
            print(f"   • Largest queue: {max(vehicle_counts)} vehicles")
        
        # Alerts summary
        print(f"\n⚠️ Alerts Generated: {len(self.alerts_shown)}")
        if self.alerts_shown:
            alert_types = {}
            for alert in self.alerts_shown:
                alert_type = alert.split('_')[0]
                alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
            
            for alert_type, count in alert_types.items():
                print(f"   • {alert_type.replace('_', ' ').title()}: {count} alerts")
        
        # Save detailed report
        self._save_detailed_report(stats)
        
        print("\n✅ Real-time processing demonstration completed successfully!")
        print("📊 Detailed report saved to 'edge_qi_demo_report.json'")
    
    def _save_detailed_report(self, stats):
        """Save detailed report to JSON file"""
        report = {
            'demo_info': {
                'timestamp': time.time(),
                'duration': stats.get('runtime', 0),
                'demo_type': 'headless_realtime'
            },
            'performance_stats': stats,
            'detection_history': self.detection_history,
            'traffic_history': self.traffic_history,
            'queue_history': self.queue_history,
            'alerts_generated': list(self.alerts_shown),
            'analysis': {
                'avg_detections_per_frame': sum(self.detection_history) / len(self.detection_history) if self.detection_history else 0,
                'total_queue_instances': len(self.queue_history),
                'avg_wait_time': sum(q['wait_time'] for q in self.queue_history) / len(self.queue_history) if self.queue_history else 0,
                'avg_traffic_speed': sum(t.get('average_speed', 0) for t in self.traffic_history) / len(self.traffic_history) if self.traffic_history else 0
            }
        }
        
        try:
            with open('edge_qi_demo_report.json', 'w') as f:
                json.dump(report, f, indent=2, default=str)
        except Exception as e:
            print(f"⚠️ Could not save report: {e}")
    
    # Callback methods
    def _on_detection_update(self, detections):
        """Handle detection updates"""
        if len(detections) > 15:  # High activity threshold
            print(f"🎯 High activity detected: {len(detections)} objects in frame")
    
    def _on_queue_update(self, queue_data):
        """Handle queue detection updates"""
        if queue_data:
            for queue in queue_data:
                if queue['vehicle_count'] > 10:  # Large queue threshold
                    print(f"🚗 Large queue detected: {queue['vehicle_count']} vehicles in queue {queue['id']}")
    
    def _on_traffic_update(self, traffic_data):
        """Handle traffic analysis updates""" 
        # Traffic updates are handled in _check_for_events
        pass

def main():
    """Main demo function"""
    print("EDGE-QI Headless Real-Time Data Integration Demo")
    print("=" * 60)
    print("This demo processes real-time data without GUI dependencies:")
    print("• Simulated camera feeds with realistic traffic")
    print("• Real-time object detection and tracking")
    print("• Queue detection and traffic analysis")
    print("• Anomaly detection and system monitoring")
    print("• Comprehensive data logging and analysis")
    print("• Performance metrics and reporting")
    print("=" * 60)
    
    demo = HeadlessRealTimeDemo()
    
    try:
        duration_input = input("Demo duration in seconds (default 30): ").strip()
        duration = int(duration_input) if duration_input.isdigit() else 30
        
        print(f"\n🚀 Starting {duration}-second headless demo...")
        demo.start_demo(duration)
        
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    main()