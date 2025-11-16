"""
EDGE-QI Real-Time Detection Service
Integrates YOLOv8 with backend for live object detection
"""

import cv2
import torch
import numpy as np
from typing import List, Dict, Optional, Callable
import asyncio
from datetime import datetime
import logging
from pathlib import Path

# Try to import YOLO, fallback to mock if not available
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️  ultralytics not installed. Install with: pip install ultralytics")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YOLODetectionService:
    """Real-time YOLOv8 detection service for edge devices"""
    
    # VisDrone class names (trained dataset)
    VISDRONE_CLASSES = {
        0: 'pedestrian',
        1: 'people', 
        2: 'bicycle',
        3: 'car',
        4: 'van',
        5: 'truck',
        6: 'tricycle',
        7: 'awning-tricycle',
        8: 'bus',
        9: 'motor'
    }
    
    def __init__(self, 
                 model_path: str = "yolov8n.pt",
                 device: str = "auto",
                 conf_threshold: float = 0.25,
                 iou_threshold: float = 0.45):
        """
        Initialize YOLOv8 detection service
        
        Args:
            model_path: Path to YOLOv8 weights (e.g., 'yolov8n.pt', 'ML/models/trained/yolov8n.pt')
            device: 'cuda', 'cpu', 'mps', or 'auto' (auto-detect)
            conf_threshold: Minimum confidence for detections (0.0-1.0)
            iou_threshold: IoU threshold for NMS
        """
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.model = None
        self.device = self._select_device(device)
        
        # Statistics
        self.stats = {
            'total_frames': 0,
            'total_detections': 0,
            'fps': 0.0,
            'avg_inference_time': 0.0
        }
        
        # Load model
        self._load_model(model_path)
    
    def _select_device(self, device: str) -> str:
        """Auto-detect best available device"""
        if device == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return "mps"  # Apple Silicon
            else:
                return "cpu"
        return device
    
    def _load_model(self, model_path: str):
        """Load YOLOv8 model"""
        if not YOLO_AVAILABLE:
            logger.error("❌ ultralytics not installed. Cannot load YOLO model.")
            logger.info("Install with: pip install ultralytics")
            return
        
        try:
            # Check if model exists
            if not Path(model_path).exists() and not model_path.startswith('yolov8'):
                logger.warning(f"⚠️  Model not found at {model_path}, using yolov8n.pt")
                model_path = "yolov8n.pt"
            
            self.model = YOLO(model_path)
            self.model.to(self.device)
            
            # Enable FP16 for CUDA
            if self.device == "cuda":
                self.model.half()
            
            logger.info(f"✅ YOLOv8 model loaded successfully on {self.device}")
            logger.info(f"   Model: {model_path}")
            logger.info(f"   Confidence: {self.conf_threshold}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            self.model = None
    
    def detect_frame(self, 
                    frame: np.ndarray, 
                    conf: Optional[float] = None) -> List[Dict]:
        """
        Run detection on a single frame
        
        Args:
            frame: Input image (BGR format, numpy array)
            conf: Optional confidence override
            
        Returns:
            List of detection dictionaries with bbox, confidence, class info
        """
        if self.model is None:
            return self._generate_mock_detections(frame)
        
        conf = conf or self.conf_threshold
        
        try:
            import time
            start_time = time.time()
            
            # Run inference
            results = self.model(
                frame, 
                conf=conf,
                iou=self.iou_threshold,
                verbose=False,
                imgsz=640  # Input size
            )[0]
            
            inference_time = time.time() - start_time
            
            # Parse results
            detections = []
            for box in results.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                
                # Get class name
                class_name = self.VISDRONE_CLASSES.get(class_id, f"class_{class_id}")
                
                detection = {
                    "bbox": {
                        "x": int(x1),
                        "y": int(y1),
                        "width": int(x2 - x1),
                        "height": int(y2 - y1)
                    },
                    "center": {
                        "x": int((x1 + x2) / 2),
                        "y": int((y1 + y2) / 2)
                    },
                    "confidence": round(confidence, 2),
                    "class_id": class_id,
                    "class_name": class_name,
                    "timestamp": datetime.utcnow().isoformat()
                }
                detections.append(detection)
            
            # Update stats
            self.stats['total_frames'] += 1
            self.stats['total_detections'] += len(detections)
            self.stats['avg_inference_time'] = (
                (self.stats['avg_inference_time'] * (self.stats['total_frames'] - 1) + inference_time) 
                / self.stats['total_frames']
            )
            self.stats['fps'] = 1.0 / inference_time if inference_time > 0 else 0
            
            return detections
            
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return []
    
    def _generate_mock_detections(self, frame: np.ndarray) -> List[Dict]:
        """Generate mock detections if model not available"""
        import random
        
        h, w = frame.shape[:2]
        num_objects = random.randint(2, 8)
        
        detections = []
        for i in range(num_objects):
            x = random.randint(50, w - 150)
            y = random.randint(50, h - 150)
            width = random.randint(60, 120)
            height = random.randint(40, 80)
            
            detections.append({
                "bbox": {"x": x, "y": y, "width": width, "height": height},
                "center": {"x": x + width // 2, "y": y + height // 2},
                "confidence": round(random.uniform(0.3, 0.95), 2),
                "class_id": random.choice([3, 0, 2]),  # car, person, bicycle
                "class_name": random.choice(['car', 'pedestrian', 'bicycle']),
                "timestamp": datetime.utcnow().isoformat()
            })
        
        return detections
    
    async def process_video_stream(self,
                                   source: str,
                                   callback: Callable,
                                   target_fps: int = 5,
                                   node_id: str = "edge-node-1"):
        """
        Process video stream continuously
        
        Args:
            source: Camera index (0, 1), video file path, or RTSP URL
            callback: Async function called with (frame, detections, frame_count)
            target_fps: Target processing FPS (actual camera FPS may be higher)
            node_id: Identifier for this edge node
        """
        cap = None
        try:
            # Open video source
            if isinstance(source, int) or source.isdigit():
                cap = cv2.VideoCapture(int(source))
            else:
                cap = cv2.VideoCapture(source)
            
            if not cap.isOpened():
                logger.error(f"❌ Cannot open video source: {source}")
                return
            
            # Get actual camera FPS
            camera_fps = cap.get(cv2.CAP_PROP_FPS)
            if camera_fps == 0:
                camera_fps = 30  # Default
            
            # Calculate frame skip for target FPS
            frame_skip = max(1, int(camera_fps / target_fps))
            
            logger.info(f"✅ Video stream opened: {source}")
            logger.info(f"   Camera FPS: {camera_fps}")
            logger.info(f"   Processing every {frame_skip} frames for {target_fps} FPS")
            
            frame_count = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    logger.warning("End of stream or read error")
                    break
                
                frame_count += 1
                
                # Process every Nth frame
                if frame_count % frame_skip == 0:
                    # Run detection
                    detections = self.detect_frame(frame)
                    
                    # Call callback with results
                    await callback(frame, detections, frame_count, node_id)
                
                # Small delay to prevent CPU thrashing
                await asyncio.sleep(0.01)
                
        except Exception as e:
            logger.error(f"Stream processing error: {e}")
        finally:
            if cap is not None:
                cap.release()
            logger.info(f"Video stream closed: {source}")
    
    def get_stats(self) -> Dict:
        """Get detection statistics"""
        return {
            **self.stats,
            'model_loaded': self.model is not None,
            'device': self.device,
            'confidence_threshold': self.conf_threshold
        }
    
    def draw_detections(self, 
                       frame: np.ndarray, 
                       detections: List[Dict],
                       show_confidence: bool = True) -> np.ndarray:
        """
        Draw bounding boxes on frame
        
        Args:
            frame: Input image
            detections: List of detections
            show_confidence: Show confidence scores
            
        Returns:
            Frame with drawn boxes
        """
        result = frame.copy()
        
        for det in detections:
            bbox = det['bbox']
            x, y, w, h = bbox['x'], bbox['y'], bbox['width'], bbox['height']
            
            # Color based on class
            color = self._get_color_for_class(det['class_name'])
            
            # Draw bounding box
            cv2.rectangle(result, (x, y), (x + w, y + h), color, 2)
            
            # Draw label
            label = f"{det['class_name']}"
            if show_confidence:
                label += f" {det['confidence']:.2f}"
            
            # Background for text
            (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(result, (x, y - 20), (x + text_w, y), color, -1)
            
            # Draw text
            cv2.putText(result, label, (x, y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return result
    
    def _get_color_for_class(self, class_name: str) -> tuple:
        """Get color for class"""
        colors = {
            'car': (0, 255, 0),      # Green
            'person': (255, 0, 0),    # Blue
            'pedestrian': (255, 0, 0),
            'bicycle': (0, 255, 255), # Yellow
            'bus': (255, 165, 0),     # Orange
            'truck': (255, 0, 255),   # Magenta
            'van': (0, 128, 255),     # Light blue
        }
        return colors.get(class_name.lower(), (128, 128, 128))


# Convenience function for quick testing
async def test_detection_service():
    """Test detection service with webcam"""
    print("🎬 Testing YOLO Detection Service...")
    
    detector = YOLODetectionService(device="auto")
    
    async def display_callback(frame, detections, frame_count, node_id):
        """Display detections in window"""
        annotated = detector.draw_detections(frame, detections)
        cv2.imshow('EDGE-QI Detection', annotated)
        
        print(f"Frame {frame_count}: {len(detections)} objects detected")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        return True
    
    try:
        await detector.process_video_stream(
            source=0,  # Webcam
            callback=display_callback,
            target_fps=5
        )
    except KeyboardInterrupt:
        print("\n⏹️  Stopped by user")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Test the detection service
    asyncio.run(test_detection_service())
