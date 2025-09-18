# EdgeQI/ML/tasks/traffic_task.py

import time
from typing import Dict, Any, List, Optional
from .base_task import Task
from ..models.vision import YOLODetector, MobileNetDetector
from Core.traffic import TrafficFlowAnalyzer, VehicleType

class TrafficAnalysisTask(Task):
    """Traffic flow analysis task for smart traffic management"""
    
    def __init__(self, detector_type: str = "yolo", frame_width: int = 640, frame_height: int = 480):
        super().__init__("TrafficAnalysisTask")
        
        # Initialize computer vision detector
        if detector_type.lower() == "yolo":
            self.detector = YOLODetector()
        elif detector_type.lower() == "mobilenet":
            self.detector = MobileNetDetector()
        else:
            raise ValueError(f"Unsupported detector type: {detector_type}")
        
        # Initialize traffic analyzer
        self.traffic_analyzer = TrafficFlowAnalyzer(frame_width, frame_height)
        
        # Performance tracking
        self.analysis_count = 0
        self.start_time = time.time()
        
        print(f"[TrafficAnalysisTask] Initialized with {detector_type} detector")
    
    def run(self) -> Dict[str, Any]:
        """Run traffic analysis on current frame"""
        try:
            # Generate dummy frame for simulation
            frame = self._generate_dummy_frame()
            
            # Perform object detection
            detections = self.detector.detect(frame)
            
            # Filter for vehicles only
            vehicle_detections = self.detector.get_vehicle_detections(detections)
            
            # Convert to format expected by traffic analyzer
            vehicle_data = []
            for detection in vehicle_detections:
                vehicle_data.append({
                    'center': detection.center,
                    'bbox': detection.bbox,
                    'confidence': detection.confidence,
                    'vehicle_type': detection.class_name
                })
            
            # Run traffic flow analysis
            traffic_analysis = self.traffic_analyzer.analyze_traffic_flow(vehicle_data)
            
            # Get additional insights
            trends = self.traffic_analyzer.get_traffic_trends(minutes=5)
            
            # Combine results
            result = {
                "frame_info": {
                    "timestamp": time.time(),
                    "frame_size": {"width": self.traffic_analyzer.frame_width, "height": self.traffic_analyzer.frame_height}
                },
                "detection_summary": {
                    "total_detections": len(detections),
                    "vehicle_count": len(vehicle_detections),
                    "people_count": len(self.detector.get_people_detections(detections)),
                    "detector_type": self.detector.model_type if hasattr(self.detector, 'model_type') else "unknown"
                },
                "traffic_analysis": traffic_analysis,
                "traffic_trends": trends,
                "system_performance": self._get_performance_metrics(),
                "alerts": self._generate_traffic_alerts(traffic_analysis)
            }
            
            self.analysis_count += 1
            
            # Log summary
            vehicle_summary = traffic_analysis.get('vehicle_summary', {})
            density_analysis = traffic_analysis.get('density_analysis', {})
            
            print(f"[TrafficAnalysisTask] Analyzed {vehicle_summary.get('total_vehicles', 0)} vehicles, "
                  f"congestion level: {density_analysis.get('congestion_level', 0):.2f}, "
                  f"avg speed: {density_analysis.get('average_speed', 0):.1f}")
            
            return result
            
        except Exception as e:
            print(f"[TrafficAnalysisTask] Error during traffic analysis: {e}")
            return {
                "error": str(e),
                "timestamp": time.time()
            }
    
    def _generate_dummy_frame(self):
        """Generate a dummy frame for simulation"""
        import numpy as np
        
        # Create a synthetic frame with some patterns
        frame = np.random.randint(0, 255, (self.traffic_analyzer.frame_height, self.traffic_analyzer.frame_width, 3), dtype=np.uint8)
        
        # Add some "road-like" patterns
        # Horizontal road
        road_y = self.traffic_analyzer.frame_height // 2
        frame[road_y-20:road_y+20, :] = [80, 80, 80]  # Gray road
        
        # Vertical road
        road_x = self.traffic_analyzer.frame_width // 2
        frame[:, road_x-20:road_x+20] = [80, 80, 80]  # Gray road
        
        # Add lane markings
        frame[road_y-2:road_y+2, ::50] = [255, 255, 255]  # White lane markings
        frame[::50, road_x-2:road_x+2] = [255, 255, 255]  # White lane markings
        
        return frame
    
    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get task performance metrics"""
        current_time = time.time()
        uptime = current_time - self.start_time
        
        return {
            "analysis_count": self.analysis_count,
            "uptime_seconds": round(uptime, 1),
            "analyses_per_minute": round((self.analysis_count / max(uptime / 60, 1)), 2),
            "memory_usage": "N/A"  # Could implement actual memory monitoring
        }
    
    def _generate_traffic_alerts(self, traffic_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate traffic alerts based on analysis results"""
        alerts = []
        
        # Get metrics
        density_analysis = traffic_analysis.get('density_analysis', {})
        vehicle_summary = traffic_analysis.get('vehicle_summary', {})
        signal_recommendations = traffic_analysis.get('signal_recommendations', {})
        
        congestion_level = density_analysis.get('congestion_level', 0)
        total_vehicles = vehicle_summary.get('total_vehicles', 0)
        stopped_vehicles = vehicle_summary.get('stopped_vehicles', 0)
        
        # Congestion alerts
        if congestion_level > 0.8:
            alerts.append({
                "type": "congestion",
                "severity": "critical",
                "message": f"Critical congestion detected (level: {congestion_level:.2f})",
                "timestamp": time.time()
            })
        elif congestion_level > 0.6:
            alerts.append({
                "type": "congestion",
                "severity": "warning",
                "message": f"High congestion detected (level: {congestion_level:.2f})",
                "timestamp": time.time()
            })
        
        # Traffic jam alerts
        if total_vehicles > 0 and stopped_vehicles / total_vehicles > 0.7:
            alerts.append({
                "type": "traffic_jam",
                "severity": "warning",
                "message": f"Traffic jam detected: {stopped_vehicles}/{total_vehicles} vehicles stopped",
                "timestamp": time.time()
            })
        
        # Signal timing alerts
        for intersection_id, signal_data in signal_recommendations.items():
            queue_lengths = signal_data.get('queue_lengths', {})
            max_queue = max(queue_lengths.values()) if queue_lengths else 0
            
            if max_queue > 10:
                alerts.append({
                    "type": "signal_optimization",
                    "severity": "info",
                    "message": f"Long queue detected at {intersection_id}: {max_queue} vehicles",
                    "intersection": intersection_id,
                    "timestamp": time.time()
                })
        
        # Hotspot alerts
        hotspots = density_analysis.get('hotspots', [])
        if len(hotspots) > 3:
            alerts.append({
                "type": "hotspot",
                "severity": "warning",
                "message": f"Multiple congestion hotspots detected: {len(hotspots)} areas",
                "timestamp": time.time()
            })
        
        return alerts
    
    def get_intersection_recommendations(self) -> Dict[str, Any]:
        """Get specific recommendations for traffic signal optimization"""
        # Get latest traffic analysis
        dummy_frame = self._generate_dummy_frame()
        detections = self.detector.detect(dummy_frame)
        vehicle_detections = self.detector.get_vehicle_detections(detections)
        
        vehicle_data = []
        for detection in vehicle_detections:
            vehicle_data.append({
                'center': detection.center,
                'bbox': detection.bbox,
                'confidence': detection.confidence,
                'vehicle_type': detection.class_name
            })
        
        traffic_analysis = self.traffic_analyzer.analyze_traffic_flow(vehicle_data)
        signal_recommendations = traffic_analysis.get('signal_recommendations', {})
        
        recommendations = {}
        for intersection_id, signal_data in signal_recommendations.items():
            recommendations[intersection_id] = {
                "current_phase": signal_data.get('current_phase'),
                "optimal_timing": signal_data.get('optimal_timing'),
                "extend_phase": signal_data.get('extend_current_phase'),
                "queue_status": signal_data.get('queue_lengths'),
                "priority_direction": self._determine_priority_direction(signal_data),
                "efficiency_gain": self._estimate_efficiency_gain(signal_data)
            }
        
        return recommendations
    
    def _determine_priority_direction(self, signal_data: Dict) -> Optional[str]:
        """Determine which direction should have priority"""
        queue_lengths = signal_data.get('queue_lengths', {})
        flow_rates = signal_data.get('flow_rates', {})
        
        if not queue_lengths and not flow_rates:
            return None
        
        # Combine queue length and flow rate for priority scoring
        priority_scores = {}
        for direction in set(list(queue_lengths.keys()) + list(flow_rates.keys())):
            queue_score = queue_lengths.get(direction, 0) * 2  # Weight queues more heavily
            flow_score = flow_rates.get(direction, 0)
            priority_scores[direction] = queue_score + flow_score
        
        if priority_scores:
            return max(priority_scores, key=priority_scores.get)
        
        return None
    
    def _estimate_efficiency_gain(self, signal_data: Dict) -> float:
        """Estimate potential efficiency gain from optimal timing"""
        current_timing = signal_data.get('optimal_timing', {})
        queue_lengths = signal_data.get('queue_lengths', {})
        
        if not current_timing or not queue_lengths:
            return 0.0
        
        # Simple efficiency calculation based on queue clearing potential
        total_queue = sum(queue_lengths.values())
        total_green_time = sum(current_timing.get(phase, 0) for phase in ['north_south', 'east_west'])
        
        if total_green_time > 0 and total_queue > 0:
            # Estimate vehicles that can be cleared per second
            clearance_rate = 0.5  # vehicles per second (approximate)
            clearable_vehicles = total_green_time * clearance_rate
            efficiency = min(clearable_vehicles / total_queue, 1.0)
            return round(efficiency * 100, 1)  # Return as percentage
        
        return 100.0  # No queue, maximum efficiency
    
    def get_traffic_statistics(self) -> Dict[str, Any]:
        """Get comprehensive traffic statistics"""
        return {
            "system_performance": self._get_performance_metrics(),
            "current_traffic_state": self.traffic_analyzer.analysis_history[-1] if self.traffic_analyzer.analysis_history else None,
            "historical_trends": self.traffic_analyzer.get_traffic_trends(minutes=30),
            "intersection_status": {
                intersection_id: {
                    "vehicles_present": len(self.traffic_analyzer.vehicle_tracker),
                    "signal_state": "adaptive",  # Would be actual state in real implementation
                    "efficiency_rating": self._estimate_efficiency_gain({}) or 85.0
                }
                for intersection_id in self.traffic_analyzer.intersections.keys()
            }
        }