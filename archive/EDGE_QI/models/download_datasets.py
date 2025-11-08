"""
EDGE-QI Dataset Download and Preparation Script

Downloads and prepares datasets for training EDGE-QI models:
- VisDrone2019 Detection Dataset
- UA-DETRAC Video Dataset (optional)
- Historical traffic data generation

Usage:
    python download_datasets.py --dataset visdrone --extract
    python download_datasets.py --all --output ../datasets/
"""

import os
import sys
import json
import argparse
import logging
import zipfile
import tarfile
import requests
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse
from tqdm import tqdm
import cv2
import numpy as np
import random
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Dataset registry
DATASETS = {
    "visdrone": {
        "name": "VisDrone2019 Detection Dataset",
        "description": "Aerial vehicle detection dataset perfect for traffic monitoring",
        "files": [
            {
                "url": "https://drive.google.com/uc?id=1a2oHjcEcwXP8oUF95qiwrqzACb2YlUhn",
                "filename": "VisDrone2019-DET-train.zip",
                "size_gb": 2.8,
                "extract_to": "VisDrone2019-DET-train/"
            },
            {
                "url": "https://drive.google.com/uc?id=1bxK5zgLn0_L8x276eKkuYA_FzwCIjb59", 
                "filename": "VisDrone2019-DET-val.zip",
                "size_gb": 0.3,
                "extract_to": "VisDrone2019-DET-val/"
            },
            {
                "url": "https://drive.google.com/uc?id=1PFdW_VFSCfZ_sTSZAGjQdifF_Xd5mf0V",
                "filename": "VisDrone2019-DET-test-dev.zip", 
                "size_gb": 0.3,
                "extract_to": "VisDrone2019-DET-test-dev/"
            }
        ],
        "classes": [
            "ignored regions", "pedestrian", "people", "bicycle", "car",
            "van", "truck", "tricycle", "awning-tricycle", "bus", "motor"
        ],
        "focus_classes": ["car", "van", "truck", "bus"],  # Vehicle classes for traffic
        "total_images": 8599,
        "annotation_format": "YOLO"
    },
    
    "ua_detrac": {
        "name": "UA-DETRAC Vehicle Detection Dataset",
        "description": "Video dataset for vehicle detection and tracking",
        "files": [
            {
                "url": "http://detrac-db.rit.albany.edu/Data/DETRAC-train-data.zip",
                "filename": "DETRAC-train-data.zip",
                "size_gb": 8.5,
                "extract_to": "DETRAC-train-data/"
            }
        ],
        "classes": ["car", "bus", "van", "others"],
        "total_videos": 60,
        "annotation_format": "XML"
    }
}

