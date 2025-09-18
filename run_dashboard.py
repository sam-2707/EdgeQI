"""
EDGE-QI Dashboard Launcher

Simple launcher script for the EDGE-QI real-time dashboard.
Handles environment setup and starts the Streamlit application.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'plotly', 
        'pandas',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("📦 Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def setup_environment():
    """Setup environment for dashboard"""
    # Add project root to Python path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Set environment variables for dashboard
    os.environ['EDGE_QI_DASHBOARD'] = '1'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    
    print(f"📁 Project root: {project_root}")
    print("🌍 Environment configured")

def launch_dashboard(port=8501, debug=False):
    """Launch the Streamlit dashboard"""
    dashboard_path = Path(__file__).parent / "App" / "dashboard.py"
    
    if not dashboard_path.exists():
        print(f"❌ Dashboard file not found: {dashboard_path}")
        return False
    
    # Streamlit command
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(dashboard_path),
        "--server.port", str(port),
        "--server.address", "localhost"
    ]
    
    if not debug:
        cmd.extend([
            "--logger.level", "error",
            "--client.showErrorDetails", "false"
        ])
    
    print(f"🚀 Launching EDGE-QI Dashboard on http://localhost:{port}")
    print("📊 Starting Streamlit application...")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Dashboard stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching dashboard: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="Launch EDGE-QI Real-time Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_dashboard.py                    # Launch on default port 8501
  python run_dashboard.py --port 8080       # Launch on custom port
  python run_dashboard.py --debug           # Launch with debug logging
  python run_dashboard.py --check-only      # Only check dependencies
        """
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=8501,
        help='Port to run the dashboard on (default: 8501)'
    )
    
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Enable debug mode with verbose logging'
    )
    
    parser.add_argument(
        '--check-only', '-c',
        action='store_true',
        help='Only check dependencies, do not launch dashboard'
    )
    
    args = parser.parse_args()
    
    print("🚦 EDGE-QI Dashboard Launcher")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    if args.check_only:
        print("✅ Dependency check completed successfully")
        sys.exit(0)
    
    # Setup environment
    setup_environment()
    
    # Launch dashboard
    success = launch_dashboard(port=args.port, debug=args.debug)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()