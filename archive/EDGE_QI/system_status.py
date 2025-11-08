#!/usr/bin/env python3
"""
EDGE-QI System Status Monitor

Check the status of all system components and display real-time metrics.
"""

import asyncio
import aiohttp
import time
import json
from datetime import datetime
import argparse

class SystemMonitor:
    def __init__(self, backend_url="http://localhost:8000"):
        self.backend_url = backend_url
        self.running = True
    
    async def check_backend_health(self):
        """Check if backend is healthy"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.backend_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        return True, data
                    else:
                        return False, f"HTTP {response.status}"
        except Exception as e:
            return False, str(e)
    
    async def get_system_metrics(self):
        """Get current system metrics"""
        try:
            async with aiohttp.ClientSession() as session:
                # Get nodes
                async with session.get(f"{self.backend_url}/api/nodes") as response:
                    nodes_data = await response.json() if response.status == 200 else {"nodes": [], "total": 0, "active": 0}
                
                # Get recent traffic data
                async with session.get(f"{self.backend_url}/api/traffic?limit=10") as response:
                    if response.status == 200:
                        traffic_response = await response.json()
                        traffic_data = traffic_response if isinstance(traffic_response, list) else []
                    else:
                        traffic_data = []
                
                return nodes_data, traffic_data
        except Exception as e:
            return {"nodes": [], "total": 0, "active": 0}, []
    
    def format_metrics(self, nodes_data, traffic_data):
        """Format metrics for display"""
        output = []
        output.append("=" * 60)
        output.append("🚀 EDGE-QI System Status Dashboard")
        output.append("=" * 60)
        output.append(f"⏰ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("")
        
        # Backend status
        output.append("🔧 Backend Status:")
        output.append(f"   ✅ API Server: Online ({self.backend_url})")
        output.append("")
        
        # Edge nodes summary
        output.append("📡 Edge Nodes Summary:")
        output.append(f"   Total Nodes: {nodes_data['total']}")
        output.append(f"   Active Nodes: {nodes_data['active']}")
        output.append(f"   Offline Nodes: {nodes_data['total'] - nodes_data['active']}")
        output.append("")
        
        # Active nodes details
        if nodes_data.get('nodes'):
            output.append("🏢 Active Edge Nodes:")
            for node in nodes_data['nodes']:
                if node['status'] == 'active':
                    metrics = node.get('metrics', {})
                    
                    # Get last update time
                    last_update = node.get('last_update', 'Unknown')
                    if last_update != 'Unknown':
                        last_update = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
                        last_update = last_update.strftime('%H:%M:%S')
                    
                    output.append(f"   📍 {node['node_id']} ({node.get('intersection_id', 'N/A')})")
                    
                    # Handle different metric structures
                    if isinstance(metrics, dict):
                        if 'cpu_usage' in metrics:
                            output.append(f"      💻 CPU: {metrics.get('cpu_usage', 0):.1f}%")
                        if 'memory_usage' in metrics:
                            output.append(f"      🧠 Memory: {metrics.get('memory_usage', 0):.1f}%")
                        if 'energy_level' in metrics:
                            output.append(f"      🔋 Energy: {metrics.get('energy_level', 0):.1f}%")
                        if 'frames_processed' in metrics:
                            output.append(f"      📷 Frames: {metrics.get('frames_processed', 0)}")
                        if 'vehicle_count' in metrics:
                            output.append(f"      🚗 Current Vehicles: {metrics.get('vehicle_count', 0)}")
                    
                    output.append(f"      🕐 Last Update: {last_update}")
                    output.append("")
        
        # Recent traffic activity
        if traffic_data and len(traffic_data) > 0:
            output.append("🚦 Recent Traffic Activity (Last 5 entries):")
            for i, entry in enumerate(traffic_data[:5]):
                timestamp = entry.get('timestamp', '')
                if timestamp:
                    try:
                        ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamp = ts.strftime('%H:%M:%S')
                    except:
                        timestamp = timestamp[:8]  # fallback
                
                output.append(f"   {i+1}. 📍 {entry.get('node_id', 'Unknown')} ({timestamp})")
                output.append(f"      🚗 Vehicles: {entry.get('vehicle_count', 0)}, "
                           f"🏁 Queue: {entry.get('queue_length', 0):.1f}, "
                           f"⚡ Speed: {entry.get('avg_speed', 0):.1f} km/h")
                if entry.get('anomaly_score', 0) > 0.5:
                    output.append(f"      ⚠️  Anomaly Detected: {entry.get('anomaly_score', 0):.2f}")
            output.append("")
        
        # System health indicators
        output.append("💚 System Health Indicators:")
        active_ratio = nodes_data['active'] / max(nodes_data['total'], 1)
        if active_ratio >= 0.8:
            output.append("   ✅ Node Availability: Excellent")
        elif active_ratio >= 0.6:
            output.append("   ⚠️  Node Availability: Good")
        else:
            output.append("   ❌ Node Availability: Poor")
        
        if traffic_data and len(traffic_data) > 0:
            recent_data = len([x for x in traffic_data[:10] if x.get('timestamp')])
            if recent_data >= 8:
                output.append("   ✅ Data Flow: Active")
            elif recent_data >= 5:
                output.append("   ⚠️  Data Flow: Moderate")
            else:
                output.append("   ❌ Data Flow: Low")
        else:
            output.append("   ❌ Data Flow: No Recent Data")
        
        output.append("")
        output.append("🌐 Access Points:")
        output.append("   Frontend Dashboard: http://localhost:3000")
        output.append("   Backend API: http://localhost:8000")
        output.append("   API Documentation: http://localhost:8000/docs")
        output.append("")
        output.append("=" * 60)
        
        return "\n".join(output)
    
    async def run_once(self):
        """Run monitoring once"""
        # Check backend health
        healthy, health_info = await self.check_backend_health()
        if not healthy:
            print(f"❌ Backend is not healthy: {health_info}")
            return
        
        # Get metrics
        nodes_data, traffic_data = await self.get_system_metrics()
        
        # Display formatted output
        output = self.format_metrics(nodes_data, traffic_data)
        print(output)
    
    async def run_continuous(self, interval=10):
        """Run monitoring continuously"""
        print("🚀 Starting EDGE-QI System Monitor...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while self.running:
                # Clear screen (works on most terminals)
                print("\033[2J\033[H", end="")
                
                await self.run_once()
                await asyncio.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped.")
        except Exception as e:
            print(f"\n❌ Error: {e}")

async def main():
    parser = argparse.ArgumentParser(description='EDGE-QI System Status Monitor')
    parser.add_argument('--backend-url', default='http://localhost:8000', help='Backend URL')
    parser.add_argument('--once', action='store_true', help='Run once instead of continuously')
    parser.add_argument('--interval', type=int, default=10, help='Update interval in seconds')
    
    args = parser.parse_args()
    
    monitor = SystemMonitor(args.backend_url)
    
    if args.once:
        await monitor.run_once()
    else:
        await monitor.run_continuous(args.interval)

if __name__ == "__main__":
    asyncio.run(main())