class DatasetDownloader:
    """
    Dataset downloader and processor for EDGE-QI platform.
    """
    
    def __init__(self, output_dir: str = "../datasets"):
        """Initialize downloader."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized DatasetDownloader with output dir: {self.output_dir}")
    
    def download_file(self, url: str, filepath: str, expected_size_gb: Optional[float] = None) -> bool:
        """
        Download a file with progress bar.
        
        Args:
            url: Download URL
            filepath: Local file path
            expected_size_gb: Expected file size in GB
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"Downloading {url}")
            logger.info(f"Saving to: {filepath}")
            
            # Handle Google Drive URLs
            if "drive.google.com" in url:
                return self.download_from_google_drive(url, filepath)
            
            # Regular HTTP download
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as f, tqdm(
                desc=os.path.basename(filepath),
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
            
            # Verify file size
            if expected_size_gb:
                actual_size_gb = os.path.getsize(filepath) / (1024**3)
                if abs(actual_size_gb - expected_size_gb) > expected_size_gb * 0.1:
                    logger.warning(f"File size mismatch. Expected: {expected_size_gb:.1f}GB, Got: {actual_size_gb:.1f}GB")
            
            logger.info(f"✅ Downloaded: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Download failed: {str(e)}")
            return False
    
    def download_from_google_drive(self, url: str, filepath: str) -> bool:
        """
        Download file from Google Drive.
        
        Note: This is a simplified implementation. For large files,
        you might need to handle Google Drive's virus scan warnings.
        """
        try:
            import gdown
            
            # Extract file ID from URL
            if "id=" in url:
                file_id = url.split("id=")[1].split("&")[0]
            else:
                file_id = url.split("/")[-2]
            
            # Download using gdown
            download_url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(download_url, filepath, quiet=False)
            
            return True
            
        except ImportError:
            logger.error("gdown not installed. Install with: pip install gdown")
            return False
        except Exception as e:
            logger.error(f"Google Drive download failed: {str(e)}")
            return False
    
    def extract_archive(self, archive_path: str, extract_to: str) -> bool:
        """
        Extract zip or tar archive.
        
        Args:
            archive_path: Path to archive file
            extract_to: Extraction directory
            
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"Extracting {archive_path} to {extract_to}")
            
            # Create extraction directory
            Path(extract_to).mkdir(parents=True, exist_ok=True)
            
            if archive_path.endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
                    
            elif archive_path.endswith(('.tar', '.tar.gz', '.tgz')):
                with tarfile.open(archive_path, 'r:*') as tar_ref:
                    tar_ref.extractall(extract_to)
                    
            else:
                logger.error(f"Unsupported archive format: {archive_path}")
                return False
            
            logger.info(f"✅ Extracted: {extract_to}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Extraction failed: {str(e)}")
            return False
    
    def convert_visdrone_annotations(self, dataset_dir: str) -> bool:
        """
        Convert VisDrone annotations to YOLO format.
        
        Args:
            dataset_dir: VisDrone dataset directory
            
        Returns:
            bool: Success status
        """
        try:
            logger.info("Converting VisDrone annotations to YOLO format...")
            
            # VisDrone class mapping (0-indexed for YOLO)
            class_mapping = {
                1: 0,  # pedestrian
                2: 1,  # people
                3: 2,  # bicycle
                4: 3,  # car
                5: 4,  # van
                6: 5,  # truck
                7: 6,  # tricycle
                8: 7,  # awning-tricycle
                9: 8,  # bus
                10: 9  # motor
            }
            
            # Process each split (train, val, test)
            for split in ['train', 'val', 'test-dev']:
                images_dir = os.path.join(dataset_dir, f"VisDrone2019-DET-{split}", "images")
                annotations_dir = os.path.join(dataset_dir, f"VisDrone2019-DET-{split}", "annotations")
                
                if not os.path.exists(annotations_dir):
                    logger.warning(f"Annotations directory not found: {annotations_dir}")
                    continue
                
                # Create YOLO labels directory
                labels_dir = os.path.join(dataset_dir, f"VisDrone2019-DET-{split}", "labels")
                Path(labels_dir).mkdir(parents=True, exist_ok=True)
                
                annotation_files = list(Path(annotations_dir).glob("*.txt"))
                
                for ann_file in tqdm(annotation_files, desc=f"Converting {split} annotations"):
                    # Read original annotation
                    with open(ann_file, 'r') as f:
                        lines = f.readlines()
                    
                    # Get corresponding image for dimensions
                    img_file = os.path.join(images_dir, ann_file.stem + ".jpg")
                    if not os.path.exists(img_file):
                        continue
                    
                    img = cv2.imread(img_file)
                    if img is None:
                        continue
                    
                    img_height, img_width = img.shape[:2]
                    
                    # Convert annotations
                    yolo_annotations = []
                    
                    for line in lines:
                        parts = line.strip().split(',')
                        if len(parts) < 8:
                            continue
                        
                        bbox_left = int(parts[0])
                        bbox_top = int(parts[1])
                        bbox_width = int(parts[2])
                        bbox_height = int(parts[3])
                        score = float(parts[4])
                        object_category = int(parts[5])
                        truncation = int(parts[6])
                        occlusion = int(parts[7])
                        
                        # Filter out ignored regions and low-quality annotations
                        if object_category == 0 or score == 0:  # ignored regions
                            continue
                        
                        if object_category not in class_mapping:
                            continue
                        
                        # Convert to YOLO format (normalized coordinates)
                        x_center = (bbox_left + bbox_width / 2) / img_width
                        y_center = (bbox_top + bbox_height / 2) / img_height
                        norm_width = bbox_width / img_width
                        norm_height = bbox_height / img_height
                        
                        # Map to YOLO class ID
                        yolo_class = class_mapping[object_category]
                        
                        yolo_annotations.append(f"{yolo_class} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}")
                    
                    # Save YOLO annotation
                    yolo_file = os.path.join(labels_dir, ann_file.stem + ".txt")
                    with open(yolo_file, 'w') as f:
                        f.write('\n'.join(yolo_annotations))
                
                logger.info(f"✅ Converted {len(annotation_files)} {split} annotations")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Annotation conversion failed: {str(e)}")
            return False
    
    def create_dataset_yaml(self, dataset_dir: str, dataset_name: str) -> str:
        """
        Create YOLO dataset configuration file.
        
        Args:
            dataset_dir: Dataset directory
            dataset_name: Name of dataset
            
        Returns:
            str: Path to created YAML file
        """
        dataset_info = DATASETS[dataset_name]
        
        yaml_content = f"""# EDGE-QI {dataset_info['name']} Configuration
# Generated by download_datasets.py

path: {os.path.abspath(dataset_dir)}
train: VisDrone2019-DET-train/images
val: VisDrone2019-DET-val/images  
test: VisDrone2019-DET-test-dev/images

# Classes
nc: {len(dataset_info['focus_classes'])}  # number of classes
names: {dataset_info['focus_classes']}  # class names

# Original VisDrone classes (for reference)
# original_classes: {dataset_info['classes']}

# Dataset info
dataset_name: "{dataset_info['name']}"
total_images: {dataset_info.get('total_images', 'unknown')}
annotation_format: "{dataset_info['annotation_format']}"
created: "{datetime.now().isoformat()}"

# Training recommendations
imgsz: 640  # input image size
batch_size: 32  # recommended batch size
epochs: 100  # recommended training epochs
"""
        
        yaml_path = os.path.join(dataset_dir, "dataset.yaml")
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)
        
        logger.info(f"Created dataset configuration: {yaml_path}")
        return yaml_path
    
    def generate_historical_data(self, output_dir: str) -> bool:
        """
        Generate synthetic historical traffic data for Algorithm 2.
        
        Args:
            output_dir: Output directory for historical data
            
        Returns:
            bool: Success status
        """
        try:
            logger.info("Generating synthetic historical traffic data...")
            
            historical_dir = os.path.join(output_dir, "historical_data")
            Path(historical_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate queue averages for each intersection
            intersections = ["intersection_1", "intersection_2", "intersection_3"]
            days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            
            queue_data = {}
            
            for intersection in intersections:
                queue_data[intersection] = {}
                
                for day in days_of_week:
                    queue_data[intersection][day] = {}
                    
                    # Generate 24 hours of data in 15-minute intervals
                    for hour in range(24):
                        for minute in [0, 15, 30, 45]:
                            time_key = f"{hour:02d}:{minute:02d}"
                            
                            # Model realistic traffic patterns
                            base_queue = self.get_base_queue_length(hour, minute, day)
                            
                            # Add some randomness
                            noise = np.random.normal(0, base_queue * 0.2)
                            mean_queue = max(0, base_queue + noise)
                            std_dev = max(0.5, base_queue * 0.3)
                            
                            queue_data[intersection][day][time_key] = {
                                "mean": round(mean_queue, 2),
                                "std_dev": round(std_dev, 2),
                                "samples": 120  # 4 weeks of data
                            }
            
            # Save queue averages
            queue_file = os.path.join(historical_dir, "queue_averages.json")
            with open(queue_file, 'w') as f:
                json.dump(queue_data, f, indent=2)
            
            # Generate traffic patterns CSV
            self.generate_traffic_patterns_csv(historical_dir)
            
            logger.info(f"✅ Generated historical data in: {historical_dir}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Historical data generation failed: {str(e)}")
            return False
    
    def get_base_queue_length(self, hour: int, minute: int, day: str) -> float:
        """
        Calculate base queue length based on time and day.
        
        Models realistic traffic patterns:
        - Morning rush: 7-9 AM
        - Evening rush: 5-7 PM
        - Weekend traffic is lighter
        - Night traffic is minimal
        """
        time_decimal = hour + minute / 60.0
        
        # Weekend factor
        weekend_factor = 0.7 if day in ["saturday", "sunday"] else 1.0
        
        # Base queue by time of day
        if 7 <= time_decimal <= 9:  # Morning rush
            base = 15 + 10 * np.sin((time_decimal - 7) * np.pi / 2)
        elif 17 <= time_decimal <= 19:  # Evening rush
            base = 18 + 8 * np.sin((time_decimal - 17) * np.pi / 2)
        elif 6 <= time_decimal <= 22:  # Regular daytime
            base = 8 + 3 * np.sin((time_decimal - 6) * np.pi / 16)
        else:  # Night time
            base = 1 + 2 * np.random.random()
        
        return base * weekend_factor
    
    def generate_traffic_patterns_csv(self, output_dir: str):
        """Generate traffic patterns CSV file."""
        import pandas as pd
        
        # Generate 30 days of traffic pattern data
        data = []
        start_date = datetime.now() - timedelta(days=30)
        
        for day in range(30):
            current_date = start_date + timedelta(days=day)
            day_name = current_date.strftime("%A").lower()
            
            # Generate hourly data
            for hour in range(24):
                for intersection in ["intersection_1", "intersection_2", "intersection_3"]:
                    # Base traffic for this hour
                    base_queue = self.get_base_queue_length(hour, 0, day_name)
                    
                    # Add daily variation
                    daily_factor = 0.8 + 0.4 * np.random.random()
                    queue_length = max(0, base_queue * daily_factor)
                    
                    # Calculate derived metrics
                    vehicle_count = int(queue_length * (1.2 + 0.6 * np.random.random()))
                    avg_speed = max(5, 25 - queue_length * 0.8 + np.random.normal(0, 3))
                    density = vehicle_count / max(1, avg_speed)
                    
                    data.append({
                        'date': current_date.strftime("%Y-%m-%d"),
                        'hour': hour,
                        'intersection': intersection,
                        'day_of_week': day_name,
                        'queue_length': round(queue_length, 2),
                        'vehicle_count': vehicle_count,
                        'average_speed': round(avg_speed, 2),
                        'density': round(density, 3)
                    })
        
        # Save to CSV
        df = pd.DataFrame(data)
        csv_file = os.path.join(output_dir, "traffic_patterns.csv")
        df.to_csv(csv_file, index=False)
        
        logger.info(f"Generated traffic patterns CSV: {csv_file}")
    
    def download_dataset(self, dataset_name: str, extract: bool = True) -> bool:
        """
        Download and prepare a dataset.
        
        Args:
            dataset_name: Name of dataset to download
            extract: Whether to extract archives
            
        Returns:
            bool: Success status
        """
        if dataset_name not in DATASETS:
            logger.error(f"Unknown dataset: {dataset_name}")
            logger.error(f"Available datasets: {list(DATASETS.keys())}")
            return False
        
        dataset_info = DATASETS[dataset_name]
        logger.info(f"Downloading {dataset_info['name']}")
        
        dataset_dir = self.output_dir / dataset_name
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        # Download all files for this dataset
        all_success = True
        
        for file_info in dataset_info['files']:
            filename = file_info['filename']
            filepath = dataset_dir / filename
            
            # Skip if file already exists
            if filepath.exists():
                logger.info(f"File already exists: {filepath}")
                continue
            
            # Download file
            success = self.download_file(
                file_info['url'],
                str(filepath),
                file_info.get('size_gb')
            )
            
            if not success:
                all_success = False
                continue
            
            # Extract if requested
            if extract and filename.endswith(('.zip', '.tar', '.tar.gz', '.tgz')):
                extract_dir = dataset_dir / file_info['extract_to']
                success = self.extract_archive(str(filepath), str(extract_dir))
                
                if not success:
                    all_success = False
        
        if all_success:
            # Post-processing for specific datasets
            if dataset_name == 'visdrone':
                self.convert_visdrone_annotations(str(dataset_dir))
                self.create_dataset_yaml(str(dataset_dir), dataset_name)
            
            logger.info(f"✅ Dataset {dataset_name} ready for training")
        else:
            logger.error(f"❌ Some files failed to download for {dataset_name}")
        
        return all_success

def main():
    """Main download function."""
    parser = argparse.ArgumentParser(description="Download EDGE-QI datasets")
    parser.add_argument(
        "--dataset",
        choices=list(DATASETS.keys()) + ["all"],
        default="visdrone",
        help="Dataset to download"
    )
    parser.add_argument(
        "--output",
        default="../datasets",
        help="Output directory for datasets"
    )
    parser.add_argument(
        "--extract",
        action="store_true",
        help="Extract downloaded archives"
    )
    parser.add_argument(
        "--historical-data",
        action="store_true",
        help="Generate synthetic historical traffic data"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available datasets"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("\nAvailable Datasets:")
        print("=" * 50)
        for name, info in DATASETS.items():
            print(f"\n{name}:")
            print(f"  Name: {info['name']}")
            print(f"  Description: {info['description']}")
            total_size = sum(f.get('size_gb', 0) for f in info['files'])
            print(f"  Total Size: {total_size:.1f} GB")
            print(f"  Classes: {', '.join(info['classes'])}")
        return
    
    # Initialize downloader
    downloader = DatasetDownloader(args.output)
    
    logger.info("Starting EDGE-QI dataset download...")
    
    try:
        # Download datasets
        if args.dataset == "all":
            datasets_to_download = list(DATASETS.keys())
        else:
            datasets_to_download = [args.dataset]
        
        success_count = 0
        
        for dataset in datasets_to_download:
            logger.info(f"\n{'='*50}")
            logger.info(f"Processing {dataset}")
            logger.info(f"{'='*50}")
            
            success = downloader.download_dataset(dataset, args.extract)
            if success:
                success_count += 1
        
        # Generate historical data if requested
        if args.historical_data:
            logger.info(f"\n{'='*50}")
            logger.info("Generating Historical Data")
            logger.info(f"{'='*50}")
            
            downloader.generate_historical_data(args.output)
        
        # Summary
        logger.info(f"\n{'='*50}")
        logger.info("DOWNLOAD SUMMARY")
        logger.info(f"{'='*50}")
        logger.info(f"Successfully downloaded: {success_count}/{len(datasets_to_download)} datasets")
        
        if success_count == len(datasets_to_download):
            logger.info("\n🎉 All datasets downloaded successfully!")
            logger.info("Next steps:")
            logger.info("  1. Run 'python train_yolo.py' to train models")
            logger.info("  2. Check dataset.yaml files for training configuration")
            logger.info("  3. Verify data quality with sample visualizations")
        else:
            logger.error(f"\n❌ {len(datasets_to_download) - success_count} datasets failed to download")
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("\n⏹️  Download interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n💥 Download failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()