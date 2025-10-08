"""
Ultra-Optimized Traffic Simulation - Maximum FPS

Extreme performance optimizations:
- Minimal resolution (640x360)
- Pre-computed graphics elements
- Efficient data structures
- Optimized rendering pipeline
- Target: 30+ FPS
"""

import streamlit as st
import cv2
import numpy as np
import time
import sys
import os
from typing import Dict, List, Optional

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Core.simulation.realtime_simulator import RealTimeDataSimulator

# Configure Streamlit page
st.set_page_config(
    page_title="⚡ Ultra-Fast Traffic",
    page_icon="⚡",
    layout="wide"
)

# Performance-focused session state
if 'ultra_simulator' not in st.session_state:
    st.session_state.ultra_simulator = None
if 'ultra_running' not in st.session_state:
    st.session_state.ultra_running = False
if 'frame_counter' not in st.session_state:
    st.session_state.frame_counter = 0
if 'last_fps_time' not in st.session_state:
    st.session_state.last_fps_time = time.time()
if 'fps_samples' not in st.session_state:
    st.session_state.fps_samples = []

class UltraFastTrafficSimulation:
    """Ultra-optimized traffic simulation for maximum FPS"""
    
    def __init__(self):
        # Ultra-small resolution for maximum speed
        self.width = 640
        self.height = 360
        
        # Pre-computed graphics elements
        self.road_overlay = None
        self.info_background = None
        
        # Optimized colors (pre-defined)
        self.colors = {
            'road': (80, 80, 80),
            'lane': (255, 255, 255),
            'vehicle_fast': (0, 255, 0),
            'vehicle_slow': (0, 0, 255),
            'text': (255, 255, 255),
            'background': (0, 0, 0)
        }
        
        # Performance tracking
        self.last_render_time = 0
        self.render_interval = 1.0 / 30  # Target 30 FPS
        
        self.setup_graphics()
    
    def setup_graphics(self):
        """Pre-compute static graphics elements"""
        # Pre-compute road overlay
        self.road_overlay = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Draw roads once
        cv2.rectangle(self.road_overlay, (0, self.height//2 - 20), 
                     (self.width, self.height//2 + 20), self.colors['road'], -1)
        cv2.rectangle(self.road_overlay, (self.width//2 - 20, 0), 
                     (self.width//2 + 20, self.height), self.colors['road'], -1)
        
        # Lane markers
        cv2.line(self.road_overlay, (0, self.height//2), 
                (self.width, self.height//2), self.colors['lane'], 1)
        cv2.line(self.road_overlay, (self.width//2, 0), 
                (self.width//2, self.height), self.colors['lane'], 1)
        
        # Pre-compute info background
        self.info_background = np.zeros((60, 300, 3), dtype=np.uint8)
    
    def setup_simulator(self):
        """Setup ultra-fast simulator"""
        if st.session_state.ultra_simulator is None:
            st.session_state.ultra_simulator = RealTimeDataSimulator(
                width=self.width,
                height=self.height,
                fps=30  # High target FPS
            )
            # Minimal traffic for maximum performance
            st.session_state.ultra_simulator.set_traffic_density(0.2)
    
    def start_simulation(self):
        """Start ultra-fast simulation"""
        if not st.session_state.ultra_running:
            self.setup_simulator()
            st.session_state.ultra_simulator.start_simulation()
            st.session_state.ultra_running = True
            st.session_state.frame_counter = 0
            st.session_state.fps_samples = []
            return True
        return False
    
    def stop_simulation(self):
        """Stop simulation"""
        if st.session_state.ultra_running:
            if st.session_state.ultra_simulator:
                st.session_state.ultra_simulator.stop_simulation()
            st.session_state.ultra_running = False
            return True
        return False
    
    def get_ultra_fast_frame(self):
        """Get frame with maximum performance optimizations"""
        current_time = time.time()
        
        # Frame rate limiting for consistent performance
        if current_time - self.last_render_time < self.render_interval:
            return None, {}
        
        if not st.session_state.ultra_simulator:
            return None, {}
        
        # Get frame data
        frame_data = st.session_state.ultra_simulator.get_latest_frame()
        if not frame_data:
            return None, {}
        
        frame = frame_data['frame']
        
        # Get minimal detection data
        detection_data = st.session_state.ultra_simulator.get_latest_detections()
        detections = detection_data.get('detections', []) if detection_data else []
        
        # Ultra-fast annotation
        annotated = self.ultra_fast_annotate(frame, detections)
        
        # Update counters
        st.session_state.frame_counter += 1
        self.last_render_time = current_time
        
        # FPS calculation (optimized)
        st.session_state.fps_samples.append(current_time)
        if len(st.session_state.fps_samples) > 10:
            st.session_state.fps_samples.pop(0)
        
        stats = {
            'vehicle_count': min(len(detections), 8),  # Limit displayed count
            'frame_count': st.session_state.frame_counter,
            'fps': self.calculate_fps()
        }
        
        return annotated, stats
    
    def ultra_fast_annotate(self, frame: np.ndarray, detections: List) -> np.ndarray:
        """Ultra-fast frame annotation with minimal operations"""
        # Start with pre-computed road overlay
        annotated = cv2.add(frame, self.road_overlay)
        
        # Draw only first 8 vehicles for performance
        vehicle_count = 0
        for detection in detections[:8]:
            if detection.get('confidence', 0) > 0.7:  # Higher threshold
                bbox = detection.get('bbox', [0, 0, 0, 0])
                x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                
                # Ultra-simple vehicle representation (just rectangles)
                speed = detection.get('speed', 0)
                color = self.colors['vehicle_fast'] if speed > 15 else self.colors['vehicle_slow']
                
                # Single rectangle draw (no labels for speed)
                cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)
                vehicle_count += 1
        
        # Minimal info overlay
        fps = self.calculate_fps()
        info_text = f"V:{vehicle_count} FPS:{fps:.0f} F:{st.session_state.frame_counter}"
        cv2.putText(annotated, info_text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                   self.colors['text'], 1)
        
        return annotated
    
    def calculate_fps(self) -> float:
        """Optimized FPS calculation"""
        if len(st.session_state.fps_samples) < 2:
            return 0.0
        
        time_span = st.session_state.fps_samples[-1] - st.session_state.fps_samples[0]
        if time_span <= 0:
            return 0.0
        
        return (len(st.session_state.fps_samples) - 1) / time_span


def main():
    """Ultra-performance main application"""
    st.title("⚡ Ultra-Fast Traffic Simulation")
    st.markdown("**Maximum performance optimization - Target: 30+ FPS**")
    
    # Initialize simulation
    sim = UltraFastTrafficSimulation()
    
    # Minimal UI for maximum performance
    col1, col2, col3, col4 = st.columns([1, 1, 2, 2])
    
    with col1:
        if st.button("⚡ Ultra Start", disabled=st.session_state.ultra_running):
            if sim.start_simulation():
                st.success("⚡ Ultra-fast mode!")
                st.rerun()
    
    with col2:
        if st.button("⏹️ Stop", disabled=not st.session_state.ultra_running):
            if sim.stop_simulation():
                st.success("Stopped")
                st.rerun()
    
    with col3:
        # Performance mode selector
        perf_mode = st.selectbox("Performance Mode", 
                                ["⚡ Ultra (0.1s)", "🏎️ High (0.2s)", "⚖️ Balanced (0.5s)"],
                                index=0)
        refresh_times = {"⚡ Ultra (0.1s)": 0.1, "🏎️ High (0.2s)": 0.2, "⚖️ Balanced (0.5s)": 0.5}
        refresh_time = refresh_times[perf_mode]
    
    with col4:
        if st.session_state.ultra_running:
            stats = {'fps': sim.calculate_fps(), 'frame_count': st.session_state.frame_counter}
            fps = stats['fps']
            if fps >= 25:
                st.success(f"🟢 EXCELLENT: {fps:.1f} FPS")
            elif fps >= 20:
                st.warning(f"🟡 GOOD: {fps:.1f} FPS")
            else:
                st.error(f"🔴 LOW: {fps:.1f} FPS")
    
    if st.session_state.ultra_running:
        # Get ultra-fast frame
        frame, stats = sim.get_ultra_fast_frame()
        
        if frame is not None:
            # Display with minimal UI overhead
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.subheader("⚡ Ultra-Fast Traffic (640x360)")
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                st.image(frame_rgb, caption=f"Ultra-Performance @ {stats['fps']:.1f} FPS", 
                        width="stretch")
            
            with col2:
                st.subheader("📊 Ultra Stats")
                
                # Performance indicator
                fps = stats['fps']
                if fps >= 30:
                    st.success("🚀 ULTRA FAST!")
                elif fps >= 25:
                    st.success("⚡ EXCELLENT")
                elif fps >= 20:
                    st.warning("🏎️ GOOD")
                elif fps >= 15:
                    st.warning("⚖️ OK")
                else:
                    st.error("🐌 SLOW")
                
                # Minimal stats
                st.metric("FPS", f"{fps:.1f}")
                st.metric("Cars", stats['vehicle_count'])
                st.metric("Frames", stats['frame_count'])
                
                # Optimization level
                st.markdown("**🔧 Optimizations:**")
                st.markdown("✅ 640x360 resolution")
                st.markdown("✅ Max 8 vehicles")
                st.markdown("✅ Pre-computed graphics")
                st.markdown("✅ Frame rate limiting")
                st.markdown("✅ Minimal UI overhead")
        else:
            st.info("⚡ Processing ultra-fast frames...")
        
        # Ultra-fast auto-refresh
        time.sleep(refresh_time)
        st.rerun()
    
    else:
        # Performance information
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("⚡ Ultra Optimizations")
            st.markdown("""
            **🎯 Target: 30+ FPS**
            - 640x360 resolution (40% smaller)
            - Max 8 vehicles displayed  
            - Pre-computed road graphics
            - Frame rate limiting (30 FPS)
            - Minimal text overlays
            """)
        
        with col2:
            st.subheader("🚀 Performance Features")
            st.markdown("""
            **Speed Optimizations:**
            - Single-pass rendering
            - Efficient color pre-computation
            - Optimized FPS calculation
            - Reduced detection processing
            - Streamlined data structures
            """)
        
        with col3:
            st.subheader("📊 Expected Results")
            st.markdown("""
            **Performance Targets:**
            - 🚀 Ultra Fast: 30+ FPS
            - ⚡ Excellent: 25-30 FPS
            - 🏎️ Good: 20-25 FPS
            - ⚖️ OK: 15-20 FPS
            - 🐌 Needs work: <15 FPS
            """)
        
        st.info("⚡ Click 'Ultra Start' for maximum performance traffic simulation!")
        
        # Performance tips
        with st.expander("🔧 Additional Performance Tips"):
            st.markdown("""
            **For even better performance:**
            1. **Close other browser tabs** - Free up memory
            2. **Use Chrome or Edge** - Better WebGL performance  
            3. **Reduce browser zoom** - Less rendering overhead
            4. **Close other applications** - More CPU for simulation
            5. **Use 'Ultra' refresh mode** - Fastest updates (0.1s)
            
            **System requirements:**
            - CPU: 2+ cores recommended
            - RAM: 4GB+ available
            - Browser: Chrome/Edge preferred
            """)


if __name__ == "__main__":
    main()