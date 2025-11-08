"""
Adaptive Streaming Module for EDGE-QI Framework

Provides adaptive bitrate streaming for video and data transmission
with intelligent quality adjustment based on network conditions.
"""

import time
import threading
from enum import Enum
from typing import Dict, List, Optional, Callable, Tuple, Any
from dataclasses import dataclass
import numpy as np
import cv2


class StreamingProfile(Enum):
    """Available streaming profiles"""
    ULTRA_LOW = "ultra_low"      # 240p, high compression
    LOW = "low"                  # 360p, medium compression  
    MEDIUM = "medium"            # 480p, balanced
    HIGH = "high"                # 720p, good quality
    ULTRA_HIGH = "ultra_high"    # 1080p, best quality
    ADAPTIVE = "adaptive"        # Dynamic adjustment


@dataclass
class BitrateSettings:
    """Bitrate and quality settings for streaming"""
    target_bitrate: int          # Target bitrate in kbps
    max_bitrate: int            # Maximum allowed bitrate
    min_bitrate: int            # Minimum allowed bitrate
    resolution: Tuple[int, int]  # Width, height
    frame_rate: int             # Frames per second
    quality_factor: float       # Quality factor (0.0-1.0)
    buffer_size: int            # Buffer size in frames


@dataclass
class StreamingMetrics:
    """Streaming performance metrics"""
    current_bitrate: int
    actual_frame_rate: float
    buffer_health: float         # 0.0-1.0
    quality_score: float         # 0.0-1.0
    latency_ms: float
    packet_loss_rate: float
    bandwidth_utilization: float
    adaptation_count: int


