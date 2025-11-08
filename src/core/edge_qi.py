"""
EDGE-QI Framework - Main Application Launcher
============================================

Unified entry point for all EDGE-QI functionality.
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

def main():
    """Main launcher with unified interface"""
    parser = argparse.ArgumentParser(
        description="EDGE-QI Framework - Edge Intelligence for Queue Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Commands:
  core-system      Run core EDGE-QI scheduler system
  dashboard        Launch web-based dashboard
  web-sim          Launch 3D web simulation (Next.js + Three.js)
  headless         Run headless processing demo
  benchmark        Launch performance benchmark
  anomaly-demo     Run anomaly detection demo
  
Examples:
  python edge_qi.py core-system              # Run main EDGE-QI system
  python edge_qi.py dashboard                # Launch dashboard on port 8501
  python edge_qi.py dashboard --port 8080    # Launch on custom port
  python edge_qi.py web-sim                  # Launch 3D web simulation
  python edge_qi.py headless --duration 60   # 60-second headless demo
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Core system
    core_parser = subparsers.add_parser('core-system', help='Run core EDGE-QI system')
    
    # Dashboard
    dash_parser = subparsers.add_parser('dashboard', help='Launch web dashboard')
    dash_parser.add_argument('--port', '-p', type=int, default=8501, help='Port (default: 8501)')
    dash_parser.add_argument('--debug', '-d', action='store_true', help='Debug mode')
    
    # 3D Web Simulation
    websim_parser = subparsers.add_parser('web-sim', help='Launch 3D web simulation (Next.js + Three.js)')
    websim_parser.add_argument('--port', '-p', type=int, default=3000, help='Port (default: 3000)')
    
    # Headless demo
    headless_parser = subparsers.add_parser('headless', help='Headless processing demo')
    headless_parser.add_argument('--duration', '-t', type=int, default=30, help='Duration in seconds')
    
    # Benchmark
    bench_parser = subparsers.add_parser('benchmark', help='Performance metrics')
    
    # Anomaly demo
    anomaly_parser = subparsers.add_parser('anomaly-demo', help='Anomaly detection demo')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print("🚦 EDGE-QI Framework")
    print("=" * 50)
    
    try:
        if args.command == 'core-system':
            print("🚀 Starting EDGE-QI Core System...")
            subprocess.run([sys.executable, "main.py"], check=True)
            
        elif args.command == 'dashboard':
            print(f"📊 Launching Dashboard on port {args.port}...")
            cmd = [sys.executable, "-m", "streamlit", "run", "App/dashboard.py"]
            if args.port != 8501:
                cmd.extend(["--server.port", str(args.port)])
            subprocess.run(cmd, check=True)
            
        elif args.command == 'web-sim':
            print(f"🌐 Launching 3D Web Simulation on port {args.port}...")
            web_sim_path = Path("traffic-sim-web")
            if not web_sim_path.exists():
                print("❌ Web simulation not found! Run setup_web_sim.ps1 first.")
                sys.exit(1)
            
            # Check if node_modules exists
            if not (web_sim_path / "node_modules").exists():
                print("� Installing dependencies...")
                subprocess.run(["npm", "install"], cwd=str(web_sim_path), check=True)
            
            # Set port environment variable
            env = os.environ.copy()
            env['PORT'] = str(args.port)
            
            # Run Next.js dev server
            subprocess.run(["npm", "run", "dev"], cwd=str(web_sim_path), env=env, check=True)
            
        elif args.command == 'headless':
            print(f"⚡ Starting {args.duration}s Headless Demo...")
            subprocess.run([sys.executable, "demo_headless_realtime.py"], 
                         input=str(args.duration), text=True, check=True)
            
        elif args.command == 'benchmark':
            print(f"📊 Performance benchmarking not yet implemented.")
            print("Use 'web-sim' for the new 3D simulation with real-time metrics.")
            
        elif args.command == 'anomaly-demo':
            print("🔍 Starting Anomaly Detection Demo...")
            subprocess.run([sys.executable, "demo_anomaly_detection.py"], check=True)
            
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
