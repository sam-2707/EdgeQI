import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Set up the figure for IEEE standard (professional look)
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')

# Define IEEE-appropriate colors (grayscale with subtle color accents)
layer_colors = ['#F8F9FA', '#E9ECEF', '#DEE2E6', '#CED4DA', '#ADB5BD', '#868E96', '#6C757D', '#495057']
text_color = '#212529'
arrow_color = '#007BFF'
accent_color = '#28A745'

# Layer definitions (from bottom to top) - IEEE standard format
layers = [
    {"name": "Layer 1: External Systems", "y": 0.5, "height": 1.0, "desc": "Cloud Services, Alert Systems, Third-party APIs", "components": ["REST APIs", "MQTT Broker", "Alert Manager"]},
    {"name": "Layer 2: Visualization", "y": 1.7, "height": 1.0, "desc": "Real-time Dashboard, Monitoring Interface", "components": ["Web Dashboard", "Mobile App", "Admin Panel"]},
    {"name": "Layer 3: Bandwidth Optimization", "y": 2.9, "height": 1.0, "desc": "Adaptive Streaming, Data Compression", "components": ["Quality Adapter", "Compressor", "Priority Queue"]},
    {"name": "Layer 4: Edge Collaboration", "y": 4.1, "height": 1.0, "desc": "Consensus Protocols, Distributed Decisions", "components": ["BFT Consensus", "Vote Manager", "State Sync"]},
    {"name": "Layer 5: Core Processing", "y": 5.3, "height": 1.0, "desc": "Task Scheduling, Resource Monitoring", "components": ["Scheduler", "Energy Monitor", "Network Monitor"]},
    {"name": "Layer 6: ML Intelligence", "y": 6.5, "height": 1.0, "desc": "Computer Vision, Anomaly Detection", "components": ["Object Detector", "Queue Analyzer", "Anomaly Engine"]},
    {"name": "Layer 7: Data Processing", "y": 7.7, "height": 1.0, "desc": "Real-time Ingestion, Quality Validation", "components": ["Data Validator", "Preprocessor", "Buffer Manager"]},
    {"name": "Layer 8: Input Sources", "y": 8.9, "height": 1.0, "desc": "Camera Feeds, Sensor Networks", "components": ["Video Stream", "IoT Sensors", "External Data"]}
]

# Draw layers with professional IEEE styling
for i, layer in enumerate(layers):
    # Main layer box with clean lines
    rect = patches.Rectangle((1, layer["y"]), 8, layer["height"], 
                           facecolor=layer_colors[i], 
                           edgecolor=text_color, 
                           linewidth=1.2)
    ax.add_patch(rect)
    
    # Layer name (left side)
    ax.text(1.2, layer["y"] + 0.7, layer["name"], 
            fontsize=11, fontweight='bold', color=text_color, va='center')
    
    # Layer description (left side, smaller text)
    ax.text(1.2, layer["y"] + 0.4, layer["desc"], 
            fontsize=9, color=text_color, va='center', style='italic')
    
    # Component boxes (right side)
    comp_x_start = 5.5
    comp_width = 1.1
    for j, component in enumerate(layer["components"]):
        comp_x = comp_x_start + j * (comp_width + 0.1)
        comp_rect = patches.Rectangle((comp_x, layer["y"] + 0.15), comp_width, 0.7, 
                                    facecolor='white', 
                                    edgecolor=accent_color, 
                                    linewidth=1.0)
        ax.add_patch(comp_rect)
        ax.text(comp_x + comp_width/2, layer["y"] + 0.5, component, 
               fontsize=8, ha='center', va='center', color=text_color)

# Add professional data flow arrows
for i in range(len(layers)-1):
    # Upward data flow arrows (left side)
    y_start = layers[i]["y"] + layers[i]["height"]
    y_end = layers[i+1]["y"]
    arrow = patches.FancyArrowPatch((2.5, y_start), (2.5, y_end),
                                  arrowstyle='->', mutation_scale=15,
                                  color=arrow_color, linewidth=2)
    ax.add_patch(arrow)
    
    # Downward control flow arrows (right side)
    arrow2 = patches.FancyArrowPatch((6.5, y_end), (6.5, y_start),
                                   arrowstyle='->', mutation_scale=15,
                                   color='#DC3545', linewidth=2)
    ax.add_patch(arrow2)

