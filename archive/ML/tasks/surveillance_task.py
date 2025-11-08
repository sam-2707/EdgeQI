# EdgeQI/ML/tasks/surveillance_task.py

import time
import cv2
from typing import Dict, Any, Optional, List
from .base_task import Task
from ..models.vision import YOLODetector, MobileNetDetector
from Core.queue import QueueDetector
from Core.video import MultiStreamManager, VideoFrame, create_webcam_config, create_file_config

class SurveillanceTask(Task):
    """Advanced surveillance task with multi-stream video processing"""
    
    def __init__(self, detector_type: str = "yolo", stream_configs: List[Dict] = None):
        super().__init__("SurveillanceTask")
        
        # Initialize computer vision detector
        if detector_type.lower() == "yolo":
            self.detector = YOLODetector()
        elif detector_type.lower() == "mobilenet":
            self.detector = MobileNetDetector()
        else:
            raise ValueError(f"Unsupported detector type: {detector_type}")
        
        # Initialize queue detector
        self.queue_detector = QueueDetector(clustering_threshold=60.0, min_queue_size=2)
        
        # Initialize multi-stream manager
        self.stream_manager = MultiStreamManager()
        
        # Setup default streams if none provided
        if not stream_configs:
            stream_configs = [
                {"type": "webcam", "id": "cam_1", "source": 0},
                # Add more default configs as needed
            ]
        
        # Add configured streams
        self._setup_streams(stream_configs)
        
        # Store recent results for analysis
        self.recent_results = {}
        self.analysis_history = []
        
        print(f"[SurveillanceTask] Initialized with {detector_type} detector and {len(stream_configs)} streams")
    
    def _setup_streams(self, stream_configs: List[Dict]):
        """Setup video streams based on configuration"""
        for config in stream_configs:
            try:
                if config["type"] == "webcam":
                    stream_config = create_webcam_config(
                        stream_id=config["id"],
                        camera_index=config.get("source", 0),
                        fps=config.get("fps", 30)
                    )
                elif config["type"] == "file":
                    stream_config = create_file_config(
                        stream_id=config["id"],
                        file_path=config["source"]
                    )
                else:
                    print(f"[SurveillanceTask] Unsupported stream type: {config['type']}")
                    continue
                
                success = self.stream_manager.add_stream(stream_config)
                if success:
                    print(f"[SurveillanceTask] Added stream: {config['id']}")
                else:
                    print(f"[SurveillanceTask] Failed to add stream: {config['id']}")
                    
            except Exception as e:
                print(f"[SurveillanceTask] Error setting up stream {config.get('id', 'unknown')}: {e}")
    
    def run(self) -> Dict[str, Any]:
        """Run surveillance analysis on all active streams"""
        try:
            # Get latest frames from all streams
            latest_frames = self.stream_manager.get_latest_frames()
            
            if not latest_frames:
                return {
                    "error": "No frames available from any stream",
                    "active_streams": 0,
                    "timestamp": time.time()
                }
            
            # Process each stream
            stream_results = {}
            overall_metrics = {
                "total_people": 0,
                "total_vehicles": 0,
                "total_queues": 0,
                "active_streams": len(latest_frames),
                "alert_level": "normal"
            }
            
            for stream_id, frame in latest_frames.items():
                stream_result = self._process_frame(stream_id, frame)
                stream_results[stream_id] = stream_result
                
                # Aggregate metrics
                if "error" not in stream_result:
                    overall_metrics["total_people"] += stream_result.get("people_count", 0)
                    overall_metrics["total_vehicles"] += stream_result.get("vehicle_count", 0)
                    
                    queue_analysis = stream_result.get("advanced_queue_analysis", {})
                    queue_metrics = queue_analysis.get("queue_metrics", {})
                    overall_metrics["total_queues"] += queue_metrics.get("total_active_queues", 0)
            
            # Determine overall alert level
            overall_metrics["alert_level"] = self._determine_alert_level(stream_results)
            
            # Store results for history
            self._update_history(stream_results, overall_metrics)
            
            result = {
                "stream_results": stream_results,
                "overall_metrics": overall_metrics,
                "stream_info": self.stream_manager.get_stream_info(),
                "timestamp": time.time(),
                "system_status": self._get_system_status()
            }
            
            print(f"[SurveillanceTask] Processed {len(latest_frames)} streams - "
                  f"People: {overall_metrics['total_people']}, "
                  f"Vehicles: {overall_metrics['total_vehicles']}, "
                  f"Queues: {overall_metrics['total_queues']}")
            
            return result
            
        except Exception as e:
            print(f"[SurveillanceTask] Error during surveillance processing: {e}")
            return {
                "error": str(e),
                "timestamp": time.time()
            }
    
    def _process_frame(self, stream_id: str, frame: VideoFrame) -> Dict[str, Any]:
        """Process a single frame from a stream"""
        try:
            # Run object detection
            detections = self.detector.detect(frame.frame)
            
            # Count objects
            people_count = self.detector.count_objects(detections, "person")
            vehicle_count = self.detector.count_objects(detections, "vehicle")
            
            # Extract detection details
            people_detections = self.detector.get_people_detections(detections)
            vehicle_detections = self.detector.get_vehicle_detections(detections)
            
            # Prepare detections for queue analysis
            people_for_queue = []
            for person in people_detections:
                people_for_queue.append({
                    'center': person.center,
                    'bbox': person.bbox,
                    'confidence': person.confidence,
                    'class_name': 'person'
                })
            
            # Run queue detection
            queue_analysis = self.queue_detector.detect_queues(people_for_queue)
            
            # Calculate frame-specific metrics
            frame_height, frame_width = frame.get_size()
            
            result = {
                "stream_id": stream_id,
                "frame_info": {
                    "timestamp": frame.timestamp,
                    "frame_number": frame.frame_number,
                    "size": {"width": frame_width, "height": frame_height}
                },
                "detection_summary": {
                    "total_detections": len(detections),
                    "people_count": people_count,
                    "vehicle_count": vehicle_count,
                    "detector_type": self.detector.model_type if hasattr(self.detector, 'model_type') else "unknown"
                },
                "people_positions": [
                    {
                        "center": det.center,
                        "bbox": det.bbox,
                        "confidence": det.confidence
                    } for det in people_detections
                ],
                "vehicle_positions": [
                    {
                        "center": det.center,
                        "bbox": det.bbox,
                        "confidence": det.confidence,
                        "type": det.class_name
                    } for det in vehicle_detections
                ],
                "advanced_queue_analysis": queue_analysis,
                "stream_quality": self._assess_stream_quality(frame, detections)
            }
            
            return result
            
        except Exception as e:
            return {
                "stream_id": stream_id,
                "error": str(e),
                "timestamp": frame.timestamp if frame else time.time()
            }
    
    def _assess_stream_quality(self, frame: VideoFrame, detections: List) -> Dict[str, Any]:
        """Assess the quality of the video stream"""
        frame_data = frame.frame
        
        # Calculate basic image quality metrics
        if len(frame_data.shape) == 3:
            # Color image
            gray = cv2.cvtColor(frame_data, cv2.COLOR_BGR2GRAY) if 'cv2' in globals() else frame_data
        else:
            gray = frame_data
        
        # Simple brightness and contrast measures
        mean_brightness = float(gray.mean()) if hasattr(gray, 'mean') else 128.0
        brightness_std = float(gray.std()) if hasattr(gray, 'std') else 50.0
        
        # Detection confidence as quality indicator
        if detections:
            avg_confidence = sum(det.confidence for det in detections) / len(detections)
        else:
            avg_confidence = 0.0
        
        # Determine quality level
        if mean_brightness < 50 or brightness_std < 20:
            quality_level = "poor"
        elif mean_brightness > 200 or brightness_std > 80:
            quality_level = "good"
        else:
            quality_level = "fair"
        
        return {
            "quality_level": quality_level,
            "brightness": round(mean_brightness, 2),
            "contrast": round(brightness_std, 2),
            "detection_confidence": round(avg_confidence, 3),
            "frame_size": frame.get_size()
        }
    
    def _determine_alert_level(self, stream_results: Dict[str, Dict]) -> str:
        """Determine overall alert level based on all streams"""
        alert_levels = []
        
        for stream_id, result in stream_results.items():
            if "error" in result:
                alert_levels.append("warning")
                continue
            
            people_count = result.get("detection_summary", {}).get("people_count", 0)
            queue_analysis = result.get("advanced_queue_analysis", {})
            queue_metrics = queue_analysis.get("queue_metrics", {})
            
            wait_time = queue_metrics.get("estimated_wait_time", 0)
            total_queues = queue_metrics.get("total_active_queues", 0)
            
            # Determine alert level for this stream
            if people_count > 20 or wait_time > 300 or total_queues > 3:
                alert_levels.append("critical")
            elif people_count > 10 or wait_time > 120 or total_queues > 1:
                alert_levels.append("warning")
            else:
                alert_levels.append("normal")
        
        # Return highest alert level
        if "critical" in alert_levels:
            return "critical"
        elif "warning" in alert_levels:
            return "warning"
        else:
            return "normal"
    
    def _update_history(self, stream_results: Dict, overall_metrics: Dict):
        """Update analysis history for trend detection"""
        history_entry = {
            "timestamp": time.time(),
            "overall_metrics": overall_metrics.copy(),
            "stream_count": len(stream_results)
        }
        
        self.analysis_history.append(history_entry)
        
        # Keep only last 100 entries
        if len(self.analysis_history) > 100:
            self.analysis_history.pop(0)
    
    def _get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            "streams_active": len(self.stream_manager.streams),
            "total_frames_processed": sum(
                info.get("frame_count", 0) 
                for info in self.stream_manager.get_stream_info().values()
            ),
            "uptime": time.time() - getattr(self, '_start_time', time.time()),
            "memory_usage": "N/A",  # Could implement actual memory monitoring
            "history_length": len(self.analysis_history)
        }
    
    def get_stream_statistics(self) -> Dict[str, Any]:
        """Get detailed statistics about stream performance"""
        if not self.analysis_history:
            return {"error": "No analysis history available"}
        
        recent_entries = self.analysis_history[-10:]  # Last 10 entries
        
        # Calculate averages
        avg_people = sum(entry["overall_metrics"]["total_people"] for entry in recent_entries) / len(recent_entries)
        avg_vehicles = sum(entry["overall_metrics"]["total_vehicles"] for entry in recent_entries) / len(recent_entries)
        avg_queues = sum(entry["overall_metrics"]["total_queues"] for entry in recent_entries) / len(recent_entries)
        
        return {
            "recent_averages": {
                "people": round(avg_people, 1),
                "vehicles": round(avg_vehicles, 1),
                "queues": round(avg_queues, 1)
            },
            "stream_info": self.stream_manager.get_stream_info(),
            "alert_frequency": {
                level: sum(1 for entry in recent_entries if entry["overall_metrics"]["alert_level"] == level)
                for level in ["normal", "warning", "critical"]
            }
        }
    
    def stop(self):
        """Stop all video streams and cleanup"""
        self.stream_manager.stop_all()
        print("[SurveillanceTask] Stopped all surveillance streams")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        if hasattr(self, 'stream_manager'):
            self.stream_manager.stop_all()