# Figures Directory

This directory contains all figures and diagrams for the EDGE-QI Technical Report.

## Required Images

Generate these images from the Mermaid codes in `MERMAID_DIAGRAMS.md`:

### System Architecture & Design
1. ✅ `architecture.png` - Three-layer architecture diagram
2. ✅ `scheduler_flowchart.png` - Multi-constraint scheduler flowchart
3. ✅ `anomaly_detection_pipeline.png` - Z-score anomaly detection pipeline
4. ✅ `byzantine_consensus.png` - Byzantine fault tolerance sequence
5. ✅ `yolov8_pipeline.png` - YOLOv8n detection pipeline
6. ✅ `yolov8_architecture.png` - YOLOv8 network architecture layers

### Performance Results
7. ✅ `performance_comparison.png` - EDGE-QI vs. state-of-the-art systems
8. ✅ `bandwidth_over_time.png` - Bandwidth savings timeline (3 phases)
9. ✅ `system_metrics.png` - System metrics dashboard
10. ✅ `scalability.png` - Scalability analysis (1-10 nodes)
11. ✅ `energy_comparison.png` - Energy consumption comparison
12. ✅ `latency_distribution.png` - Latency breakdown visualization

## Image Specifications

- **Format:** PNG with transparent background
- **Resolution:** 1920×1080 (Full HD)
- **DPI:** 300 (print quality)
- **Color Scheme:** 
  - Blue (#2196F3): Edge Computing
  - Green (#4CAF50): Success/Achievement
  - Orange (#FF9800): Optimization
  - Purple (#9C27B0): Byzantine Fault Tolerance
  - Red (#F44336): Critical metrics

## Generation Instructions

### Using Mermaid Live Editor
1. Visit: https://mermaid.live/
2. Copy Mermaid code from `MERMAID_DIAGRAMS.md`
3. Click "Download PNG" (set size to 1920x1080)
4. Save with the exact filename listed above

### Using Mermaid CLI
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i input.mmd -o figures/output.png -w 1920 -H 1080 -b transparent
```

### Using VS Code Extension
1. Install "Markdown Preview Mermaid Support"
2. Open `MERMAID_DIAGRAMS.md`
3. Right-click on diagram → Export as PNG
4. Save to this directory

## Current Status

- [x] Directory created
- [ ] Generate 12 diagrams from Mermaid codes
- [ ] Verify all images in place
- [ ] Recompile LaTeX document

## Placeholder Status

Currently, the LaTeX document has placeholder boxes for all figures. Once you generate and save the images in this directory, they will automatically be included when you recompile the LaTeX document.

## Quick Test

After generating images, verify they're correctly placed:

```bash
ls figures/
# Should show all 12 PNG files
```

Then recompile the LaTeX document:

```bash
cd "d:\DS LiT\Distri Sys\EDGE-QI\docs\academic"
pdflatex EDGE_QI_Technical_Report.tex
pdflatex EDGE_QI_Technical_Report.tex  # Run twice for references
```

## Notes

- Placeholders show as gray boxes with filename labels
- Replace placeholders by saving generated images with exact filenames
- All figure references in text will automatically update
- LaTeX will scale images to fit page width (0.85\textwidth)
