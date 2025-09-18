# EdgeQI/tests/test_vision.py

import unittest
import numpy as np
from ML.models.vision import YOLODetector, MobileNetDetector, Detection
from ML.tasks.vision_task import ComputerVisionTask, QueueAnalysisTask

class TestComputerVision(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.yolo_detector = YOLODetector()
        self.mobilenet_detector = MobileNetDetector()
        self.vision_task = ComputerVisionTask(detector_type="yolo")
        self.queue_task = QueueAnalysisTask(detector_type="yolo")
    
    def test_yolo_detector_initialization(self):
        """Test YOLO detector initialization"""
        self.assertIsNotNone(self.yolo_detector)
        self.assertEqual(self.yolo_detector.person_class_id, 0)
        self.assertIn(2, self.yolo_detector.vehicle_classes)  # car class
    
    def test_detection_simulation(self):
        """Test simulated object detection"""
        # Create dummy frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Run detection
        detections = self.yolo_detector.detect(frame)
        
        # Verify detections structure
        self.assertIsInstance(detections, list)
        for detection in detections:
            self.assertIsInstance(detection, Detection)
            self.assertGreaterEqual(detection.confidence, 0.0)
            self.assertLessEqual(detection.confidence, 1.0)
            self.assertEqual(len(detection.bbox), 4)
            self.assertEqual(len(detection.center), 2)
    
    def test_object_counting(self):
        """Test object counting functionality"""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        detections = self.yolo_detector.detect(frame)
        
        people_count = self.yolo_detector.count_objects(detections, "person")
        vehicle_count = self.yolo_detector.count_objects(detections, "vehicle")
        
        self.assertIsInstance(people_count, int)
        self.assertIsInstance(vehicle_count, int)
        self.assertGreaterEqual(people_count, 0)
        self.assertGreaterEqual(vehicle_count, 0)
    
    def test_vision_task_execution(self):
        """Test computer vision task execution"""
        result = self.vision_task.run()
        
        # Verify result structure
        self.assertIn("people_count", result)
        self.assertIn("vehicle_count", result)
        self.assertIn("detector_type", result)
        self.assertIn("frame_size", result)
        self.assertIn("people_positions", result)
        self.assertIn("vehicle_positions", result)
        
        # Verify data types
        self.assertIsInstance(result["people_count"], int)
        self.assertIsInstance(result["vehicle_count"], int)
        self.assertEqual(result["detector_type"], "yolo")
    
    def test_queue_analysis_task(self):
        """Test queue analysis task execution"""
        result = self.queue_task.run()
        
        # Verify basic vision results are present
        self.assertIn("people_count", result)
        self.assertIn("vehicle_count", result)
        
        # Verify queue analysis results
        self.assertIn("queue_analysis", result)
        queue_metrics = result["queue_analysis"]
        
        self.assertIn("estimated_queue_length", queue_metrics)
        self.assertIn("queue_density", queue_metrics)
        self.assertIn("waiting_area_occupancy", queue_metrics)
        
        # Verify data types and ranges
        self.assertIsInstance(queue_metrics["estimated_queue_length"], int)
        self.assertGreaterEqual(queue_metrics["estimated_queue_length"], 0)
        self.assertGreaterEqual(queue_metrics["queue_density"], 0.0)
        self.assertGreaterEqual(queue_metrics["waiting_area_occupancy"], 0.0)
    
    def test_detector_filtering(self):
        """Test detection filtering methods"""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        detections = self.yolo_detector.detect(frame)
        
        people_detections = self.yolo_detector.get_people_detections(detections)
        vehicle_detections = self.yolo_detector.get_vehicle_detections(detections)
        
        # Verify all people detections have correct class
        for detection in people_detections:
            self.assertEqual(detection.class_id, 0)
        
        # Verify all vehicle detections have correct class
        for detection in vehicle_detections:
            self.assertIn(detection.class_id, self.yolo_detector.vehicle_classes)
    
    def test_mobilenet_detector(self):
        """Test MobileNet detector"""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        detections = self.mobilenet_detector.detect(frame)
        
        self.assertIsInstance(detections, list)
        # MobileNet should generally have slightly lower confidence than YOLO (due to simulation)
        for detection in detections:
            self.assertLessEqual(detection.confidence, 0.95)  # Should be scaled down


if __name__ == '__main__':
    unittest.main()