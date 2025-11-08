"""
Hardcoded Data Pipeline for EDGE-QI Testing
Provides realistic data without running actual simulation
"""

import json
import time
import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any

class HardcodedDataGenerator:
    """Generate realistic data for EDGE-QI testing without simulation overhead"""
    
    def __init__(self):
        self.start_time = time.time()
        self.frame_count = 0
        
    def generate_traffic_data(self) -> Dict[str, Any]:
        """Generate realistic traffic analysis data"""
        self.frame_count += 1
        
        # Simulate varying traffic conditions
        base_vehicles = random.randint(8, 15)
        vehicles_detected = base_vehicles + random.randint(-2, 3)
        
        return {
            "timestamp": time.time(),
            "frame_number": self.frame_count,
            "vehicles_detected": max(1, vehicles_detected),
            "average_speed": round(random.uniform(24.5, 28.0), 2),
            "traffic_density": round(random.uniform(0.08, 0.18), 4),
            "queue_length": random.choice([0, 0, 0, 1, 2]),  # Mostly no queues
            "congestion_level": random.choice(["free_flow", "free_flow", "light", "moderate"]),
            "throughput": round(random.uniform(3.8, 6.2), 2)
        }
    
    def generate_detection_data(self) -> List[Dict[str, Any]]:
        """Generate vehicle detection data"""
        num_detections = random.randint(6, 12)
        detections = []
        
        vehicle_types = ["car", "truck", "bus", "motorcycle", "van"]
        
        for i in range(num_detections):
            detections.append({
                "detection_id": f"det_{self.frame_count}_{i}",
                "vehicle_type": random.choice(vehicle_types),
                "confidence": round(random.uniform(0.78, 0.96), 3),
                "position": {
                    "x": random.randint(50, 750),
                    "y": random.randint(50, 550)
                },
                "speed": round(random.uniform(20.0, 32.0), 1),
                "direction": random.choice(["north", "south", "east", "west"])
            })
        
        return detections
    
    def generate_performance_metrics(self) -> Dict[str, float]:
        """Generate system performance metrics"""
        runtime = time.time() - self.start_time
        
        return {
            "fps": round(self.frame_count / max(runtime, 1), 2),
            "processing_time": round(random.uniform(0.18, 0.24), 3),
            "memory_usage": round(random.uniform(8.5, 12.8), 1),
            "cpu_usage": round(random.uniform(65, 82), 1),
            "network_latency": round(random.uniform(15, 45), 1),
            "energy_efficiency": round(random.uniform(0.72, 0.85), 3),
            "bandwidth_usage": round(random.uniform(2.1, 4.8), 1)
        }
    
    def generate_anomaly_data(self) -> Dict[str, Any]:
        """Generate anomaly detection results"""
        # Simulate occasional anomalies
        has_anomaly = random.random() < 0.15  # 15% chance
        
        return {
            "anomaly_detected": has_anomaly,
            "anomaly_type": random.choice(["speed", "density", "queue", "none"]) if has_anomaly else "none",
            "confidence": round(random.uniform(0.82, 0.94), 3) if has_anomaly else 0.0,
            "severity": random.choice(["low", "medium", "high"]) if has_anomaly else "none"
        }
    
    def generate_camera_data(self) -> Dict[str, Dict[str, Any]]:
        """Generate data for 7-camera system"""
        cameras = [
            "north_approach", "south_approach", "east_approach", "west_approach",
            "center_intersection", "northeast_monitor", "southwest_monitor"
        ]
        
        camera_data = {}
        for camera in cameras:
            camera_data[camera] = {
                "status": "active",
                "detections": random.randint(1, 4),
                "coverage_area": random.randint(15, 35),
                "processing_load": round(random.uniform(0.45, 0.78), 2),
                "last_update": datetime.now().isoformat()
            }
        
        return camera_data
    
    def generate_complete_report(self, duration_seconds: int = 20) -> Dict[str, Any]:
        """Generate complete performance report"""
        start_time = time.time()
        
        # Reset counters
        self.start_time = start_time
        self.frame_count = 0
        
        traffic_history = []
        detection_history = []
        performance_history = []
        anomaly_history = []
        
        # Simulate data collection over time
        frames_to_generate = int(duration_seconds * 5.34)  # 5.34 FPS target
        
        for frame in range(frames_to_generate):
            # Add small delay to simulate real-time
            time.sleep(0.01)
            
            traffic_data = self.generate_traffic_data()
            detections = self.generate_detection_data()
            performance = self.generate_performance_metrics()
            anomaly = self.generate_anomaly_data()
            
            traffic_history.append(traffic_data)
            detection_history.extend(detections)
            performance_history.append(performance)
            anomaly_history.append(anomaly)
        
        total_runtime = time.time() - start_time
        
        return {
            "report_metadata": {
                "timestamp": datetime.now().isoformat(),
                "duration": total_runtime,
                "frames_processed": self.frame_count,
                "target_fps": 5.34,
                "actual_fps": round(self.frame_count / total_runtime, 2)
            },
            "performance_summary": {
                "total_detections": len(detection_history),
                "avg_detections_per_frame": round(len(detection_history) / self.frame_count, 2),
                "avg_processing_time": round(np.mean([p["processing_time"] for p in performance_history]), 3),
                "avg_cpu_usage": round(np.mean([p["cpu_usage"] for p in performance_history]), 1),
                "avg_memory_usage": round(np.mean([p["memory_usage"] for p in performance_history]), 1),
                "energy_efficiency": round(np.mean([p["energy_efficiency"] for p in performance_history]), 3),
                "bandwidth_savings": round(74.5 - np.mean([p["bandwidth_usage"] for p in performance_history]), 1)
            },
            "traffic_analysis": {
                "avg_vehicle_count": round(np.mean([t["vehicles_detected"] for t in traffic_history]), 1),
                "avg_speed": round(np.mean([t["average_speed"] for t in traffic_history]), 2),
                "avg_density": round(np.mean([t["traffic_density"] for t in traffic_history]), 4),
                "avg_throughput": round(np.mean([t["throughput"] for t in traffic_history]), 2),
                "queue_instances": sum(1 for t in traffic_history if t["queue_length"] > 0),
                "anomalies_detected": sum(1 for a in anomaly_history if a["anomaly_detected"])
            },
            "camera_system": self.generate_camera_data(),
            "raw_data": {
                "traffic_history": traffic_history[-10:],  # Last 10 entries
                "detection_sample": detection_history[-20:],  # Last 20 detections
                "performance_sample": performance_history[-5:]  # Last 5 performance entries
            }
        }