# Add edge devices with IEEE-standard styling
# Edge Device A (left)
device_a = patches.Rectangle((0.2, 4.5), 0.6, 2.0, 
                           facecolor='#FFF3CD', 
                           edgecolor=text_color, 
                           linewidth=1.5)
ax.add_patch(device_a)
ax.text(0.5, 5.7, 'Edge', fontsize=10, ha='center', va='center', fontweight='bold')
ax.text(0.5, 5.4, 'Node A', fontsize=10, ha='center', va='center', fontweight='bold')
ax.text(0.5, 5.0, 'Jetson', fontsize=8, ha='center', va='center')
ax.text(0.5, 4.8, 'Nano', fontsize=8, ha='center', va='center')

# Edge Device B (right)
device_b = patches.Rectangle((10.2, 4.5), 0.6, 2.0, 
                           facecolor='#FFF3CD', 
                           edgecolor=text_color, 
                           linewidth=1.5)
ax.add_patch(device_b)
ax.text(10.5, 5.7, 'Edge', fontsize=10, ha='center', va='center', fontweight='bold')
ax.text(10.5, 5.4, 'Node B', fontsize=10, ha='center', va='center', fontweight='bold')
ax.text(10.5, 5.0, 'Raspberry', fontsize=8, ha='center', va='center')
ax.text(10.5, 4.8, 'Pi', fontsize=8, ha='center', va='center')

# Collaboration arrows between edge devices
collab_arrow = patches.FancyArrowPatch((0.8, 5.5), (10.2, 5.5),
                                     arrowstyle='<->', mutation_scale=12,
                                     color=accent_color, linewidth=2.5)
ax.add_patch(collab_arrow)
ax.text(5.5, 5.8, 'Consensus Protocol', fontsize=9, ha='center', va='center', 
        fontweight='bold', color=accent_color)

# Add professional title and labels
ax.text(5.5, 9.7, 'EDGE-QI Layered Architecture', 
        fontsize=14, fontweight='bold', ha='center', color=text_color)

# Add flow labels
ax.text(2.5, 0.2, 'Data Flow', fontsize=10, ha='center', va='center', 
        color=arrow_color, fontweight='bold', rotation=90)
ax.text(6.5, 0.2, 'Control Flow', fontsize=10, ha='center', va='center', 
        color='#DC3545', fontweight='bold', rotation=90)

# Add legend with IEEE-appropriate styling
legend_elements = [
    plt.Line2D([0], [0], color=arrow_color, lw=3, label='Data Flow'),
    plt.Line2D([0], [0], color='#DC3545', lw=3, label='Control Flow'),
    plt.Line2D([0], [0], color=accent_color, lw=3, label='Inter-node Communication'),
    patches.Rectangle((0, 0), 1, 1, facecolor='#FFF3CD', edgecolor='black', label='Edge Nodes')
]
legend = ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.35),
                  frameon=True, fancybox=False, shadow=False, fontsize=9)
legend.get_frame().set_linewidth(1)
legend.get_frame().set_edgecolor('black')

# Add component legend
ax.text(9.8, 3.8, 'Components:', fontsize=9, fontweight='bold', color=text_color)
comp_legend = patches.Rectangle((9.5, 3.4), 0.6, 0.3, 
                              facecolor='white', 
                              edgecolor=accent_color, 
                              linewidth=1.0)
ax.add_patch(comp_legend)
ax.text(9.8, 3.55, 'Functional\nModules', fontsize=7, ha='center', va='center', color=text_color)

plt.tight_layout()
plt.savefig('architecture_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('architecture_diagram.pdf', bbox_inches='tight', facecolor='white')
plt.close()

print("IEEE-standard architecture diagram generated: architecture_diagram.png and architecture_diagram.pdf")