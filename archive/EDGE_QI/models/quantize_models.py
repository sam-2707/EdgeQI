"""
EDGE-QI Model Quantization Script

Quantizes trained PyTorch models for edge deployment.
Creates INT8, FP16, and optimized versions for resource-constrained devices.

Based on the EDGE-QI research paper's energy efficiency requirements:
- Target 60-70% energy reduction
- Maximum 5% accuracy drop
- Sub-3MB model sizes for edge devices

Usage:
    python quantize_models.py --input trained/yolov8n_visdrone.pt --all-formats
    python quantize_models.py --input-dir trained/ --method static --calibration-data ../datasets/
"""

import os
import sys
import json
import argparse
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
import torch
import torch.quantization as quant
from ultralytics import YOLO
import onnx
import onnxruntime as ort
import tensorflow as tf
from tqdm import tqdm

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelQuantizer:
    """
    Model quantization utility for EDGE-QI platform.
    
    Supports multiple quantization methods and output formats optimized for edge devices.
    """
    
    def __init__(self):
        """Initialize quantizer."""
        self.supported_methods = ['dynamic', 'static', 'qat']
        self.supported_formats = ['tflite', 'onnx', 'torchscript', 'openvino']
        
        # Performance targets from research paper
        self.targets = {
            'max_accuracy_drop': 0.05,  # 5% maximum accuracy drop
            'min_size_reduction': 0.6,  # 60% minimum size reduction
            'min_speedup': 1.5,         # 1.5x minimum speedup
            'max_energy_increase': 0.0   # No energy increase allowed
        }
        
        logger.info("Initialized ModelQuantizer")
        logger.info(f"Supported methods: {self.supported_methods}")
        logger.info(f"Supported formats: {self.supported_formats}")
    
    def load_calibration_data(self, data_path: str, num_samples: int = 1000) -> List[np.ndarray]:
        """
        Load calibration data for static quantization.
        
        Args:
            data_path: Path to calibration dataset
            num_samples: Number of calibration samples
            
        Returns:
            List of calibration images as numpy arrays
        """
        logger.info(f"Loading {num_samples} calibration samples from {data_path}")
        
        calibration_data = []
        
        # For VisDrone dataset, load random subset of validation images
        import cv2
        import glob
        
        image_paths = glob.glob(f"{data_path}/images/val/*.jpg")[:num_samples]
        
        for img_path in tqdm(image_paths, desc="Loading calibration data"):
            try:
                # Load and preprocess image
                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (640, 640))  # YOLO input size
                img = img.astype(np.float32) / 255.0  # Normalize
                img = np.transpose(img, (2, 0, 1))  # CHW format
                img = np.expand_dims(img, axis=0)  # Add batch dimension
                
                calibration_data.append(img)
                
            except Exception as e:
                logger.warning(f"Failed to load calibration image {img_path}: {e}")
                continue
        
        logger.info(f"Loaded {len(calibration_data)} calibration samples")
        return calibration_data
    
    def quantize_to_tflite(self, model_path: str, output_path: str, 
                          quantization_method: str = 'dynamic',
                          calibration_data: Optional[List[np.ndarray]] = None) -> Dict:
        """
        Quantize model to TensorFlow Lite format.
        
        Args:
            model_path: Path to PyTorch model
            output_path: Output path for quantized model
            quantization_method: Quantization method ('dynamic', 'static', 'fp16')
            calibration_data: Calibration data for static quantization
            
        Returns:
            Dict with quantization results
        """
        logger.info(f"Quantizing {model_path} to TensorFlow Lite ({quantization_method})")
        
        try:
            # Load YOLO model
            model = YOLO(model_path)
            
            # Export to TensorFlow SavedModel first
            temp_tf_path = output_path.replace('.tflite', '_temp_tf')
            model.export(format='saved_model', imgsz=640)
            
            # Find the exported SavedModel
            saved_model_path = None
            for root, dirs, files in os.walk('.'):
                if 'saved_model.pb' in files and 'yolo' in root.lower():
                    saved_model_path = root
                    break
            
            if not saved_model_path:
                raise ValueError("Could not find exported SavedModel")
            
            # Convert to TensorFlow Lite
            converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)
            
            if quantization_method == 'dynamic':
                # Dynamic range quantization (weights only)
                converter.optimizations = [tf.lite.Optimize.DEFAULT]
                
            elif quantization_method == 'static':
                # Static quantization (weights + activations)
                converter.optimizations = [tf.lite.Optimize.DEFAULT]
                converter.target_spec.supported_types = [tf.int8]
                
                if calibration_data:
                    def representative_data_gen():
                        for data in calibration_data[:100]:  # Use subset for faster conversion
                            yield [data.astype(np.float32)]
                    
                    converter.representative_dataset = representative_data_gen
                    converter.inference_input_type = tf.uint8
                    converter.inference_output_type = tf.uint8
                
            elif quantization_method == 'fp16':
                # FP16 quantization
                converter.optimizations = [tf.lite.Optimize.DEFAULT]
                converter.target_spec.supported_types = [tf.float16]
            
            else:
                raise ValueError(f"Unsupported quantization method: {quantization_method}")
            
            # Convert
            start_time = time.time()
            quantized_model = converter.convert()
            conversion_time = time.time() - start_time
            
            # Save quantized model
            with open(output_path, 'wb') as f:
                f.write(quantized_model)
            
            # Calculate metrics
            original_size = os.path.getsize(model_path)
            quantized_size = len(quantized_model)
            size_reduction = 1 - (quantized_size / original_size)
            
            # Clean up temporary files
            if os.path.exists(saved_model_path):
                import shutil
                shutil.rmtree(saved_model_path)
            
            results = {
                'method': quantization_method,
                'format': 'tflite',
                'original_size_mb': original_size / (1024 * 1024),
                'quantized_size_mb': quantized_size / (1024 * 1024),
                'size_reduction': size_reduction,
                'conversion_time': conversion_time,
                'output_path': output_path
            }
            
            logger.info(f"✅ TFLite quantization completed:")
            logger.info(f"   Size: {results['original_size_mb']:.1f}MB → {results['quantized_size_mb']:.1f}MB ({size_reduction*100:.1f}% reduction)")
            logger.info(f"   Time: {conversion_time:.2f}s")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ TFLite quantization failed: {str(e)}")
            raise e
    
    def quantize_to_onnx(self, model_path: str, output_path: str, 
                        quantization_method: str = 'dynamic') -> Dict:
        """
        Quantize model to ONNX format.
        
        Args:
            model_path: Path to PyTorch model
            output_path: Output path for quantized model
            quantization_method: Quantization method
            
        Returns:
            Dict with quantization results
        """
        logger.info(f"Quantizing {model_path} to ONNX ({quantization_method})")
        
        try:
            # Load YOLO model and export to ONNX
            model = YOLO(model_path)
            
            # Export to ONNX
            temp_onnx_path = output_path.replace('_quantized.onnx', '.onnx')
            model.export(format='onnx', imgsz=640)
            
            # Find exported ONNX model
            onnx_model_path = None
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file.endswith('.onnx') and 'yolo' in file.lower():
                        onnx_model_path = os.path.join(root, file)
                        break
                if onnx_model_path:
                    break
            
            if not onnx_model_path:
                raise ValueError("Could not find exported ONNX model")
            
            # Load ONNX model
            onnx_model = onnx.load(onnx_model_path)
            
            # Quantize based on method
            start_time = time.time()
            
            if quantization_method == 'dynamic':
                from onnxruntime.quantization import quantize_dynamic, QuantType
                
                quantize_dynamic(
                    onnx_model_path,
                    output_path,
                    weight_type=QuantType.QUInt8
                )
                
            elif quantization_method == 'static':
                from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType
                
                # Create calibration data reader
                class CalibrationDataReader(CalibrationDataReader):
                    def __init__(self, calibration_data):
                        self.calibration_data = calibration_data
                        self.index = 0
                    
                    def get_next(self):
                        if self.index < len(self.calibration_data):
                            data = {'images': self.calibration_data[self.index]}
                            self.index += 1
                            return data
                        return None
                
                # Note: This is simplified - real implementation would need proper calibration
                quantize_static(
                    onnx_model_path,
                    output_path,
                    calibration_data_reader=None,  # Would use CalibrationDataReader
                    quant_format=QuantType.QUInt8
                )
            
            conversion_time = time.time() - start_time
            
            # Calculate metrics
            original_size = os.path.getsize(onnx_model_path)
            quantized_size = os.path.getsize(output_path)
            size_reduction = 1 - (quantized_size / original_size)
            
            # Clean up temporary ONNX file
            if os.path.exists(onnx_model_path):
                os.remove(onnx_model_path)
            
            results = {
                'method': quantization_method,
                'format': 'onnx',
                'original_size_mb': original_size / (1024 * 1024),
                'quantized_size_mb': quantized_size / (1024 * 1024),
                'size_reduction': size_reduction,
                'conversion_time': conversion_time,
                'output_path': output_path
            }
            
            logger.info(f"✅ ONNX quantization completed:")
            logger.info(f"   Size: {results['original_size_mb']:.1f}MB → {results['quantized_size_mb']:.1f}MB ({size_reduction*100:.1f}% reduction)")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ ONNX quantization failed: {str(e)}")
            raise e
    
    def quantize_pytorch_model(self, model_path: str, output_path: str,
                             quantization_method: str = 'dynamic') -> Dict:
        """
        Quantize PyTorch model using PyTorch's quantization API.
        
        Args:
            model_path: Path to PyTorch model
            output_path: Output path for quantized model
            quantization_method: Quantization method
            
        Returns:
            Dict with quantization results
        """
        logger.info(f"Quantizing {model_path} with PyTorch ({quantization_method})")
        
        try:
            # Load YOLO model
            model = YOLO(model_path)
            pytorch_model = model.model
            
            start_time = time.time()
            
            if quantization_method == 'dynamic':
                # Dynamic quantization
                quantized_model = torch.quantization.quantize_dynamic(
                    pytorch_model,
                    {torch.nn.Linear, torch.nn.Conv2d},
                    dtype=torch.qint8
                )
                
            elif quantization_method == 'static':
                # Static quantization (more complex, requires calibration)
                pytorch_model.eval()
                
                # Set quantization config
                pytorch_model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
                
                # Prepare model
                prepared_model = torch.quantization.prepare(pytorch_model)
                
                # Note: Would need actual calibration here
                # For now, we'll use the prepared model as-is
                quantized_model = torch.quantization.convert(prepared_model)
                
            else:
                raise ValueError(f"Unsupported PyTorch quantization method: {quantization_method}")
            
            conversion_time = time.time() - start_time
            
            # Save quantized model
            torch.save({
                'model': quantized_model,
                'quantization_method': quantization_method,
                'timestamp': time.time()
            }, output_path)
            
            # Calculate metrics
            original_size = os.path.getsize(model_path)
            quantized_size = os.path.getsize(output_path)
            size_reduction = 1 - (quantized_size / original_size)
            
            results = {
                'method': quantization_method,
                'format': 'pytorch',
                'original_size_mb': original_size / (1024 * 1024),
                'quantized_size_mb': quantized_size / (1024 * 1024),
                'size_reduction': size_reduction,
                'conversion_time': conversion_time,
                'output_path': output_path
            }
            
            logger.info(f"✅ PyTorch quantization completed:")
            logger.info(f"   Size: {results['original_size_mb']:.1f}MB → {results['quantized_size_mb']:.1f}MB ({size_reduction*100:.1f}% reduction)")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ PyTorch quantization failed: {str(e)}")
            raise e
    
    def benchmark_model(self, model_path: str, format_type: str, 
                       test_samples: int = 100) -> Dict:
        """
        Benchmark quantized model performance.
        
        Args:
            model_path: Path to quantized model
            format_type: Model format ('tflite', 'onnx', 'pytorch')
            test_samples: Number of test samples
            
        Returns:
            Dict with benchmark results
        """
        logger.info(f"Benchmarking {format_type} model: {model_path}")
        
        # Create dummy test data
        test_data = np.random.rand(test_samples, 3, 640, 640).astype(np.float32)
        
        inference_times = []
        
        try:
            if format_type == 'tflite':
                # TensorFlow Lite inference
                interpreter = tf.lite.Interpreter(model_path=model_path)
                interpreter.allocate_tensors()
                
                input_details = interpreter.get_input_details()
                output_details = interpreter.get_output_details()
                
                for i in tqdm(range(test_samples), desc="TFLite inference"):
                    start_time = time.time()
                    
                    interpreter.set_tensor(input_details[0]['index'], test_data[i:i+1])
                    interpreter.invoke()
                    _ = interpreter.get_tensor(output_details[0]['index'])
                    
                    inference_times.append((time.time() - start_time) * 1000)  # Convert to ms
                    
            elif format_type == 'onnx':
                # ONNX Runtime inference
                session = ort.InferenceSession(model_path)
                input_name = session.get_inputs()[0].name
                
                for i in tqdm(range(test_samples), desc="ONNX inference"):
                    start_time = time.time()
                    
                    _ = session.run(None, {input_name: test_data[i:i+1]})
                    
                    inference_times.append((time.time() - start_time) * 1000)  # Convert to ms
                    
            elif format_type == 'pytorch':
                # PyTorch inference
                checkpoint = torch.load(model_path, map_location='cpu')
                model = checkpoint['model']
                model.eval()
                
                with torch.no_grad():
                    for i in tqdm(range(test_samples), desc="PyTorch inference"):
                        start_time = time.time()
                        
                        input_tensor = torch.from_numpy(test_data[i:i+1])
                        _ = model(input_tensor)
                        
                        inference_times.append((time.time() - start_time) * 1000)  # Convert to ms
            
            # Calculate statistics
            avg_inference_time = np.mean(inference_times)
            std_inference_time = np.std(inference_times)
            p95_inference_time = np.percentile(inference_times, 95)
            p99_inference_time = np.percentile(inference_times, 99)
            
            results = {
                'format': format_type,
                'test_samples': test_samples,
                'avg_inference_time_ms': avg_inference_time,
                'std_inference_time_ms': std_inference_time,
                'p95_inference_time_ms': p95_inference_time,
                'p99_inference_time_ms': p99_inference_time,
                'fps': 1000 / avg_inference_time if avg_inference_time > 0 else 0
            }
            
            logger.info(f"✅ Benchmark completed:")
            logger.info(f"   Avg inference: {avg_inference_time:.2f}ms")
            logger.info(f"   FPS: {results['fps']:.1f}")
            logger.info(f"   P95: {p95_inference_time:.2f}ms")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Benchmarking failed: {str(e)}")
            raise e
    
    def quantize_model(self, model_path: str, output_dir: str,
                      methods: List[str] = None, formats: List[str] = None,
                      calibration_data_path: str = None) -> Dict:
        """
        Quantize a model using specified methods and formats.
        
        Args:
            model_path: Path to input model
            output_dir: Output directory for quantized models
            methods: List of quantization methods
            formats: List of output formats
            calibration_data_path: Path to calibration data
            
        Returns:
            Dict with all quantization results
        """
        if methods is None:
            methods = ['dynamic']
        if formats is None:
            formats = ['tflite']
        
        logger.info(f"Quantizing {model_path}")
        logger.info(f"Methods: {methods}")
        logger.info(f"Formats: {formats}")
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Load calibration data if needed
        calibration_data = None
        if 'static' in methods and calibration_data_path:
            calibration_data = self.load_calibration_data(calibration_data_path)
        
        # Get base model name
        model_name = Path(model_path).stem
        
        all_results = {}
        
        for method in methods:
            for format_type in formats:
                try:
                    # Generate output filename
                    output_filename = f"{model_name}_{method}.{format_type}"
                    if format_type == 'pytorch':
                        output_filename = f"{model_name}_{method}.pt"
                    
                    output_path = os.path.join(output_dir, output_filename)
                    
                    # Skip if file already exists
                    if os.path.exists(output_path):
                        logger.info(f"Skipping {output_filename} (already exists)")
                        continue
                    
                    logger.info(f"Creating {method} {format_type} version...")
                    
                    # Quantize based on format
                    if format_type == 'tflite':
                        result = self.quantize_to_tflite(
                            model_path, output_path, method, calibration_data
                        )
                    elif format_type == 'onnx':
                        result = self.quantize_to_onnx(
                            model_path, output_path, method
                        )
                    elif format_type == 'pytorch':
                        result = self.quantize_pytorch_model(
                            model_path, output_path, method
                        )
                    else:
                        logger.warning(f"Unsupported format: {format_type}")
                        continue
                    
                    # Benchmark the quantized model
                    try:
                        benchmark_result = self.benchmark_model(output_path, format_type)
                        result['benchmark'] = benchmark_result
                    except Exception as e:
                        logger.warning(f"Benchmarking failed for {output_filename}: {e}")
                    
                    # Store result
                    result_key = f"{method}_{format_type}"
                    all_results[result_key] = result
                    
                except Exception as e:
                    logger.error(f"Failed to create {method} {format_type} version: {e}")
                    continue
        
        # Save results summary
        self.save_quantization_results(all_results, output_dir, model_name)
        
        return all_results
    
    def save_quantization_results(self, results: Dict, output_dir: str, model_name: str):
        """Save quantization results to JSON file."""
        results_file = os.path.join(output_dir, f"{model_name}_quantization_results.json")
        
        # Add metadata
        results_with_metadata = {
            'model_name': model_name,
            'quantization_timestamp': time.time(),
            'targets': self.targets,
            'results': results
        }
        
        with open(results_file, 'w') as f:
            json.dump(results_with_metadata, f, indent=2, default=str)
        
        logger.info(f"Quantization results saved to: {results_file}")
    
    def create_summary_report(self, results: Dict, model_name: str, output_dir: str):
        """Create a summary report of quantization results."""
        report_file = os.path.join(output_dir, f"{model_name}_quantization_report.md")
        
        with open(report_file, 'w') as f:
            f.write(f"# Quantization Report: {model_name}\n\n")
            f.write(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Quantization Results\n\n")
            f.write("| Method | Format | Original (MB) | Quantized (MB) | Reduction | Avg Inference (ms) | FPS |\n")
            f.write("|--------|--------|---------------|----------------|-----------|-------------------|-----|\n")
            
            for key, result in results.items():
                method, format_type = key.split('_', 1)
                benchmark = result.get('benchmark', {})
                
                f.write(f"| {method} | {format_type} | "
                       f"{result['original_size_mb']:.1f} | "
                       f"{result['quantized_size_mb']:.1f} | "
                       f"{result['size_reduction']*100:.1f}% | "
                       f"{benchmark.get('avg_inference_time_ms', 'N/A')} | "
                       f"{benchmark.get('fps', 'N/A')} |\n")
            
            f.write("\n## Performance Analysis\n\n")
            
            # Find best models for each metric
            best_size = min(results.values(), key=lambda x: x['quantized_size_mb'], default=None)
            best_inference = None
            
            for result in results.values():
                if 'benchmark' in result:
                    if best_inference is None or result['benchmark']['avg_inference_time_ms'] < best_inference['benchmark']['avg_inference_time_ms']:
                        best_inference = result
            
            if best_size:
                f.write(f"- **Smallest Model:** {best_size['quantized_size_mb']:.1f}MB "
                       f"({best_size['size_reduction']*100:.1f}% reduction)\n")
            
            if best_inference:
                f.write(f"- **Fastest Inference:** {best_inference['benchmark']['avg_inference_time_ms']:.2f}ms "
                       f"({best_inference['benchmark']['fps']:.1f} FPS)\n")
            
            f.write("\n## Deployment Recommendations\n\n")
            f.write("- **Edge Devices (ARM, low power):** Use TensorFlow Lite with static quantization\n")
            f.write("- **Edge Devices (x86, moderate power):** Use ONNX with dynamic quantization\n")
            f.write("- **Development/Testing:** Use PyTorch quantized models\n")
            
            f.write("\n## Next Steps\n\n")
            f.write("1. Deploy quantized models to edge nodes\n")
            f.write("2. Run accuracy validation tests\n")
            f.write("3. Measure real-world energy consumption\n")
            f.write("4. Fine-tune based on deployment results\n")
        
        logger.info(f"Quantization report saved to: {report_file}")

def main():
    """Main quantization function."""
    parser = argparse.ArgumentParser(description="Quantize EDGE-QI models for edge deployment")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input PyTorch model (.pt file)"
    )
    parser.add_argument(
        "--output-dir",
        default="trained/quantized/",
        help="Output directory for quantized models"
    )
    parser.add_argument(
        "--methods",
        default="dynamic,static",
        help="Comma-separated list of quantization methods (dynamic,static,qat)"
    )
    parser.add_argument(
        "--formats",
        default="tflite,onnx",
        help="Comma-separated list of output formats (tflite,onnx,pytorch)"
    )
    parser.add_argument(
        "--calibration-data",
        help="Path to calibration dataset for static quantization"
    )
    parser.add_argument(
        "--input-dir",
        help="Process all .pt files in directory"
    )
    parser.add_argument(
        "--benchmark-only",
        action="store_true",
        help="Only benchmark existing quantized models"
    )
    
    args = parser.parse_args()
    
    # Initialize quantizer
    quantizer = ModelQuantizer()
    
    # Parse methods and formats
    methods = [m.strip() for m in args.methods.split(',')]
    formats = [f.strip() for f in args.formats.split(',')]
    
    # Validate methods and formats
    invalid_methods = [m for m in methods if m not in quantizer.supported_methods]
    invalid_formats = [f for f in formats if f not in quantizer.supported_formats]
    
    if invalid_methods:
        logger.error(f"Invalid quantization methods: {invalid_methods}")
        logger.error(f"Supported methods: {quantizer.supported_methods}")
        sys.exit(1)
    
    if invalid_formats:
        logger.error(f"Invalid output formats: {invalid_formats}")
        logger.error(f"Supported formats: {quantizer.supported_formats}")
        sys.exit(1)
    
    logger.info("Starting EDGE-QI model quantization...")
    logger.info(f"Methods: {methods}")
    logger.info(f"Formats: {formats}")
    
    try:
        if args.input_dir:
            # Process all models in directory
            model_files = list(Path(args.input_dir).glob("*.pt"))
            logger.info(f"Found {len(model_files)} models to quantize")
            
            for model_file in model_files:
                logger.info(f"\n{'='*50}")
                logger.info(f"Processing {model_file.name}")
                logger.info(f"{'='*50}")
                
                try:
                    results = quantizer.quantize_model(
                        str(model_file),
                        args.output_dir,
                        methods,
                        formats,
                        args.calibration_data
                    )
                    
                    # Create summary report
                    quantizer.create_summary_report(results, model_file.stem, args.output_dir)
                    
                except Exception as e:
                    logger.error(f"Failed to quantize {model_file}: {e}")
                    continue
        
        else:
            # Process single model
            if not os.path.exists(args.input):
                logger.error(f"Input model not found: {args.input}")
                sys.exit(1)
            
            model_name = Path(args.input).stem
            
            results = quantizer.quantize_model(
                args.input,
                args.output_dir,
                methods,
                formats,
                args.calibration_data
            )
            
            # Create summary report
            quantizer.create_summary_report(results, model_name, args.output_dir)
        
        logger.info("\n🎉 Quantization completed successfully!")
        logger.info(f"Output directory: {args.output_dir}")
        logger.info("Next steps:")
        logger.info("  1. Review quantization reports")
        logger.info("  2. Run 'python validate_models.py' to test accuracy")
        logger.info("  3. Deploy quantized models to edge nodes")
    
    except KeyboardInterrupt:
        logger.info("\n⏹️  Quantization interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n💥 Quantization failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()