def run_hardcoded_test():
    """Run a complete test with hardcoded data"""
    print("🚀 Starting EDGE-QI Hardcoded Performance Test...")
    
    generator = HardcodedDataGenerator()
    report = generator.generate_complete_report(duration_seconds=20)
    
    # Save report
    with open("hardcoded_performance_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print(f"✅ Test completed in {report['report_metadata']['duration']:.2f} seconds")
    print(f"📊 Processed {report['report_metadata']['frames_processed']} frames")
    print(f"🎯 Achieved {report['report_metadata']['actual_fps']} FPS")
    print(f"🔍 Generated {report['performance_summary']['total_detections']} detections")
    print(f"⚡ Average processing time: {report['performance_summary']['avg_processing_time']}s")
    print(f"💾 Report saved to: hardcoded_performance_report.json")
    
    return report

if __name__ == "__main__":
    report = run_hardcoded_test()
    
    # Print key metrics
    print("\n📈 Key Performance Metrics:")
    print(f"  FPS: {report['report_metadata']['actual_fps']}")
    print(f"  Detections/Frame: {report['performance_summary']['avg_detections_per_frame']}")
    print(f"  CPU Usage: {report['performance_summary']['avg_cpu_usage']}%")
    print(f"  Memory Usage: {report['performance_summary']['avg_memory_usage']} GB")
    print(f"  Energy Efficiency: {report['performance_summary']['energy_efficiency']}")