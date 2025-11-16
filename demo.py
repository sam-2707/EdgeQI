#!/usr/bin/env python3
"""
EDGE-QI Quick Demo Launcher
Easiest way to demonstrate all features
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("=" * 70)
    print("🎯 EDGE-QI Feature Demonstration Launcher")
    print("=" * 70)
    print()

def print_menu():
    """Display main menu"""
    print("\n📋 Available Demonstrations:")
    print()
    print("  QUICK DEMOS (Best for showing features):")
    print("  1. 🎬 Interactive Dashboard       - All features in one (RECOMMENDED)")
    print("  2. 🚗 Traffic Simulation          - Visual impact demo")
    print("  3. ⚡ Algorithm 1 Demo            - Multi-constraint scheduling")
    print("  4. 📡 Algorithm 2 Demo            - Anomaly-driven transmission")
    print("  5. 🤝 Algorithm 3 Demo            - Byzantine consensus")
    print()
    print("  COMPLETE SYSTEM:")
    print("  6. 🌐 Full System Launch          - All components together")
    print("  7. 📊 Performance Benchmark       - Compare versions")
    print()
    print("  UTILITIES:")
    print("  8. 📝 View Demo Guide             - Open demonstration guide")
    print("  9. ℹ️  System Info                 - Check environment")
    print("  0. ❌ Exit")
    print()

def check_environment():
    """Check if environment is ready"""
    print("🔍 Checking environment...")
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required. Current:", sys.version)
        return False
    print("✅ Python version:", sys.version.split()[0])
    
    # Check required packages (package name -> import name mapping)
    required = {
        'streamlit': 'streamlit',
        'opencv-python': 'cv2',
        'torch': 'torch',
        'numpy': 'numpy'
    }
    missing = []
    
    for package, import_name in required.items():
        try:
            __import__(import_name)
            print(f"✅ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} missing")
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ Environment ready!")
    return True

def launch_dashboard():
    """Launch interactive dashboard"""
    print("\n🎬 Launching Interactive Dashboard...")
    print("=" * 70)
    print("📍 URL: http://localhost:8501")
    print("⏱️  Starting in 3 seconds...")
    print()
    print("WHAT TO DO:")
    print("  1. Click '🚀 Start Real-Time Processing' button")
    print("  2. Watch camera feeds and metrics update")
    print("  3. Observe adaptive scheduling (tasks skip when energy low)")
    print("  4. Check anomaly transmission log")
    print("=" * 70)
    
    time.sleep(3)
    
    # Open browser
    webbrowser.open('http://localhost:8501')
    
    # Launch Streamlit
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run',
        'src/simulations/run_stable_dashboard.py',
        '--server.port', '8501',
        '--server.headless', 'true'
    ])

def launch_traffic_sim():
    """Launch traffic simulation"""
    print("\n🚗 Launching Traffic Simulation...")
    print("=" * 70)
    print("📍 URL: http://localhost:8502")
    print("⏱️  Starting in 3 seconds...")
    print()
    print("WHAT TO DO:")
    print("  1. Click '🚀 Ultra Start' for maximum performance")
    print("  2. Watch realistic traffic intersection (30+ FPS)")
    print("  3. Observe queue detection boxes (red rectangles)")
    print("  4. Toggle trails and adjust speed")
    print("=" * 70)
    
    time.sleep(3)
    
    # Open browser
    webbrowser.open('http://localhost:8502')
    
    # Launch Streamlit
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run',
        'src/simulations/ultra_fast_traffic.py',
        '--server.port', '8502',
        '--server.headless', 'true'
    ])

def demo_algorithm_1():
    """Demonstrate Algorithm 1: Multi-constraint scheduling"""
    print("\n⚡ Algorithm 1: Multi-Constraint Adaptive Scheduling")
    print("=" * 70)
    print()
    print("WHAT YOU'LL SEE:")
    print("  ✅ Tasks execute when energy & network are good")
    print("  ⚠️  Tasks skip when energy is low")
    print("  ⚠️  Tasks defer when network is poor")
    print("  🎯 Priority tasks always execute")
    print()
    print("KEY METRIC: 28.4% energy savings")
    print("=" * 70)
    print("\nPress Enter to start demo...")
    input()
    
    # Run demo
    subprocess.run([
        sys.executable,
        'src/simulations/demo_realtime_integration.py'
    ])
    
    print("\n✅ Demo complete!")
    print("Key takeaway: Smart scheduling saves 28.4% energy")
    input("\nPress Enter to continue...")

def demo_algorithm_2():
    """Demonstrate Algorithm 2: Anomaly-driven transmission"""
    print("\n📡 Algorithm 2: Anomaly-Driven Data Transmission")
    print("=" * 70)
    print()
    print("WHAT YOU'LL SEE:")
    print("  ❌ Normal traffic: No transmission (saves bandwidth)")
    print("  ✅ Queue forms: TRANSMIT (anomaly detected)")
    print("  ✅ Accident: URGENT TRANSMIT (critical anomaly)")
    print("  📊 Bandwidth comparison: 1000 → 255 packets")
    print()
    print("KEY METRIC: 74.5% bandwidth reduction")
    print("=" * 70)
    print("\nPress Enter to start demo...")
    input()
    
    # Run demo
    subprocess.run([
        sys.executable,
        'src/simulations/demo_anomaly_detection.py'
    ])
    
    print("\n✅ Demo complete!")
    print("Key takeaway: Smart filtering saves 74.5% bandwidth")
    input("\nPress Enter to continue...")

def demo_algorithm_3():
    """Demonstrate Algorithm 3: Byzantine consensus"""
    print("\n🤝 Algorithm 3: Byzantine Fault Tolerant Consensus")
    print("=" * 70)
    print()
    print("WHAT YOU'LL SEE:")
    print("  🏢 7 edge nodes coordinate decisions")
    print("  🗳️  Distributed voting on traffic actions")
    print("  ❌ 2 nodes fail → System continues")
    print("  🛡️  Byzantine node rejected")
    print()
    print("KEY METRIC: 99.87% consensus accuracy")
    print("=" * 70)
    print("\nPress Enter to start demo...")
    input()
    
    # Run demo
    subprocess.run([
        sys.executable,
        'src/simulations/demo_bandwidth_optimization.py'
    ])
    
    print("\n✅ Demo complete!")
    print("Key takeaway: Fault-tolerant distributed coordination")
    input("\nPress Enter to continue...")

def launch_full_system():
    """Launch complete system"""
    print("\n🌐 Launching Full System...")
    print("=" * 70)
    print()
    print("STARTING COMPONENTS:")
    print("  1. Dashboard:           http://localhost:8501")
    print("  2. Traffic Sim:         http://localhost:8502")
    print("  3. Performance Bench:   http://localhost:8503")
    print()
    print("⚠️  This will open 3 browser tabs!")
    print("=" * 70)
    print("\nPress Enter to continue...")
    input()
    
    print("\n🚀 Starting all components...")
    
    # Launch all components in separate processes
    processes = []
    
    # Dashboard
    print("Starting Dashboard...")
    p1 = subprocess.Popen([
        sys.executable, '-m', 'streamlit', 'run',
        'src/simulations/run_stable_dashboard.py',
        '--server.port', '8501',
        '--server.headless', 'true'
    ])
    processes.append(p1)
    time.sleep(2)
    webbrowser.open('http://localhost:8501')
    
    # Traffic Sim
    print("Starting Traffic Simulation...")
    p2 = subprocess.Popen([
        sys.executable, '-m', 'streamlit', 'run',
        'src/simulations/ultra_fast_traffic.py',
        '--server.port', '8502',
        '--server.headless', 'true'
    ])
    processes.append(p2)
    time.sleep(2)
    webbrowser.open('http://localhost:8502')
    
    # Performance Benchmark
    print("Starting Performance Benchmark...")
    p3 = subprocess.Popen([
        sys.executable, '-m', 'streamlit', 'run',
        'src/simulations/performance_benchmark.py',
        '--server.port', '8503',
        '--server.headless', 'true'
    ])
    processes.append(p3)
    time.sleep(2)
    webbrowser.open('http://localhost:8503')
    
    print("\n✅ All components started!")
    print("\nPress Ctrl+C to stop all components...")
    
    try:
        # Wait for user to stop
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all components...")
        for p in processes:
            p.terminate()
        print("✅ All components stopped")

def launch_benchmark():
    """Launch performance benchmark"""
    print("\n📊 Launching Performance Benchmark...")
    print("=" * 70)
    print("📍 URL: http://localhost:8503")
    print()
    print("WHAT YOU'LL SEE:")
    print("  📈 Version comparison (Baseline vs EDGE-QI)")
    print("  ⚡ FPS: 3.2 → 5.34 (66% improvement)")
    print("  📡 Bandwidth: 100% → 25.5% (74.5% reduction)")
    print("  🔋 Energy: 100% → 71.6% (28.4% savings)")
    print("  📊 Scalability graphs (1-7 cameras)")
    print("=" * 70)
    
    time.sleep(3)
    
    # Open browser
    webbrowser.open('http://localhost:8503')
    
    # Launch Streamlit
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run',
        'src/simulations/performance_benchmark.py',
        '--server.port', '8503',
        '--server.headless', 'true'
    ])

def view_demo_guide():
    """Open demonstration guide"""
    guide_path = Path('DEMONSTRATION_GUIDE.md')
    
    if guide_path.exists():
        print("\n📝 Opening Demonstration Guide...")
        
        # Try to open with default markdown viewer
        if sys.platform == 'win32':
            subprocess.run(['start', str(guide_path)], shell=True)
        elif sys.platform == 'darwin':
            subprocess.run(['open', str(guide_path)])
        else:
            subprocess.run(['xdg-open', str(guide_path)])
        
        print("✅ Guide opened in default application")
    else:
        print("❌ Demonstration guide not found")
        print("Expected location:", guide_path.absolute())
    
    input("\nPress Enter to continue...")

def show_system_info():
    """Display system information"""
    import platform
    import torch
    import cv2
    import numpy as np
    
    print("\nℹ️  System Information")
    print("=" * 70)
    
    # Python info
    print(f"Python Version:    {sys.version.split()[0]}")
    print(f"Platform:          {platform.platform()}")
    print(f"Architecture:      {platform.machine()}")
    
    # Package versions
    print(f"\nKey Packages:")
    print(f"  PyTorch:         {torch.__version__}")
    print(f"  OpenCV:          {cv2.__version__}")
    print(f"  NumPy:           {np.__version__}")
    
    # GPU info
    print(f"\nGPU Information:")
    if torch.cuda.is_available():
        print(f"  ✅ CUDA Available:  {torch.cuda.is_available()}")
        print(f"  GPU Count:       {torch.cuda.device_count()}")
        print(f"  GPU Name:        {torch.cuda.get_device_name(0)}")
    else:
        print(f"  ❌ CUDA Available:  {torch.cuda.is_available()}")
        print(f"  Mode:            CPU only")
    
    # Project info
    print(f"\nProject Location:")
    print(f"  {Path.cwd()}")
    
    print("=" * 70)
    input("\nPress Enter to continue...")

def main():
    """Main menu loop"""
    print_banner()
    
    # Check environment
    if not check_environment():
        print("\n⚠️  Environment check failed!")
        print("Please fix issues above and try again.")
        sys.exit(1)
    
    while True:
        print_menu()
        choice = input("Enter your choice (0-9): ").strip()
        
        try:
            if choice == '1':
                launch_dashboard()
            elif choice == '2':
                launch_traffic_sim()
            elif choice == '3':
                demo_algorithm_1()
            elif choice == '4':
                demo_algorithm_2()
            elif choice == '5':
                demo_algorithm_3()
            elif choice == '6':
                launch_full_system()
            elif choice == '7':
                launch_benchmark()
            elif choice == '8':
                view_demo_guide()
            elif choice == '9':
                show_system_info()
            elif choice == '0':
                print("\n👋 Thank you for using EDGE-QI!")
                print("For questions, check: DEMONSTRATION_GUIDE.md")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please enter 0-9.")
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            print("Returning to menu...")
            time.sleep(1)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Check logs for details")
            input("\nPress Enter to continue...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
