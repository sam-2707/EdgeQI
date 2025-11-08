# EdgeQI/Core/queue/queue_detector.py

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from collections import deque
import time
import math

@dataclass
class TrackPoint:
    """Represents a point in an object's trajectory"""
    x: float
    y: float
    timestamp: float
    confidence: float

@dataclass
class ObjectTrack:
    """Represents a tracked object over time"""
    track_id: int
    class_name: str
    positions: deque = field(default_factory=lambda: deque(maxlen=30))  # Keep last 30 positions
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    is_active: bool = True
    
    def add_position(self, x: float, y: float, confidence: float = 1.0):
        """Add a new position to the track"""
        self.positions.append(TrackPoint(x, y, time.time(), confidence))
        self.last_seen = time.time()
    
    def get_current_position(self) -> Optional[TrackPoint]:
        """Get the most recent position"""
        return self.positions[-1] if self.positions else None
    
    def get_velocity(self) -> Tuple[float, float]:
        """Calculate current velocity (dx/dt, dy/dt)"""
        if len(self.positions) < 2:
            return (0.0, 0.0)
        
        recent = list(self.positions)[-5:]  # Use last 5 positions for smoothing
        if len(recent) < 2:
            return (0.0, 0.0)
        
        dx = recent[-1].x - recent[0].x
        dy = recent[-1].y - recent[0].y
        dt = recent[-1].timestamp - recent[0].timestamp
        
        if dt > 0:
            return (dx / dt, dy / dt)
        return (0.0, 0.0)
    
    def get_total_distance(self) -> float:
        """Calculate total distance traveled"""
        if len(self.positions) < 2:
            return 0.0
        
        total_distance = 0.0
        positions = list(self.positions)
        for i in range(1, len(positions)):
            dx = positions[i].x - positions[i-1].x
            dy = positions[i].y - positions[i-1].y
            total_distance += math.sqrt(dx*dx + dy*dy)
        
        return total_distance

class SimpleTracker:
    """Simple object tracker using IoU and distance-based association"""
    
    def __init__(self, max_disappeared: int = 5, max_distance: float = 100.0):
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance
        self.tracks: Dict[int, ObjectTrack] = {}
        self.next_track_id = 1
        self.disappeared_counts: Dict[int, int] = {}
    
    def update(self, detections: List[Dict]) -> List[ObjectTrack]:
        """
        Update tracker with new detections
        
        Args:
            detections: List of detection dicts with 'center', 'bbox', 'class_name', 'confidence'
        
        Returns:
            List of active tracks
        """
        if not detections:
            # Mark all tracks as disappeared
            for track_id in list(self.tracks.keys()):
                self.disappeared_counts[track_id] = self.disappeared_counts.get(track_id, 0) + 1
                if self.disappeared_counts[track_id] > self.max_disappeared:
                    self._remove_track(track_id)
            return list(self.tracks.values())
        
        # Extract centers from detections
        detection_centers = [det['center'] for det in detections]
        
        if not self.tracks:
            # No existing tracks, create new ones
            for i, detection in enumerate(detections):
                self._create_new_track(detection)
        else:
            # Associate detections with existing tracks
            self._associate_detections(detections, detection_centers)
        
        return list(self.tracks.values())
    
    def _create_new_track(self, detection: Dict) -> ObjectTrack:
        """Create a new track from a detection"""
        track = ObjectTrack(
            track_id=self.next_track_id,
            class_name=detection.get('class_name', 'unknown')
        )
        
        center = detection['center']
        confidence = detection.get('confidence', 1.0)
        track.add_position(center[0], center[1], confidence)
        
        self.tracks[self.next_track_id] = track
        self.next_track_id += 1
        
        return track
    
    def _associate_detections(self, detections: List[Dict], detection_centers: List[Tuple]):
        """Associate detections with existing tracks"""
        track_ids = list(self.tracks.keys())
        track_centers = []
        
        for track_id in track_ids:
            pos = self.tracks[track_id].get_current_position()
            if pos:
                track_centers.append((pos.x, pos.y))
            else:
                track_centers.append((0, 0))
        
        # Compute distance matrix
        associations = self._compute_associations(track_centers, detection_centers)
        
        # Reset disappeared counts for associated tracks
        for track_idx, det_idx in associations:
            track_id = track_ids[track_idx]
            if track_id in self.disappeared_counts:
                del self.disappeared_counts[track_id]
            
            # Update track position
            detection = detections[det_idx]
            center = detection['center']
            confidence = detection.get('confidence', 1.0)
            self.tracks[track_id].add_position(center[0], center[1], confidence)
        
        # Mark unassociated tracks as disappeared
        associated_track_indices = {assoc[0] for assoc in associations}
        for i, track_id in enumerate(track_ids):
            if i not in associated_track_indices:
                self.disappeared_counts[track_id] = self.disappeared_counts.get(track_id, 0) + 1
                if self.disappeared_counts[track_id] > self.max_disappeared:
                    self._remove_track(track_id)
        
        # Create new tracks for unassociated detections
        associated_det_indices = {assoc[1] for assoc in associations}
        for i, detection in enumerate(detections):
            if i not in associated_det_indices:
                self._create_new_track(detection)
    
    def _compute_associations(self, track_centers: List[Tuple], detection_centers: List[Tuple]) -> List[Tuple[int, int]]:
        """Compute associations between tracks and detections using Hungarian algorithm approximation"""
        if not track_centers or not detection_centers:
            return []
        
        # Simple greedy association based on minimum distance
        associations = []
        used_detections = set()
        
        for track_idx, track_center in enumerate(track_centers):
            best_det_idx = None
            best_distance = float('inf')
            
            for det_idx, det_center in enumerate(detection_centers):
                if det_idx in used_detections:
                    continue
                
                distance = math.sqrt(
                    (track_center[0] - det_center[0])**2 + 
                    (track_center[1] - det_center[1])**2
                )
                
                if distance < best_distance and distance < self.max_distance:
                    best_distance = distance
                    best_det_idx = det_idx
            
            if best_det_idx is not None:
                associations.append((track_idx, best_det_idx))
                used_detections.add(best_det_idx)
        
        return associations
    
    def _remove_track(self, track_id: int):
        """Remove a track"""
        if track_id in self.tracks:
            del self.tracks[track_id]
        if track_id in self.disappeared_counts:
            del self.disappeared_counts[track_id]

