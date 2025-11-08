from ultralytics import YOLO
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# Class names
class_names = {
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

# Load trained model
model = YOLO('/home/tilak/my_projects/EDGE_QI/models/trained/yolov8n_visdrone_20251101_194104/weights/best.pt')

# Val images
val_dir = '/home/tilak/my_projects/EDGE_QI/datasets/visdrone/images/val'
val_images = os.listdir(val_dir)[:5]  # First 5

def visualize_predictions(image_file):
    img_path = os.path.join(val_dir, image_file)
    img = Image.open(img_path)
    fig, ax = plt.subplots(1)
    ax.imshow(img)

    # Run inference
    results = model(img_path, conf=0.25)  # Low conf for more detections

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = box.conf[0].cpu().numpy()
            cls = int(box.cls[0].cpu().numpy())

            # Draw rectangle
            rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, edgecolor='b', facecolor='none')
            ax.add_patch(rect)

            # Add label with conf
            label = f'{class_names[cls]} {conf:.2f}'
            ax.text(x1, y1, label, color='blue', fontsize=12, backgroundcolor='white')

    ax.axis('off')
    plt.title(f'Predictions: {image_file}')
    plt.savefig(f'/home/tilak/my_projects/EDGE_QI/{image_file.replace(".jpg", "_pred.png")}')
    plt.close()

# Visualize each
for img_file in val_images:
    if img_file.endswith('.jpg'):
        visualize_predictions(img_file)

print("Prediction visualization complete.")