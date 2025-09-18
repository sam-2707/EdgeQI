# EdgeQI/ML/tasks/vision_task.py

import cv2
import numpy as np
from typing import Dict, Any, Optional
from .base_task import Task
from ..models.vision import YOLODetector, MobileNetDetector, Detection
from Core.queue import QueueDetector

class ComputerVisionTask(Task):
    """Computer vision task for object detection and counting"""
    
    def __init__(self, detector_type: str = "yolo", use_camera: bool = False, video_source: Optional[str] = None):
        super().__init__("ComputerVisionTask")
        self.detector_type = detector_type
        self.use_camera = use_camera
        self.video_source = video_source
        
        # Initialize detector
        if detector_type.lower() == "yolo":
            self.detector = YOLODetector()
        elif detector_type.lower() == "mobilenet":
            self.detector = MobileNetDetector()
        else:
            raise ValueError(f"Unsupported detector type: {detector_type}")
        
        # Initialize video capture
        self.cap = None
        if self.use_camera or self.video_source:
            self._init_video_capture()
    
    def _init_video_capture(self):
        """Initialize video capture from camera or file"""
        try:
            if self.use_camera:
                self.cap = cv2.VideoCapture(0)  # Default camera
                print("[VisionTask] Initialized camera capture")
            elif self.video_source:
                self.cap = cv2.VideoCapture(self.video_source)
                print(f"[VisionTask] Initialized video file capture: {self.video_source}")
            
            if self.cap and not self.cap.isOpened():
                print("[VisionTask] Warning: Could not open video source")
                self.cap = None
        except Exception as e:
            print(f"[VisionTask] Error initializing video capture: {e}")
            self.cap = None
    
    def _generate_dummy_frame(self) -> np.ndarray:
        """Generate a dummy frame for simulation"""
        # Create a simple synthetic frame
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Add some simple shapes to make it more realistic
        cv2.rectangle(frame, (50, 50), (150, 200), (100, 150, 200), -1)  # Person-like shape
        cv2.rectangle(frame, (300, 300), (500, 400), (50, 100, 150), -1)  # Vehicle-like shape
        
        return frame
    
    def run(self) -> Dict[str, Any]:
        """Run computer vision detection on current frame"""
        try:
            # Get frame from video source or generate dummy frame
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    print("[VisionTask] Could not read frame from video source")
                    frame = self._generate_dummy_frame()
            else:
                frame = self._generate_dummy_frame()
            
            # Perform object detection
            detections = self.detector.detect(frame)
            
            # Count objects
            people_count = self.detector.count_objects(detections, "person")
            vehicle_count = self.detector.count_objects(detections, "vehicle")
            
            # Extract detection details
            people_detections = self.detector.get_people_detections(detections)
            vehicle_detections = self.detector.get_vehicle_detections(detections)
            
            # Calculate frame metrics
            frame_height, frame_width = frame.shape[:2]
            
            result = {
                "timestamp": cv2.getTickCount() / cv2.getTickFrequency(),
                "frame_size": {"width": frame_width, "height": frame_height},
                "total_detections": len(detections),
                "people_count": people_count,
                "vehicle_count": vehicle_count,
                "detector_type": self.detector_type,
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
                ]
            }
            
            print(f"[VisionTask] Detected {people_count} people, {vehicle_count} vehicles")
            return result
            
        except Exception as e:
            print(f"[VisionTask] Error during detection: {e}")
            return {
                "error": str(e),
                "people_count": 0,
                "vehicle_count": 0,
                "detector_type": self.detector_type
            }
    
    def __del__(self):
        """Clean up video capture resources"""
        if self.cap:
            self.cap.release()

class QueueAnalysisTask(Task):
    """Advanced queue detection and analysis task using trajectory tracking"""
    
    def __init__(self, detector_type: str = "yolo"):
        super().__init__("QueueAnalysisTask")
        self.vision_task = ComputerVisionTask(detector_type)
        self.queue_detector = QueueDetector(clustering_threshold=60.0, min_queue_size=2)
        print(f"[QueueAnalysisTask] Initialized with {detector_type} detector and advanced queue tracking")
    
    def run(self) -> Dict[str, Any]:
        """Run advanced queue analysis with tracking"""
        # Get current frame detections
        vision_result = self.vision_task.run()
        
        if "error" in vision_result:
            return vision_result
        
        # Prepare detections for queue detector
        people_detections = []
        for person in vision_result.get("people_positions", []):
            people_detections.append({
                'center': person['center'],
                'bbox': person['bbox'],
                'confidence': person['confidence'],
                'class_name': 'person'
            })
        
        # Run advanced queue detection
        queue_analysis = self.queue_detector.detect_queues(people_detections)
        
        # Combine results
        result = {
            **vision_result,
            "advanced_queue_analysis": queue_analysis,
            "summary": self._generate_summary(queue_analysis)
        }
        
        # Log detailed results
        total_queues = queue_analysis.get('queue_metrics', {}).get('total_active_queues', 0)
        avg_wait = queue_analysis.get('queue_metrics', {}).get('estimated_wait_time', 0)
        print(f"[QueueAnalysisTask] Detected {total_queues} active queues, avg wait time: {avg_wait:.1f}s")
        
        return result
    
    def _generate_summary(self, queue_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a human-readable summary of queue analysis"""
        metrics = queue_analysis.get('queue_metrics', {})
        clusters = queue_analysis.get('queue_clusters', [])
        
        # Count different types of formations
        active_queues = [c for c in clusters if c.get('is_queue', False)]
        crowd_formations = [c for c in clusters if not c.get('is_queue', False)]
        
        # Calculate total people in queues vs crowds
        people_in_queues = sum(q.get('queue_length', 0) for q in active_queues)
        people_in_crowds = sum(c.get('queue_length', 0) for c in crowd_formations)
        
        return {
            'status': self._determine_status(metrics, len(active_queues)),
            'active_queues': len(active_queues),
            'crowd_formations': len(crowd_formations),
            'people_in_queues': people_in_queues,
            'people_in_crowds': people_in_crowds,
            'average_wait_time': round(metrics.get('estimated_wait_time', 0), 1),
            'queue_efficiency': metrics.get('queue_efficiency', 0),
            'congestion_level': self._assess_congestion(queue_analysis)
        }
    
    def _determine_status(self, metrics: Dict, num_queues: int) -> str:
        """Determine overall queue status"""
        wait_time = metrics.get('estimated_wait_time', 0)
        efficiency = metrics.get('queue_efficiency', 1.0)
        
        if num_queues == 0:
            return "normal"
        elif wait_time > 300:  # 5 minutes
            return "critical"
        elif wait_time > 120 or efficiency < 0.5:  # 2 minutes or low efficiency
            return "warning"
        else:
            return "optimal"
    
    def _assess_congestion(self, queue_analysis: Dict) -> str:
        """Assess overall congestion level"""
        total_people = queue_analysis.get('total_people', 0)
        metrics = queue_analysis.get('queue_metrics', {})
        stationary_pct = metrics.get('stationary_percentage', 0)
        
        if total_people > 20 and stationary_pct > 80:
            return "high"
        elif total_people > 10 or stationary_pct > 60:
            return "medium"
        else:
            return "low"