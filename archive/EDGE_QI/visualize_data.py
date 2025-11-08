import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# Class names from dataset.yaml
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

# Paths
image_dir = '/home/tilak/my_projects/EDGE_QI/datasets/visdrone/images/train'
label_dir = '/home/tilak/my_projects/EDGE_QI/datasets/visdrone/labels/train'

# Select first 5 images
image_files = [
    '9999955_00000_d_0000318.jpg',
    '9999955_00000_d_0000319.jpg',
    '9999955_00000_d_0000320.jpg',
    '9999955_00000_d_0000321.jpg',
    '9999955_00000_d_0000322.jpg'
]

def visualize_image(image_file):
    # Load image
    img_path = os.path.join(image_dir, image_file)
    img = Image.open(img_path)
    fig, ax = plt.subplots(1)
    ax.imshow(img)

    # Load labels
    label_file = image_file.replace('.jpg', '.txt')
    label_path = os.path.join(label_dir, label_file)
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                class_id = int(parts[0])
                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])

                # Convert to pixel coordinates
                img_width, img_height = img.size
                x1 = (x_center - width / 2) * img_width
                y1 = (y_center - height / 2) * img_height
                w = width * img_width
                h = height * img_height

                # Draw rectangle
                rect = patches.Rectangle((x1, y1), w, h, linewidth=2, edgecolor='r', facecolor='none')
                ax.add_patch(rect)

                # Add label
                ax.text(x1, y1, class_names[class_id], color='red', fontsize=12, backgroundcolor='white')

    ax.axis('off')
    plt.title(f'Ground Truth: {image_file}')
    plt.savefig(f'/home/tilak/my_projects/EDGE_QI/{image_file.replace(".jpg", "_gt.png")}')
    plt.close()

# Visualize each image
for img_file in image_files:
    visualize_image(img_file)

print("Visualization complete. Images saved as PNG files.")