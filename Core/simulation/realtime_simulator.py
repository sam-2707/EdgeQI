"""
Real-Time Data Simulator for EDGE-QI Framework

Simulates realistic hardware data sources including cameras, sensors,
and network conditions without requiring actual hardware.
"""

import cv2
import numpy as np
import threading
import time
import json
import random
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio
from queue import Queue, Empty

@dataclass
class SimulatedVehicle:
    """Simulated vehicle for traffic generation"""
    id: int
    x: float
    y: float
    speed: float
    direction: float  # radians
    vehicle_type: str
    color: tuple
    size: tuple
    last_update: float

@dataclass
class SimulatedCamera:
    """Simulated camera feed"""
    camera_id: str
    position: tuple
    resolution: tuple
    fps: int
    is_active: bool = True

class RealTimeDataSimulator:
    """
    Comprehensive real-time data simulator that generates:
    - Live video streams with moving objects
    - Traffic patterns and vehicle movements  
    - Network conditions and latency
    - Sensor data (temperature, power, etc.)
    - Queue formations and dynamics
    """
    
    def __init__(self, 
                 width: int = 1280, 
                 height: int = 720,
                 fps: int = 30):
        
        self.width = width
        self.height = height
        self.fps = fps
        self.frame_interval = 1.0 / fps
        
        # Simulation state
        self.is_running = False
        self.vehicles = {}
        self.next_vehicle_id = 1
        self.cameras = {}
        
        # Data queues for real-time streaming
        self.frame_queue = Queue(maxsize=60)
        self.detection_queue = Queue(maxsize=100)
        self.sensor_queue = Queue(maxsize=100)
        
        # Traffic simulation parameters
        self.traffic_density = 0.3  # 0.0 to 1.0
        self.spawn_probability = 0.1
        self.congestion_zones = []
        
        # Initialize default cameras
        self._setup_default_cameras()
        
        # Initialize road network
        self._setup_road_network()
        
        # Callbacks for real-time data
        self.frame_callbacks = []
        self.detection_callbacks = []
        self.sensor_callbacks = []
        
    def _setup_default_cameras(self):
        """Setup simulated camera feeds"""
        self.cameras = {
            'main_intersection': SimulatedCamera(
                camera_id='main_intersection',
                position=(self.width // 2, self.height // 2),
                resolution=(self.width, self.height),
                fps=self.fps
            ),
            'north_approach': SimulatedCamera(
                camera_id='north_approach', 
                position=(self.width // 2, self.height // 4),
                resolution=(self.width, self.height),
                fps=self.fps
            ),
            'south_approach': SimulatedCamera(
                camera_id='south_approach',
                position=(self.width // 2, 3 * self.height // 4), 
                resolution=(self.width, self.height),
                fps=self.fps
            )
        }
    
    def _setup_road_network(self):
        """Define road network for realistic vehicle movement"""
        self.roads = [
            # Horizontal roads
            {'start': (0, self.height // 2 - 40), 'end': (self.width, self.height // 2 - 40), 'direction': 0},
            {'start': (self.width, self.height // 2 + 40), 'end': (0, self.height // 2 + 40), 'direction': np.pi},
            
            # Vertical roads  
            {'start': (self.width // 2 - 40, 0), 'end': (self.width // 2 - 40, self.height), 'direction': np.pi/2},
            {'start': (self.width // 2 + 40, self.height), 'end': (self.width // 2 + 40, 0), 'direction': -np.pi/2},
        ]
        
        # Define traffic light positions
        self.traffic_lights = [
            {'x': self.width // 2, 'y': self.height // 2, 'state': 'red', 'timer': 0}
        ]
    
    def start_simulation(self):
        """Start real-time data simulation"""
        if self.is_running:
            return
            
        self.is_running = True
        print("🚦 Starting Real-Time Data Simulation...")
        
        # Start simulation threads
        self.frame_thread = threading.Thread(target=self._frame_simulation_loop)
        self.vehicle_thread = threading.Thread(target=self._vehicle_simulation_loop)
        self.sensor_thread = threading.Thread(target=self._sensor_simulation_loop)
        
        self.frame_thread.daemon = True
        self.vehicle_thread.daemon = True
        self.sensor_thread.daemon = True
        
        self.frame_thread.start()
        self.vehicle_thread.start()
        self.sensor_thread.start()
        
        print("✅ Real-time simulation started")
    
    def stop_simulation(self):
        """Stop real-time data simulation"""
        self.is_running = False
        print("⏹️ Real-time simulation stopped")
    
    def _frame_simulation_loop(self):
        """Generate real-time video frames"""
        while self.is_running:
            start_time = time.time()
            
            # Generate frame for each camera
            for camera_id, camera in self.cameras.items():
                if camera.is_active:
                    frame = self._generate_frame(camera)
                    
                    # Add frame to queue
                    try:
                        self.frame_queue.put({
                            'camera_id': camera_id,
                            'frame': frame,
                            'timestamp': time.time(),
                            'frame_number': getattr(self, f'frame_count_{camera_id}', 0)
                        }, block=False)
                        
                        # Update frame counter
                        setattr(self, f'frame_count_{camera_id}', 
                               getattr(self, f'frame_count_{camera_id}', 0) + 1)
                        
                    except:
                        pass  # Queue full, skip frame
                    
                    # Generate object detections
                    detections = self._generate_detections(frame, camera_id)
                    try:
                        self.detection_queue.put({
                            'camera_id': camera_id,
                            'detections': detections,
                            'timestamp': time.time()
                        }, block=False)
                    except:
                        pass
            
            # Maintain target FPS
            elapsed = time.time() - start_time
            sleep_time = max(0, self.frame_interval - elapsed)
            time.sleep(sleep_time)
    
    def _generate_frame(self, camera: SimulatedCamera) -> np.ndarray:
        """Generate a realistic video frame"""
        # Create base road scene
        frame = np.ones((camera.resolution[1], camera.resolution[0], 3), dtype=np.uint8) * 50
        
        # Draw roads
        self._draw_roads(frame)
        
        # Draw traffic lights
        self._draw_traffic_lights(frame)
        
        # Draw vehicles
        self._draw_vehicles(frame, camera)
        
        # Add realistic noise and lighting
        self._add_realistic_effects(frame)
        
        return frame
    
    def _draw_roads(self, frame: np.ndarray):
        """Draw road network on frame"""
        road_color = (80, 80, 80)
        line_color = (200, 200, 200)
        
        for road in self.roads:
            start = road['start']
            end = road['end']
            
            # Draw road surface
            cv2.rectangle(frame, 
                         (min(start[0], end[0]) - 40, min(start[1], end[1]) - 40),
                         (max(start[0], end[0]) + 40, max(start[1], end[1]) + 40),
                         road_color, -1)
            
            # Draw lane markings
            if start[1] == end[1]:  # Horizontal road
                y = start[1]
                for x in range(0, self.width, 50):
                    cv2.line(frame, (x, y), (x + 20, y), line_color, 2)
            else:  # Vertical road
                x = start[0]
                for y in range(0, self.height, 50):
                    cv2.line(frame, (x, y), (x, y + 20), line_color, 2)
    
    def _draw_traffic_lights(self, frame: np.ndarray):
        """Draw traffic lights"""
        for light in self.traffic_lights:
            x, y = light['x'], light['y']
            state = light['state']
            
            # Draw traffic light pole
            cv2.rectangle(frame, (x-5, y-60), (x+5, y+10), (100, 100, 100), -1)
            
            # Draw lights
            colors = {'red': (0, 0, 255), 'yellow': (0, 255, 255), 'green': (0, 255, 0)}
            positions = {'red': (x, y-50), 'yellow': (x, y-30), 'green': (x, y-10)}
            
            for light_color, pos in positions.items():
                color = colors[light_color] if state == light_color else (50, 50, 50)
                cv2.circle(frame, pos, 8, color, -1)
    
    def _draw_vehicles(self, frame: np.ndarray, camera: SimulatedCamera):
        """Draw vehicles on frame"""
        # Create a snapshot of vehicles to avoid iteration issues
        vehicles_snapshot = list(self.vehicles.values())
        for vehicle in vehicles_snapshot:
            if self._is_vehicle_in_camera_view(vehicle, camera):
                self._draw_vehicle(frame, vehicle)
    
    def _draw_vehicle(self, frame: np.ndarray, vehicle: SimulatedVehicle):
        """Draw individual vehicle"""
        x, y = int(vehicle.x), int(vehicle.y)
        w, h = vehicle.size
        
        # Draw vehicle body
        cv2.rectangle(frame, (x - w//2, y - h//2), (x + w//2, y + h//2), 
                     vehicle.color, -1)
        
        # Draw vehicle outline
        cv2.rectangle(frame, (x - w//2, y - h//2), (x + w//2, y + h//2), 
                     (255, 255, 255), 1)
        
        # Add headlight effect if moving
        if vehicle.speed > 0.1:
            headlight_x = x + int((w//2 + 5) * np.cos(vehicle.direction))
            headlight_y = y + int((w//2 + 5) * np.sin(vehicle.direction))
            cv2.circle(frame, (headlight_x, headlight_y), 3, (255, 255, 200), -1)
    
    def _vehicle_simulation_loop(self):
        """Simulate vehicle movement and spawning"""
        while self.is_running:
            current_time = time.time()
            
            # Spawn new vehicles
            if random.random() < self.spawn_probability * self.traffic_density:
                self._spawn_vehicle()
            
            # Update existing vehicles
            vehicles_to_remove = []
            for vehicle_id, vehicle in self.vehicles.items():
                self._update_vehicle(vehicle, current_time)
                
                # Remove vehicles that left the scene
                if (vehicle.x < -50 or vehicle.x > self.width + 50 or 
                    vehicle.y < -50 or vehicle.y > self.height + 50):
                    vehicles_to_remove.append(vehicle_id)
            
            # Clean up vehicles
            for vehicle_id in vehicles_to_remove:
                del self.vehicles[vehicle_id]
            
            # Update traffic lights
            self._update_traffic_lights(current_time)
            
            time.sleep(0.1)  # Update at 10 Hz
    
    def _spawn_vehicle(self):
        """Spawn a new vehicle on a random road"""
        road = random.choice(self.roads)
        vehicle_types = ['car', 'truck', 'bus', 'motorcycle']
        vehicle_type = random.choice(vehicle_types)
        
        # Vehicle properties based on type
        if vehicle_type == 'car':
            size = (25, 15)
            color = random.choice([(0, 0, 200), (200, 0, 0), (0, 200, 0), (100, 100, 100)])
            speed = random.uniform(20, 40)
        elif vehicle_type == 'truck':
            size = (35, 20)
            color = (150, 150, 150)
            speed = random.uniform(15, 25)
        elif vehicle_type == 'bus':
            size = (40, 20)
            color = (200, 200, 0)
            speed = random.uniform(15, 30)
        else:  # motorcycle
            size = (15, 10)
            color = (0, 100, 200)
            speed = random.uniform(25, 50)
        
        vehicle = SimulatedVehicle(
            id=self.next_vehicle_id,
            x=road['start'][0],
            y=road['start'][1],
            speed=speed,
            direction=road['direction'],
            vehicle_type=vehicle_type,
            color=color,
            size=size,
            last_update=time.time()
        )
        
        self.vehicles[self.next_vehicle_id] = vehicle
        self.next_vehicle_id += 1
    
    def _update_vehicle(self, vehicle: SimulatedVehicle, current_time: float):
        """Update vehicle position and behavior"""
        dt = current_time - vehicle.last_update
        vehicle.last_update = current_time
        
        # Check for traffic light stops
        should_stop = self._should_vehicle_stop(vehicle)
        
        if should_stop:
            vehicle.speed = max(0, vehicle.speed - 50 * dt)  # Decelerate
        else:
            # Accelerate back to normal speed
            target_speed = 30 if vehicle.vehicle_type == 'car' else 20
            if vehicle.speed < target_speed:
                vehicle.speed = min(target_speed, vehicle.speed + 30 * dt)
        
        # Update position
        vehicle.x += vehicle.speed * np.cos(vehicle.direction) * dt
        vehicle.y += vehicle.speed * np.sin(vehicle.direction) * dt
        
        # Add some randomness to movement
        vehicle.direction += random.uniform(-0.05, 0.05)
    
    def _should_vehicle_stop(self, vehicle: SimulatedVehicle) -> bool:
        """Check if vehicle should stop for traffic light"""
        for light in self.traffic_lights:
            distance = np.sqrt((vehicle.x - light['x'])**2 + (vehicle.y - light['y'])**2)
            if distance < 80 and light['state'] == 'red':
                return True
        return False
    
    def _update_traffic_lights(self, current_time: float):
        """Update traffic light states"""
        for light in self.traffic_lights:
            light['timer'] += 0.1
            
            # Simple traffic light cycle: Red(30s) -> Green(45s) -> Yellow(5s)
            if light['state'] == 'red' and light['timer'] > 30:
                light['state'] = 'green'
                light['timer'] = 0
            elif light['state'] == 'green' and light['timer'] > 45:
                light['state'] = 'yellow'
                light['timer'] = 0
            elif light['state'] == 'yellow' and light['timer'] > 5:
                light['state'] = 'red'
                light['timer'] = 0
    
    def _generate_detections(self, frame: np.ndarray, camera_id: str) -> List[Dict]:
        """Generate object detection results from frame"""
        detections = []
        
        for vehicle in self.vehicles.values():
            if self._is_vehicle_in_frame(vehicle, frame):
                # Add some detection noise/confidence variation
                confidence = random.uniform(0.7, 0.95)
                
                detection = {
                    'class': vehicle.vehicle_type,
                    'confidence': confidence,
                    'bbox': [
                        vehicle.x - vehicle.size[0]//2,
                        vehicle.y - vehicle.size[1]//2,
                        vehicle.size[0],
                        vehicle.size[1]
                    ],
                    'center': (vehicle.x, vehicle.y),
                    'speed': vehicle.speed,
                    'direction': vehicle.direction
                }
                detections.append(detection)
        
        return detections
    
    def _sensor_simulation_loop(self):
        """Generate sensor data (temperature, power, network, etc.)"""
        while self.is_running:
            sensor_data = {
                'timestamp': time.time(),
                'temperature': 35 + random.uniform(-5, 15),  # CPU temperature
                'power_usage': 45 + random.uniform(-10, 20),  # Power in watts
                'memory_usage': random.uniform(30, 85),       # Memory percentage
                'cpu_usage': random.uniform(20, 80),          # CPU percentage
                'network_latency': random.uniform(10, 100),   # Network latency in ms
                'bandwidth_usage': random.uniform(10, 90),    # Bandwidth percentage
                'disk_usage': random.uniform(40, 85),         # Disk usage percentage
            }
            
            try:
                self.sensor_queue.put(sensor_data, block=False)
            except:
                pass  # Queue full
            
            # Notify sensor callbacks
            for callback in self.sensor_callbacks:
                try:
                    callback(sensor_data)
                except:
                    pass
            
            time.sleep(1.0)  # Update every second
    
    def _is_vehicle_in_camera_view(self, vehicle: SimulatedVehicle, camera: SimulatedCamera) -> bool:
        """Check if vehicle is visible in camera view"""
        return (0 <= vehicle.x <= camera.resolution[0] and 
                0 <= vehicle.y <= camera.resolution[1])
    
    def _is_vehicle_in_frame(self, vehicle: SimulatedVehicle, frame: np.ndarray) -> bool:
        """Check if vehicle is within frame bounds"""
        return (0 <= vehicle.x <= frame.shape[1] and 
                0 <= vehicle.y <= frame.shape[0])
    
    def _add_realistic_effects(self, frame: np.ndarray):
        """Add realistic camera effects (noise, lighting, etc.)"""
        # Add slight Gaussian noise
        noise = np.random.normal(0, 2, frame.shape).astype(np.int16)
        frame_noisy = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        # Simulate time-of-day lighting
        hour = datetime.now().hour
        if 6 <= hour <= 18:  # Daylight
            brightness_factor = 1.0
        else:  # Night
            brightness_factor = 0.3
        
        frame_noisy = (frame_noisy * brightness_factor).astype(np.uint8)
        
        # Copy back to original frame
        frame[:] = frame_noisy
    
    # Public API methods for integration
    def get_latest_frame(self, camera_id: str = None) -> Optional[Dict]:
        """Get the latest frame from specified camera or any camera"""
        try:
            while not self.frame_queue.empty():
                frame_data = self.frame_queue.get_nowait()
                if camera_id is None or frame_data['camera_id'] == camera_id:
                    return frame_data
            return None
        except Empty:
            return None
    
    def get_latest_detections(self) -> Optional[Dict]:
        """Get latest object detection results"""
        try:
            return self.detection_queue.get_nowait()
        except Empty:
            return None
    
    def get_latest_sensor_data(self) -> Optional[Dict]:
        """Get latest sensor readings"""
        try:
            return self.sensor_queue.get_nowait()
        except Empty:
            return None
    
    def register_frame_callback(self, callback: Callable):
        """Register callback for real-time frame updates"""
        self.frame_callbacks.append(callback)
    
    def register_detection_callback(self, callback: Callable):
        """Register callback for real-time detection updates"""
        self.detection_callbacks.append(callback)
    
    def register_sensor_callback(self, callback: Callable):
        """Register callback for real-time sensor updates"""
        self.sensor_callbacks.append(callback)
    
    def set_traffic_density(self, density: float):
        """Adjust traffic density (0.0 to 1.0)"""
        self.traffic_density = max(0.0, min(1.0, density))
    
    def add_congestion_zone(self, x: int, y: int, radius: int):
        """Add a congestion zone that slows down traffic"""
        self.congestion_zones.append({'x': x, 'y': y, 'radius': radius})