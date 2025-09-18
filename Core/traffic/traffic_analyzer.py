# EdgeQI/Core/traffic/traffic_analyzer.py

import numpy as np
import time
import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque
from enum import Enum

class VehicleType(Enum):
    """Types of vehicles that can be detected"""
    CAR = "car"
    MOTORCYCLE = "motorcycle"
    BUS = "bus"
    TRUCK = "truck"
    BICYCLE = "bicycle"
    UNKNOWN = "unknown"

class TrafficLightState(Enum):
    """Traffic light states"""
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    FLASHING_RED = "flashing_red"
    FLASHING_YELLOW = "flashing_yellow"

@dataclass
class VehicleTrack:
    """Represents a tracked vehicle"""
    vehicle_id: int
    vehicle_type: VehicleType
    positions: deque = field(default_factory=lambda: deque(maxlen=20))
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    is_stopped: bool = False
    waiting_time: float = 0.0
    speed_history: deque = field(default_factory=lambda: deque(maxlen=10))
    
    def add_position(self, x: float, y: float, timestamp: float = None):
        """Add a new position to the vehicle track"""
        if timestamp is None:
            timestamp = time.time()
        
        self.positions.append((x, y, timestamp))
        self.last_seen = timestamp
        
        # Calculate speed if we have enough positions
        if len(self.positions) >= 2:
            self._calculate_speed()
    
    def _calculate_speed(self):
        """Calculate current speed based on recent positions"""
        if len(self.positions) < 2:
            return
        
        recent_positions = list(self.positions)[-3:]  # Use last 3 positions
        if len(recent_positions) < 2:
            return
        
        # Calculate distance and time
        distances = []
        times = []
        
        for i in range(1, len(recent_positions)):
            x1, y1, t1 = recent_positions[i-1]
            x2, y2, t2 = recent_positions[i]
            
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            time_diff = t2 - t1
            
            if time_diff > 0:
                speed = distance / time_diff  # pixels per second
                self.speed_history.append(speed)
    
    def get_current_speed(self) -> float:
        """Get current speed (average of recent speeds)"""
        if not self.speed_history:
            return 0.0
        return sum(self.speed_history) / len(self.speed_history)
    
    def get_direction(self) -> Optional[Tuple[float, float]]:
        """Get movement direction as a unit vector"""
        if len(self.positions) < 2:
            return None
        
        # Use first and last positions for direction
        x1, y1, _ = self.positions[0]
        x2, y2, _ = self.positions[-1]
        
        dx = x2 - x1
        dy = y2 - y1
        
        magnitude = math.sqrt(dx**2 + dy**2)
        if magnitude == 0:
            return None
        
        return (dx / magnitude, dy / magnitude)
    
    def is_stationary(self, threshold: float = 2.0) -> bool:
        """Check if vehicle is stationary based on speed threshold"""
        current_speed = self.get_current_speed()
        return current_speed < threshold
    
    def update_stationary_status(self):
        """Update the is_stopped status based on recent movement"""
        self.is_stopped = self.is_stationary()

