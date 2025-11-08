# EdgeQI/Core/video/video_stream.py

import cv2
import numpy as np
import threading
import queue
import time
from typing import Optional, Callable, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

class StreamType(Enum):
    """Types of video streams supported"""
    WEBCAM = "webcam"
    IP_CAMERA = "ip_camera"
    FILE = "file"
    RTSP = "rtsp"
    USB_CAMERA = "usb_camera"

@dataclass
class StreamConfig:
    """Configuration for a video stream"""
    stream_id: str
    stream_type: StreamType
    source: str  # Can be file path, URL, camera index, etc.
    fps: int = 30
    resolution: Tuple[int, int] = (640, 480)  # (width, height)
    buffer_size: int = 10
    auto_restart: bool = True
    preprocessing: Dict = None

class VideoFrame:
    """Represents a video frame with metadata"""
    
    def __init__(self, frame: np.ndarray, timestamp: float, stream_id: str, frame_number: int):
        self.frame = frame
        self.timestamp = timestamp
        self.stream_id = stream_id
        self.frame_number = frame_number
        self.metadata = {}
    
    def add_metadata(self, key: str, value):
        """Add metadata to the frame"""
        self.metadata[key] = value
    
    def get_size(self) -> Tuple[int, int]:
        """Get frame dimensions (height, width)"""
        return self.frame.shape[:2]

