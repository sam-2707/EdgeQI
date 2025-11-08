"""
Demo: Realistic Intersection Simulation

This script demonstrates the complete realistic intersection simulation
with rendered maps, multiple cameras, traffic lights, and analytics.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def main():
    """Demo the realistic intersection simulation"""
    
    print("🗺️ EDGE-QI Realistic Intersection Demo")
    print("=" * 50)
    print()
    
    print("🎯 Features to be demonstrated:")
    print("   📹 7 strategically placed cameras")
    print("   🚦 3 traffic lights with realistic timing")
    print("   🗺️ Rendered intersection map")
    print("   🚗 Realistic vehicle movement and queuing")
    print("   📊 Real-time analytics and graphs")
    print("   📈 Camera coverage analysis")
    print("   ⚡ Traffic efficiency metrics")
    print()
    
    # Check if the simulation file exists
    sim_file = Path("realistic_intersection_sim.py")
    if not sim_file.exists():
        print("❌ Simulation file not found!")
        return
    
    print("🚀 Starting realistic intersection simulation...")
    print("   📍 URL: http://localhost:8504")
    print("   ⏹️  Press Ctrl+C to stop")
    print()
    
    try:
        # Start the simulation
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            "realistic_intersection_sim.py", 
            "--server.port", "8504",
            "--server.headless", "false"
        ]
        
        print("🔧 Command:", " ".join(cmd))
        print()
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open("http://localhost:8504")
                print("🌐 Browser opened automatically")
            except:
                print("🌐 Please open http://localhost:8504 manually")
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run the simulation
        process = subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start simulation: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure Streamlit is installed: pip install streamlit")
        print("   2. Check if port 8504 is available")
        print("   3. Run directly: streamlit run realistic_intersection_sim.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n✅ Demo completed!")
    print("\n🎯 What you should have seen:")
    print("   🗺️ Live intersection map with roads and crosswalks")
    print("   📹 7 camera positions with coverage areas") 
    print("   🚦 3 traffic lights changing states realistically")
    print("   🚗 Vehicles moving, stopping, and forming queues")
    print("   📊 Real-time analytics dashboard with multiple charts")
    print("   📈 Vehicle counting, speed analysis, and efficiency metrics")
    print("   🎮 Interactive controls (Start/Stop/Reset)")

if __name__ == "__main__":
    main()