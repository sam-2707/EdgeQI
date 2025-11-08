"""
High-Performance Intersection Simulation - Simplified Version
Native desktop application with better performance and stability

Features:
- Simple matplotlib-based rendering
- Real-time vehicle simulation  
- 7 camera monitoring system
- 3 traffic light control
- Performance metrics display
- Stable cross-platform operation
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time
import random
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
import tkinter as tk
from tkinter import ttk
import threading

# Performance configuration
UPDATE_INTERVAL = 100  # milliseconds
VEHICLE_SPAWN_RATE = 0.15

@dataclass 
class Camera:
    id: str
    name: str
    position: Tuple[int, int]
    coverage_area: List[Tuple[int, int]]
    vehicle_count: int = 0
    active: bool = True

@dataclass
class TrafficLight:
    id: str
    position: Tuple[int, int] 
    current_state: str = "red"
    timer: float = 0.0
    cycle_times: Dict[str, float] = field(default_factory=lambda: {
        "red": 20.0, "green": 15.0, "yellow": 3.0
    })

@dataclass
class Vehicle:
    id: str
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    direction: str
    color: Tuple[float, float, float]
    size: float = 3.0

class SimpleIntersectionSim:
    def __init__(self):
        self.width = 100
        self.height = 70
        self.running = False
        self.paused = False
        
        # Performance tracking
        self.fps_counter = 0
        self.fps_timer = time.time()
        self.current_fps = 0
        
        # Initialize components
        self.setup_components()
        
        # Vehicle management
        self.vehicles = []
        self.vehicle_id_counter = 0
        
        # Statistics
        self.stats = {
            'total_vehicles': 0,
            'vehicles_passed': 0,
            'simulation_time': 0.0
        }
        
        # Setup visualization
        self.setup_visualization()
        
        # Create control UI
        self.setup_ui()
        
    def setup_components(self):
        """Initialize cameras and traffic lights"""
        self.cameras = [
            Camera("CAM01", "North", (50, 10), [(40, 0), (60, 25)]),
            Camera("CAM02", "South", (50, 60), [(40, 45), (60, 70)]),
            Camera("CAM03", "East", (80, 35), [(60, 25), (100, 45)]),
            Camera("CAM04", "West", (20, 35), [(0, 25), (40, 45)]),
            Camera("CAM05", "Center", (50, 35), [(40, 25), (60, 45)]),
            Camera("CAM06", "NE Monitor", (70, 15), [(60, 0), (100, 25)]),
            Camera("CAM07", "SW Monitor", (30, 55), [(0, 45), (40, 70)])
        ]
        
        self.traffic_lights = [
            TrafficLight("TL01", (45, 30), "red", 0.0),
            TrafficLight("TL02", (55, 40), "green", 0.0), 
            TrafficLight("TL03", (50, 20), "red", 5.0)
        ]
        
    def setup_visualization(self):
        """Setup matplotlib figure"""
        plt.ion()  # Interactive mode
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_aspect('equal')
        self.ax.set_title('High-Performance Intersection Simulation')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Create road network
        self.create_roads()
        
    def create_roads(self):
        """Draw the intersection roads"""
        # Road surfaces
        road_h = patches.Rectangle((0, 25), self.width, 20, facecolor='#333', alpha=0.8)
        road_v = patches.Rectangle((40, 0), 20, self.height, facecolor='#333', alpha=0.8)
        self.ax.add_patch(road_h)
        self.ax.add_patch(road_v)
        
        # Lane lines
        self.ax.axhline(y=32.5, xmin=0, xmax=0.4, color='white', linewidth=1)
        self.ax.axhline(y=32.5, xmin=0.6, xmax=1, color='white', linewidth=1)
        self.ax.axhline(y=37.5, xmin=0, xmax=0.4, color='white', linewidth=1) 
        self.ax.axhline(y=37.5, xmin=0.6, xmax=1, color='white', linewidth=1)
        
        self.ax.axvline(x=47.5, ymin=0, ymax=0.36, color='white', linewidth=1)
        self.ax.axvline(x=47.5, ymin=0.64, ymax=1, color='white', linewidth=1)
        self.ax.axvline(x=52.5, ymin=0, ymax=0.36, color='white', linewidth=1)
        self.ax.axvline(x=52.5, ymin=0.64, ymax=1, color='white', linewidth=1)
        
        # Camera positions
        for cam in self.cameras:
            x, y = cam.position
            circle = patches.Circle((x, y), 1.5, facecolor='lime', edgecolor='white')
            self.ax.add_patch(circle)
            self.ax.text(x+2, y, cam.id, fontsize=8, color='white')
            
    def setup_ui(self):
        """Create control interface"""
        self.root = tk.Tk()
        self.root.title("Intersection Simulation Control")
        self.root.geometry("300x400")
        
        # Controls
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="Start", command=self.start_sim).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Pause", command=self.pause_sim).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Stop", command=self.stop_sim).pack(side=tk.LEFT, padx=5)
        
        # Performance info
        perf_frame = ttk.LabelFrame(self.root, text="Performance")
        perf_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.fps_label = ttk.Label(perf_frame, text="FPS: 0")
        self.fps_label.pack(anchor=tk.W)
        
        self.vehicles_label = ttk.Label(perf_frame, text="Vehicles: 0")
        self.vehicles_label.pack(anchor=tk.W)
        
        # Camera info
        cam_frame = ttk.LabelFrame(self.root, text="Cameras")
        cam_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.cam_labels = {}
        for cam in self.cameras:
            label = ttk.Label(cam_frame, text=f"{cam.id}: 0")
            label.pack(anchor=tk.W)
            self.cam_labels[cam.id] = label
            
        # Traffic lights
        tl_frame = ttk.LabelFrame(self.root, text="Traffic Lights")
        tl_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.tl_labels = {}
        for tl in self.traffic_lights:
            label = ttk.Label(tl_frame, text=f"{tl.id}: {tl.current_state.upper()}")
            label.pack(anchor=tk.W)
            self.tl_labels[tl.id] = label
            
    def spawn_vehicle(self):
        """Add new vehicle"""
        if random.random() < VEHICLE_SPAWN_RATE:
            entries = [
                ((50, 0), (0, 1), "N"),
                ((50, 70), (0, -1), "S"),
                ((0, 35), (1, 0), "E"),
                ((100, 35), (-1, 0), "W")
            ]
            
            pos, vel, direction = random.choice(entries)
            color = (random.random(), random.random(), random.random())
            
            vehicle = Vehicle(
                id=f"V{self.vehicle_id_counter}",
                position=pos,
                velocity=vel,
                direction=direction,
                color=color
            )
            
            self.vehicles.append(vehicle)
            self.vehicle_id_counter += 1
            self.stats['total_vehicles'] += 1
            
    def update_vehicles(self):
        """Update vehicle positions"""
        for vehicle in self.vehicles[:]:
            # Move vehicle
            x, y = vehicle.position
            vx, vy = vehicle.velocity
            vehicle.position = (x + vx * 1.5, y + vy * 1.5)
            
            # Remove if outside bounds
            if (vehicle.position[0] < -10 or vehicle.position[0] > self.width + 10 or
                vehicle.position[1] < -10 or vehicle.position[1] > self.height + 10):
                self.vehicles.remove(vehicle)
                self.stats['vehicles_passed'] += 1
                
    def update_traffic_lights(self):
        """Update traffic light states"""
        current_time = time.time()
        for tl in self.traffic_lights:
            tl.timer += UPDATE_INTERVAL / 1000.0
            
            cycle_time = tl.cycle_times[tl.current_state]
            if tl.timer >= cycle_time:
                if tl.current_state == "red":
                    tl.current_state = "green"
                elif tl.current_state == "green":
                    tl.current_state = "yellow"
                else:
                    tl.current_state = "red"
                tl.timer = 0.0
                
    def update_cameras(self):
        """Update camera vehicle counts"""
        for cam in self.cameras:
            cam.vehicle_count = 0
            x1, y1 = cam.coverage_area[0] 
            x2, y2 = cam.coverage_area[1]
            
            for vehicle in self.vehicles:
                vx, vy = vehicle.position
                if x1 <= vx <= x2 and y1 <= vy <= y2:
                    cam.vehicle_count += 1
                    
    def update_display(self):
        """Update the visualization"""
        if not self.running or self.paused:
            return
            
        # Clear vehicles and traffic lights
        patches_to_remove = []
        for patch in self.ax.patches:
            if hasattr(patch, '_is_dynamic'):
                patches_to_remove.append(patch)
        for patch in patches_to_remove:
            patch.remove()
            
        # Draw vehicles
        for vehicle in self.vehicles:
            x, y = vehicle.position
            circle = patches.Circle((x, y), vehicle.size, facecolor=vehicle.color, 
                                  edgecolor='white', linewidth=0.5)
            circle._is_dynamic = True
            self.ax.add_patch(circle)
            
        # Draw traffic lights
        colors = {"red": 'red', "yellow": 'yellow', "green": 'lime'}
        for tl in self.traffic_lights:
            x, y = tl.position
            circle = patches.Circle((x, y), 2, facecolor=colors[tl.current_state],
                                  edgecolor='white', linewidth=1)
            circle._is_dynamic = True
            self.ax.add_patch(circle)
            
        # Update title
        title = f"Intersection Sim | FPS: {self.current_fps:.1f} | Vehicles: {len(self.vehicles)}"
        self.ax.set_title(title)
        
        # Redraw
        self.fig.canvas.draw_idle()
        
    def simulation_step(self):
        """One simulation step"""
        if not self.running or self.paused:
            if self.running:
                self.root.after(UPDATE_INTERVAL, self.simulation_step)
            return
            
        # Update simulation
        self.spawn_vehicle()
        self.update_vehicles()
        self.update_traffic_lights()
        self.update_cameras()
        self.update_display()
        
        # Update UI
        self.fps_counter += 1
        current_time = time.time()
        if current_time - self.fps_timer >= 1.0:
            self.current_fps = self.fps_counter * (1000.0 / UPDATE_INTERVAL)
            self.fps_counter = 0
            self.fps_timer = current_time
            
        # Update labels
        self.fps_label.config(text=f"FPS: {self.current_fps:.1f}")
        self.vehicles_label.config(text=f"Vehicles: {len(self.vehicles)}")
        
        for cam in self.cameras:
            self.cam_labels[cam.id].config(text=f"{cam.id}: {cam.vehicle_count}")
            
        for tl in self.traffic_lights:
            self.tl_labels[tl.id].config(text=f"{tl.id}: {tl.current_state.upper()}")
            
        # Schedule next step
        self.root.after(UPDATE_INTERVAL, self.simulation_step)
        
    def start_sim(self):
        """Start simulation"""
        if not self.running:
            self.running = True
            self.paused = False
            plt.show(block=False)
            self.simulation_step()
            print("🚀 High-performance simulation started!")
            
    def pause_sim(self):
        """Toggle pause"""
        self.paused = not self.paused
        if not self.paused and self.running:
            self.simulation_step()
            
    def stop_sim(self):
        """Stop simulation"""
        self.running = False
        self.paused = False
        plt.close('all')
        print("⏹️ Simulation stopped!")
        
    def run(self):
        """Main application loop"""
        print("🚀 High-Performance Intersection Simulation")
        print("="*50)
        print("Features:")
        print("  - 7 Strategic Cameras")
        print("  - 3 Traffic Lights")
        print("  - Real-time vehicle simulation")
        print("  - Performance optimized")
        print("="*50)
        print("Use the control panel to start simulation")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n⏹️ Stopped by user")
        finally:
            plt.close('all')

if __name__ == "__main__":
    app = SimpleIntersectionSim()
    app.run()