class VideoStreamProcessor:
    """Handles video stream capture and processing"""
    
    def __init__(self, config: StreamConfig):
        self.config = config
        self.cap = None
        self.frame_queue = queue.Queue(maxsize=config.buffer_size)
        self.is_running = False
        self.capture_thread = None
        self.frame_count = 0
        self.start_time = time.time()
        self.last_frame_time = 0
        self.fps_counter = 0
        self.actual_fps = 0
        
        # Setup logging
        self.logger = logging.getLogger(f"VideoStream-{config.stream_id}")
        
        # Preprocessing functions
        self.preprocessors = []
        if config.preprocessing:
            self._setup_preprocessing(config.preprocessing)
    
    def _setup_preprocessing(self, preprocessing_config: Dict):
        """Setup preprocessing functions based on configuration"""
        if preprocessing_config.get('resize'):
            target_size = preprocessing_config['resize']
            self.preprocessors.append(lambda frame: cv2.resize(frame, target_size))
        
        if preprocessing_config.get('blur'):
            kernel_size = preprocessing_config['blur']
            self.preprocessors.append(lambda frame: cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0))
        
        if preprocessing_config.get('normalize'):
            self.preprocessors.append(lambda frame: frame.astype(np.float32) / 255.0)
        
        if preprocessing_config.get('grayscale'):
            self.preprocessors.append(lambda frame: cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    
    def _apply_preprocessing(self, frame: np.ndarray) -> np.ndarray:
        """Apply all preprocessing functions to a frame"""
        processed_frame = frame.copy()
        for preprocessor in self.preprocessors:
            processed_frame = preprocessor(processed_frame)
        return processed_frame
    
    def start(self) -> bool:
        """Start the video stream"""
        try:
            self.cap = self._create_capture()
            if not self.cap or not self.cap.isOpened():
                self.logger.error(f"Failed to open video source: {self.config.source}")
                return False
            
            # Set capture properties
            self._configure_capture()
            
            self.is_running = True
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            
            self.logger.info(f"Started video stream: {self.config.stream_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting video stream: {e}")
            return False
    
    def _create_capture(self) -> Optional[cv2.VideoCapture]:
        """Create appropriate VideoCapture object based on stream type"""
        try:
            if self.config.stream_type == StreamType.WEBCAM:
                return cv2.VideoCapture(int(self.config.source))
            elif self.config.stream_type == StreamType.USB_CAMERA:
                return cv2.VideoCapture(int(self.config.source))
            elif self.config.stream_type == StreamType.FILE:
                return cv2.VideoCapture(self.config.source)
            elif self.config.stream_type in [StreamType.IP_CAMERA, StreamType.RTSP]:
                return cv2.VideoCapture(self.config.source)
            else:
                self.logger.error(f"Unsupported stream type: {self.config.stream_type}")
                return None
        except Exception as e:
            self.logger.error(f"Error creating capture: {e}")
            return None
    
    def _configure_capture(self):
        """Configure capture properties"""
        if not self.cap:
            return
        
        try:
            # Set resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.resolution[1])
            
            # Set FPS for cameras (not files)
            if self.config.stream_type in [StreamType.WEBCAM, StreamType.USB_CAMERA, StreamType.IP_CAMERA]:
                self.cap.set(cv2.CAP_PROP_FPS, self.config.fps)
            
            # Set buffer size to reduce latency
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
        except Exception as e:
            self.logger.warning(f"Could not set capture properties: {e}")
    
    def _capture_loop(self):
        """Main capture loop running in separate thread"""
        frame_interval = 1.0 / self.config.fps
        
        while self.is_running:
            try:
                ret, frame = self.cap.read()
                
                if not ret:
                    if self.config.auto_restart and self.config.stream_type != StreamType.FILE:
                        self.logger.warning("Frame capture failed, attempting restart...")
                        self._restart_capture()
                        continue
                    else:
                        self.logger.info("End of stream or capture failed")
                        break
                
                # Apply preprocessing
                processed_frame = self._apply_preprocessing(frame)
                
                # Create VideoFrame object
                current_time = time.time()
                video_frame = VideoFrame(
                    frame=processed_frame,
                    timestamp=current_time,
                    stream_id=self.config.stream_id,
                    frame_number=self.frame_count
                )
                
                # Add frame to queue (non-blocking)
                try:
                    self.frame_queue.put_nowait(video_frame)
                except queue.Full:
                    # Remove oldest frame and add new one
                    try:
                        self.frame_queue.get_nowait()
                        self.frame_queue.put_nowait(video_frame)
                    except queue.Empty:
                        pass
                
                self.frame_count += 1
                self._update_fps_counter()
                
                # Control frame rate
                if self.config.stream_type != StreamType.FILE:
                    elapsed = time.time() - current_time
                    sleep_time = max(0, frame_interval - elapsed)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                
            except Exception as e:
                self.logger.error(f"Error in capture loop: {e}")
                if self.config.auto_restart:
                    time.sleep(1)  # Wait before retry
                else:
                    break
        
        self.logger.info(f"Capture loop ended for stream: {self.config.stream_id}")
    
    def _restart_capture(self):
        """Restart the video capture"""
        try:
            if self.cap:
                self.cap.release()
            
            time.sleep(2)  # Wait before restart
            self.cap = self._create_capture()
            
            if self.cap and self.cap.isOpened():
                self._configure_capture()
                self.logger.info("Video capture restarted successfully")
            else:
                self.logger.error("Failed to restart video capture")
                
        except Exception as e:
            self.logger.error(f"Error restarting capture: {e}")
    
    def _update_fps_counter(self):
        """Update FPS counter"""
        current_time = time.time()
        if current_time - self.last_frame_time >= 1.0:  # Update every second
            self.actual_fps = self.fps_counter
            self.fps_counter = 0
            self.last_frame_time = current_time
        else:
            self.fps_counter += 1
    
    def get_frame(self, timeout: float = 1.0) -> Optional[VideoFrame]:
        """Get the next frame from the queue"""
        try:
            return self.frame_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def get_latest_frame(self) -> Optional[VideoFrame]:
        """Get the most recent frame, discarding older ones"""
        latest_frame = None
        while True:
            try:
                latest_frame = self.frame_queue.get_nowait()
            except queue.Empty:
                break
        return latest_frame
    
    def get_stream_info(self) -> Dict:
        """Get information about the stream"""
        info = {
            'stream_id': self.config.stream_id,
            'stream_type': self.config.stream_type.value,
            'source': self.config.source,
            'is_running': self.is_running,
            'frame_count': self.frame_count,
            'actual_fps': self.actual_fps,
            'queue_size': self.frame_queue.qsize(),
            'uptime': time.time() - self.start_time
        }
        
        if self.cap:
            try:
                info.update({
                    'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                    'codec': int(self.cap.get(cv2.CAP_PROP_FOURCC))
                })
            except:
                pass
        
        return info
    
    def stop(self):
        """Stop the video stream"""
        self.is_running = False
        
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=2.0)
        
        if self.cap:
            self.cap.release()
        
        # Clear frame queue
        while not self.frame_queue.empty():
            try:
                self.frame_queue.get_nowait()
            except queue.Empty:
                break
        
        self.logger.info(f"Stopped video stream: {self.config.stream_id}")