class AdaptiveStreamer:
    """
    Adaptive bitrate streaming manager for video and data streams
    """
    
    def __init__(self, 
                 initial_profile: StreamingProfile = StreamingProfile.MEDIUM,
                 adaptation_interval: float = 2.0,
                 buffer_target: int = 30):
        """
        Initialize adaptive streamer
        
        Args:
            initial_profile: Starting streaming profile
            adaptation_interval: How often to check for adaptation (seconds)
            buffer_target: Target buffer size in frames
        """
        self.current_profile = initial_profile
        self.adaptation_interval = adaptation_interval
        self.buffer_target = buffer_target
        
        # Streaming profiles configuration
        self.profiles = {
            StreamingProfile.ULTRA_LOW: BitrateSettings(
                target_bitrate=150, max_bitrate=200, min_bitrate=100,
                resolution=(320, 240), frame_rate=15, quality_factor=0.3,
                buffer_size=15
            ),
            StreamingProfile.LOW: BitrateSettings(
                target_bitrate=300, max_bitrate=400, min_bitrate=200,
                resolution=(480, 360), frame_rate=20, quality_factor=0.5,
                buffer_size=20
            ),
            StreamingProfile.MEDIUM: BitrateSettings(
                target_bitrate=600, max_bitrate=800, min_bitrate=400,
                resolution=(640, 480), frame_rate=25, quality_factor=0.7,
                buffer_size=25
            ),
            StreamingProfile.HIGH: BitrateSettings(
                target_bitrate=1200, max_bitrate=1600, min_bitrate=800,
                resolution=(1280, 720), frame_rate=30, quality_factor=0.85,
                buffer_size=30
            ),
            StreamingProfile.ULTRA_HIGH: BitrateSettings(
                target_bitrate=2500, max_bitrate=3000, min_bitrate=1500,
                resolution=(1920, 1080), frame_rate=30, quality_factor=0.95,
                buffer_size=40
            )
        }
        
        # Streaming state
        self.is_streaming = False
        self.current_settings = self.profiles[initial_profile]
        self.frame_buffer = []
        self.buffer_lock = threading.Lock()
        
        # Metrics tracking
        self.metrics = StreamingMetrics(
            current_bitrate=self.current_settings.target_bitrate,
            actual_frame_rate=0.0,
            buffer_health=1.0,
            quality_score=self.current_settings.quality_factor,
            latency_ms=0.0,
            packet_loss_rate=0.0,
            bandwidth_utilization=0.0,
            adaptation_count=0
        )
        
        # Network condition tracking
        self.network_history = []
        self.last_adaptation = time.time()
        
        # Callbacks
        self.on_profile_change: Optional[Callable] = None
        self.on_metrics_update: Optional[Callable] = None
        
    def start_streaming(self, 
                       frame_source: Callable[[], np.ndarray],
                       output_callback: Callable[[bytes, Dict], None]):
        """
        Start adaptive streaming
        
        Args:
            frame_source: Function that returns video frames
            output_callback: Function to handle encoded stream output
        """
        self.is_streaming = True
        
        # Start streaming thread
        streaming_thread = threading.Thread(
            target=self._streaming_loop,
            args=(frame_source, output_callback)
        )
        streaming_thread.daemon = True
        streaming_thread.start()
        
        # Start adaptation monitoring
        adaptation_thread = threading.Thread(target=self._adaptation_loop)
        adaptation_thread.daemon = True
        adaptation_thread.start()
    
    def stop_streaming(self):
        """Stop adaptive streaming"""
        self.is_streaming = False
        
        # Clear buffer
        with self.buffer_lock:
            self.frame_buffer.clear()
    
    def _streaming_loop(self, frame_source: Callable, output_callback: Callable):
        """Main streaming loop"""
        frame_count = 0
        start_time = time.time()
        last_frame_time = start_time
        
        while self.is_streaming:
            try:
                # Get frame from source
                frame = frame_source()
                if frame is None:
                    time.sleep(0.01)
                    continue
                
                current_time = time.time()
                
                # Process frame according to current settings
                processed_frame = self._process_frame(frame)
                
                # Encode frame
                encoded_data, metadata = self._encode_frame(processed_frame)
                
                # Buffer management
                self._manage_buffer(encoded_data, metadata)
                
                # Send to output
                if encoded_data:
                    output_callback(encoded_data, metadata)
                
                # Update metrics
                frame_count += 1
                if current_time - last_frame_time >= 1.0:
                    self.metrics.actual_frame_rate = frame_count / (current_time - last_frame_time)
                    frame_count = 0
                    last_frame_time = current_time
                
                # Frame rate control
                target_interval = 1.0 / self.current_settings.frame_rate
                elapsed = time.time() - current_time
                if elapsed < target_interval:
                    time.sleep(target_interval - elapsed)
                    
            except Exception as e:
                print(f"Streaming error: {e}")
                time.sleep(0.1)
    
    def _adaptation_loop(self):
        """Background adaptation monitoring"""
        while self.is_streaming:
            try:
                # Check for adaptation conditions
                if time.time() - self.last_adaptation >= self.adaptation_interval:
                    self._check_adaptation_conditions()
                    self.last_adaptation = time.time()
                
                # Update metrics
                self._update_metrics()
                
                if self.on_metrics_update:
                    self.on_metrics_update(self.metrics)
                
                time.sleep(0.5)  # Check every 500ms
                
            except Exception as e:
                print(f"Adaptation error: {e}")
                time.sleep(1.0)
    
    def _process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process frame according to current streaming settings"""
        target_resolution = self.current_settings.resolution
        current_height, current_width = frame.shape[:2]
        
        # Resize if needed
        if (current_width, current_height) != target_resolution:
            frame = cv2.resize(frame, target_resolution, interpolation=cv2.INTER_AREA)
        
        # Apply quality factor (simulate compression artifacts)
        if self.current_settings.quality_factor < 1.0:
            # Simulate quality reduction
            quality_scale = max(0.1, self.current_settings.quality_factor)
            temp_size = (
                int(target_resolution[0] * quality_scale),
                int(target_resolution[1] * quality_scale)
            )
            
            # Downscale and upscale to simulate compression
            temp_frame = cv2.resize(frame, temp_size, interpolation=cv2.INTER_AREA)
            frame = cv2.resize(temp_frame, target_resolution, interpolation=cv2.INTER_LINEAR)
        
        return frame
    
    def _encode_frame(self, frame: np.ndarray) -> Tuple[bytes, Dict]:
        """Encode frame for streaming"""
        # Simulate encoding with JPEG compression
        encode_param = [cv2.IMWRITE_JPEG_QUALITY, 
                       int(self.current_settings.quality_factor * 100)]
        
        success, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
        
        if not success:
            return b'', {}
        
        # Calculate estimated bitrate
        frame_size_bits = len(encoded_frame) * 8
        estimated_bitrate = int(frame_size_bits * self.current_settings.frame_rate / 1000)
        
        metadata = {
            'timestamp': time.time(),
            'frame_size': len(encoded_frame),
            'estimated_bitrate': estimated_bitrate,
            'resolution': self.current_settings.resolution,
            'frame_rate': self.current_settings.frame_rate,
            'quality_factor': self.current_settings.quality_factor,
            'profile': self.current_profile.value
        }
        
        return encoded_frame.tobytes(), metadata
    
    def _manage_buffer(self, encoded_data: bytes, metadata: Dict):
        """Manage frame buffer for smooth streaming"""
        with self.buffer_lock:
            # Add to buffer
            self.frame_buffer.append({
                'data': encoded_data,
                'metadata': metadata,
                'timestamp': time.time()
            })
            
            # Remove old frames if buffer is too large
            while len(self.frame_buffer) > self.current_settings.buffer_size:
                self.frame_buffer.pop(0)
            
            # Update buffer health
            self.metrics.buffer_health = len(self.frame_buffer) / self.current_settings.buffer_size
    
    def _check_adaptation_conditions(self):
        """Check if streaming profile should be adapted"""
        # Simulate network conditions (in real implementation, this would use actual network metrics)
        current_bandwidth = self._estimate_available_bandwidth()
        buffer_health = self.metrics.buffer_health
        packet_loss = self._estimate_packet_loss()
        
        # Store network condition
        self.network_history.append({
            'timestamp': time.time(),
            'bandwidth': current_bandwidth,
            'buffer_health': buffer_health,
            'packet_loss': packet_loss
        })
        
        # Keep only recent history
        if len(self.network_history) > 10:
            self.network_history.pop(0)
        
        # Determine if adaptation is needed
        adaptation_needed = False
        new_profile = self.current_profile
        
        # Check for downgrade conditions
        if (buffer_health < 0.3 or 
            packet_loss > 0.05 or 
            current_bandwidth < self.current_settings.target_bitrate * 0.8):
            
            # Need to downgrade
            new_profile = self._get_lower_profile()
            adaptation_needed = True
            
        # Check for upgrade conditions  
        elif (buffer_health > 0.8 and 
              packet_loss < 0.01 and 
              current_bandwidth > self.current_settings.target_bitrate * 1.5):
            
            # Can upgrade
            new_profile = self._get_higher_profile()
            adaptation_needed = True
        
        # Apply adaptation
        if adaptation_needed and new_profile != self.current_profile:
            self._switch_profile(new_profile)
    
    def _estimate_available_bandwidth(self) -> int:
        """Estimate available bandwidth (simulated)"""
        # In real implementation, this would measure actual network bandwidth
        # For simulation, create realistic bandwidth variations
        base_bandwidth = 1000  # 1 Mbps base
        variation = np.random.normal(0, 200)  # +/- 200 kbps variation
        network_load = np.random.uniform(0.5, 1.5)  # Load factor
        
        estimated_bandwidth = max(100, int((base_bandwidth + variation) * network_load))
        return estimated_bandwidth
    
    def _estimate_packet_loss(self) -> float:
        """Estimate packet loss rate (simulated)"""
        # Simulate packet loss based on network conditions
        base_loss = 0.001  # 0.1% base loss
        congestion_factor = max(0, (self.metrics.current_bitrate - 800) / 1000)
        
        packet_loss = base_loss + congestion_factor * 0.02
        return min(0.1, max(0.0, packet_loss))
    
    def _get_lower_profile(self) -> StreamingProfile:
        """Get next lower quality profile"""
        profiles = [
            StreamingProfile.ULTRA_HIGH,
            StreamingProfile.HIGH,
            StreamingProfile.MEDIUM,
            StreamingProfile.LOW,
            StreamingProfile.ULTRA_LOW
        ]
        
        try:
            current_index = profiles.index(self.current_profile)
            if current_index < len(profiles) - 1:
                return profiles[current_index + 1]
        except ValueError:
            pass
        
        return StreamingProfile.LOW
    
    def _get_higher_profile(self) -> StreamingProfile:
        """Get next higher quality profile"""
        profiles = [
            StreamingProfile.ULTRA_LOW,
            StreamingProfile.LOW,
            StreamingProfile.MEDIUM,
            StreamingProfile.HIGH,
            StreamingProfile.ULTRA_HIGH
        ]
        
        try:
            current_index = profiles.index(self.current_profile)
            if current_index > 0:
                return profiles[current_index - 1]
        except ValueError:
            pass
        
        return StreamingProfile.MEDIUM
    
    def _switch_profile(self, new_profile: StreamingProfile):
        """Switch to new streaming profile"""
        old_profile = self.current_profile
        self.current_profile = new_profile
        self.current_settings = self.profiles[new_profile]
        
        # Update metrics
        self.metrics.current_bitrate = self.current_settings.target_bitrate
        self.metrics.quality_score = self.current_settings.quality_factor
        self.metrics.adaptation_count += 1
        
        print(f"Streaming profile changed: {old_profile.value} -> {new_profile.value}")
        
        # Notify callback
        if self.on_profile_change:
            self.on_profile_change(old_profile, new_profile, self.current_settings)
    
    def _update_metrics(self):
        """Update streaming metrics"""
        current_time = time.time()
        
        # Update bandwidth utilization
        if hasattr(self, 'last_bandwidth_check'):
            time_diff = current_time - self.last_bandwidth_check
            if time_diff > 0:
                # Calculate based on recent frame sizes
                recent_frames = [f for f in self.frame_buffer 
                               if current_time - f['timestamp'] < 1.0]
                
                if recent_frames:
                    total_bits = sum(len(f['data']) * 8 for f in recent_frames)
                    actual_bitrate = int(total_bits / len(recent_frames) * self.metrics.actual_frame_rate / 1000)
                    
                    self.metrics.bandwidth_utilization = (
                        actual_bitrate / max(self.current_settings.target_bitrate, 1)
                    )
        
        self.last_bandwidth_check = current_time
        
        # Update latency (simulated)
        self.metrics.latency_ms = np.random.uniform(10, 100)
        
        # Update packet loss
        self.metrics.packet_loss_rate = self._estimate_packet_loss()
    
    def get_current_settings(self) -> BitrateSettings:
        """Get current streaming settings"""
        return self.current_settings
    
    def get_metrics(self) -> StreamingMetrics:
        """Get current streaming metrics"""
        return self.metrics
    
    def set_profile(self, profile: StreamingProfile):
        """Manually set streaming profile"""
        if profile in self.profiles:
            self._switch_profile(profile)
    
    def get_available_profiles(self) -> List[StreamingProfile]:
        """Get list of available streaming profiles"""
        return list(self.profiles.keys())
    
    def estimate_bandwidth_requirement(self, profile: StreamingProfile) -> int:
        """Estimate bandwidth requirement for given profile"""
        if profile in self.profiles:
            return self.profiles[profile].target_bitrate
        return 600  # Default estimate
    
    def get_buffer_status(self) -> Dict[str, Any]:
        """Get current buffer status"""
        with self.buffer_lock:
            return {
                'buffer_size': len(self.frame_buffer),
                'buffer_capacity': self.current_settings.buffer_size,
                'buffer_health': self.metrics.buffer_health,
                'oldest_frame_age': (
                    time.time() - self.frame_buffer[0]['timestamp'] 
                    if self.frame_buffer else 0
                ),
                'newest_frame_age': (
                    time.time() - self.frame_buffer[-1]['timestamp']
                    if self.frame_buffer else 0
                )
            }
    
    def configure_adaptation(self, 
                           min_buffer_health: float = 0.3,
                           max_packet_loss: float = 0.05,
                           bandwidth_margin: float = 0.2):
        """
        Configure adaptation thresholds
        
        Args:
            min_buffer_health: Minimum buffer health before downgrading
            max_packet_loss: Maximum packet loss before downgrading  
            bandwidth_margin: Required bandwidth margin for upgrades
        """
        self.adaptation_config = {
            'min_buffer_health': min_buffer_health,
            'max_packet_loss': max_packet_loss,
            'bandwidth_margin': bandwidth_margin
        }