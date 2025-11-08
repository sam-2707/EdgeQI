"""
Data Compression Module for EDGE-QI Framework

Provides intelligent data compression algorithms with adaptive quality control
for efficient bandwidth utilization in edge computing environments.
"""

import io
import gzip
import lzma
import zlib
import pickle
import json
import numpy as np
from enum import Enum
from typing import Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass
import time
import cv2
from PIL import Image


class CompressionMethod(Enum):
    """Available compression methods"""
    GZIP = "gzip"
    LZMA = "lzma"
    ZLIB = "zlib"
    JPEG = "jpeg"
    WEBP = "webp"
    H264 = "h264"
    ADAPTIVE = "adaptive"


@dataclass
class CompressionResult:
    """Result of compression operation"""
    compressed_data: bytes
    original_size: int
    compressed_size: int
    compression_ratio: float
    method_used: CompressionMethod
    compression_time: float
    quality_score: Optional[float] = None


class DataCompressor:
    """
    Intelligent data compressor with adaptive quality control
    """
    
    def __init__(self):
        self.compression_stats = {}
        self.adaptive_settings = {
            'image_quality': 85,
            'video_crf': 23,
            'data_compression_level': 6
        }
        
    def compress_data(self, 
                     data: Union[bytes, np.ndarray, Dict, Any],
                     method: CompressionMethod = CompressionMethod.ADAPTIVE,
                     quality: Optional[int] = None,
                     target_size: Optional[int] = None) -> CompressionResult:
        """
        Compress data using specified method with adaptive quality control
        
        Args:
            data: Data to compress (bytes, numpy array, dict, etc.)
            method: Compression method to use
            quality: Quality setting (0-100, higher = better quality)
            target_size: Target compressed size in bytes
            
        Returns:
            CompressionResult with compression details
        """
        start_time = time.time()
        
        # Determine data type and select optimal compression
        if method == CompressionMethod.ADAPTIVE:
            method = self._select_optimal_method(data)
        
        # Get original data size
        if isinstance(data, np.ndarray):
            original_data = data.tobytes()
            original_size = data.nbytes
        elif isinstance(data, (dict, list)):
            original_data = json.dumps(data, separators=(',', ':')).encode('utf-8')
            original_size = len(original_data)
        elif isinstance(data, bytes):
            original_data = data
            original_size = len(data)
        else:
            original_data = pickle.dumps(data)
            original_size = len(original_data)
        
        # Apply compression
        compressed_data, quality_score = self._apply_compression(
            data, original_data, method, quality, target_size
        )
        
        compression_time = time.time() - start_time
        compressed_size = len(compressed_data)
        compression_ratio = original_size / compressed_size if compressed_size > 0 else 1.0
        
        # Update statistics
        self._update_compression_stats(method, compression_ratio, compression_time)
        
        return CompressionResult(
            compressed_data=compressed_data,
            original_size=original_size,
            compressed_size=compressed_size,
            compression_ratio=compression_ratio,
            method_used=method,
            compression_time=compression_time,
            quality_score=quality_score
        )
    
    def decompress_data(self, 
                       compressed_data: bytes,
                       method: CompressionMethod,
                       original_shape: Optional[Tuple] = None,
                       data_type: Optional[str] = None) -> Any:
        """
        Decompress data using specified method
        
        Args:
            compressed_data: Compressed data bytes
            method: Method used for compression
            original_shape: Original shape for numpy arrays
            data_type: Original data type ('numpy', 'json', 'pickle', 'bytes')
            
        Returns:
            Decompressed data
        """
        try:
            if method == CompressionMethod.GZIP:
                decompressed = gzip.decompress(compressed_data)
            elif method == CompressionMethod.LZMA:
                decompressed = lzma.decompress(compressed_data)
            elif method == CompressionMethod.ZLIB:
                decompressed = zlib.decompress(compressed_data)
            elif method in [CompressionMethod.JPEG, CompressionMethod.WEBP]:
                # Image decompression
                image = Image.open(io.BytesIO(compressed_data))
                decompressed = np.array(image)
                return decompressed
            else:
                raise ValueError(f"Unsupported decompression method: {method}")
            
            # Convert back to original format
            if data_type == 'numpy' and original_shape:
                return np.frombuffer(decompressed, dtype=np.uint8).reshape(original_shape)
            elif data_type == 'json':
                return json.loads(decompressed.decode('utf-8'))
            elif data_type == 'pickle':
                return pickle.loads(decompressed)
            else:
                return decompressed
                
        except Exception as e:
            raise RuntimeError(f"Decompression failed: {e}")
    
    def _select_optimal_method(self, data: Any) -> CompressionMethod:
        """Select optimal compression method based on data type and characteristics"""
        if isinstance(data, np.ndarray):
            # Image or video frame
            if len(data.shape) == 3 and data.shape[2] in [1, 3, 4]:
                # Likely an image
                return CompressionMethod.WEBP
            else:
                # Numerical data
                return CompressionMethod.LZMA
        elif isinstance(data, (dict, list)):
            # JSON-serializable data
            return CompressionMethod.GZIP
        else:
            # General data
            return CompressionMethod.ZLIB
    
    def _apply_compression(self, 
                          original_data: Any,
                          serialized_data: bytes,
                          method: CompressionMethod,
                          quality: Optional[int],
                          target_size: Optional[int]) -> Tuple[bytes, Optional[float]]:
        """Apply the specified compression method"""
        quality_score = None
        
        if method == CompressionMethod.GZIP:
            level = self._get_compression_level(quality, 6)
            compressed = gzip.compress(serialized_data, compresslevel=level)
            
        elif method == CompressionMethod.LZMA:
            level = self._get_compression_level(quality, 6)
            compressed = lzma.compress(serialized_data, preset=level)
            
        elif method == CompressionMethod.ZLIB:
            level = self._get_compression_level(quality, 6)
            compressed = zlib.compress(serialized_data, level)
            
        elif method == CompressionMethod.JPEG:
            compressed, quality_score = self._compress_image_jpeg(
                original_data, quality or self.adaptive_settings['image_quality']
            )
            
        elif method == CompressionMethod.WEBP:
            compressed, quality_score = self._compress_image_webp(
                original_data, quality or self.adaptive_settings['image_quality']
            )
            
        else:
            # Fallback to gzip
            compressed = gzip.compress(serialized_data)
        
        # Adaptive quality adjustment if target size is specified
        if target_size and len(compressed) > target_size:
            compressed, quality_score = self._adjust_for_target_size(
                original_data, method, target_size
            )
        
        return compressed, quality_score
    
    def _compress_image_jpeg(self, image_data: np.ndarray, quality: int) -> Tuple[bytes, float]:
        """Compress image using JPEG with specified quality"""
        if isinstance(image_data, np.ndarray):
            # Convert numpy array to PIL Image
            if len(image_data.shape) == 3:
                if image_data.shape[2] == 4:  # RGBA
                    image = Image.fromarray(image_data, 'RGBA')
                    image = image.convert('RGB')  # JPEG doesn't support alpha
                else:  # RGB
                    image = Image.fromarray(image_data, 'RGB')
            else:  # Grayscale
                image = Image.fromarray(image_data, 'L')
        else:
            raise ValueError("Image data must be numpy array")
        
        # Compress to bytes
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        compressed_data = output.getvalue()
        
        # Calculate quality score (approximate)
        quality_score = quality / 100.0
        
        return compressed_data, quality_score
    
    def _compress_image_webp(self, image_data: np.ndarray, quality: int) -> Tuple[bytes, float]:
        """Compress image using WebP with specified quality"""
        if isinstance(image_data, np.ndarray):
            if len(image_data.shape) == 3:
                if image_data.shape[2] == 4:  # RGBA
                    image = Image.fromarray(image_data, 'RGBA')
                else:  # RGB
                    image = Image.fromarray(image_data, 'RGB')
            else:  # Grayscale
                image = Image.fromarray(image_data, 'L')
        else:
            raise ValueError("Image data must be numpy array")
        
        # Compress to bytes
        output = io.BytesIO()
        image.save(output, format='WebP', quality=quality, optimize=True)
        compressed_data = output.getvalue()
        
        # Calculate quality score
        quality_score = quality / 100.0
        
        return compressed_data, quality_score
    
    def _get_compression_level(self, quality: Optional[int], default: int) -> int:
        """Convert quality (0-100) to compression level"""
        if quality is None:
            return default
        
        # Convert quality to compression level (inverse relationship)
        # Higher quality = lower compression level for speed
        # Lower quality = higher compression level for size
        level = max(1, min(9, 10 - (quality // 10)))
        return level
    
    def _adjust_for_target_size(self, 
                               original_data: Any,
                               method: CompressionMethod,
                               target_size: int) -> Tuple[bytes, Optional[float]]:
        """Adjust compression parameters to meet target size"""
        if method in [CompressionMethod.JPEG, CompressionMethod.WEBP]:
            # Binary search for optimal quality
            min_quality, max_quality = 10, 95
            best_compressed = None
            best_quality_score = None
            
            for _ in range(8):  # Max 8 iterations
                mid_quality = (min_quality + max_quality) // 2
                
                if method == CompressionMethod.JPEG:
                    compressed, quality_score = self._compress_image_jpeg(
                        original_data, mid_quality
                    )
                else:  # WebP
                    compressed, quality_score = self._compress_image_webp(
                        original_data, mid_quality
                    )
                
                if len(compressed) <= target_size:
                    best_compressed = compressed
                    best_quality_score = quality_score
                    min_quality = mid_quality + 1
                else:
                    max_quality = mid_quality - 1
                
                if min_quality > max_quality:
                    break
            
            return best_compressed or compressed, best_quality_score or quality_score
        
        # For other methods, reduce compression level
        serialized_data = original_data.tobytes() if isinstance(original_data, np.ndarray) else original_data
        
        for level in range(9, 0, -1):  # Try highest compression first
            if method == CompressionMethod.GZIP:
                compressed = gzip.compress(serialized_data, compresslevel=level)
            elif method == CompressionMethod.LZMA:
                compressed = lzma.compress(serialized_data, preset=level)
            elif method == CompressionMethod.ZLIB:
                compressed = zlib.compress(serialized_data, level)
            else:
                compressed = gzip.compress(serialized_data)
            
            if len(compressed) <= target_size:
                return compressed, None
        
        # If still too large, return best effort
        return compressed, None
    
    def _update_compression_stats(self, 
                                 method: CompressionMethod,
                                 ratio: float,
                                 time_taken: float):
        """Update compression statistics for adaptive optimization"""
        if method not in self.compression_stats:
            self.compression_stats[method] = {
                'total_compressions': 0,
                'avg_ratio': 0.0,
                'avg_time': 0.0,
                'efficiency_score': 0.0
            }
        
        stats = self.compression_stats[method]
        stats['total_compressions'] += 1
        
        # Update running averages
        n = stats['total_compressions']
        stats['avg_ratio'] = ((n - 1) * stats['avg_ratio'] + ratio) / n
        stats['avg_time'] = ((n - 1) * stats['avg_time'] + time_taken) / n
        
        # Calculate efficiency score (ratio/time trade-off)
        stats['efficiency_score'] = stats['avg_ratio'] / max(stats['avg_time'], 0.001)
    
    def get_compression_stats(self) -> Dict[str, Dict[str, float]]:
        """Get compression statistics for all methods"""
        return dict(self.compression_stats)
    
    def get_optimal_method_for_target(self, 
                                    data_type: str,
                                    target_ratio: float = 2.0,
                                    max_time: float = 0.1) -> CompressionMethod:
        """
        Get optimal compression method based on requirements
        
        Args:
            data_type: Type of data ('image', 'numerical', 'text', 'mixed')
            target_ratio: Desired compression ratio
            max_time: Maximum acceptable compression time
            
        Returns:
            Optimal compression method
        """
        candidates = []
        
        # Filter methods based on data type
        if data_type == 'image':
            candidates = [CompressionMethod.WEBP, CompressionMethod.JPEG]
        elif data_type == 'numerical':
            candidates = [CompressionMethod.LZMA, CompressionMethod.ZLIB]
        elif data_type == 'text':
            candidates = [CompressionMethod.GZIP, CompressionMethod.ZLIB]
        else:  # mixed
            candidates = [CompressionMethod.GZIP, CompressionMethod.LZMA, CompressionMethod.ZLIB]
        
        # Select best method based on statistics
        best_method = candidates[0] if candidates else CompressionMethod.GZIP
        best_score = 0
        
        for method in candidates:
            if method in self.compression_stats:
                stats = self.compression_stats[method]
                
                # Score based on ratio and time constraints
                ratio_score = min(stats['avg_ratio'] / target_ratio, 1.0)
                time_score = 1.0 if stats['avg_time'] <= max_time else max_time / stats['avg_time']
                
                total_score = ratio_score * 0.7 + time_score * 0.3
                
                if total_score > best_score:
                    best_score = total_score
                    best_method = method
        
        return best_method
    
    def estimate_compression_ratio(self, 
                                 data_size: int,
                                 method: CompressionMethod,
                                 data_type: str = 'mixed') -> float:
        """
        Estimate compression ratio for given data size and method
        
        Args:
            data_size: Size of data in bytes
            method: Compression method
            data_type: Type of data
            
        Returns:
            Estimated compression ratio
        """
        if method in self.compression_stats:
            return self.compression_stats[method]['avg_ratio']
        
        # Default estimates based on method and data type
        estimates = {
            CompressionMethod.GZIP: {'image': 1.1, 'numerical': 2.5, 'text': 3.0, 'mixed': 2.0},
            CompressionMethod.LZMA: {'image': 1.2, 'numerical': 3.0, 'text': 3.5, 'mixed': 2.5},
            CompressionMethod.ZLIB: {'image': 1.1, 'numerical': 2.3, 'text': 2.8, 'mixed': 1.9},
            CompressionMethod.JPEG: {'image': 5.0, 'numerical': 1.0, 'text': 1.0, 'mixed': 2.0},
            CompressionMethod.WEBP: {'image': 6.0, 'numerical': 1.0, 'text': 1.0, 'mixed': 2.2},
        }
        
        return estimates.get(method, {}).get(data_type, 2.0)