class MultiStreamManager:
    """Manages multiple video streams simultaneously"""
    
    def __init__(self):
        self.streams: Dict[str, VideoStreamProcessor] = {}
        self.frame_callbacks: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger("MultiStreamManager")
    
    def add_stream(self, config: StreamConfig) -> bool:
        """Add a new video stream"""
        if config.stream_id in self.streams:
            self.logger.warning(f"Stream {config.stream_id} already exists")
            return False
        
        processor = VideoStreamProcessor(config)
        if processor.start():
            self.streams[config.stream_id] = processor
            self.frame_callbacks[config.stream_id] = []
            self.logger.info(f"Added stream: {config.stream_id}")
            return True
        else:
            self.logger.error(f"Failed to start stream: {config.stream_id}")
            return False
    
    def remove_stream(self, stream_id: str) -> bool:
        """Remove a video stream"""
        if stream_id not in self.streams:
            self.logger.warning(f"Stream {stream_id} not found")
            return False
        
        self.streams[stream_id].stop()
        del self.streams[stream_id]
        del self.frame_callbacks[stream_id]
        self.logger.info(f"Removed stream: {stream_id}")
        return True
    
    def add_frame_callback(self, stream_id: str, callback: Callable[[VideoFrame], None]):
        """Add a callback function to process frames from a specific stream"""
        if stream_id in self.frame_callbacks:
            self.frame_callbacks[stream_id].append(callback)
        else:
            self.logger.warning(f"Stream {stream_id} not found for callback")
    
    def get_frame(self, stream_id: str, timeout: float = 1.0) -> Optional[VideoFrame]:
        """Get frame from a specific stream"""
        if stream_id in self.streams:
            return self.streams[stream_id].get_frame(timeout)
        return None
    
    def get_latest_frames(self) -> Dict[str, VideoFrame]:
        """Get the latest frame from all streams"""
        frames = {}
        for stream_id, processor in self.streams.items():
            frame = processor.get_latest_frame()
            if frame:
                frames[stream_id] = frame
        return frames
    
    def get_stream_info(self, stream_id: Optional[str] = None) -> Dict:
        """Get information about streams"""
        if stream_id:
            if stream_id in self.streams:
                return self.streams[stream_id].get_stream_info()
            return {}
        else:
            return {sid: processor.get_stream_info() for sid, processor in self.streams.items()}
    
    def process_all_streams(self, processor_func: Callable[[str, VideoFrame], None]):
        """Process frames from all streams using a provided function"""
        while True:
            frames = self.get_latest_frames()
            if not frames:
                time.sleep(0.1)
                continue
            
            for stream_id, frame in frames.items():
                try:
                    processor_func(stream_id, frame)
                    
                    # Call registered callbacks
                    for callback in self.frame_callbacks.get(stream_id, []):
                        callback(frame)
                        
                except Exception as e:
                    self.logger.error(f"Error processing frame from {stream_id}: {e}")
    
    def stop_all(self):
        """Stop all video streams"""
        for stream_id in list(self.streams.keys()):
            self.remove_stream(stream_id)
        self.logger.info("Stopped all video streams")

# Utility functions for common stream configurations
def create_webcam_config(stream_id: str, camera_index: int = 0, fps: int = 30) -> StreamConfig:
    """Create configuration for webcam stream"""
    return StreamConfig(
        stream_id=stream_id,
        stream_type=StreamType.WEBCAM,
        source=str(camera_index),
        fps=fps
    )

def create_ip_camera_config(stream_id: str, url: str, fps: int = 30) -> StreamConfig:
    """Create configuration for IP camera stream"""
    return StreamConfig(
        stream_id=stream_id,
        stream_type=StreamType.IP_CAMERA,
        source=url,
        fps=fps
    )

def create_file_config(stream_id: str, file_path: str) -> StreamConfig:
    """Create configuration for video file stream"""
    return StreamConfig(
        stream_id=stream_id,
        stream_type=StreamType.FILE,
        source=file_path,
        auto_restart=False
    )

def create_rtsp_config(stream_id: str, rtsp_url: str, fps: int = 30) -> StreamConfig:
    """Create configuration for RTSP stream"""
    return StreamConfig(
        stream_id=stream_id,
        stream_type=StreamType.RTSP,
        source=rtsp_url,
        fps=fps
    )