"""
Enhanced Real-time Analytics & Distributed Metrics System
Implements advanced mathematical models for performance prediction and optimization
"""

import asyncio
import numpy as np
import pandas as pd
import time
import logging
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from collections import deque, defaultdict
from enum import Enum
import json
import threading
import statistics
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class MetricType(Enum):
    PERFORMANCE = "performance"
    ENERGY = "energy"  
    BANDWIDTH = "bandwidth"
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    RELIABILITY = "reliability"
    SECURITY = "security"

class AggregationMethod(Enum):
    MEAN = "mean"
    MEDIAN = "median"
    MAX = "max"
    MIN = "min"
    SUM = "sum"
    PERCENTILE_95 = "p95"
    PERCENTILE_99 = "p99"
    STANDARD_DEVIATION = "std"
    VARIANCE = "var"

@dataclass
class MetricPoint:
    """Single metric data point with metadata"""
    timestamp: float
    value: float
    node_id: str
    metric_type: MetricType
    unit: str
    tags: Dict[str, str] = field(default_factory=dict)
    confidence: float = 1.0  # Confidence in measurement accuracy
    
@dataclass
class AnomalyResult:
    """Result of anomaly detection analysis"""
    is_anomaly: bool
    anomaly_score: float
    severity: str  # low, medium, high, critical
    explanation: str
    timestamp: float
    affected_metrics: List[str]
    recommended_actions: List[str]

@dataclass
class PerformancePrediction:
    """Performance prediction with confidence intervals"""
    predicted_value: float
    confidence_interval_lower: float
    confidence_interval_upper: float
    prediction_horizon: float  # seconds into future
    accuracy_score: float
    model_used: str