@dataclass
class IntersectionZone:
    """Represents an intersection zone for traffic analysis"""
    zone_id: str
    bounds: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    approach_directions: List[str] = field(default_factory=lambda: ["north", "south", "east", "west"])
    traffic_lights: Dict[str, TrafficLightState] = field(default_factory=dict)
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if a point is within the intersection zone"""
        x1, y1, x2, y2 = self.bounds
        return x1 <= x <= x2 and y1 <= y <= y2
    
    def get_approach_direction(self, x: float, y: float, prev_x: float, prev_y: float) -> Optional[str]:
        """Determine approach direction based on vehicle movement"""
        center_x = (self.bounds[0] + self.bounds[2]) / 2
        center_y = (self.bounds[1] + self.bounds[3]) / 2
        
        # Calculate movement vector
        dx = x - prev_x
        dy = y - prev_y
        
        # Determine primary direction
        if abs(dx) > abs(dy):
            return "east" if dx > 0 else "west"
        else:
            return "south" if dy > 0 else "north"

class TrafficDensityAnalyzer:
    """Analyzes traffic density and flow patterns"""
    
    def __init__(self, frame_width: int = 640, frame_height: int = 480, grid_size: int = 64):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.grid_size = grid_size
        
        # Calculate grid dimensions
        self.grid_cols = math.ceil(frame_width / grid_size)
        self.grid_rows = math.ceil(frame_height / grid_size)
        
        # Initialize density grid
        self.density_grid = np.zeros((self.grid_rows, self.grid_cols))
        self.speed_grid = np.zeros((self.grid_rows, self.grid_cols))
        self.direction_grid = np.zeros((self.grid_rows, self.grid_cols, 2))  # dx, dy
        
        # Traffic metrics
        self.total_vehicles = 0
        self.average_speed = 0.0
        self.congestion_level = 0.0
        
    def update_density(self, vehicle_tracks: List[VehicleTrack]):
        """Update density grid based on current vehicle positions"""
        # Reset grids
        self.density_grid.fill(0)
        self.speed_grid.fill(0)
        self.direction_grid.fill(0)
        
        vehicle_count_grid = np.zeros((self.grid_rows, self.grid_cols))
        
        for track in vehicle_tracks:
            if not track.positions:
                continue
            
            # Get current position
            x, y, _ = track.positions[-1]
            
            # Convert to grid coordinates
            grid_x = int(x // self.grid_size)
            grid_y = int(y // self.grid_size)
            
            # Ensure within bounds
            if 0 <= grid_x < self.grid_cols and 0 <= grid_y < self.grid_rows:
                self.density_grid[grid_y, grid_x] += 1
                vehicle_count_grid[grid_y, grid_x] += 1
                
                # Add speed information
                speed = track.get_current_speed()
                self.speed_grid[grid_y, grid_x] += speed
                
                # Add direction information
                direction = track.get_direction()
                if direction:
                    dx, dy = direction
                    self.direction_grid[grid_y, grid_x, 0] += dx
                    self.direction_grid[grid_y, grid_x, 1] += dy
        
        # Normalize speed and direction grids
        for y in range(self.grid_rows):
            for x in range(self.grid_cols):
                count = vehicle_count_grid[y, x]
                if count > 0:
                    self.speed_grid[y, x] /= count
                    self.direction_grid[y, x, 0] /= count
                    self.direction_grid[y, x, 1] /= count
        
        # Update overall metrics
        self.total_vehicles = len(vehicle_tracks)
        if vehicle_tracks:
            speeds = [track.get_current_speed() for track in vehicle_tracks]
            self.average_speed = np.mean(speeds) if speeds else 0.0
        else:
            self.average_speed = 0.0
        self.congestion_level = self._calculate_congestion_level()
    
    def _calculate_congestion_level(self) -> float:
        """Calculate overall congestion level (0.0 = free flow, 1.0 = gridlock)"""
        if self.total_vehicles == 0:
            return 0.0
        
        # Factor 1: Vehicle density (amplified for better sensitivity)
        max_density = self.grid_rows * self.grid_cols
        density_factor = min(np.sum(self.density_grid) / max_density * 5.0, 1.0)  # Amplify by 5x
        
        # Factor 2: Average speed (lower speed = higher congestion)
        max_expected_speed = 50.0  # pixels per second
        speed_factor = max(0.0, 1.0 - (self.average_speed / max_expected_speed))
        
        # Factor 3: Uniformity of distribution (clustering indicates congestion)
        density_variance = np.var(self.density_grid)
        uniformity_factor = min(density_variance / 10.0, 1.0)  # Normalized variance
        
        # Weighted combination with higher emphasis on density
        congestion = (0.6 * density_factor + 0.3 * speed_factor + 0.1 * uniformity_factor)
        return min(max(congestion, 0.0), 1.0)
    
    def get_hotspots(self, threshold: float = 0.7) -> List[Tuple[int, int, float]]:
        """Get congestion hotspots (grid cells with high density)"""
        hotspots = []
        max_density = np.max(self.density_grid) if np.max(self.density_grid) > 0 else 1
        
        for y in range(self.grid_rows):
            for x in range(self.grid_cols):
                normalized_density = self.density_grid[y, x] / max_density
                if normalized_density >= threshold:
                    hotspots.append((x, y, normalized_density))
        
        return sorted(hotspots, key=lambda h: h[2], reverse=True)
    
    def get_flow_vectors(self) -> List[Tuple[int, int, float, float, float]]:
        """Get flow direction vectors for visualization"""
        vectors = []
        
        for y in range(self.grid_rows):
            for x in range(self.grid_cols):
                if self.density_grid[y, x] > 0:
                    dx = self.direction_grid[y, x, 0]
                    dy = self.direction_grid[y, x, 1]
                    magnitude = math.sqrt(dx**2 + dy**2)
                    
                    if magnitude > 0.1:  # Only include significant flows
                        vectors.append((x, y, dx, dy, magnitude))
        
        return vectors

class TrafficSignalOptimizer:
    """Optimizes traffic signal timing based on real-time traffic data"""
    
    def __init__(self, intersection: IntersectionZone):
        self.intersection = intersection
        self.phase_durations = {
            "north_south": 30.0,  # seconds
            "east_west": 30.0,
            "all_red": 3.0
        }
        self.current_phase = "north_south"
        self.phase_start_time = time.time()
        self.min_green_time = 15.0
        self.max_green_time = 90.0
        
        # Traffic data for optimization
        self.approach_queues = defaultdict(list)  # direction -> list of waiting vehicles
        self.approach_flows = defaultdict(float)  # direction -> vehicles per minute
        self.optimization_history = deque(maxlen=20)
    
    def update_traffic_data(self, vehicle_tracks: List[VehicleTrack]):
        """Update traffic data for signal optimization"""
        current_time = time.time()
        
        # Reset approach data
        for direction in self.intersection.approach_directions:
            self.approach_queues[direction] = []
            self.approach_flows[direction] = 0.0
        
        # Analyze vehicles in intersection area
        for track in vehicle_tracks:
            if not track.positions:
                continue
            
            current_pos = track.positions[-1]
            x, y, _ = current_pos
            
            # Check if vehicle is in intersection area
            if self.intersection.contains_point(x, y):
                # Determine approach direction
                if len(track.positions) >= 2:
                    prev_pos = track.positions[-2]
                    prev_x, prev_y, _ = prev_pos
                    
                    direction = self.intersection.get_approach_direction(x, y, prev_x, prev_y)
                    if direction:
                        self.approach_queues[direction].append(track)
                        
                        # Count flow if vehicle is moving
                        if not track.is_stationary():
                            self.approach_flows[direction] += 1
        
        # Calculate flow rates (vehicles per minute)
        for direction in self.approach_flows:
            self.approach_flows[direction] = self.approach_flows[direction] * 60.0  # Convert to per minute
    
    def calculate_optimal_timing(self) -> Dict[str, float]:
        """Calculate optimal signal timing based on current traffic"""
        # Get queue lengths for each direction
        ns_queue = len(self.approach_queues["north"]) + len(self.approach_queues["south"])
        ew_queue = len(self.approach_queues["east"]) + len(self.approach_queues["west"])
        
        # Get flow rates
        ns_flow = self.approach_flows["north"] + self.approach_flows["south"]
        ew_flow = self.approach_flows["east"] + self.approach_flows["west"]
        
        # Calculate demand ratios
        total_demand = ns_queue + ew_queue + ns_flow + ew_flow
        if total_demand == 0:
            # No traffic - use minimum timings
            return {
                "north_south": self.min_green_time,
                "east_west": self.min_green_time,
                "all_red": 3.0
            }
        
        # Webster's method for optimal cycle time
        lost_time = 6.0  # seconds (all-red + startup lost time)
        saturation_flow = 1800.0  # vehicles per hour per lane
        
        # Calculate critical flow ratios
        ns_ratio = (ns_queue + ns_flow) / saturation_flow if saturation_flow > 0 else 0
        ew_ratio = (ew_queue + ew_flow) / saturation_flow if saturation_flow > 0 else 0
        
        total_ratio = ns_ratio + ew_ratio
        if total_ratio >= 0.9:  # Oversaturated
            total_ratio = 0.85  # Prevent excessive cycle times
        
        # Calculate optimal cycle time
        optimal_cycle = (1.5 * lost_time + 5) / (1 - total_ratio) if total_ratio < 1 else 120
        optimal_cycle = min(max(optimal_cycle, 60), 180)  # Constrain between 60-180 seconds
        
        # Allocate green time proportionally
        if ns_ratio + ew_ratio > 0:
            ns_green = (optimal_cycle - lost_time) * (ns_ratio / (ns_ratio + ew_ratio))
            ew_green = (optimal_cycle - lost_time) * (ew_ratio / (ns_ratio + ew_ratio))
        else:
            ns_green = ew_green = (optimal_cycle - lost_time) / 2
        
        # Apply constraints
        ns_green = min(max(ns_green, self.min_green_time), self.max_green_time)
        ew_green = min(max(ew_green, self.min_green_time), self.max_green_time)
        
        return {
            "north_south": ns_green,
            "east_west": ew_green,
            "all_red": 3.0
        }
    
    def should_extend_phase(self) -> bool:
        """Determine if current phase should be extended"""
        current_time = time.time()
        phase_duration = current_time - self.phase_start_time
        
        # Don't extend beyond maximum
        if phase_duration >= self.max_green_time:
            return False
        
        # Don't cut short minimum time
        if phase_duration < self.min_green_time:
            return True
        
        # Check if there's still significant demand
        if self.current_phase == "north_south":
            current_demand = len(self.approach_queues["north"]) + len(self.approach_queues["south"])
            competing_demand = len(self.approach_queues["east"]) + len(self.approach_queues["west"])
        else:
            current_demand = len(self.approach_queues["east"]) + len(self.approach_queues["west"])
            competing_demand = len(self.approach_queues["north"]) + len(self.approach_queues["south"])
        
        # Extend if current direction still has more demand (more lenient threshold)
        return current_demand >= competing_demand and current_demand > 1
    
    def get_signal_recommendation(self) -> Dict[str, Any]:
        """Get signal timing recommendation"""
        optimal_timing = self.calculate_optimal_timing()
        extend_current = self.should_extend_phase()
        
        current_time = time.time()
        phase_duration = current_time - self.phase_start_time
        
        return {
            "current_phase": self.current_phase,
            "phase_duration": round(phase_duration, 1),
            "optimal_timing": optimal_timing,
            "extend_current_phase": extend_current,
            "queue_lengths": {
                direction: len(vehicles) 
                for direction, vehicles in self.approach_queues.items()
            },
            "flow_rates": dict(self.approach_flows),
            "recommendation_time": current_time
        }

class TrafficFlowAnalyzer:
    """Main traffic flow analysis engine"""
    
    def __init__(self, frame_width: int = 640, frame_height: int = 480):
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # Initialize components
        self.density_analyzer = TrafficDensityAnalyzer(frame_width, frame_height)
        self.vehicle_tracker = {}  # track_id -> VehicleTrack
        self.next_vehicle_id = 1
        
        # Define intersection zones (can be configured)
        self.intersections = {}
        self._setup_default_intersection()
        
        # Signal optimizers
        self.signal_optimizers = {}
        self._setup_signal_optimizers()
        
        # Analysis history
        self.analysis_history = deque(maxlen=100)
        
    def _setup_default_intersection(self):
        """Setup a default intersection zone"""
        # Define intersection in center of frame
        center_x, center_y = self.frame_width // 2, self.frame_height // 2
        intersection_size = min(self.frame_width, self.frame_height) // 4
        
        intersection = IntersectionZone(
            zone_id="main_intersection",
            bounds=(
                center_x - intersection_size // 2,
                center_y - intersection_size // 2,
                center_x + intersection_size // 2,
                center_y + intersection_size // 2
            )
        )
        
        self.intersections["main_intersection"] = intersection
    
    def _setup_signal_optimizers(self):
        """Setup signal optimizers for each intersection"""
        for intersection_id, intersection in self.intersections.items():
            self.signal_optimizers[intersection_id] = TrafficSignalOptimizer(intersection)
    
    def update_vehicle_tracks(self, vehicle_detections: List[Dict]):
        """Update vehicle tracking from detection results"""
        current_time = time.time()
        
        # Convert detections to VehicleTrack objects
        active_tracks = []
        
        for detection in vehicle_detections:
            # Create or update tracks (simplified tracking)
            center = detection.get('center', (0, 0))
            vehicle_type = VehicleType.CAR  # Default, could be improved with classification
            
            # For now, create new track for each detection (simplified)
            # In a real implementation, you'd use proper tracking algorithms
            track = VehicleTrack(
                vehicle_id=self.next_vehicle_id,
                vehicle_type=vehicle_type
            )
            track.add_position(center[0], center[1], current_time)
            active_tracks.append(track)
            self.next_vehicle_id += 1
        
        # Update components
        self.density_analyzer.update_density(active_tracks)
        
        for optimizer in self.signal_optimizers.values():
            optimizer.update_traffic_data(active_tracks)
        
        # Store current tracks
        self.vehicle_tracker = {track.vehicle_id: track for track in active_tracks}
        
        return active_tracks
    
    def analyze_traffic_flow(self, vehicle_detections: List[Dict]) -> Dict[str, Any]:
        """Comprehensive traffic flow analysis"""
        # Update vehicle tracking
        vehicle_tracks = self.update_vehicle_tracks(vehicle_detections)
        
        # Get density analysis
        density_metrics = {
            "total_vehicles": self.density_analyzer.total_vehicles,
            "average_speed": round(self.density_analyzer.average_speed, 2),
            "congestion_level": round(self.density_analyzer.congestion_level, 3),
            "hotspots": self.density_analyzer.get_hotspots(),
            "flow_vectors": self.density_analyzer.get_flow_vectors()
        }
        
        # Get signal recommendations
        signal_recommendations = {}
        for intersection_id, optimizer in self.signal_optimizers.items():
            signal_recommendations[intersection_id] = optimizer.get_signal_recommendation()
        
        # Calculate additional metrics
        stopped_vehicles = sum(1 for track in vehicle_tracks if track.is_stationary())
        moving_vehicles = len(vehicle_tracks) - stopped_vehicles
        
        # Vehicle type distribution
        vehicle_types = defaultdict(int)
        for track in vehicle_tracks:
            vehicle_types[track.vehicle_type.value] += 1
        
        result = {
            "timestamp": time.time(),
            "vehicle_summary": {
                "total_vehicles": len(vehicle_tracks),
                "moving_vehicles": moving_vehicles,
                "stopped_vehicles": stopped_vehicles,
                "vehicle_types": dict(vehicle_types)
            },
            "density_analysis": density_metrics,
            "signal_recommendations": signal_recommendations,
            "intersection_analysis": self._analyze_intersections(),
            "traffic_efficiency": self._calculate_traffic_efficiency(vehicle_tracks)
        }
        
        # Store in history
        self.analysis_history.append(result)
        
        return result
    
    def _analyze_intersections(self) -> Dict[str, Any]:
        """Analyze traffic conditions at intersections"""
        intersection_data = {}
        
        for intersection_id, intersection in self.intersections.items():
            vehicles_in_intersection = []
            
            for track in self.vehicle_tracker.values():
                if track.positions:
                    x, y, _ = track.positions[-1]
                    if intersection.contains_point(x, y):
                        vehicles_in_intersection.append(track)
            
            intersection_data[intersection_id] = {
                "vehicles_present": len(vehicles_in_intersection),
                "average_speed": np.mean([track.get_current_speed() for track in vehicles_in_intersection]) if vehicles_in_intersection else 0.0,
                "congestion_severity": "high" if len(vehicles_in_intersection) > 10 else "medium" if len(vehicles_in_intersection) > 5 else "low"
            }
        
        return intersection_data
    
    def _calculate_traffic_efficiency(self, vehicle_tracks: List[VehicleTrack]) -> Dict[str, float]:
        """Calculate overall traffic efficiency metrics"""
        if not vehicle_tracks:
            return {
                "flow_efficiency": 1.0,
                "speed_consistency": 1.0,
                "congestion_index": 0.0
            }
        
        # Flow efficiency (moving vehicles / total vehicles)
        moving_count = sum(1 for track in vehicle_tracks if not track.is_stationary())
        flow_efficiency = moving_count / len(vehicle_tracks) if vehicle_tracks else 1.0
        
        # Speed consistency (1 - coefficient of variation of speeds)
        speeds = [track.get_current_speed() for track in vehicle_tracks]
        if speeds and np.mean(speeds) > 0:
            speed_cv = np.std(speeds) / np.mean(speeds)
            speed_consistency = max(0.0, 1.0 - speed_cv)
        else:
            speed_consistency = 1.0
        
        # Congestion index (from density analyzer)
        congestion_index = self.density_analyzer.congestion_level
        
        return {
            "flow_efficiency": round(flow_efficiency, 3),
            "speed_consistency": round(speed_consistency, 3),
            "congestion_index": round(congestion_index, 3)
        }
    
    def get_traffic_trends(self, minutes: int = 10) -> Dict[str, Any]:
        """Get traffic trends over the specified time period"""
        if not self.analysis_history:
            return {"error": "No historical data available"}
        
        # Filter recent history
        current_time = time.time()
        cutoff_time = current_time - (minutes * 60)
        
        recent_history = [
            entry for entry in self.analysis_history 
            if entry["timestamp"] >= cutoff_time
        ]
        
        if not recent_history:
            return {"error": "No recent data available"}
        
        # Calculate trends
        vehicle_counts = [entry["vehicle_summary"]["total_vehicles"] for entry in recent_history]
        congestion_levels = [entry["density_analysis"]["congestion_level"] for entry in recent_history]
        average_speeds = [entry["density_analysis"]["average_speed"] for entry in recent_history]
        
        return {
            "time_period_minutes": minutes,
            "data_points": len(recent_history),
            "vehicle_count_trend": {
                "current": vehicle_counts[-1] if vehicle_counts else 0,
                "average": round(np.mean(vehicle_counts), 1),
                "peak": max(vehicle_counts) if vehicle_counts else 0,
                "trend": "increasing" if len(vehicle_counts) > 1 and vehicle_counts[-1] > vehicle_counts[0] else "stable"
            },
            "congestion_trend": {
                "current": round(congestion_levels[-1], 3) if congestion_levels else 0,
                "average": round(np.mean(congestion_levels), 3),
                "peak": round(max(congestion_levels), 3) if congestion_levels else 0
            },
            "speed_trend": {
                "current": round(average_speeds[-1], 2) if average_speeds else 0,
                "average": round(np.mean(average_speeds), 2),
                "minimum": round(min(average_speeds), 2) if average_speeds else 0
            }
        }