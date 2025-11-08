"""
Bandwidth Optimization Module for EDGE-QI Framework

This module provides intelligent bandwidth management and optimization for efficient
edge-to-cloud communication in distributed surveillance systems.

Components:
- Data Compression: Smart compression algorithms with adaptive quality control
- Bitrate Streaming: Adaptive bitrate streaming for video and data transmission
- Priority Transfer: Priority-based data transfer with QoS management
- Bandwidth Monitor: Real-time bandwidth monitoring and prediction
"""

from .data_compressor import DataCompressor, CompressionMethod, CompressionResult
from .adaptive_streaming import AdaptiveStreamer, StreamingProfile, BitrateSettings
from .priority_transfer import PriorityTransferManager, DataPriority, TransferRequest
from .bandwidth_monitor import BandwidthMonitor, BandwidthMetrics, NetworkCondition

__all__ = [
    'DataCompressor',
    'CompressionMethod', 
    'CompressionResult',
    'AdaptiveStreamer',
    'StreamingProfile',
    'BitrateSettings',
    'PriorityTransferManager',
    'DataPriority',
    'TransferRequest', 
    'BandwidthMonitor',
    'BandwidthMetrics',
    'NetworkCondition'
]