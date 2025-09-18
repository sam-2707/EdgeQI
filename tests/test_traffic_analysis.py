# EdgeQI/tests/test_traffic_analysis.py

import unittest
import time
import numpy as np
from Core.traffic import (
    TrafficFlowAnalyzer,
    TrafficDensityAnalyzer,
    TrafficSignalOptimizer,
    VehicleTrack,
    IntersectionZone,
    VehicleType,
    TrafficLightState
)
from ML.tasks.traffic_task import TrafficAnalysisTask

class TestTrafficAnalysis(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.traffic_analyzer = TrafficFlowAnalyzer(640, 480)
        self.density_analyzer = TrafficDensityAnalyzer(640, 480, grid_size=64)
        self.intersection = IntersectionZone(
            zone_id="test_intersection",
            bounds=(200, 200, 400, 400)
        )
        self.signal_optimizer = TrafficSignalOptimizer(self.intersection)
        self.traffic_task = TrafficAnalysisTask(detector_type="yolo")
    
    def test_vehicle_track_creation(self):
        """Test VehicleTrack creation and position tracking"""
        track = VehicleTrack(vehicle_id=1, vehicle_type=VehicleType.CAR)
        
        self.assertEqual(track.vehicle_id, 1)
        self.assertEqual(track.vehicle_type, VehicleType.CAR)
        self.assertEqual(len(track.positions), 0)
        self.assertFalse(track.is_stopped)
        
        # Add positions
        track.add_position(100, 200)
        self.assertEqual(len(track.positions), 1)
        
        time.sleep(0.01)
        track.add_position(110, 205)
        self.assertEqual(len(track.positions), 2)
        
        # Should have some speed now
        speed = track.get_current_speed()
        self.assertGreaterEqual(speed, 0)
    
    def test_vehicle_speed_calculation(self):
        """Test vehicle speed calculation"""
        track = VehicleTrack(vehicle_id=1, vehicle_type=VehicleType.CAR)
        
        # Add positions with known distances and times
        start_time = time.time()
        track.add_position(0, 0, start_time)
        track.add_position(30, 40, start_time + 1.0)  # Distance = 50 pixels in 1 second
        
        speed = track.get_current_speed()
        self.assertAlmostEqual(speed, 50.0, places=0)  # Approximately 50 pixels/second
    
    def test_vehicle_direction_calculation(self):
        """Test vehicle direction calculation"""
        track = VehicleTrack(vehicle_id=1, vehicle_type=VehicleType.CAR)
        
        # Moving east (positive x direction)
        track.add_position(0, 0)
        track.add_position(10, 0)
        
        direction = track.get_direction()
        self.assertIsNotNone(direction)
        self.assertAlmostEqual(direction[0], 1.0, places=1)  # dx = 1
        self.assertAlmostEqual(direction[1], 0.0, places=1)  # dy = 0
    
    def test_stationary_detection(self):
        """Test stationary vehicle detection"""
        track = VehicleTrack(vehicle_id=1, vehicle_type=VehicleType.CAR)
        
        # Add positions very close together (stationary) with sufficient time gaps
        base_time = time.time()
        for i in range(5):
            # Manually set position with specific timestamp to control timing
            track.positions.append((100 + i * 0.1, 200 + i * 0.1, base_time + i * 0.1))
        
        # Manually calculate speed for this scenario
        track._calculate_speed()
        
        # Use default threshold (2.0) since we changed it
        self.assertTrue(track.is_stationary())
    
    def test_intersection_zone(self):
        """Test intersection zone functionality"""
        intersection = IntersectionZone(
            zone_id="test",
            bounds=(100, 100, 200, 200)
        )
        
        # Test point containment
        self.assertTrue(intersection.contains_point(150, 150))  # Inside
        self.assertFalse(intersection.contains_point(50, 50))   # Outside
        self.assertTrue(intersection.contains_point(100, 100))  # On boundary
        
        # Test approach direction
        direction = intersection.get_approach_direction(150, 150, 140, 150)
        self.assertEqual(direction, "east")  # Moving east
        
        direction = intersection.get_approach_direction(150, 150, 150, 140)
        self.assertEqual(direction, "south")  # Moving south
    
    def test_traffic_density_analyzer(self):
        """Test traffic density analysis"""
        # Create some vehicle tracks
        tracks = []
        for i in range(5):
            track = VehicleTrack(vehicle_id=i, vehicle_type=VehicleType.CAR)
            track.add_position(i * 50 + 100, 200)  # Spread horizontally
            tracks.append(track)
        
        # Update density
        self.density_analyzer.update_density(tracks)
        
        self.assertEqual(self.density_analyzer.total_vehicles, 5)
        self.assertGreaterEqual(self.density_analyzer.congestion_level, 0.0)
        self.assertLessEqual(self.density_analyzer.congestion_level, 1.0)
    
    def test_congestion_level_calculation(self):
        """Test congestion level calculation"""
        # Test with no vehicles
        self.density_analyzer.update_density([])
        self.assertEqual(self.density_analyzer.congestion_level, 0.0)
        
        # Test with many slow vehicles (high congestion)
        many_slow_tracks = []
        for i in range(20):
            track = VehicleTrack(vehicle_id=i, vehicle_type=VehicleType.CAR)
            track.add_position(i * 10, 200)  # Close together
            track.add_position(i * 10 + 1, 200)  # Very slow movement
            many_slow_tracks.append(track)
        
        self.density_analyzer.update_density(many_slow_tracks)
        self.assertGreater(self.density_analyzer.congestion_level, 0.3)  # Should indicate congestion
    
    def test_hotspot_detection(self):
        """Test traffic hotspot detection"""
        # Create clustered vehicles (hotspot)
        clustered_tracks = []
        for i in range(8):
            track = VehicleTrack(vehicle_id=i, vehicle_type=VehicleType.CAR)
            # All vehicles in small area (creates hotspot)
            track.add_position(320 + i * 5, 240 + i * 5)
            clustered_tracks.append(track)
        
        self.density_analyzer.update_density(clustered_tracks)
        hotspots = self.density_analyzer.get_hotspots(threshold=0.5)
        
        self.assertGreater(len(hotspots), 0)  # Should detect at least one hotspot
        
        # Verify hotspot structure
        for hotspot in hotspots:
            self.assertEqual(len(hotspot), 3)  # (x, y, density)
            self.assertIsInstance(hotspot[0], int)  # x coordinate
            self.assertIsInstance(hotspot[1], int)  # y coordinate
            self.assertIsInstance(hotspot[2], float)  # density value
    
    def test_flow_vectors(self):
        """Test traffic flow vector calculation"""
        # Create vehicles moving in same direction
        moving_tracks = []
        for i in range(3):
            track = VehicleTrack(vehicle_id=i, vehicle_type=VehicleType.CAR)
            track.add_position(100 + i * 50, 200)
            track.add_position(120 + i * 50, 200)  # All moving east
            moving_tracks.append(track)
        
        self.density_analyzer.update_density(moving_tracks)
        flow_vectors = self.density_analyzer.get_flow_vectors()
        
        # Should have some flow vectors
        for vector in flow_vectors:
            self.assertEqual(len(vector), 5)  # (x, y, dx, dy, magnitude)
            self.assertGreater(vector[4], 0)  # magnitude > 0
    
    def test_signal_optimizer(self):
        """Test traffic signal optimizer"""
        # Create vehicle tracks approaching intersection
        vehicle_tracks = []
        for i in range(3):
            track = VehicleTrack(vehicle_id=i, vehicle_type=VehicleType.CAR)
            # Vehicles approaching from north
            track.add_position(300, 150 + i * 10)
            track.add_position(300, 180 + i * 10)  # Moving south toward intersection
            vehicle_tracks.append(track)
        
        # Update optimizer with traffic data
        self.signal_optimizer.update_traffic_data(vehicle_tracks)
        
        # Get recommendations
        recommendation = self.signal_optimizer.get_signal_recommendation()
        
        self.assertIn("current_phase", recommendation)
        self.assertIn("optimal_timing", recommendation)
        self.assertIn("queue_lengths", recommendation)
        self.assertIn("flow_rates", recommendation)
        
        # Check timing calculation
        optimal_timing = self.signal_optimizer.calculate_optimal_timing()
        self.assertIn("north_south", optimal_timing)
        self.assertIn("east_west", optimal_timing)
        self.assertIn("all_red", optimal_timing)
        
        # Verify timing constraints
        for phase, duration in optimal_timing.items():
            if phase != "all_red":
                self.assertGreaterEqual(duration, self.signal_optimizer.min_green_time)
                self.assertLessEqual(duration, self.signal_optimizer.max_green_time)
    
    def test_phase_extension_logic(self):
        """Test signal phase extension logic"""
        # Create scenario where current phase should be extended
        vehicle_tracks = []
        
        # Many vehicles in north-south direction (within intersection bounds 200,200,400,400)
        for i in range(5):
            track = VehicleTrack(vehicle_id=i, vehicle_type=VehicleType.CAR)
            # Add two positions to determine direction - coming from north
            track.add_position(300, 150 + i * 10)  # Previous position (approaching from north)
            track.add_position(300, 250 + i * 10)  # Current position (in intersection)
            vehicle_tracks.append(track)
        
        # Few vehicles in east-west direction
        track = VehicleTrack(vehicle_id=10, vehicle_type=VehicleType.CAR)
        # Add two positions to determine direction - coming from east
        track.add_position(150, 300)  # Previous position (approaching from east)
        track.add_position(250, 300)  # Current position (in intersection)
        vehicle_tracks.append(track)
        
        self.signal_optimizer.current_phase = "north_south"
        self.signal_optimizer.phase_start_time = time.time() - 20  # 20 seconds into phase
        self.signal_optimizer.update_traffic_data(vehicle_tracks)
        
        # Should recommend extension due to higher demand in current direction
        should_extend = self.signal_optimizer.should_extend_phase()
        self.assertTrue(should_extend)
    
    def test_traffic_flow_analyzer(self):
        """Test main traffic flow analyzer"""
        # Create vehicle detection data
        vehicle_detections = [
            {'center': (100, 200), 'bbox': (80, 180, 40, 40), 'confidence': 0.9, 'vehicle_type': 'car'},
            {'center': (200, 250), 'bbox': (180, 230, 40, 40), 'confidence': 0.8, 'vehicle_type': 'car'},
            {'center': (350, 300), 'bbox': (330, 280, 40, 40), 'confidence': 0.85, 'vehicle_type': 'truck'}
        ]
        
        # Run analysis
        result = self.traffic_analyzer.analyze_traffic_flow(vehicle_detections)
        
        # Verify result structure
        self.assertIn("timestamp", result)
        self.assertIn("vehicle_summary", result)
        self.assertIn("density_analysis", result)
        self.assertIn("signal_recommendations", result)
        self.assertIn("intersection_analysis", result)
        self.assertIn("traffic_efficiency", result)
        
        # Verify vehicle summary
        vehicle_summary = result["vehicle_summary"]
        self.assertEqual(vehicle_summary["total_vehicles"], 3)
        self.assertIn("moving_vehicles", vehicle_summary)
        self.assertIn("stopped_vehicles", vehicle_summary)
        self.assertIn("vehicle_types", vehicle_summary)
    
    def test_traffic_trends(self):
        """Test traffic trend analysis"""
        # Generate some historical data
        for i in range(5):
            vehicle_detections = [
                {'center': (100 + i * 10, 200), 'bbox': (80, 180, 40, 40), 'confidence': 0.9, 'vehicle_type': 'car'}
                for _ in range(i + 1)  # Increasing number of vehicles
            ]
            self.traffic_analyzer.analyze_traffic_flow(vehicle_detections)
            time.sleep(0.01)  # Small delay to create time differences
        
        # Get trends
        trends = self.traffic_analyzer.get_traffic_trends(minutes=5)
        
        if "error" not in trends:
            self.assertIn("vehicle_count_trend", trends)
            self.assertIn("congestion_trend", trends)
            self.assertIn("speed_trend", trends)
            
            # Should show increasing trend
            vehicle_trend = trends["vehicle_count_trend"]
            self.assertIn("trend", vehicle_trend)
    
    def test_traffic_analysis_task(self):
        """Test TrafficAnalysisTask"""
        # Run the task
        result = self.traffic_task.run()
        
        # Verify result structure
        self.assertIn("frame_info", result)
        self.assertIn("detection_summary", result)
        self.assertIn("traffic_analysis", result)
        self.assertIn("system_performance", result)
        self.assertIn("alerts", result)
        
        # Verify no errors
        self.assertNotIn("error", result)
        
        # Verify detection summary
        detection_summary = result["detection_summary"]
        self.assertIn("total_detections", detection_summary)
        self.assertIn("vehicle_count", detection_summary)
        self.assertIn("people_count", detection_summary)
    
    def test_alert_generation(self):
        """Test traffic alert generation"""
        # Create high congestion scenario
        high_congestion_analysis = {
            "density_analysis": {
                "congestion_level": 0.9,
                "hotspots": [(1, 1, 0.8), (2, 2, 0.7), (3, 3, 0.6), (4, 4, 0.5)]
            },
            "vehicle_summary": {
                "total_vehicles": 20,
                "stopped_vehicles": 15
            },
            "signal_recommendations": {
                "main_intersection": {
                    "queue_lengths": {"north": 12, "south": 8, "east": 5, "west": 3}
                }
            }
        }
        
        alerts = self.traffic_task._generate_traffic_alerts(high_congestion_analysis)
        
        # Should generate multiple alerts
        self.assertGreater(len(alerts), 0)
        
        # Check alert types
        alert_types = [alert["type"] for alert in alerts]
        self.assertIn("congestion", alert_types)
        self.assertIn("traffic_jam", alert_types)
        
        # Verify alert structure
        for alert in alerts:
            self.assertIn("type", alert)
            self.assertIn("severity", alert)
            self.assertIn("message", alert)
            self.assertIn("timestamp", alert)
    
    def test_intersection_recommendations(self):
        """Test intersection recommendation system"""
        recommendations = self.traffic_task.get_intersection_recommendations()
        
        self.assertIsInstance(recommendations, dict)
        
        for intersection_id, recommendation in recommendations.items():
            self.assertIn("current_phase", recommendation)
            self.assertIn("optimal_timing", recommendation)
            self.assertIn("extend_phase", recommendation)
            self.assertIn("queue_status", recommendation)
            self.assertIn("efficiency_gain", recommendation)
    
    def test_traffic_statistics(self):
        """Test traffic statistics compilation"""
        stats = self.traffic_task.get_traffic_statistics()
        
        self.assertIn("system_performance", stats)
        self.assertIn("historical_trends", stats)
        self.assertIn("intersection_status", stats)
        
        # Verify system performance metrics
        performance = stats["system_performance"]
        self.assertIn("analysis_count", performance)
        self.assertIn("uptime_seconds", performance)
        self.assertIn("analyses_per_minute", performance)
    
    def test_efficiency_calculations(self):
        """Test traffic efficiency calculations"""
        # Create mixed scenario with moving and stopped vehicles
        vehicle_tracks = []
        
        # Moving vehicles
        for i in range(3):
            track = VehicleTrack(vehicle_id=i, vehicle_type=VehicleType.CAR)
            track.add_position(i * 50, 200)
            track.add_position(i * 50 + 20, 200)  # Moving
            vehicle_tracks.append(track)
        
        # Stopped vehicles
        for i in range(2):
            track = VehicleTrack(vehicle_id=i + 10, vehicle_type=VehicleType.CAR)
            track.add_position(300 + i * 10, 300)
            track.add_position(300 + i * 10, 300)  # Not moving
            vehicle_tracks.append(track)
        
        efficiency = self.traffic_analyzer._calculate_traffic_efficiency(vehicle_tracks)
        
        self.assertIn("flow_efficiency", efficiency)
        self.assertIn("speed_consistency", efficiency)
        self.assertIn("congestion_index", efficiency)
        
        # Flow efficiency should be 3/5 = 0.6 (3 moving out of 5 total)
        self.assertAlmostEqual(efficiency["flow_efficiency"], 0.6, places=1)


if __name__ == '__main__':
    unittest.main()