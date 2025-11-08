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
        "red": 25.0, "green": 20.0, "yellow": 4.0
    })

@dataclass
class Vehicle:
    id: str
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    direction: str  # N, S, E, W
    color: Tuple[float, float, float]
    size: Tuple[int, int] = (8, 5)
    speed: float = 2.0
    lane: int = 0

class HighPerformanceIntersection:
    def __init__(self):
        self.width = 120
        self.height = 80
        self.running = False
        self.paused = False
        
        # Performance tracking
        self.fps_counter = 0
        self.fps_timer = time.time()
        self.current_fps = 0
        
        # Initialize components
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
        
        # Setup matplotlib
        self.setup_visualization()
        
        # Create control UI
        self.setup_ui()
        
    def setup_cameras(self):
        """Initialize the 7 camera monitoring system"""
        self.cameras = [
            Camera("CAM01", "North Approach", (60, 10), 180, 20, [(50, 0), (70, 30)]),
            Camera("CAM02", "South Approach", (60, 70), 0, 20, [(50, 50), (70, 80)]),
            Camera("CAM03", "East Approach", (100, 40), 270, 20, [(70, 30), (120, 50)]),
            Camera("CAM04", "West Approach", (20, 40), 90, 20, [(0, 30), (50, 50)]),
            Camera("CAM05", "Center Intersection", (60, 40), 0, 15, [(50, 30), (70, 50)]),
            Camera("CAM06", "Northeast Monitor", (80, 20), 225, 18, [(70, 0), (120, 30)]),
            Camera("CAM07", "Southwest Monitor", (40, 60), 45, 18, [(0, 50), (50, 80)])
        ]
        
    def setup_traffic_lights(self):
        """Initialize the 3 traffic light system"""
        self.traffic_lights = [
            TrafficLight("TL01", (55, 35), "red", 0.0),    # North-South main
            TrafficLight("TL02", (65, 45), "green", 0.0),  # East-West cross  
            TrafficLight("TL03", (60, 25), "red", 10.0)    # Pedestrian signal
        ]
        
    def setup_visualization(self):
        """Setup matplotlib visualization"""
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_aspect('equal')
        self.ax.set_title('High-Performance Intersection Simulation', fontsize=16, color='white')
        
        # Remove axes for cleaner look
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Create intersection background
        self.create_intersection_background()
        
    def create_intersection_background(self):
        """Create the intersection road network"""
        # Road color scheme
        road_color = '#3a3a3a'
        line_color = 'white'
        crosswalk_color = '#cccccc'
        
        # Main roads
        # Horizontal road (East-West)
        road_h = patches.Rectangle((0, 30), self.width, 20, facecolor=road_color, edgecolor='none')
        self.ax.add_patch(road_h)
        
        # Vertical road (North-South)
        road_v = patches.Rectangle((50, 0), 20, self.height, facecolor=road_color, edgecolor='none')
        self.ax.add_patch(road_v)
        
        # Lane dividers - Horizontal
        self.ax.plot([0, 50], [37.5, 37.5], color=line_color, linewidth=1, linestyle='-')
        self.ax.plot([70, self.width], [37.5, 37.5], color=line_color, linewidth=1, linestyle='-')
        self.ax.plot([0, 50], [42.5, 42.5], color=line_color, linewidth=1, linestyle='-')
        self.ax.plot([70, self.width], [42.5, 42.5], color=line_color, linewidth=1, linestyle='-')
        
        # Lane dividers - Vertical
        self.ax.plot([57.5, 57.5], [0, 30], color=line_color, linewidth=1, linestyle='-')
        self.ax.plot([57.5, 57.5], [50, self.height], color=line_color, linewidth=1, linestyle='-')
        self.ax.plot([62.5, 62.5], [0, 30], color=line_color, linewidth=1, linestyle='-')
        self.ax.plot([62.5, 62.5], [50, self.height], color=line_color, linewidth=1, linestyle='-')
        
        # Crosswalks
        for i in range(52, 68, 3):
            crosswalk = patches.Rectangle((i, 28), 2, 4, facecolor=crosswalk_color, edgecolor='none')
            self.ax.add_patch(crosswalk)
            crosswalk = patches.Rectangle((i, 48), 2, 4, facecolor=crosswalk_color, edgecolor='none')
            self.ax.add_patch(crosswalk)
        
        for i in range(32, 48, 3):
            crosswalk = patches.Rectangle((48, i), 4, 2, facecolor=crosswalk_color, edgecolor='none')
            self.ax.add_patch(crosswalk)
            crosswalk = patches.Rectangle((68, i), 4, 2, facecolor=crosswalk_color, edgecolor='none')
            self.ax.add_patch(crosswalk)
            
    def setup_ui(self):
        """Create the control UI"""
        self.root = tk.Tk()
        self.root.title("High-Performance Intersection Control")
        self.root.geometry("350x500")
        
        # Control buttons
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(control_frame, text="Start", command=self.start_simulation)
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
            label = ttk.Label(camera_frame, text=f"{cam.id}: 0 vehicles")
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
            
    def spawn_vehicle(self):
        """Spawn a new vehicle at random entry point"""
        if random.random() < VEHICLE_SPAWN_RATE:
            entry_points = [
                ((60, 0), (0, 1.5), "N"),      # North entry
                ((60, self.height), (0, -1.5), "S"),  # South entry
                ((0, 37.5), (1.5, 0), "E"),   # East entry
                ((self.width, 37.5), (-1.5, 0), "W")  # West entry
            ]
            
            pos, vel, direction = random.choice(entry_points)
            color = (random.random(), random.random(), random.random())
            
            vehicle = Vehicle(
                id=f"V{self.vehicle_id_counter}",
                position=pos,
                velocity=vel,
                direction=direction,
                color=color,
                speed=random.uniform(1.0, 2.5)
            )
            
            self.vehicles.append(vehicle)
            self.vehicle_id_counter += 1
            self.stats['total_vehicles'] += 1
            
    def update_vehicles(self, dt):
        """Update vehicle positions and handle traffic logic"""
        for vehicle in self.vehicles[:]:  # Copy list to allow removal
            # Basic movement
            vehicle.position = (
                vehicle.position[0] + vehicle.velocity[0] * vehicle.speed * dt * 10,
                vehicle.position[1] + vehicle.velocity[1] * vehicle.speed * dt * 10
            )
            
            # Remove vehicles that left the simulation area
            if (vehicle.position[0] < -10 or vehicle.position[0] > self.width + 10 or
                vehicle.position[1] < -10 or vehicle.position[1] > self.height + 10):
                self.vehicles.remove(vehicle)
                self.stats['vehicles_passed'] += 1
                continue
                
            # Simple traffic light logic
            x, y = vehicle.position
            if 55 < x < 65 and 32 < y < 48:  # In intersection area
                for tl in self.traffic_lights:
                    if tl.id == "TL01" and vehicle.direction in ["N", "S"]:
                        if tl.current_state == "red":
                            vehicle.velocity = (0, 0)  # Stop
                        elif tl.current_state == "green":
                            # Restore movement
                            if vehicle.direction == "N":
                                vehicle.velocity = (0, 1.5)
                            else:
                                vehicle.velocity = (0, -1.5)
                                
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
        """Update camera vehicle counts"""
        for cam in self.cameras:
            cam.vehicle_count = 0
            x1, y1 = cam.coverage_area[0]
            x2, y2 = cam.coverage_area[1]
            
            for vehicle in self.vehicles:
                vx, vy = vehicle.position
                if x1 <= vx <= x2 and y1 <= vy <= y2:
                    cam.vehicle_count += 1
                    
    def animate(self, frame):
        """Animation function for matplotlib"""
        if not self.running or self.paused:
            return []
            
        # Clear previous dynamic elements
        # Keep roads and static elements, remove vehicles and lights
        for artist in self.ax.collections + self.ax.patches[4:]:  # Keep first 4 patches (roads)
            artist.remove()
            
        # Update simulation
        dt = 1.0 / FPS_TARGET
        self.spawn_vehicle()
        self.update_vehicles(dt)
        self.update_traffic_lights(dt)
        self.update_camera_data()
        self.stats['simulation_time'] += dt
        
        # Draw vehicles
        for vehicle in self.vehicles:
            x, y = vehicle.position
            w, h = vehicle.size
            
            vehicle_rect = patches.Rectangle(
                (x - w/2, y - h/2), w, h,
                facecolor=vehicle.color, edgecolor='white', linewidth=0.5
            )
            self.ax.add_patch(vehicle_rect)
            
        # Draw traffic lights
        colors = {"red": 'red', "yellow": 'yellow', "green": 'lime'}
        for tl in self.traffic_lights:
            x, y = tl.position
            light = patches.Circle(
                (x, y), 1.5, 
                facecolor=colors[tl.current_state], 
                edgecolor='white', linewidth=1
            )
            self.ax.add_patch(light)
            
        # Draw cameras
        for cam in self.cameras:
            x, y = cam.position
            cam_circle = patches.Circle(
                (x, y), 1, 
                facecolor='lime' if cam.active else 'red', 
                edgecolor='white', linewidth=1
            )
            self.ax.add_patch(cam_circle)
            
        # Update FPS
        self.fps_counter += 1
        current_time = time.time()
        if current_time - self.fps_timer >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_timer = current_time
            
        # Update title with stats
        title = (f"High-Performance Intersection | FPS: {self.current_fps:.1f} | "
                f"Vehicles: {len(self.vehicles)} | Total: {self.stats['total_vehicles']}")
        self.ax.set_title(title, fontsize=14, color='white')
        
        return []
        
    def update_ui(self):
        """Update the UI with current statistics"""
        if not self.running:
            return
            
        # Update performance metrics
        self.fps_label.config(text=f"FPS: {self.current_fps:.1f}")
        self.vehicles_label.config(text=f"Active Vehicles: {len(self.vehicles)}")
        
        # Update camera status
        for cam in self.cameras:
            self.camera_labels[cam.id].config(text=f"{cam.id}: {cam.vehicle_count} vehicles")
            
        # Update traffic light status
        for tl in self.traffic_lights:
            self.traffic_labels[tl.id].config(text=f"{tl.id}: {tl.current_state.upper()}")
            
        # Schedule next update
        if self.running:
            self.root.after(200, self.update_ui)
        
    def start_simulation(self):
        """Start the simulation"""
        if not self.running:
            self.running = True
            self.paused = False
            
            # Start animation
            self.anim = FuncAnimation(
                self.fig, self.animate, interval=1000//FPS_TARGET, 
                blit=False, repeat=True
            )
            
            # Show matplotlib window
            plt.show(block=False)
            
            # Start UI updates
            self.update_ui()
            
            self.start_btn.config(state=tk.DISABLED)
            print("🚀 Simulation started!")
            
    def toggle_pause(self):
        """Toggle simulation pause"""
        self.paused = not self.paused
        self.pause_btn.config(text="Resume" if self.paused else "Pause")
        
    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False
        self.paused = False
        
        if hasattr(self, 'anim'):
            self.anim.event_source.stop()
            
        plt.close('all')
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(text="Pause")
        print("⏹️ Simulation stopped!")
        
    def run(self):
        """Start the application"""
        print("🚀 High-Performance Intersection Simulation")
        print("="*50)
        print("Features:")
        print("  - 7 Strategic Cameras monitoring traffic")
        print("  - 3 Traffic Lights with realistic timing")
        print("  - Real-time vehicle simulation")
        print("  - Performance metrics tracking")
        print("  - Target FPS: 30 (matplotlib optimized)")
        print("="*50)
        print("Use the control panel to start the simulation")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n⏹️ Stopped by user")
        finally:
            plt.close('all')

if __name__ == "__main__":
    app = HighPerformanceIntersection()
    app.run()