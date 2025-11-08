"""
High-Performance Realistic Intersection Simulation
Native desktop application using matplotlib for visualization

Features:
- Matplotlib-based rendering for cross-platform compatibility
- Real-time vehicle simulation
- 7 camera monitoring system
- 3 traffic light control
- Performance metrics display
- High FPS capability without web overhead
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
import time
import random
import threading
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import tkinter as tk
from tkinter import ttk

# Performance configuration
FPS_TARGET = 30  # Matplotlib is slower than OpenCV, so use 30 FPS
SIMULATION_SPEED = 1.0
VEHICLE_SPAWN_RATE = 0.2

@dataclass
class Camera:
    id: str
    name: str
    position: Tuple[int, int]
    view_angle: float
    view_distance: int
    coverage_area: List[Tuple[int, int]]
    vehicle_count: int = 0
    queue_length: int = 0
    avg_speed: float = 0.0
    active: bool = True

@dataclass
class TrafficLight:
    id: str
    position: Tuple[int, int]
    current_state: str = "red"  # red, yellow, green
    timer: float = 0.0
    cycle_times: Dict[str, float] = field(default_factory=lambda: {
        "red": 30.0, "green": 25.0, "yellow": 5.0
    })

@dataclass
class Vehicle:
    id: str
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    direction: str  # N, S, E, W
    color: Tuple[int, int, int]
    size: Tuple[int, int] = (20, 12)
    speed: float = 2.0
    lane: int = 0

class HighPerformanceIntersection:
    def __init__(self):
        self.width = 1200
        self.height = 800
        self.running = False
        self.paused = False
        
        # Performance tracking
        self.fps_counter = 0
        self.fps_timer = time.time()
        self.current_fps = 0
        
        # Initialize components
        self.setup_intersection()
        self.setup_cameras()
        self.setup_traffic_lights()
        
        # Vehicle management
        self.vehicles = []
        self.vehicle_id_counter = 0
        
        # Statistics
        self.stats = {
            'total_vehicles': 0,
            'vehicles_passed': 0,
            'average_speed': 0.0,
            'peak_queue_length': 0,
            'simulation_time': 0.0
        }
        
        # Create main window
        self.setup_ui()
        
    def setup_intersection(self):
        """Create the intersection map"""
        self.intersection_map = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Road colors
        road_color = (60, 60, 60)  # Dark gray
        line_color = (255, 255, 255)  # White lines
        crosswalk_color = (200, 200, 200)  # Light gray
        
        # Draw main roads
        # Horizontal road (East-West)
        cv2.rectangle(self.intersection_map, (0, 300), (self.width, 500), road_color, -1)
        
        # Vertical road (North-South) 
        cv2.rectangle(self.intersection_map, (500, 0), (700, self.height), road_color, -1)
        
        # Lane dividers
        # Horizontal lanes
        cv2.line(self.intersection_map, (0, 375), (500, 375), line_color, 2)  # Left side
        cv2.line(self.intersection_map, (700, 375), (self.width, 375), line_color, 2)  # Right side
        cv2.line(self.intersection_map, (0, 425), (500, 425), line_color, 2)  # Left side
        cv2.line(self.intersection_map, (700, 425), (self.width, 425), line_color, 2)  # Right side
        
        # Vertical lanes
        cv2.line(self.intersection_map, (575, 0), (575, 300), line_color, 2)  # Top
        cv2.line(self.intersection_map, (575, 500), (575, self.height), line_color, 2)  # Bottom
        cv2.line(self.intersection_map, (625, 0), (625, 300), line_color, 2)  # Top
        cv2.line(self.intersection_map, (625, 500), (625, self.height), line_color, 2)  # Bottom
        
        # Crosswalks
        for i in range(520, 680, 20):
            cv2.rectangle(self.intersection_map, (i, 290), (i+10, 310), crosswalk_color, -1)
            cv2.rectangle(self.intersection_map, (i, 490), (i+10, 510), crosswalk_color, -1)
        
        for i in range(320, 480, 20):
            cv2.rectangle(self.intersection_map, (490, i), (510, i+10), crosswalk_color, -1)
            cv2.rectangle(self.intersection_map, (690, i), (710, i+10), crosswalk_color, -1)
        
    def setup_cameras(self):
        """Initialize the 7 camera monitoring system"""
        self.cameras = [
            Camera("CAM01", "North Approach", (600, 100), 180, 200, [(500, 0), (700, 300)]),
            Camera("CAM02", "South Approach", (600, 700), 0, 200, [(500, 500), (700, 800)]),
            Camera("CAM03", "East Approach", (1000, 400), 270, 200, [(700, 300), (1200, 500)]),
            Camera("CAM04", "West Approach", (200, 400), 90, 200, [(0, 300), (500, 500)]),
            Camera("CAM05", "Center Intersection", (600, 400), 0, 150, [(500, 300), (700, 500)]),
            Camera("CAM06", "Northeast Monitor", (800, 200), 225, 180, [(700, 0), (1200, 300)]),
            Camera("CAM07", "Southwest Monitor", (400, 600), 45, 180, [(0, 500), (500, 800)])
        ]
        
    def setup_traffic_lights(self):
        """Initialize the 3 traffic light system"""
        self.traffic_lights = [
            TrafficLight("TL01", (550, 350), "red", 0.0),  # North-South main
            TrafficLight("TL02", (650, 450), "green", 0.0),  # East-West cross  
            TrafficLight("TL03", (600, 250), "red", 15.0)   # Pedestrian signal
        ]
        
    def setup_ui(self):
        """Create the control UI"""
        self.root = tk.Tk()
        self.root.title("High-Performance Intersection Simulation")
        self.root.geometry("300x600")
        
        # Control buttons
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(control_frame, text="Start Simulation", command=self.start_simulation)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = ttk.Button(control_frame, text="Pause", command=self.toggle_pause)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="Stop", command=self.stop_simulation)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Performance metrics
        perf_frame = ttk.LabelFrame(self.root, text="Performance Metrics")
        perf_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.fps_label = ttk.Label(perf_frame, text="FPS: 0")
        self.fps_label.pack(anchor=tk.W)
        
        self.vehicles_label = ttk.Label(perf_frame, text="Active Vehicles: 0")
        self.vehicles_label.pack(anchor=tk.W)
        
        # Camera status
        camera_frame = ttk.LabelFrame(self.root, text="Camera Status")
        camera_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.camera_labels = {}
        for cam in self.cameras:
            label = ttk.Label(camera_frame, text=f"{cam.id}: Active - 0 vehicles")
            label.pack(anchor=tk.W)
            self.camera_labels[cam.id] = label
            
        # Traffic light status
        traffic_frame = ttk.LabelFrame(self.root, text="Traffic Lights")
        traffic_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.traffic_labels = {}
        for tl in self.traffic_lights:
            label = ttk.Label(traffic_frame, text=f"{tl.id}: {tl.current_state.upper()}")
            label.pack(anchor=tk.W)
            self.traffic_labels[tl.id] = label
            
        # Statistics
        stats_frame = ttk.LabelFrame(self.root, text="Statistics")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_labels = {}
        for key in self.stats:
            label = ttk.Label(stats_frame, text=f"{key.replace('_', ' ').title()}: 0")
            label.pack(anchor=tk.W)
            self.stats_labels[key] = label
            
    def spawn_vehicle(self):
        """Spawn a new vehicle at random entry point"""
        if random.random() < VEHICLE_SPAWN_RATE:
            entry_points = [
                ((600, 0), (0, 2), "N"),      # North entry
                ((600, self.height), (0, -2), "S"),  # South entry
                ((0, 375), (2, 0), "E"),      # East entry
                ((self.width, 375), (-2, 0), "W")    # West entry
            ]
            
            pos, vel, direction = random.choice(entry_points)
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            
            vehicle = Vehicle(
                id=f"V{self.vehicle_id_counter}",
                position=pos,
                velocity=vel,
                direction=direction,
                color=color,
                speed=random.uniform(1.5, 3.0)
            )
            
            self.vehicles.append(vehicle)
            self.vehicle_id_counter += 1
            self.stats['total_vehicles'] += 1
            
    def update_vehicles(self):
        """Update vehicle positions and handle traffic logic"""
        for vehicle in self.vehicles[:]:  # Copy list to allow removal
            # Basic movement
            vehicle.position = (
                vehicle.position[0] + vehicle.velocity[0] * vehicle.speed,
                vehicle.position[1] + vehicle.velocity[1] * vehicle.speed
            )
            
            # Remove vehicles that left the simulation area
            if (vehicle.position[0] < -50 or vehicle.position[0] > self.width + 50 or
                vehicle.position[1] < -50 or vehicle.position[1] > self.height + 50):
                self.vehicles.remove(vehicle)
                self.stats['vehicles_passed'] += 1
                continue
                
            # Traffic light logic (simplified)
            # Check if vehicle is approaching red light
            x, y = vehicle.position
            if (550 < x < 650 and 320 < y < 480):  # In intersection area
                # Get relevant traffic light
                for tl in self.traffic_lights:
                    if tl.id == "TL01" and vehicle.direction in ["N", "S"]:
                        if tl.current_state == "red" and abs(y - 400) > 50:
                            # Stop before intersection
                            vehicle.velocity = (0, 0)
                        elif tl.current_state == "green":
                            # Restore normal movement
                            if vehicle.direction == "N":
                                vehicle.velocity = (0, 2)
                            else:
                                vehicle.velocity = (0, -2)
                                
    def update_traffic_lights(self, dt):
        """Update traffic light timing and states"""
        for tl in self.traffic_lights:
            tl.timer += dt
            
            current_cycle_time = tl.cycle_times[tl.current_state]
            if tl.timer >= current_cycle_time:
                # Switch to next state
                if tl.current_state == "red":
                    tl.current_state = "green"
                elif tl.current_state == "green":
                    tl.current_state = "yellow"
                else:  # yellow
                    tl.current_state = "red"
                    
                tl.timer = 0.0
                
    def update_camera_data(self):
        """Update camera vehicle counts and statistics"""
        for cam in self.cameras:
            cam.vehicle_count = 0
            cam.queue_length = 0
            
            # Count vehicles in camera coverage area
            x1, y1 = cam.coverage_area[0]
            x2, y2 = cam.coverage_area[1]
            
            vehicles_in_area = []
            for vehicle in self.vehicles:
                vx, vy = vehicle.position
                if x1 <= vx <= x2 and y1 <= vy <= y2:
                    cam.vehicle_count += 1
                    vehicles_in_area.append(vehicle)
                    
            # Calculate queue length (vehicles moving slowly)
            cam.queue_length = sum(1 for v in vehicles_in_area 
                                 if abs(v.velocity[0]) + abs(v.velocity[1]) < 0.5)
            
            # Update peak queue length
            self.stats['peak_queue_length'] = max(self.stats['peak_queue_length'], cam.queue_length)
            
    def draw_frame(self):
        """Draw the current simulation frame"""
        frame = self.intersection_map.copy()
        
        # Draw vehicles
        for vehicle in self.vehicles:
            x, y = int(vehicle.position[0]), int(vehicle.position[1])
            w, h = vehicle.size
            
            # Draw vehicle as rectangle
            cv2.rectangle(frame, (x - w//2, y - h//2), (x + w//2, y + h//2), vehicle.color, -1)
            cv2.rectangle(frame, (x - w//2, y - h//2), (x + w//2, y + h//2), (255, 255, 255), 1)
            
        # Draw traffic lights
        for tl in self.traffic_lights:
            x, y = tl.position
            color = {"red": (0, 0, 255), "yellow": (0, 255, 255), "green": (0, 255, 0)}[tl.current_state]
            cv2.circle(frame, (x, y), 15, color, -1)
            cv2.circle(frame, (x, y), 15, (255, 255, 255), 2)
            
        # Draw camera positions
        for cam in self.cameras:
            x, y = cam.position
            color = (0, 255, 0) if cam.active else (0, 0, 255)
            cv2.circle(frame, (x, y), 8, color, -1)
            cv2.putText(frame, cam.id, (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
        # Draw performance info
        cv2.putText(frame, f"FPS: {self.current_fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Vehicles: {len(self.vehicles)}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Total Spawned: {self.stats['total_vehicles']}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return frame
        
    def update_ui(self):
        """Update the UI with current statistics"""
        if not self.running:
            return
            
        # Update performance metrics
        self.fps_label.config(text=f"FPS: {self.current_fps:.1f}")
        self.vehicles_label.config(text=f"Active Vehicles: {len(self.vehicles)}")
        
        # Update camera status
        for cam in self.cameras:
            status = "Active" if cam.active else "Inactive"
            self.camera_labels[cam.id].config(text=f"{cam.id}: {status} - {cam.vehicle_count} vehicles")
            
        # Update traffic light status
        for tl in self.traffic_lights:
            self.traffic_labels[tl.id].config(text=f"{tl.id}: {tl.current_state.upper()}")
            
        # Update statistics
        for key, value in self.stats.items():
            display_value = f"{value:.1f}" if isinstance(value, float) else str(value)
            self.stats_labels[key].config(text=f"{key.replace('_', ' ').title()}: {display_value}")
            
        # Schedule next update
        self.root.after(100, self.update_ui)
        
    def simulation_loop(self):
        """Main simulation loop for maximum performance"""
        last_time = time.time()
        
        while self.running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            if not self.paused:
                # Update simulation
                self.spawn_vehicle()
                self.update_vehicles()
                self.update_traffic_lights(dt)
                self.update_camera_data()
                self.stats['simulation_time'] += dt
                
            # Render frame
            frame = self.draw_frame()
            cv2.imshow("High-Performance Intersection Simulation", frame)
            
            # Handle OpenCV events
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.stop_simulation()
                break
            elif key == ord(' '):
                self.toggle_pause()
                
            # Calculate FPS
            self.fps_counter += 1
            if current_time - self.fps_timer >= 1.0:
                self.current_fps = self.fps_counter
                self.fps_counter = 0
                self.fps_timer = current_time
                
            # Target FPS control
            target_dt = 1.0 / FPS_TARGET
            actual_dt = time.time() - current_time
            if actual_dt < target_dt:
                time.sleep(target_dt - actual_dt)
                
    def start_simulation(self):
        """Start the simulation"""
        if not self.running:
            self.running = True
            self.paused = False
            
            # Start simulation thread
            self.sim_thread = threading.Thread(target=self.simulation_loop, daemon=True)
            self.sim_thread.start()
            
            # Start UI updates
            self.update_ui()
            
            self.start_btn.config(state=tk.DISABLED)
            
    def toggle_pause(self):
        """Toggle simulation pause"""
        self.paused = not self.paused
        self.pause_btn.config(text="Resume" if self.paused else "Pause")
        
    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False
        self.paused = False
        
        cv2.destroyAllWindows()
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(text="Pause")
        
    def run(self):
        """Start the application"""
        print("🚀 High-Performance Intersection Simulation")
        print("="*50)
        print("Controls:")
        print("  - Use GUI buttons to control simulation")
        print("  - Press 'Q' in OpenCV window to quit")
        print("  - Press 'SPACE' in OpenCV window to pause/resume")
        print("  - Target FPS: 60")
        print("="*50)
        
        self.root.mainloop()

if __name__ == "__main__":
    app = HighPerformanceIntersection()
    app.run()