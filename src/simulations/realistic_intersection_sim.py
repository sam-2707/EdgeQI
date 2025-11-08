"""
Realistic Intersection Simulation with Map Rendering

Features:
- 6-7 cameras positioned around intersections
- 2-3 traffic signals with realistic timing
- Rendered road network map
- Real-time analytics and graphs
- Vehicle counting and flow analysis
- Queue detection and analysis
"""

import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import time
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
from functools import lru_cache

# Configure Streamlit
st.set_page_config(
    page_title="🗺️ Realistic Intersection Simulation",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS for better performance
st.markdown("""
<style>
    .stApp {
        max-width: 100%;
    }
    [data-testid="stMetricValue"] {
        font-size: 20px;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
    div[data-testid="stImage"] {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

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

@dataclass
class TrafficLight:
    id: str
    position: Tuple[int, int]
    state: str  # 'red', 'yellow', 'green'
    timer: float
    cycle_time: Dict[str, float]  # Duration for each state

@dataclass
class Vehicle:
    id: int
    position: Tuple[float, float]
    speed: float
    direction: str  # 'north', 'south', 'east', 'west'
    vehicle_type: str  # 'car', 'truck', 'bus'
    color: Tuple[int, int, int]
    in_queue: bool = False
    wait_time: float = 0.0

class RealisticIntersectionSimulation:
    def __init__(self):
        self.width = 1200
        self.height = 800
        self.update_frequency = 10  # FPS target for better performance
        
        # Initialize session state
        if 'sim_running' not in st.session_state:
            st.session_state.sim_running = False
        if 'vehicles' not in st.session_state:
            st.session_state.vehicles = {}
        if 'analytics_data' not in st.session_state:
            st.session_state.analytics_data = {
                'timestamps': [],
                'total_vehicles': [],
                'queue_lengths': [],
                'avg_speeds': [],
                'traffic_light_states': [],
                'camera_data': {}
            }
        if 'start_time' not in st.session_state:
            st.session_state.start_time = time.time()
        if 'last_update' not in st.session_state:
            st.session_state.last_update = time.time()
        
        self.setup_infrastructure()
        
    def setup_infrastructure(self):
        """Setup cameras, traffic lights, and road network"""
        # Define 7 cameras around the intersection
        self.cameras = {
            'cam_north': Camera(
                id='cam_north',
                name='North Approach',
                position=(600, 150),
                view_angle=180,
                view_distance=200,
                coverage_area=[(500, 50), (700, 300)]
            ),
            'cam_south': Camera(
                id='cam_south', 
                name='South Approach',
                position=(600, 650),
                view_angle=0,
                view_distance=200,
                coverage_area=[(500, 500), (700, 750)]
            ),
            'cam_east': Camera(
                id='cam_east',
                name='East Approach', 
                position=(1050, 400),
                view_angle=270,
                view_distance=200,
                coverage_area=[(850, 300), (1150, 500)]
            ),
            'cam_west': Camera(
                id='cam_west',
                name='West Approach',
                position=(150, 400),
                view_angle=90,
                view_distance=200,
                coverage_area=[(50, 300), (350, 500)]
            ),
            'cam_center': Camera(
                id='cam_center',
                name='Center Intersection',
                position=(600, 400),
                view_angle=360,
                view_distance=150,
                coverage_area=[(450, 250), (750, 550)]
            ),
            'cam_northeast': Camera(
                id='cam_northeast',
                name='Northeast Monitor',
                position=(800, 200),
                view_angle=225,
                view_distance=180,
                coverage_area=[(650, 150), (950, 350)]
            ),
            'cam_southwest': Camera(
                id='cam_southwest', 
                name='Southwest Monitor',
                position=(400, 600),
                view_angle=45,
                view_distance=180,
                coverage_area=[(250, 450), (550, 650)]
            )
        }
        
        # Define 3 traffic lights
        self.traffic_lights = {
            'light_ns': TrafficLight(
                id='light_ns',
                position=(580, 380),
                state='green',
                timer=0,
                cycle_time={'green': 30, 'yellow': 5, 'red': 35}
            ),
            'light_ew': TrafficLight(
                id='light_ew', 
                position=(620, 420),
                state='red',
                timer=0,
                cycle_time={'green': 25, 'yellow': 5, 'red': 40}
            ),
            'light_pedestrian': TrafficLight(
                id='light_pedestrian',
                position=(560, 440),
                state='red',
                timer=0,
                cycle_time={'green': 15, 'yellow': 3, 'red': 52}
            )
        }
        
        # Road network definition
        self.roads = {
            'main_ns': [(550, 0), (650, 800)],  # North-South main road
            'main_ew': [(0, 350), (1200, 450)],  # East-West main road
            'turn_lanes': [
                [(520, 300), (580, 350)],  # Left turn lane
                [(620, 450), (680, 500)],  # Right turn lane
            ]
        }
        
    def generate_intersection_map(self) -> np.ndarray:
        """Generate the intersection map with roads, cameras, and traffic lights"""
        # Create base map
        map_img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 40  # Dark background
        
        # Draw roads
        # Main North-South road
        cv2.rectangle(map_img, (550, 0), (650, 800), (80, 80, 80), -1)
        # Main East-West road  
        cv2.rectangle(map_img, (0, 350), (1200, 450), (80, 80, 80), -1)
        
        # Draw intersection
        cv2.rectangle(map_img, (550, 350), (650, 450), (70, 70, 70), -1)
        
        # Draw lane markings
        # North-South lanes
        cv2.line(map_img, (600, 0), (600, 350), (255, 255, 255), 2)
        cv2.line(map_img, (600, 450), (600, 800), (255, 255, 255), 2)
        
        # East-West lanes  
        cv2.line(map_img, (0, 400), (550, 400), (255, 255, 255), 2)
        cv2.line(map_img, (650, 400), (1200, 400), (255, 255, 255), 2)
        
        # Draw crosswalks
        for i in range(0, 100, 20):
            cv2.rectangle(map_img, (560 + i, 340), (570 + i, 350), (255, 255, 255), -1)
            cv2.rectangle(map_img, (560 + i, 450), (570 + i, 460), (255, 255, 255), -1)
            cv2.rectangle(map_img, (540, 360 + i), (550, 370 + i), (255, 255, 255), -1)
            cv2.rectangle(map_img, (650, 360 + i), (660, 370 + i), (255, 255, 255), -1)
        
        # Draw cameras
        for cam in self.cameras.values():
            x, y = cam.position
            # Camera body
            cv2.circle(map_img, (x, y), 8, (0, 255, 0), -1)
            cv2.circle(map_img, (x, y), 12, (0, 200, 0), 2)
            # Camera ID
            cv2.putText(map_img, cam.id.replace('cam_', ''), (x-15, y-20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
            # Draw coverage area (subtle)
            coverage = np.array(cam.coverage_area, np.int32)
            overlay = map_img.copy()
            cv2.fillPoly(overlay, [coverage], (0, 255, 0))
            cv2.addWeighted(map_img, 0.9, overlay, 0.1, 0, map_img)
        
        # Draw traffic lights
        for light in self.traffic_lights.values():
            x, y = light.position
            # Traffic light pole
            cv2.rectangle(map_img, (x-3, y-15), (x+3, y+5), (100, 100, 100), -1)
            
            # Light colors based on state
            colors = {
                'red': (0, 0, 255),
                'yellow': (0, 255, 255), 
                'green': (0, 255, 0)
            }
            color = colors.get(light.state, (100, 100, 100))
            cv2.circle(map_img, (x, y-10), 4, color, -1)
            
            # Light ID
            cv2.putText(map_img, light.id.replace('light_', ''), (x-10, y+20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
        
        return map_img
    
    def update_traffic_lights(self, dt: float):
        """Update traffic light states based on timing"""
        for light in self.traffic_lights.values():
            light.timer += dt
            
            current_duration = light.cycle_time[light.state]
            if light.timer >= current_duration:
                light.timer = 0
                
                # State transitions
                if light.state == 'green':
                    light.state = 'yellow'
                elif light.state == 'yellow':
                    light.state = 'red'
                elif light.state == 'red':
                    light.state = 'green'
    
    def generate_vehicles(self):
        """Generate realistic vehicle traffic"""
        current_time = time.time()
        
        # Spawn vehicles based on traffic patterns
        spawn_rate = 0.1  # Probability per frame
        if random.random() < spawn_rate:
            vehicle_id = len(st.session_state.vehicles) + 1
            
            # Random spawn points and directions
            spawn_points = [
                ((100, 400), 'east'),   # West entrance
                ((1100, 400), 'west'), # East entrance  
                ((600, 100), 'south'), # North entrance
                ((600, 700), 'north')  # South entrance
            ]
            
            spawn_pos, direction = random.choice(spawn_points)
            vehicle_type = random.choice(['car', 'car', 'car', 'truck', 'bus'])  # More cars
            
            colors = {
                'car': [(255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)],
                'truck': [(139, 69, 19), (105, 105, 105)],
                'bus': [(255, 165, 0), (0, 128, 0)]
            }
            
            vehicle = Vehicle(
                id=vehicle_id,
                position=spawn_pos,
                speed=random.uniform(20, 40),
                direction=direction,
                vehicle_type=vehicle_type,
                color=random.choice(colors[vehicle_type])
            )
            
            st.session_state.vehicles[vehicle_id] = vehicle
    
    def update_vehicles(self, dt: float):
        """Update vehicle positions and detect queues"""
        vehicles_to_remove = []
        
        for vehicle in st.session_state.vehicles.values():
            # Update position based on direction
            speed_factor = dt * vehicle.speed
            
            # Check for traffic light stops
            should_stop = self.check_traffic_light_stop(vehicle)
            
            if should_stop:
                vehicle.in_queue = True
                vehicle.wait_time += dt
                vehicle.speed = max(0, vehicle.speed - 10 * dt)  # Gradual stop
            else:
                vehicle.in_queue = False
                vehicle.wait_time = 0
                vehicle.speed = min(40, vehicle.speed + 15 * dt)  # Accelerate
            
            # Move vehicle
            if vehicle.direction == 'east':
                vehicle.position = (vehicle.position[0] + speed_factor, vehicle.position[1])
                if vehicle.position[0] > 1200:
                    vehicles_to_remove.append(vehicle.id)
            elif vehicle.direction == 'west':
                vehicle.position = (vehicle.position[0] - speed_factor, vehicle.position[1])
                if vehicle.position[0] < 0:
                    vehicles_to_remove.append(vehicle.id)
            elif vehicle.direction == 'south':
                vehicle.position = (vehicle.position[0], vehicle.position[1] + speed_factor)
                if vehicle.position[1] > 800:
                    vehicles_to_remove.append(vehicle.id)
            elif vehicle.direction == 'north':
                vehicle.position = (vehicle.position[0], vehicle.position[1] - speed_factor)
                if vehicle.position[1] < 0:
                    vehicles_to_remove.append(vehicle.id)
        
        # Remove vehicles that have left the scene
        for vehicle_id in vehicles_to_remove:
            del st.session_state.vehicles[vehicle_id]
    
    def check_traffic_light_stop(self, vehicle: Vehicle) -> bool:
        """Check if vehicle should stop for traffic light"""
        x, y = vehicle.position
        
        # Check intersection approach zones
        if vehicle.direction == 'east' and 450 <= x <= 550 and 380 <= y <= 420:
            return self.traffic_lights['light_ew'].state in ['red', 'yellow']
        elif vehicle.direction == 'west' and 650 <= x <= 750 and 380 <= y <= 420:
            return self.traffic_lights['light_ew'].state in ['red', 'yellow']
        elif vehicle.direction == 'south' and 580 <= x <= 620 and 250 <= y <= 350:
            return self.traffic_lights['light_ns'].state in ['red', 'yellow']
        elif vehicle.direction == 'north' and 580 <= x <= 620 and 450 <= y <= 550:
            return self.traffic_lights['light_ns'].state in ['red', 'yellow']
        
        return False
    
    def update_camera_analytics(self):
        """Update analytics for each camera"""
        for camera in self.cameras.values():
            # Count vehicles in camera coverage area
            vehicles_in_view = []
            queue_count = 0
            total_speed = 0
            
            for vehicle in st.session_state.vehicles.values():
                x, y = vehicle.position
                x1, y1 = camera.coverage_area[0] 
                x2, y2 = camera.coverage_area[1]
                
                if x1 <= x <= x2 and y1 <= y <= y2:
                    vehicles_in_view.append(vehicle)
                    if vehicle.in_queue:
                        queue_count += 1
                    total_speed += vehicle.speed
            
            camera.vehicle_count = len(vehicles_in_view)
            camera.queue_length = queue_count
            camera.avg_speed = total_speed / len(vehicles_in_view) if vehicles_in_view else 0
    
    def draw_vehicles_on_map(self, map_img: np.ndarray) -> np.ndarray:
        """Draw vehicles on the intersection map"""
        result = map_img.copy()
        
        for vehicle in st.session_state.vehicles.values():
            x, y = int(vehicle.position[0]), int(vehicle.position[1])
            
            # Vehicle size based on type
            sizes = {'car': (15, 8), 'truck': (20, 10), 'bus': (25, 12)}
            w, h = sizes[vehicle.vehicle_type]
            
            # Draw vehicle rectangle
            color = vehicle.color
            if vehicle.in_queue:
                # Add red border for queued vehicles
                cv2.rectangle(result, (x-w//2-2, y-h//2-2), (x+w//2+2, y+h//2+2), (0, 0, 255), 2)
            
            cv2.rectangle(result, (x-w//2, y-h//2), (x+w//2, y+h//2), color, -1)
            
            # Direction indicator
            if vehicle.direction == 'east':
                cv2.arrowedLine(result, (x-5, y), (x+5, y), (255, 255, 255), 1)
            elif vehicle.direction == 'west':
                cv2.arrowedLine(result, (x+5, y), (x-5, y), (255, 255, 255), 1)
            elif vehicle.direction == 'south':
                cv2.arrowedLine(result, (x, y-5), (x, y+5), (255, 255, 255), 1)
            elif vehicle.direction == 'north':
                cv2.arrowedLine(result, (x, y+5), (x, y-5), (255, 255, 255), 1)
        
        return result
    
    def collect_analytics(self):
        """Collect analytics data for graphs"""
        current_time = time.time() - st.session_state.start_time
        
        total_vehicles = len(st.session_state.vehicles)
        total_queues = sum(1 for v in st.session_state.vehicles.values() if v.in_queue)
        avg_speed = np.mean([v.speed for v in st.session_state.vehicles.values()]) if st.session_state.vehicles else 0
        
        # Update analytics data
        analytics = st.session_state.analytics_data
        analytics['timestamps'].append(current_time)
        analytics['total_vehicles'].append(total_vehicles)
        analytics['queue_lengths'].append(total_queues)
        analytics['avg_speeds'].append(avg_speed)
        
        # Traffic light states
        light_states = {light.id: light.state for light in self.traffic_lights.values()}
        analytics['traffic_light_states'].append(light_states)
        
        # Camera data
        for cam_id, camera in self.cameras.items():
            if cam_id not in analytics['camera_data']:
                analytics['camera_data'][cam_id] = {'counts': [], 'queues': [], 'speeds': []}
            
            analytics['camera_data'][cam_id]['counts'].append(camera.vehicle_count)
            analytics['camera_data'][cam_id]['queues'].append(camera.queue_length)
            analytics['camera_data'][cam_id]['speeds'].append(camera.avg_speed)
        
        # Keep only last 100 data points for performance
        max_points = 100
        if len(analytics['timestamps']) > max_points:
            analytics['timestamps'] = analytics['timestamps'][-max_points:]
            analytics['total_vehicles'] = analytics['total_vehicles'][-max_points:]
            analytics['queue_lengths'] = analytics['queue_lengths'][-max_points:]
            analytics['avg_speeds'] = analytics['avg_speeds'][-max_points:]
            analytics['traffic_light_states'] = analytics['traffic_light_states'][-max_points:]
            
            for cam_data in analytics['camera_data'].values():
                cam_data['counts'] = cam_data['counts'][-max_points:]
                cam_data['queues'] = cam_data['queues'][-max_points:]
                cam_data['speeds'] = cam_data['speeds'][-max_points:]

def create_analytics_dashboard(sim: RealisticIntersectionSimulation):
    """Create comprehensive analytics dashboard"""
    analytics = st.session_state.analytics_data
    
    if not analytics['timestamps']:
        st.info("📊 Starting analytics collection...")
        return
    
    # Main metrics
    st.subheader("📊 Real-time Analytics Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_vehicles = analytics['total_vehicles'][-1] if analytics['total_vehicles'] else 0
        st.metric("🚗 Total Vehicles", total_vehicles)
    
    with col2:
        total_queues = analytics['queue_lengths'][-1] if analytics['queue_lengths'] else 0
        st.metric("🚦 Vehicles in Queue", total_queues)
    
    with col3:
        avg_speed = analytics['avg_speeds'][-1] if analytics['avg_speeds'] else 0
        st.metric("⚡ Avg Speed", f"{avg_speed:.1f} km/h")
    
    with col4:
        efficiency = ((total_vehicles - total_queues) / total_vehicles * 100) if total_vehicles > 0 else 0
        st.metric("📈 Traffic Efficiency", f"{efficiency:.1f}%")
    
    # Create comprehensive plots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=[
            'Vehicle Count Over Time',
            'Queue Length Analysis', 
            'Average Speed Trends',
            'Camera Coverage Analysis',
            'Traffic Light States',
            'Intersection Efficiency'
        ],
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    timestamps = analytics['timestamps']
    
    # Vehicle count
    fig.add_trace(
        go.Scatter(x=timestamps, y=analytics['total_vehicles'],
                  name='Total Vehicles', line=dict(color='blue')),
        row=1, col=1
    )
    
    # Queue analysis
    fig.add_trace(
        go.Scatter(x=timestamps, y=analytics['queue_lengths'],
                  name='Queued Vehicles', line=dict(color='red')),
        row=1, col=2
    )
    
    # Speed trends
    fig.add_trace(
        go.Scatter(x=timestamps, y=analytics['avg_speeds'],
                  name='Avg Speed', line=dict(color='green')),
        row=2, col=1
    )
    
    # Camera analysis
    for cam_id, cam_data in analytics['camera_data'].items():
        if cam_data['counts']:
            fig.add_trace(
                go.Scatter(x=timestamps, y=cam_data['counts'],
                          name=f'{cam_id}', mode='lines'),
                row=2, col=2
            )
    
    # Traffic light timing (simplified representation)
    if analytics['traffic_light_states']:
        light_ns_states = [1 if state.get('light_ns') == 'green' else 0 
                          for state in analytics['traffic_light_states']]
        fig.add_trace(
            go.Scatter(x=timestamps, y=light_ns_states,
                      name='NS Light (Green)', line=dict(color='green')),
            row=3, col=1
        )
    
    # Efficiency calculation
    if len(timestamps) > 1:
        efficiency_data = []
        for i in range(len(analytics['total_vehicles'])):
            total = analytics['total_vehicles'][i]
            queued = analytics['queue_lengths'][i]
            eff = ((total - queued) / total * 100) if total > 0 else 0
            efficiency_data.append(eff)
        
        fig.add_trace(
            go.Scatter(x=timestamps, y=efficiency_data,
                      name='Efficiency %', line=dict(color='purple')),
            row=3, col=2
        )
    
    fig.update_layout(height=800, showlegend=True)
    st.plotly_chart(fig, use_column_width=True)

def main():
    """Main application"""
    st.title("🗺️ Realistic Intersection Simulation")
    st.markdown("**Advanced traffic simulation with 7 cameras, 3 traffic lights, and comprehensive analytics**")
    
    # Initialize simulation
    sim = RealisticIntersectionSimulation()
    
    # Control panel
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    with col1:
        if st.button("🚀 Start Simulation", disabled=st.session_state.sim_running):
            st.session_state.sim_running = True
            st.session_state.start_time = time.time()
            st.rerun()
    
    with col2:
        if st.button("⏹️ Stop Simulation", disabled=not st.session_state.sim_running):
            st.session_state.sim_running = False
            st.rerun()
    
    with col3:
        if st.button("🔄 Reset"):
            st.session_state.vehicles = {}
            st.session_state.analytics_data = {
                'timestamps': [], 'total_vehicles': [], 'queue_lengths': [],
                'avg_speeds': [], 'traffic_light_states': [], 'camera_data': {}
            }
            st.session_state.start_time = time.time()
            st.rerun()
    
    with col4:
        st.info(f"🎯 Status: {'🟢 Running' if st.session_state.sim_running else '🔴 Stopped'} | "
                f"Vehicles: {len(st.session_state.vehicles)} | "
                f"Cameras: 7 | Traffic Lights: 3")
    
    if st.session_state.sim_running:
        # Calculate delta time for smooth updates
        current_time = time.time()
        dt = current_time - st.session_state.last_update
        st.session_state.last_update = current_time
        
        # Limit update frequency for better performance
        if dt < 1.0 / sim.update_frequency:
            dt = 1.0 / sim.update_frequency
        
        # Update simulation
        sim.generate_vehicles()
        sim.update_vehicles(dt)
        sim.update_traffic_lights(dt)
        sim.update_camera_analytics()
        sim.collect_analytics()
        
        # Display simulation
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("🗺️ Live Intersection Map")
            
            # Generate and display map
            base_map = sim.generate_intersection_map()
            live_map = sim.draw_vehicles_on_map(base_map)
            
            # Convert BGR to RGB for Streamlit
            live_map_rgb = cv2.cvtColor(live_map, cv2.COLOR_BGR2RGB)
            st.image(live_map_rgb, caption="Real-time intersection with 7 cameras and 3 traffic lights", width="stretch")
        
        with col2:
            st.subheader("📹 Camera Status")
            
            for camera in sim.cameras.values():
                with st.container():
                    st.markdown(f"**{camera.name}**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Vehicles", camera.vehicle_count)
                        st.metric("Queue", camera.queue_length)
                    with col_b:
                        st.metric("Speed", f"{camera.avg_speed:.1f}")
                        status = "🟢" if camera.vehicle_count > 0 else "⚪"
                        st.write(f"Status: {status}")
            
            st.subheader("🚦 Traffic Lights")
            for light in sim.traffic_lights.values():
                color_emoji = {"red": "🔴", "yellow": "🟡", "green": "🟢"}
                st.write(f"{light.id}: {color_emoji[light.state]} {light.state.upper()}")
        
        # Analytics dashboard
        create_analytics_dashboard(sim)
        
        # Auto-refresh for real-time updates with controlled rate
        time.sleep(1.0 / sim.update_frequency)
        st.rerun()
    
    else:
        # Show information when not running
        st.subheader("🎯 Simulation Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **📹 7 Strategic Cameras:**
            - North/South/East/West approaches
            - Center intersection monitor
            - Northeast corner coverage
            - Southwest corner coverage
            """)
        
        with col2:
            st.markdown("""
            **🚦 3 Traffic Signal System:**
            - North-South main signal
            - East-West cross signal  
            - Pedestrian crossing signal
            - Realistic timing cycles
            """)
        
        with col3:
            st.markdown("""
            **📊 Real-time Analytics:**
            - Vehicle counting & tracking
            - Queue length detection
            - Speed analysis
            - Traffic efficiency metrics
            """)
        
        # Show static map when stopped
        base_map = sim.generate_intersection_map()
        base_map_rgb = cv2.cvtColor(base_map, cv2.COLOR_BGR2RGB)
        st.image(base_map_rgb, caption="Intersection layout with camera positions and traffic lights")

if __name__ == "__main__":
    main()