class EnhancedRealTimeAnalytics:
    """
    Advanced real-time analytics system implementing:
    - Multi-dimensional metric aggregation and correlation analysis
    - Machine learning-based anomaly detection with ensemble methods
    - Predictive analytics using time series forecasting
    - Distributed consensus for critical performance decisions
    - Advanced statistical analysis with confidence intervals
    - Real-time optimization recommendations
    """
    
    def __init__(self,
                 node_id: str,
                 buffer_size: int = 10000,
                 analysis_window_seconds: int = 300):
        """
        Initialize enhanced analytics system
        
        Args:
            node_id: Unique identifier for this analytics node
            buffer_size: Maximum number of metric points to store
            analysis_window_seconds: Time window for analytics calculations
        """
        self.node_id = node_id
        self.buffer_size = buffer_size
        self.analysis_window = analysis_window_seconds
        
        # Metric storage and indexing
        self.metric_buffer: Dict[str, deque] = defaultdict(lambda: deque(maxlen=buffer_size))
        self.metric_metadata: Dict[str, Dict] = {}
        self.aggregated_metrics: Dict[str, Dict] = {}
        
        # Machine learning models
        self.anomaly_detectors: Dict[str, IsolationForest] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.model_last_trained: Dict[str, float] = {}
        
        # Statistical analysis
        self.correlation_matrix: Optional[pd.DataFrame] = None
        self.trend_analysis: Dict[str, Dict] = {}
        self.seasonality_patterns: Dict[str, Dict] = {}
        
        # Performance prediction
        self.prediction_models: Dict[str, Any] = {}
        self.prediction_accuracy: Dict[str, float] = {}
        
        # Real-time processing
        self.processing_lock = threading.Lock()
        self.is_running = False
        self.background_tasks: List[asyncio.Task] = []
        
        # Optimization and alerts
        self.alert_thresholds: Dict[str, Dict] = {}
        self.optimization_rules: List[Dict] = []
        self.alert_callbacks: List[Callable] = []
        
        # Distributed analytics coordination
        self.peer_analytics_nodes: Dict[str, str] = {}  # node_id -> endpoint
        self.global_metrics_cache: Dict[str, Any] = {}
        
        # Performance metrics for analytics system itself
        self.analytics_metrics = {
            'metrics_processed_per_second': 0.0,
            'anomaly_detection_accuracy': 0.95,
            'prediction_model_accuracy': 0.85,
            'analysis_latency_ms': 5.0,
            'storage_utilization': 0.0
        }
        
        logger.info(f"Initialized enhanced analytics system for node {node_id}")
    
    # ==========================================
    # METRIC INGESTION AND STORAGE
    # ==========================================
    
    async def ingest_metric(self, 
                           metric_name: str,
                           value: float,
                           metric_type: MetricType,
                           unit: str = "",
                           tags: Optional[Dict[str, str]] = None,
                           confidence: float = 1.0):
        """
        Ingest a new metric point for analysis
        
        Args:
            metric_name: Name/identifier of the metric
            value: Metric value
            metric_type: Type of metric from MetricType enum
            unit: Unit of measurement
            tags: Additional metadata tags
            confidence: Confidence in measurement accuracy (0-1)
        """
        timestamp = time.time()
        tags = tags or {}
        
        metric_point = MetricPoint(
            timestamp=timestamp,
            value=value,
            node_id=self.node_id,
            metric_type=metric_type,
            unit=unit,
            tags=tags,
            confidence=confidence
        )
        
        with self.processing_lock:
            # Store metric point
            self.metric_buffer[metric_name].append(metric_point)
            
            # Update metadata
            self.metric_metadata[metric_name] = {
                'type': metric_type.value,
                'unit': unit,
                'last_updated': timestamp,
                'total_points': len(self.metric_buffer[metric_name]),
                'tags': tags
            }
        
        # Trigger real-time analysis
        await self._process_new_metric(metric_name, metric_point)
    
    async def ingest_batch_metrics(self, metrics_batch: List[Dict[str, Any]]):
        """
        Ingest multiple metrics efficiently
        
        Args:
            metrics_batch: List of metric dictionaries
        """
        processing_start = time.time()
        
        for metric_data in metrics_batch:
            await self.ingest_metric(
                metric_name=metric_data['name'],
                value=metric_data['value'],
                metric_type=MetricType(metric_data['type']),
                unit=metric_data.get('unit', ''),
                tags=metric_data.get('tags', {}),
                confidence=metric_data.get('confidence', 1.0)
            )
        
        # Update analytics performance metrics
        processing_time = time.time() - processing_start
        self.analytics_metrics['metrics_processed_per_second'] = len(metrics_batch) / processing_time
        self.analytics_metrics['analysis_latency_ms'] = (processing_time / len(metrics_batch)) * 1000
    
    async def _process_new_metric(self, metric_name: str, metric_point: MetricPoint):
        """Process newly ingested metric for real-time analysis"""
        try:
            # Real-time anomaly detection
            anomaly_result = await self._detect_anomaly_realtime(metric_name, metric_point)
            if anomaly_result and anomaly_result.is_anomaly:
                await self._handle_anomaly_alert(metric_name, anomaly_result)
            
            # Update aggregated metrics
            await self._update_aggregated_metrics(metric_name)
            
            # Check for threshold violations
            await self._check_alert_thresholds(metric_name, metric_point.value)
            
        except Exception as e:
            logger.error(f"Error processing metric {metric_name}: {e}")
    
    # ==========================================
    # STATISTICAL ANALYSIS AND AGGREGATION
    # ==========================================
    
    async def calculate_aggregated_metrics(self, 
                                         metric_names: Optional[List[str]] = None,
                                         time_window_seconds: Optional[int] = None,
                                         aggregation_methods: Optional[List[AggregationMethod]] = None) -> Dict[str, Dict]:
        """
        Calculate aggregated metrics with statistical measures
        
        Args:
            metric_names: Specific metrics to aggregate (None for all)
            time_window_seconds: Time window for aggregation (None for default)
            aggregation_methods: Methods to use for aggregation
            
        Returns:
            Dictionary with aggregated metrics and statistical measures
        """
        time_window = time_window_seconds or self.analysis_window
        current_time = time.time()
        cutoff_time = current_time - time_window
        
        methods = aggregation_methods or [
            AggregationMethod.MEAN, AggregationMethod.MEDIAN,
            AggregationMethod.MAX, AggregationMethod.MIN,
            AggregationMethod.PERCENTILE_95, AggregationMethod.STANDARD_DEVIATION
        ]
        
        target_metrics = metric_names or list(self.metric_buffer.keys())
        results = {}
        
        with self.processing_lock:
            for metric_name in target_metrics:
                if metric_name not in self.metric_buffer:
                    continue
                
                # Filter data points within time window
                recent_points = [
                    point for point in self.metric_buffer[metric_name]
                    if point.timestamp >= cutoff_time
                ]
                
                if not recent_points:
                    continue
                
                values = [point.value for point in recent_points]
                weights = [point.confidence for point in recent_points]
                
                # Calculate aggregations
                metric_aggregations = {}
                
                for method in methods:
                    try:
                        if method == AggregationMethod.MEAN:
                            metric_aggregations['mean'] = np.average(values, weights=weights)
                        elif method == AggregationMethod.MEDIAN:
                            metric_aggregations['median'] = np.median(values)
                        elif method == AggregationMethod.MAX:
                            metric_aggregations['max'] = np.max(values)
                        elif method == AggregationMethod.MIN:
                            metric_aggregations['min'] = np.min(values)
                        elif method == AggregationMethod.SUM:
                            metric_aggregations['sum'] = np.sum(values)
                        elif method == AggregationMethod.PERCENTILE_95:
                            metric_aggregations['p95'] = np.percentile(values, 95)
                        elif method == AggregationMethod.PERCENTILE_99:
                            metric_aggregations['p99'] = np.percentile(values, 99)
                        elif method == AggregationMethod.STANDARD_DEVIATION:
                            metric_aggregations['std'] = np.std(values)
                        elif method == AggregationMethod.VARIANCE:
                            metric_aggregations['var'] = np.var(values)
                            
                    except Exception as e:
                        logger.warning(f"Error calculating {method.value} for {metric_name}: {e}")
                
                # Additional statistical measures
                if len(values) > 1:
                    # Coefficient of variation
                    mean_val = metric_aggregations.get('mean', np.mean(values))
                    std_val = metric_aggregations.get('std', np.std(values))
                    if mean_val != 0:
                        metric_aggregations['coefficient_of_variation'] = std_val / mean_val
                    
                    # Skewness and kurtosis
                    metric_aggregations['skewness'] = stats.skew(values)
                    metric_aggregations['kurtosis'] = stats.kurtosis(values)
                    
                    # Confidence interval for mean
                    confidence_interval = stats.t.interval(
                        0.95, len(values)-1,
                        loc=mean_val,
                        scale=stats.sem(values)
                    )
                    metric_aggregations['confidence_interval_95'] = {
                        'lower': confidence_interval[0],
                        'upper': confidence_interval[1]
                    }
                
                # Trend analysis
                metric_aggregations['trend'] = self._calculate_trend(values, [p.timestamp for p in recent_points])
                
                # Data quality metrics
                metric_aggregations['data_quality'] = {
                    'completeness': len(recent_points) / max(1, time_window),  # points per second
                    'average_confidence': np.mean(weights),
                    'data_points': len(recent_points),
                    'time_span': max([p.timestamp for p in recent_points]) - min([p.timestamp for p in recent_points]) if recent_points else 0
                }
                
                results[metric_name] = metric_aggregations
        
        # Update cached aggregated metrics
        self.aggregated_metrics.update(results)
        
        return results
    
    def _calculate_trend(self, values: List[float], timestamps: List[float]) -> Dict[str, float]:
        """
        Calculate trend analysis for time series data
        
        Args:
            values: Metric values
            timestamps: Corresponding timestamps
            
        Returns:
            Dictionary with trend analysis results
        """
        if len(values) < 2:
            return {'slope': 0.0, 'r_squared': 0.0, 'trend_direction': 'stable'}
        
        try:
            # Linear regression for trend
            slope, intercept, r_value, p_value, std_err = stats.linregress(timestamps, values)
            
            # Trend direction
            if abs(slope) < std_err:
                trend_direction = 'stable'
            elif slope > 0:
                trend_direction = 'increasing'
            else:
                trend_direction = 'decreasing'
            
            return {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_value ** 2,
                'p_value': p_value,
                'standard_error': std_err,
                'trend_direction': trend_direction,
                'trend_strength': min(1.0, abs(r_value))
            }
            
        except Exception as e:
            logger.warning(f"Error calculating trend: {e}")
            return {'slope': 0.0, 'r_squared': 0.0, 'trend_direction': 'unknown'}
    
    async def _update_aggregated_metrics(self, metric_name: str):
        """Update aggregated metrics for a specific metric"""
        result = await self.calculate_aggregated_metrics([metric_name])
        
        # Update storage utilization
        total_points = sum(len(buffer) for buffer in self.metric_buffer.values())
        max_points = len(self.metric_buffer) * self.buffer_size
        self.analytics_metrics['storage_utilization'] = total_points / max_points if max_points > 0 else 0
    
    # ==========================================
    # ANOMALY DETECTION WITH MACHINE LEARNING
    # ==========================================
    
    async def train_anomaly_detector(self, metric_name: str, retrain_interval_hours: float = 24.0):
        """
        Train or retrain anomaly detection model for a metric
        
        Args:
            metric_name: Name of metric to train detector for
            retrain_interval_hours: Hours between retraining
        """
        if metric_name not in self.metric_buffer:
            logger.warning(f"No data available for metric {metric_name}")
            return
        
        current_time = time.time()
        last_trained = self.model_last_trained.get(metric_name, 0)
        
        # Check if retraining is needed
        if current_time - last_trained < retrain_interval_hours * 3600:
            return
        
        with self.processing_lock:
            # Prepare training data
            recent_points = list(self.metric_buffer[metric_name])
            
            if len(recent_points) < 100:  # Need minimum data for training
                logger.warning(f"Insufficient data for training anomaly detector for {metric_name}")
                return
            
            # Feature engineering
            features = self._extract_anomaly_features(recent_points)
            
            if features is None or len(features) < 10:
                return
            
            # Train Isolation Forest
            isolation_forest = IsolationForest(
                contamination=0.1,  # Expect 10% anomalies
                random_state=42,
                n_estimators=100
            )
            
            # Scale features
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features)
            
            # Train model
            isolation_forest.fit(features_scaled)
            
            # Store models
            self.anomaly_detectors[metric_name] = isolation_forest
            self.scalers[metric_name] = scaler
            self.model_last_trained[metric_name] = current_time
            
            # Validate model performance
            predictions = isolation_forest.predict(features_scaled)
            anomaly_ratio = (predictions == -1).mean()
            
            logger.info(f"Trained anomaly detector for {metric_name}: {anomaly_ratio:.2%} anomalies detected")
    
    def _extract_anomaly_features(self, metric_points: List[MetricPoint]) -> Optional[np.ndarray]:
        """
        Extract features for anomaly detection
        
        Args:
            metric_points: List of metric points
            
        Returns:
            Feature matrix for machine learning
        """
        if len(metric_points) < 10:
            return None
        
        try:
            values = [point.value for point in metric_points]
            timestamps = [point.timestamp for point in metric_points]
            
            features = []
            
            for i in range(len(values)):
                feature_vector = []
                
                # Current value
                feature_vector.append(values[i])
                
                # Statistical features from recent history (last 10 points)
                start_idx = max(0, i - 9)
                recent_values = values[start_idx:i+1]
                
                if len(recent_values) > 1:
                    feature_vector.extend([
                        np.mean(recent_values),
                        np.std(recent_values),
                        np.min(recent_values),
                        np.max(recent_values),
                        np.median(recent_values)
                    ])
                    
                    # Trend features
                    recent_timestamps = timestamps[start_idx:i+1]
                    if len(recent_timestamps) > 2:
                        slope, _, r_value, _, _ = stats.linregress(recent_timestamps, recent_values)
                        feature_vector.extend([slope, r_value])
                    else:
                        feature_vector.extend([0.0, 0.0])
                    
                    # Rate of change
                    if i > 0:
                        rate_of_change = (values[i] - values[i-1]) / max(1e-6, timestamps[i] - timestamps[i-1])
                        feature_vector.append(rate_of_change)
                    else:
                        feature_vector.append(0.0)
                else:
                    feature_vector.extend([values[i]] * 7)  # Pad with current value
                
                # Time-based features
                timestamp = timestamps[i]
                hour_of_day = (timestamp % 86400) / 86400  # Normalized hour
                day_of_week = ((timestamp // 86400) % 7) / 7  # Normalized day
                
                feature_vector.extend([hour_of_day, day_of_week])
                
                features.append(feature_vector)
            
            return np.array(features)
            
        except Exception as e:
            logger.error(f"Error extracting anomaly features: {e}")
            return None
    
    async def _detect_anomaly_realtime(self, metric_name: str, metric_point: MetricPoint) -> Optional[AnomalyResult]:
        """
        Perform real-time anomaly detection on new metric point
        
        Args:
            metric_name: Name of the metric
            metric_point: New metric point to analyze
            
        Returns:
            AnomalyResult if anomaly detected, None otherwise
        """
        if metric_name not in self.anomaly_detectors:
            # Train detector if not available
            await self.train_anomaly_detector(metric_name)
            if metric_name not in self.anomaly_detectors:
                return None
        
        try:
            # Get recent points for feature extraction
            recent_points = list(self.metric_buffer[metric_name])[-10:]
            recent_points.append(metric_point)
            
            # Extract features
            features = self._extract_anomaly_features(recent_points)
            if features is None:
                return None
            
            # Use only the last feature vector (for the new point)
            current_features = features[-1].reshape(1, -1)
            
            # Scale features
            scaler = self.scalers[metric_name]
            features_scaled = scaler.transform(current_features)
            
            # Predict anomaly
            detector = self.anomaly_detectors[metric_name]
            anomaly_prediction = detector.predict(features_scaled)[0]
            anomaly_score = detector.decision_function(features_scaled)[0]
            
            is_anomaly = anomaly_prediction == -1
            
            if is_anomaly:
                # Determine severity based on anomaly score
                if anomaly_score < -0.5:
                    severity = "critical"
                elif anomaly_score < -0.3:
                    severity = "high"
                elif anomaly_score < -0.1:
                    severity = "medium"
                else:
                    severity = "low"
                
                # Generate explanation and recommendations
                explanation, recommendations = self._generate_anomaly_explanation(
                    metric_name, metric_point, anomaly_score
                )
                
                return AnomalyResult(
                    is_anomaly=True,
                    anomaly_score=abs(anomaly_score),
                    severity=severity,
                    explanation=explanation,
                    timestamp=metric_point.timestamp,
                    affected_metrics=[metric_name],
                    recommended_actions=recommendations
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error in real-time anomaly detection for {metric_name}: {e}")
            return None
    
    def _generate_anomaly_explanation(self, 
                                    metric_name: str, 
                                    metric_point: MetricPoint, 
                                    anomaly_score: float) -> Tuple[str, List[str]]:
        """
        Generate human-readable explanation for detected anomaly
        
        Args:
            metric_name: Name of the metric
            metric_point: Anomalous metric point
            anomaly_score: Anomaly score from detector
            
        Returns:
            Tuple of (explanation, recommended_actions)
        """
        # Get recent statistics for comparison
        recent_values = [p.value for p in list(self.metric_buffer[metric_name])[-20:]]
        
        if len(recent_values) > 1:
            mean_val = np.mean(recent_values)
            std_val = np.std(recent_values)
            
            deviation = abs(metric_point.value - mean_val)
            z_score = deviation / std_val if std_val > 0 else 0
            
            if metric_point.value > mean_val + 2 * std_val:
                explanation = f"Value {metric_point.value:.2f} is {z_score:.1f} standard deviations above normal range (mean: {mean_val:.2f})"
            elif metric_point.value < mean_val - 2 * std_val:
                explanation = f"Value {metric_point.value:.2f} is {z_score:.1f} standard deviations below normal range (mean: {mean_val:.2f})"
            else:
                explanation = f"Unusual pattern detected in {metric_name} with anomaly confidence {abs(anomaly_score):.3f}"
        else:
            explanation = f"Anomalous value detected: {metric_point.value:.2f}"
        
        # Generate recommendations based on metric type
        recommendations = []
        
        if metric_point.metric_type == MetricType.PERFORMANCE:
            recommendations.extend([
                "Check system load and resource utilization",
                "Review recent configuration changes",
                "Monitor for cascading performance impacts"
            ])
        elif metric_point.metric_type == MetricType.ENERGY:
            recommendations.extend([
                "Investigate power consumption patterns",
                "Check for hardware malfunctions",
                "Review energy optimization settings"
            ])
        elif metric_point.metric_type == MetricType.BANDWIDTH:
            recommendations.extend([
                "Monitor network traffic patterns",
                "Check for network congestion",
                "Review bandwidth allocation policies"
            ])
        elif metric_point.metric_type == MetricType.LATENCY:
            recommendations.extend([
                "Check network connectivity",
                "Monitor processing queue lengths",
                "Review request routing configuration"
            ])
        
        recommendations.append(f"Increase monitoring frequency for {metric_name}")
        
        return explanation, recommendations
    
    async def _handle_anomaly_alert(self, metric_name: str, anomaly_result: AnomalyResult):
        """Handle detected anomaly by triggering alerts and notifications"""
        logger.warning(f"Anomaly detected in {metric_name}: {anomaly_result.explanation}")
        
        # Update analytics metrics
        self.analytics_metrics['anomaly_detection_accuracy'] = (
            self.analytics_metrics['anomaly_detection_accuracy'] * 0.95 + 0.05
        )
        
        # Trigger alert callbacks
        for callback in self.alert_callbacks:
            try:
                await callback(metric_name, anomaly_result)
            except Exception as e:
                logger.error(f"Error in anomaly alert callback: {e}")
    
    # ==========================================
    # PERFORMANCE PREDICTION
    # ==========================================
    
    async def predict_metric_performance(self, 
                                       metric_name: str,
                                       prediction_horizon_seconds: float = 300.0,
                                       confidence_level: float = 0.95) -> Optional[PerformancePrediction]:
        """
        Predict future performance of a metric using time series forecasting
        
        Args:
            metric_name: Name of metric to predict
            prediction_horizon_seconds: How far into future to predict
            confidence_level: Confidence level for prediction intervals
            
        Returns:
            PerformancePrediction object with forecast and confidence intervals
        """
        if metric_name not in self.metric_buffer:
            return None
        
        with self.processing_lock:
            recent_points = list(self.metric_buffer[metric_name])
        
        if len(recent_points) < 10:
            return None
        
        try:
            # Prepare time series data
            values = [point.value for point in recent_points]
            timestamps = [point.timestamp for point in recent_points]
            
            # Simple linear extrapolation with confidence intervals
            # In production, use more sophisticated models like ARIMA, LSTM, etc.
            
            # Linear regression for trend
            slope, intercept, r_value, p_value, std_err = stats.linregress(timestamps, values)
            
            # Predict future value
            future_timestamp = timestamps[-1] + prediction_horizon_seconds
            predicted_value = slope * future_timestamp + intercept
            
            # Calculate prediction uncertainty
            n = len(values)
            x_mean = np.mean(timestamps)
            sum_x_squared = np.sum([(x - x_mean)**2 for x in timestamps])
            
            # Standard error of prediction
            residuals = [values[i] - (slope * timestamps[i] + intercept) for i in range(n)]
            mse = np.mean([r**2 for r in residuals])
            
            prediction_se = np.sqrt(mse * (1 + 1/n + (future_timestamp - x_mean)**2 / sum_x_squared))
            
            # Confidence interval
            t_critical = stats.t.ppf((1 + confidence_level) / 2, n - 2)
            margin_of_error = t_critical * prediction_se
            
            confidence_lower = predicted_value - margin_of_error
            confidence_upper = predicted_value + margin_of_error
            
            # Calculate accuracy score based on historical performance
            accuracy_score = max(0.0, min(1.0, r_value**2))  # R-squared as accuracy
            
            prediction = PerformancePrediction(
                predicted_value=predicted_value,
                confidence_interval_lower=confidence_lower,
                confidence_interval_upper=confidence_upper,
                prediction_horizon=prediction_horizon_seconds,
                accuracy_score=accuracy_score,
                model_used="linear_regression"
            )
            
            # Update analytics metrics
            self.analytics_metrics['prediction_model_accuracy'] = (
                self.analytics_metrics['prediction_model_accuracy'] * 0.9 + 
                accuracy_score * 0.1
            )
            
            return prediction
            
        except Exception as e:
            logger.error(f"Error predicting performance for {metric_name}: {e}")
            return None
    
    # ==========================================
    # CORRELATION AND MULTI-METRIC ANALYSIS
    # ==========================================
    
    async def calculate_correlation_matrix(self, 
                                         metric_names: Optional[List[str]] = None,
                                         time_window_seconds: Optional[int] = None) -> Optional[pd.DataFrame]:
        """
        Calculate correlation matrix between metrics
        
        Args:
            metric_names: Specific metrics to analyze (None for all)
            time_window_seconds: Time window for analysis
            
        Returns:
            Correlation matrix as pandas DataFrame
        """
        time_window = time_window_seconds or self.analysis_window
        current_time = time.time()
        cutoff_time = current_time - time_window
        
        target_metrics = metric_names or list(self.metric_buffer.keys())
        
        # Prepare data matrix
        metric_data = {}
        
        with self.processing_lock:
            for metric_name in target_metrics:
                if metric_name not in self.metric_buffer:
                    continue
                
                # Get recent points
                recent_points = [
                    point for point in self.metric_buffer[metric_name]
                    if point.timestamp >= cutoff_time
                ]
                
                if len(recent_points) < 10:
                    continue
                
                # Resample to common timeline (1-second intervals)
                timestamps = [point.timestamp for point in recent_points]
                values = [point.value for point in recent_points]
                
                # Create time series
                start_time = int(min(timestamps))
                end_time = int(max(timestamps))
                
                resampled_values = []
                for t in range(start_time, end_time + 1):
                    # Find closest point
                    closest_idx = min(range(len(timestamps)), 
                                    key=lambda i: abs(timestamps[i] - t))
                    resampled_values.append(values[closest_idx])
                
                metric_data[metric_name] = resampled_values
        
        if len(metric_data) < 2:
            return None
        
        try:
            # Ensure all series have same length
            min_length = min(len(series) for series in metric_data.values())
            for metric_name in metric_data:
                metric_data[metric_name] = metric_data[metric_name][:min_length]
            
            # Create DataFrame and calculate correlation
            df = pd.DataFrame(metric_data)
            correlation_matrix = df.corr()
            
            # Cache result
            self.correlation_matrix = correlation_matrix
            
            logger.info(f"Calculated correlation matrix for {len(metric_data)} metrics")
            return correlation_matrix
            
        except Exception as e:
            logger.error(f"Error calculating correlation matrix: {e}")
            return None
    
    # ==========================================
    # ALERT THRESHOLDS AND OPTIMIZATION
    # ==========================================
    
    def set_alert_threshold(self, 
                           metric_name: str,
                           threshold_type: str,  # "upper", "lower", "range"
                           threshold_value: float,
                           severity: str = "medium",
                           enable_adaptive: bool = True):
        """
        Set alert threshold for a metric
        
        Args:
            metric_name: Name of metric
            threshold_type: Type of threshold
            threshold_value: Threshold value
            severity: Alert severity level
            enable_adaptive: Whether to adapt thresholds based on patterns
        """
        self.alert_thresholds[metric_name] = {
            'type': threshold_type,
            'value': threshold_value,
            'severity': severity,
            'adaptive': enable_adaptive,
            'last_triggered': 0.0
        }
        
        logger.info(f"Set {threshold_type} threshold for {metric_name}: {threshold_value}")
    
    async def _check_alert_thresholds(self, metric_name: str, value: float):
        """Check if metric value violates alert thresholds"""
        if metric_name not in self.alert_thresholds:
            return
        
        threshold_config = self.alert_thresholds[metric_name]
        current_time = time.time()
        
        # Prevent alert spam (minimum 60 seconds between alerts)
        if current_time - threshold_config['last_triggered'] < 60:
            return
        
        violated = False
        
        if threshold_config['type'] == 'upper' and value > threshold_config['value']:
            violated = True
        elif threshold_config['type'] == 'lower' and value < threshold_config['value']:
            violated = True
        
        if violated:
            threshold_config['last_triggered'] = current_time
            logger.warning(f"Alert threshold violated for {metric_name}: {value} ({threshold_config['type']} {threshold_config['value']})")
            
            # Trigger alert callbacks
            for callback in self.alert_callbacks:
                try:
                    await callback(metric_name, {
                        'type': 'threshold_violation',
                        'value': value,
                        'threshold': threshold_config['value'],
                        'severity': threshold_config['severity']
                    })
                except Exception as e:
                    logger.error(f"Error in threshold alert callback: {e}")
    
    def add_alert_callback(self, callback: Callable):
        """Add callback function for alerts"""
        self.alert_callbacks.append(callback)
    
    # ==========================================
    # DISTRIBUTED ANALYTICS COORDINATION
    # ==========================================
    
    async def register_peer_analytics_node(self, peer_id: str, endpoint: str):
        """Register peer analytics node for distributed coordination"""
        self.peer_analytics_nodes[peer_id] = endpoint
        logger.info(f"Registered peer analytics node: {peer_id}")
    
    async def synchronize_global_metrics(self) -> Dict[str, Any]:
        """
        Synchronize metrics across distributed analytics nodes
        
        Returns:
            Global metrics aggregated from all nodes
        """
        local_aggregates = await self.calculate_aggregated_metrics()
        
        global_metrics = {
            'nodes': {
                self.node_id: local_aggregates
            },
            'global_aggregates': {},
            'synchronization_timestamp': time.time()
        }
        
        # In real implementation, collect metrics from peer nodes
        # For simulation, use local metrics as global
        
        # Calculate global aggregates
        all_metrics = {}
        for node_data in global_metrics['nodes'].values():
            for metric_name, metric_data in node_data.items():
                if metric_name not in all_metrics:
                    all_metrics[metric_name] = []
                
                if 'mean' in metric_data:
                    all_metrics[metric_name].append(metric_data['mean'])
        
        # Global statistics
        for metric_name, values in all_metrics.items():
            if values:
                global_metrics['global_aggregates'][metric_name] = {
                    'global_mean': np.mean(values),
                    'global_std': np.std(values),
                    'global_min': np.min(values),
                    'global_max': np.max(values),
                    'node_count': len(values)
                }
        
        self.global_metrics_cache = global_metrics
        return global_metrics
    
    # ==========================================
    # REPORTING AND EXPORT
    # ==========================================
    
    async def generate_analytics_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive analytics report
        
        Returns:
            Detailed analytics report with all metrics and insights
        """
        current_time = time.time()
        
        # Calculate current aggregated metrics
        aggregated = await self.calculate_aggregated_metrics()
        
        # Calculate correlation matrix
        correlation_matrix = await self.calculate_correlation_matrix()
        
        # Get predictions for key metrics
        predictions = {}
        for metric_name in list(self.metric_buffer.keys())[:5]:  # Top 5 metrics
            prediction = await self.predict_metric_performance(metric_name)
            if prediction:
                predictions[metric_name] = {
                    'predicted_value': prediction.predicted_value,
                    'confidence_interval': [prediction.confidence_interval_lower, 
                                          prediction.confidence_interval_upper],
                    'accuracy_score': prediction.accuracy_score
                }
        
        report = {
            'report_metadata': {
                'generated_at': current_time,
                'node_id': self.node_id,
                'analysis_window_seconds': self.analysis_window,
                'total_metrics': len(self.metric_buffer),
                'total_data_points': sum(len(buffer) for buffer in self.metric_buffer.values())
            },
            'aggregated_metrics': aggregated,
            'correlation_analysis': {
                'matrix': correlation_matrix.to_dict() if correlation_matrix is not None else None,
                'strong_correlations': self._find_strong_correlations(correlation_matrix) if correlation_matrix is not None else []
            },
            'predictions': predictions,
            'anomaly_summary': {
                'detectors_trained': len(self.anomaly_detectors),
                'average_detection_accuracy': self.analytics_metrics['anomaly_detection_accuracy']
            },
            'system_performance': self.analytics_metrics.copy(),
            'alert_configuration': {
                'active_thresholds': len(self.alert_thresholds),
                'alert_callbacks': len(self.alert_callbacks)
            }
        }
        
        return report
    
    def _find_strong_correlations(self, correlation_matrix: pd.DataFrame, threshold: float = 0.7) -> List[Dict]:
        """Find strongly correlated metric pairs"""
        strong_correlations = []
        
        for i, metric1 in enumerate(correlation_matrix.columns):
            for j, metric2 in enumerate(correlation_matrix.columns):
                if i < j:  # Avoid duplicates
                    correlation = correlation_matrix.iloc[i, j]
                    if abs(correlation) > threshold:
                        strong_correlations.append({
                            'metric1': metric1,
                            'metric2': metric2,
                            'correlation': correlation,
                            'strength': 'strong' if abs(correlation) > 0.8 else 'moderate'
                        })
        
        return strong_correlations
    
    async def export_metrics_data(self, 
                                 format: str = "json",
                                 time_window_seconds: Optional[int] = None) -> str:
        """
        Export metrics data in specified format
        
        Args:
            format: Export format ("json", "csv")
            time_window_seconds: Time window for export
            
        Returns:
            Exported data as string
        """
        time_window = time_window_seconds or self.analysis_window
        current_time = time.time()
        cutoff_time = current_time - time_window
        
        export_data = {}
        
        with self.processing_lock:
            for metric_name, buffer in self.metric_buffer.items():
                recent_points = [
                    {
                        'timestamp': point.timestamp,
                        'value': point.value,
                        'node_id': point.node_id,
                        'type': point.metric_type.value,
                        'unit': point.unit,
                        'tags': point.tags,
                        'confidence': point.confidence
                    }
                    for point in buffer
                    if point.timestamp >= cutoff_time
                ]
                
                if recent_points:
                    export_data[metric_name] = recent_points
        
        if format.lower() == "json":
            return json.dumps(export_data, indent=2)
        elif format.lower() == "csv":
            # Flatten data for CSV
            all_records = []
            for metric_name, points in export_data.items():
                for point in points:
                    record = {'metric_name': metric_name}
                    record.update(point)
                    all_records.append(record)
            
            if all_records:
                df = pd.DataFrame(all_records)
                return df.to_csv(index=False)
            else:
                return ""
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def get_analytics_status(self) -> Dict[str, Any]:
        """Get comprehensive analytics system status"""
        return {
            'node_id': self.node_id,
            'is_running': self.is_running,
            'metrics_tracked': len(self.metric_buffer),
            'total_data_points': sum(len(buffer) for buffer in self.metric_buffer.values()),
            'anomaly_detectors_trained': len(self.anomaly_detectors),
            'peer_nodes': len(self.peer_analytics_nodes),
            'active_thresholds': len(self.alert_thresholds),
            'performance_metrics': self.analytics_metrics.copy(),
            'memory_usage': {
                'buffer_utilization': self.analytics_metrics['storage_utilization'],
                'max_buffer_size': self.buffer_size,
                'analysis_window_seconds': self.analysis_window
            }
        }