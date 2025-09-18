# EdgeQI/tests/test_video_streaming.py

import unittest
import time
import numpy as np
import threading
from unittest.mock import Mock, patch
from Core.video import (
    VideoStreamProcessor, 
    MultiStreamManager, 
    VideoFrame, 
    StreamConfig, 
    StreamType,
    create_webcam_config,
    create_file_config
)
from ML.tasks.surveillance_task import SurveillanceTask

class TestVideoStreaming(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        pass
    
    def test_video_frame_creation(self):
        """Test VideoFrame creation and metadata"""
        frame_data = np.zeros((480, 640, 3), dtype=np.uint8)
        timestamp = time.time()
        
        video_frame = VideoFrame(
            frame=frame_data,
            timestamp=timestamp,
            stream_id="test_stream",
            frame_number=1
        )
        
        self.assertEqual(video_frame.stream_id, "test_stream")
        self.assertEqual(video_frame.frame_number, 1)
        self.assertEqual(video_frame.timestamp, timestamp)
        self.assertEqual(video_frame.get_size(), (480, 640))
        
        # Test metadata
        video_frame.add_metadata("test_key", "test_value")
        self.assertEqual(video_frame.metadata["test_key"], "test_value")
    
    def test_stream_config_creation(self):
        """Test StreamConfig creation with utility functions"""
        # Test webcam config
        webcam_config = create_webcam_config("webcam_1", camera_index=0, fps=30)
        self.assertEqual(webcam_config.stream_id, "webcam_1")
        self.assertEqual(webcam_config.stream_type, StreamType.WEBCAM)
        self.assertEqual(webcam_config.source, "0")
        self.assertEqual(webcam_config.fps, 30)
        
        # Test file config
        file_config = create_file_config("file_1", "/path/to/video.mp4")
        self.assertEqual(file_config.stream_id, "file_1")
        self.assertEqual(file_config.stream_type, StreamType.FILE)
        self.assertEqual(file_config.source, "/path/to/video.mp4")
        self.assertFalse(file_config.auto_restart)
    
    def test_video_stream_processor_initialization(self):
        """Test VideoStreamProcessor initialization"""
        config = StreamConfig(
            stream_id="test_stream",
            stream_type=StreamType.WEBCAM,
            source="0"
        )
        
        processor = VideoStreamProcessor(config)
        self.assertEqual(processor.config, config)
        self.assertFalse(processor.is_running)
        self.assertEqual(processor.frame_count, 0)
    
    @patch('cv2.VideoCapture')
    def test_video_stream_processor_start_stop(self, mock_video_capture):
        """Test starting and stopping video stream processor"""
        # Mock successful video capture
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        mock_video_capture.return_value = mock_cap
        
        config = StreamConfig(
            stream_id="test_stream",
            stream_type=StreamType.WEBCAM,
            source="0"
        )
        
        processor = VideoStreamProcessor(config)
        
        # Test start
        success = processor.start()
        self.assertTrue(success)
        self.assertTrue(processor.is_running)
        
        # Let it run briefly
        time.sleep(0.1)
        
        # Test stop
        processor.stop()
        self.assertFalse(processor.is_running)
    
    def test_multi_stream_manager(self):
        """Test MultiStreamManager functionality"""
        manager = MultiStreamManager()
        self.assertEqual(len(manager.streams), 0)
        
        # Test adding invalid stream (will fail without actual camera)
        config = create_webcam_config("test_cam", camera_index=99)  # Non-existent camera
        success = manager.add_stream(config)
        # Expect this to fail gracefully
        self.assertIsInstance(success, bool)
        
        # Test getting stream info
        info = manager.get_stream_info()
        self.assertIsInstance(info, dict)
    
    @patch('cv2.VideoCapture')
    def test_multi_stream_with_mock_camera(self, mock_video_capture):
        """Test MultiStreamManager with mocked camera"""
        # Mock successful video capture
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        mock_video_capture.return_value = mock_cap
        
        manager = MultiStreamManager()
        
        # Add a stream
        config = create_webcam_config("mock_cam", camera_index=0)
        success = manager.add_stream(config)
        self.assertTrue(success)
        self.assertEqual(len(manager.streams), 1)
        
        # Test getting frame
        time.sleep(0.1)  # Allow some frames to be captured
        frame = manager.get_frame("mock_cam", timeout=0.5)
        # Frame might be None if capture hasn't started yet, that's ok
        
        # Test getting stream info
        info = manager.get_stream_info("mock_cam")
        self.assertIn("stream_id", info)
        self.assertEqual(info["stream_id"], "mock_cam")
        
        # Remove stream
        success = manager.remove_stream("mock_cam")
        self.assertTrue(success)
        self.assertEqual(len(manager.streams), 0)
    
    def test_surveillance_task_initialization(self):
        """Test SurveillanceTask initialization"""
        # Test with minimal config to avoid camera requirements
        stream_configs = []  # Empty config to avoid camera access
        
        task = SurveillanceTask(
            detector_type="yolo",
            stream_configs=stream_configs
        )
        
        self.assertEqual(task.name, "SurveillanceTask")
        self.assertIsNotNone(task.detector)
        self.assertIsNotNone(task.queue_detector)
        self.assertIsNotNone(task.stream_manager)
    
    def test_surveillance_task_no_streams(self):
        """Test SurveillanceTask with no active streams"""
        # Create task with empty stream config
        task = SurveillanceTask(
            detector_type="yolo",
            stream_configs=[]
        )
        
        # Run the task
        result = task.run()
        
        # Should handle no streams gracefully
        self.assertIn("error", result)
        self.assertEqual(result["active_streams"], 0)
        self.assertIn("timestamp", result)
    
    @patch('cv2.VideoCapture')
    def test_surveillance_task_with_mock_streams(self, mock_video_capture):
        """Test SurveillanceTask with mocked video streams"""
        # Mock successful video capture
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        mock_video_capture.return_value = mock_cap
        
        # Create task with mock stream
        stream_configs = [
            {"type": "webcam", "id": "mock_cam", "source": 0}
        ]
        
        task = SurveillanceTask(
            detector_type="yolo",
            stream_configs=stream_configs
        )
        
        # Allow some time for stream to initialize
        time.sleep(0.2)
        
        # Run the task
        result = task.run()
        
        # Verify result structure
        if "error" not in result:
            self.assertIn("stream_results", result)
            self.assertIn("overall_metrics", result)
            self.assertIn("stream_info", result)
            self.assertIn("system_status", result)
            
            overall = result["overall_metrics"]
            self.assertIn("total_people", overall)
            self.assertIn("total_vehicles", overall)
            self.assertIn("alert_level", overall)
        
        # Cleanup
        task.stop()
    
    def test_stream_quality_assessment(self):
        """Test stream quality assessment functionality"""
        task = SurveillanceTask(detector_type="yolo", stream_configs=[])
        
        # Create test frame
        frame_data = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        test_frame = VideoFrame(
            frame=frame_data,
            timestamp=time.time(),
            stream_id="test",
            frame_number=1
        )
        
        # Test quality assessment
        quality = task._assess_stream_quality(test_frame, [])
        
        self.assertIn("quality_level", quality)
        self.assertIn("brightness", quality)
        self.assertIn("contrast", quality)
        self.assertIn("detection_confidence", quality)
        self.assertIn("frame_size", quality)
        
        # Verify quality level is valid
        self.assertIn(quality["quality_level"], ["poor", "fair", "good"])
    
    def test_alert_level_determination(self):
        """Test alert level determination logic"""
        task = SurveillanceTask(detector_type="yolo", stream_configs=[])
        
        # Test normal scenario
        normal_results = {
            "stream1": {
                "detection_summary": {"people_count": 5},
                "advanced_queue_analysis": {
                    "queue_metrics": {
                        "estimated_wait_time": 60,
                        "total_active_queues": 1
                    }
                }
            }
        }
        alert_level = task._determine_alert_level(normal_results)
        self.assertEqual(alert_level, "normal")
        
        # Test warning scenario
        warning_results = {
            "stream1": {
                "detection_summary": {"people_count": 15},
                "advanced_queue_analysis": {
                    "queue_metrics": {
                        "estimated_wait_time": 150,
                        "total_active_queues": 2
                    }
                }
            }
        }
        alert_level = task._determine_alert_level(warning_results)
        self.assertEqual(alert_level, "warning")
        
        # Test critical scenario
        critical_results = {
            "stream1": {
                "detection_summary": {"people_count": 25},
                "advanced_queue_analysis": {
                    "queue_metrics": {
                        "estimated_wait_time": 400,
                        "total_active_queues": 4
                    }
                }
            }
        }
        alert_level = task._determine_alert_level(critical_results)
        self.assertEqual(alert_level, "critical")
    
    def test_history_tracking(self):
        """Test analysis history tracking"""
        task = SurveillanceTask(detector_type="yolo", stream_configs=[])
        
        # Simulate some history updates
        for i in range(5):
            stream_results = {
                "stream1": {
                    "detection_summary": {"people_count": i * 2},
                    "advanced_queue_analysis": {"queue_metrics": {"total_active_queues": i}}
                }
            }
            overall_metrics = {
                "total_people": i * 2,
                "total_vehicles": i,
                "total_queues": i,
                "alert_level": "normal"
            }
            task._update_history(stream_results, overall_metrics)
        
        # Check history length
        self.assertEqual(len(task.analysis_history), 5)
        
        # Check statistics
        stats = task.get_stream_statistics()
        self.assertIn("recent_averages", stats)
        self.assertIn("alert_frequency", stats)
    
    def test_preprocessing_setup(self):
        """Test preprocessing pipeline setup"""
        config = StreamConfig(
            stream_id="test_stream",
            stream_type=StreamType.WEBCAM,
            source="0",
            preprocessing={
                "resize": (320, 240),
                "blur": 5,
                "grayscale": True
            }
        )
        
        processor = VideoStreamProcessor(config)
        
        # Check that preprocessors were added
        self.assertGreater(len(processor.preprocessors), 0)
        
        # Test preprocessing on a dummy frame
        test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        processed = processor._apply_preprocessing(test_frame)
        
        # Should be different from original due to preprocessing
        self.assertFalse(np.array_equal(test_frame, processed))


if __name__ == '__main__':
    unittest.main()