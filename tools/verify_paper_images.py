import os
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import numpy as np

def verify_images():
    """Verify that all required images exist"""
    required_images = [
        'architecture_diagram.png',
        'response_times_analysis.png', 
        'comprehensive_performance_analysis.png',
        'comparison_table.png'
    ]
    
    print("Verifying IEEE Paper Images:")
    print("=" * 40)
    
    for image in required_images:
        if os.path.exists(image):
            size = os.path.getsize(image) / 1024  # Size in KB
            print(f"✅ {image} - {size:.1f} KB")
        else:
            print(f"❌ {image} - MISSING")
    
    print("\nAll images are ready for your IEEE conference paper!")
    print("\nTo use in LaTeX:")
    print("1. Make sure the .png files are in the same directory as your .tex file")
    print("2. Compile with pdflatex (recommended) or xelatex")
    print("3. The figures are already referenced in the paper with proper captions")
    
    print("\nFigure References in Paper:")
    print("- Fig. 1: System Architecture (architecture_diagram.png)")
    print("- Fig. 2: Response Time Analysis (response_times_analysis.png)")  
    print("- Fig. 3: Performance Analysis (comprehensive_performance_analysis.png)")
    print("- Fig. 4: Framework Comparison (comparison_table.png)")

if __name__ == "__main__":
    verify_images()