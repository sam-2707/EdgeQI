import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Create comparison table figure
fig, ax = plt.subplots(1, 1, figsize=(14, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Title
ax.text(5, 7.5, 'EDGE-QI vs. State-of-the-Art Comparison', 
        fontsize=16, fontweight='bold', ha='center')

# Table headers
headers = ['Framework', 'Energy\nSavings', 'Bandwidth\nReduction', 'Response Time\n(Critical)', 
           'Multi-Edge\nCollaboration', 'Queue\nSpecialization']
row_height = 0.8
col_width = 1.6
start_x = 0.2
start_y = 6

# Header styling
header_color = '#4472C4'
for i, header in enumerate(headers):
    rect = patches.Rectangle((start_x + i * col_width, start_y), col_width, row_height, 
                           facecolor=header_color, edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(start_x + i * col_width + col_width/2, start_y + row_height/2, header, 
           ha='center', va='center', fontweight='bold', color='white', fontsize=10)

# Data rows
frameworks = [
    ['EDGE-QI', '28.4%', '74.5%', '<250ms', 'Yes (BFT)', 'Optimized'],
    ['Mobile Edge Computing', '15-20%', '30-40%', '400-600ms', 'Limited', 'General'],
    ['Standard Task Scheduler', '10-15%', '20-30%', '500-800ms', 'No', 'General'],
    ['Cloud-Edge Hybrid', '5-10%', '40-50%', '600-1000ms', 'Partial', 'General'],
    ['Fog Computing Framework', '12-18%', '35-45%', '300-500ms', 'Limited', 'General']
]

# Row colors
row_colors = ['#E8F4FD', '#F2F2F2', '#F8F8F8', '#F2F2F2', '#F8F8F8']
text_colors = ['#1F4E79', 'black', 'black', 'black', 'black']

for row_idx, (framework_data, row_color, text_color) in enumerate(zip(frameworks, row_colors, text_colors)):
    y_pos = start_y - (row_idx + 1) * row_height
    
    for col_idx, cell_data in enumerate(framework_data):
        x_pos = start_x + col_idx * col_width
        
        # Highlight EDGE-QI row
        if row_idx == 0:
            rect = patches.Rectangle((x_pos, y_pos), col_width, row_height, 
                                   facecolor=row_color, edgecolor='black', linewidth=2)
        else:
            rect = patches.Rectangle((x_pos, y_pos), col_width, row_height, 
                                   facecolor=row_color, edgecolor='gray', linewidth=1)
        ax.add_patch(rect)
        
        # Bold text for EDGE-QI
        weight = 'bold' if row_idx == 0 else 'normal'
        ax.text(x_pos + col_width/2, y_pos + row_height/2, cell_data, 
               ha='center', va='center', fontweight=weight, color=text_color, fontsize=9)

# Add performance indicators
indicators_y = 1.5
ax.text(5, indicators_y, 'Key Performance Indicators', 
        fontsize=14, fontweight='bold', ha='center')

# Performance metrics boxes
metrics = [
    {'label': 'Real-time FPS', 'value': '30+', 'color': '#2E8B57'},
    {'label': 'Accuracy (F1)', 'value': '93.0%', 'color': '#4682B4'},
    {'label': 'Consensus Latency', 'value': '<200ms', 'color': '#CD853F'},
    {'label': 'Edge Devices', 'value': 'Up to 6', 'color': '#8B4513'}
]

metric_width = 2
metric_height = 0.6
metrics_start_x = 1
metrics_y = 0.5

for i, metric in enumerate(metrics):
    x_pos = metrics_start_x + i * metric_width
    
    # Metric box
    rect = patches.FancyBboxPatch((x_pos, metrics_y), metric_width * 0.8, metric_height, 
                                 boxstyle="round,pad=0.05", 
                                 facecolor=metric['color'], 
                                 edgecolor='black', 
                                 alpha=0.8)
    ax.add_patch(rect)
    
    # Metric text
    ax.text(x_pos + metric_width * 0.4, metrics_y + metric_height * 0.7, metric['value'], 
           ha='center', va='center', fontweight='bold', color='white', fontsize=12)
    ax.text(x_pos + metric_width * 0.4, metrics_y + metric_height * 0.3, metric['label'], 
           ha='center', va='center', fontweight='normal', color='white', fontsize=8)

plt.tight_layout()
plt.savefig('comparison_table.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('comparison_table.pdf', bbox_inches='tight', facecolor='white')
plt.close()

print("Comparison table generated: comparison_table.png and comparison_table.pdf")