class QueueDetector:
    """Advanced queue detection using clustering and trajectory analysis"""
    
    def __init__(self, clustering_threshold: float = 50.0, min_queue_size: int = 2):
        self.clustering_threshold = clustering_threshold
        self.min_queue_size = min_queue_size
        self.tracker = SimpleTracker()
        self.queue_regions: List[Dict] = []
        self.waiting_times: Dict[int, float] = {}  # track_id -> wait_start_time
    
    def detect_queues(self, detections: List[Dict]) -> Dict:
        """
        Detect queues from object detections
        
        Args:
            detections: List of detection dicts from computer vision
        
        Returns:
            Dictionary with queue analysis results
        """
        # Update object tracking
        tracks = self.tracker.update(detections)
        
        # Filter for people only (assuming people form queues)
        people_tracks = [track for track in tracks if track.class_name == 'person']
        
        # Even single people should be tracked for potential queue formation
        result = {
            'total_people': len(people_tracks),
            'queue_clusters': [],
            'queue_metrics': {},
            'individual_tracks': self._serialize_tracks(people_tracks),
            'timestamp': time.time()
        }
        
        if len(people_tracks) < self.min_queue_size:
            result['queue_metrics'] = self._get_minimal_metrics(people_tracks)
            self._update_waiting_times(people_tracks)
            return result
        
        # Detect queue formations using clustering
        queue_clusters = self._detect_queue_clusters(people_tracks)
        
        # Analyze queue dynamics
        queue_metrics = self._analyze_queue_dynamics(people_tracks, queue_clusters)
        
        # Update waiting times
        self._update_waiting_times(people_tracks)
        
        result['queue_clusters'] = queue_clusters
        result['queue_metrics'] = queue_metrics
        
        return result
    
    def _detect_queue_clusters(self, tracks: List[ObjectTrack]) -> List[Dict]:
        """Detect queue formations using spatial clustering"""
        if len(tracks) < self.min_queue_size:
            return []
        
        # Get current positions
        positions = []
        track_mapping = {}
        
        for i, track in enumerate(tracks):
            pos = track.get_current_position()
            if pos:
                positions.append([pos.x, pos.y])
                track_mapping[i] = track
        
        if len(positions) < self.min_queue_size:
            return []
        
        # Simple clustering based on distance threshold
        clusters = self._simple_clustering(positions, self.clustering_threshold)
        
        # Convert clusters to queue information
        queue_clusters = []
        for cluster_indices in clusters:
            if len(cluster_indices) >= self.min_queue_size:
                cluster_tracks = [track_mapping[i] for i in cluster_indices if i in track_mapping]
                queue_info = self._analyze_cluster(cluster_tracks)
                queue_clusters.append(queue_info)
        
        return queue_clusters
    
    def _simple_clustering(self, positions: List[List[float]], threshold: float) -> List[List[int]]:
        """Simple distance-based clustering"""
        clusters = []
        used = set()
        
        for i, pos1 in enumerate(positions):
            if i in used:
                continue
            
            cluster = [i]
            used.add(i)
            
            for j, pos2 in enumerate(positions):
                if j in used:
                    continue
                
                distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
                if distance <= threshold:
                    cluster.append(j)
                    used.add(j)
            
            if len(cluster) >= self.min_queue_size:
                clusters.append(cluster)
        
        return clusters
    
    def _analyze_cluster(self, tracks: List[ObjectTrack]) -> Dict:
        """Analyze a cluster of tracks to determine if it's a queue"""
        if not tracks:
            return {}
        
        positions = []
        for track in tracks:
            pos = track.get_current_position()
            if pos:
                positions.append((pos.x, pos.y))
        
        if len(positions) < 2:
            return {
                'queue_length': len(tracks),
                'is_queue': False,
                'linearity_score': 0.0,
                'average_spacing': 0.0,
                'queue_direction': None
            }
        
        # Calculate linearity (how much the points form a line)
        linearity_score = self._calculate_linearity(positions)
        
        # Calculate average spacing between people
        spacings = []
        for i in range(len(positions) - 1):
            for j in range(i + 1, len(positions)):
                dist = math.sqrt(
                    (positions[i][0] - positions[j][0])**2 + 
                    (positions[i][1] - positions[j][1])**2
                )
                spacings.append(dist)
        
        avg_spacing = np.mean(spacings) if spacings else 0.0
        
        # Determine if this cluster represents a queue
        is_queue = linearity_score > 0.7 and avg_spacing < self.clustering_threshold
        
        # Estimate queue direction
        queue_direction = self._estimate_queue_direction(positions) if is_queue else None
        
        return {
            'queue_length': len(tracks),
            'is_queue': is_queue,
            'linearity_score': round(linearity_score, 3),
            'average_spacing': round(avg_spacing, 2),
            'queue_direction': queue_direction,
            'track_ids': [track.track_id for track in tracks]
        }
    
    def _calculate_linearity(self, positions: List[Tuple[float, float]]) -> float:
        """Calculate how linear a set of points is (0=scattered, 1=perfect line)"""
        if len(positions) < 3:
            return 1.0 if len(positions) == 2 else 0.0
        
        # Use principal component analysis approximation
        positions_array = np.array(positions)
        centroid = np.mean(positions_array, axis=0)
        centered = positions_array - centroid
        
        # Calculate covariance matrix
        cov_matrix = np.cov(centered.T)
        eigenvalues = np.linalg.eigvals(cov_matrix)
        
        # Linearity is the ratio of largest to smallest eigenvalue
        eigenvalues = sorted(eigenvalues, reverse=True)
        if eigenvalues[1] > 0:
            linearity = 1.0 - (eigenvalues[1] / eigenvalues[0])
        else:
            linearity = 1.0
        
        return min(max(linearity, 0.0), 1.0)
    
    def _estimate_queue_direction(self, positions: List[Tuple[float, float]]) -> Optional[str]:
        """Estimate the primary direction of the queue"""
        if len(positions) < 2:
            return None
        
        # Calculate the primary direction using first and last points
        first = positions[0]
        last = positions[-1]
        
        dx = last[0] - first[0]
        dy = last[1] - first[1]
        
        # Determine primary direction
        if abs(dx) > abs(dy):
            return "horizontal"
        else:
            return "vertical"
    
    def _analyze_queue_dynamics(self, tracks: List[ObjectTrack], clusters: List[Dict]) -> Dict:
        """Analyze queue dynamics like movement and waiting times"""
        if not tracks:
            return {}
        
        total_movement = 0.0
        stationary_count = 0
        avg_wait_time = 0.0
        
        for track in tracks:
            velocity = track.get_velocity()
            speed = math.sqrt(velocity[0]**2 + velocity[1]**2)
            total_movement += speed
            
            if speed < 5.0:  # pixels per second - considered stationary
                stationary_count += 1
            
            # Calculate waiting time
            if track.track_id in self.waiting_times:
                wait_time = time.time() - self.waiting_times[track.track_id]
                avg_wait_time += wait_time
        
        avg_movement = total_movement / len(tracks) if tracks else 0.0
        avg_wait_time = avg_wait_time / len(tracks) if tracks else 0.0
        
        # Calculate queue efficiency metrics
        queue_efficiency = 1.0 - (stationary_count / len(tracks)) if tracks else 0.0
        
        return {
            'average_movement_speed': round(avg_movement, 2),
            'stationary_percentage': round((stationary_count / len(tracks)) * 100, 1) if tracks else 0,
            'estimated_wait_time': round(avg_wait_time, 1),
            'queue_efficiency': round(queue_efficiency, 3),
            'total_active_queues': len([c for c in clusters if c.get('is_queue', False)])
        }
    
    def _update_waiting_times(self, tracks: List[ObjectTrack]):
        """Update waiting times for tracked objects"""
        current_time = time.time()
        
        for track in tracks:
            if track.track_id not in self.waiting_times:
                # New track - start timing
                self.waiting_times[track.track_id] = current_time
            
            # Clean up old waiting times for tracks that no longer exist
            active_track_ids = {track.track_id for track in tracks}
            self.waiting_times = {
                tid: start_time for tid, start_time in self.waiting_times.items()
                if tid in active_track_ids
            }
    
    def _serialize_tracks(self, tracks: List[ObjectTrack]) -> List[Dict]:
        """Convert tracks to serializable format"""
        serialized = []
        for track in tracks:
            pos = track.get_current_position()
            velocity = track.get_velocity()
            
            serialized.append({
                'track_id': track.track_id,
                'position': (pos.x, pos.y) if pos else None,
                'velocity': velocity,
                'total_distance': round(track.get_total_distance(), 2),
                'duration': round(time.time() - track.first_seen, 1),
                'confidence': pos.confidence if pos else 0.0
            })
        
        return serialized
    
    def _get_minimal_metrics(self, tracks: List[ObjectTrack]) -> Dict:
        """Get minimal metrics for cases with few people"""
        if not tracks:
            return {
                'average_movement_speed': 0.0,
                'stationary_percentage': 0.0,
                'estimated_wait_time': 0.0,
                'queue_efficiency': 0.0,
                'total_active_queues': 0
            }
        
        total_movement = 0.0
        stationary_count = 0
        avg_wait_time = 0.0
        
        for track in tracks:
            velocity = track.get_velocity()
            speed = math.sqrt(velocity[0]**2 + velocity[1]**2)
            total_movement += speed
            
            if speed < 5.0:  # pixels per second - considered stationary
                stationary_count += 1
            
            # Calculate waiting time
            if track.track_id in self.waiting_times:
                wait_time = time.time() - self.waiting_times[track.track_id]
                avg_wait_time += wait_time
        
        avg_movement = total_movement / len(tracks)
        avg_wait_time = avg_wait_time / len(tracks)
        
        return {
            'average_movement_speed': round(avg_movement, 2),
            'stationary_percentage': round((stationary_count / len(tracks)) * 100, 1),
            'estimated_wait_time': round(avg_wait_time, 1),
            'queue_efficiency': 1.0 - (stationary_count / len(tracks)),
            'total_active_queues': 0  # No queues with insufficient people
        }

    def _empty_queue_result(self) -> Dict:
        """Return empty queue analysis result"""
        return {
            'total_people': 0,
            'queue_clusters': [],
            'queue_metrics': {
                'average_movement_speed': 0.0,
                'stationary_percentage': 0.0,
                'estimated_wait_time': 0.0,
                'queue_efficiency': 0.0,
                'total_active_queues': 0
            },
            'individual_tracks': [],
            'timestamp': time.time()
        }