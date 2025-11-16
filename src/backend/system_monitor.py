"""
EDGE-QI System Monitor
Real-time system resource monitoring for edge devices
"""

import psutil
import time
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SystemMonitor:
    """Monitor system resources in real-time"""
    
    def __init__(self):
        self.start_time = time.time()
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()
        
        # Check capabilities
        self._gpu_available = self._check_gpu()
        self._battery_available = self._check_battery()
        
        logger.info("✅ System Monitor initialized")
        logger.info(f"   GPU available: {self._gpu_available}")
        logger.info(f"   Battery available: {self._battery_available}")
    
    def _check_gpu(self) -> bool:
        """Check if GPU monitoring is available"""
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False
    
    def _check_battery(self) -> bool:
        """Check if battery monitoring is available"""
        try:
            battery = psutil.sensors_battery()
            return battery is not None
        except:
            return False
    
    def get_cpu_usage(self) -> Dict:
        """
        Get CPU usage statistics
        
        Returns:
            Dict with overall and per-core CPU usage
        """
        try:
            # Overall CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Per-core usage
            per_core = psutil.cpu_percent(interval=0.1, percpu=True)
            
            # CPU frequency
            freq = psutil.cpu_freq()
            
            # CPU count
            cpu_count = psutil.cpu_count(logical=False)
            logical_count = psutil.cpu_count(logical=True)
            
            return {
                'usage_percent': round(cpu_percent, 1),
                'per_core': [round(x, 1) for x in per_core],
                'frequency_mhz': round(freq.current, 0) if freq else None,
                'physical_cores': cpu_count,
                'logical_cores': logical_count,
                'available': True
            }
        except Exception as e:
            logger.error(f"CPU monitoring error: {e}")
            return {'usage_percent': 0, 'available': False}
    
    def get_memory_usage(self) -> Dict:
        """
        Get memory usage statistics
        
        Returns:
            Dict with memory usage details
        """
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'percent': round(mem.percent, 1),
                'used_gb': round(mem.used / (1024**3), 2),
                'total_gb': round(mem.total / (1024**3), 2),
                'available_gb': round(mem.available / (1024**3), 2),
                'swap_used_gb': round(swap.used / (1024**3), 2),
                'swap_total_gb': round(swap.total / (1024**3), 2),
                'available': True
            }
        except Exception as e:
            logger.error(f"Memory monitoring error: {e}")
            return {'percent': 0, 'available': False}
    
    def get_gpu_usage(self) -> Dict:
        """
        Get GPU usage statistics (NVIDIA CUDA only for now)
        
        Returns:
            Dict with GPU usage details
        """
        if not self._gpu_available:
            return {
                'available': False,
                'usage_percent': 0,
                'memory_used_gb': 0,
                'memory_total_gb': 0
            }
        
        try:
            import torch
            
            # GPU memory usage
            mem_allocated = torch.cuda.memory_allocated(0)
            mem_reserved = torch.cuda.memory_reserved(0)
            mem_total = torch.cuda.get_device_properties(0).total_memory
            
            # GPU utilization (approximate)
            usage_percent = (mem_allocated / mem_total) * 100
            
            return {
                'available': True,
                'usage_percent': round(usage_percent, 1),
                'memory_used_gb': round(mem_allocated / (1024**3), 2),
                'memory_reserved_gb': round(mem_reserved / (1024**3), 2),
                'memory_total_gb': round(mem_total / (1024**3), 2),
                'device_name': torch.cuda.get_device_name(0),
                'device_count': torch.cuda.device_count()
            }
        except Exception as e:
            logger.error(f"GPU monitoring error: {e}")
            return {'available': False, 'usage_percent': 0}
    
    def get_battery_status(self) -> Dict:
        """
        Get battery status (for laptops and edge devices)
        
        Returns:
            Dict with battery information
        """
        if not self._battery_available:
            return {
                'present': False,
                'percent': 100,
                'plugged_in': True,
                'time_left_minutes': None
            }
        
        try:
            battery = psutil.sensors_battery()
            
            if battery is None:
                return {
                    'present': False,
                    'percent': 100,
                    'plugged_in': True
                }
            
            # Calculate time left
            time_left = None
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft != psutil.POWER_TIME_UNKNOWN:
                time_left = round(battery.secsleft / 60, 1)  # Convert to minutes
            
            return {
                'present': True,
                'percent': round(battery.percent, 1),
                'plugged_in': battery.power_plugged,
                'time_left_minutes': time_left,
                'available': True
            }
        except Exception as e:
            logger.error(f"Battery monitoring error: {e}")
            return {'present': False, 'available': False}
    
    def get_network_stats(self) -> Dict:
        """
        Get network I/O statistics
        
        Returns:
            Dict with network statistics
        """
        try:
            net = psutil.net_io_counters()
            current_time = time.time()
            
            # Calculate bandwidth (bytes/sec since last call)
            time_diff = current_time - self.last_net_time
            if time_diff > 0:
                bytes_sent_per_sec = (net.bytes_sent - self.last_net_io.bytes_sent) / time_diff
                bytes_recv_per_sec = (net.bytes_recv - self.last_net_io.bytes_recv) / time_diff
            else:
                bytes_sent_per_sec = 0
                bytes_recv_per_sec = 0
            
            # Update last values
            self.last_net_io = net
            self.last_net_time = current_time
            
            return {
                'bytes_sent_mb': round(net.bytes_sent / (1024**2), 2),
                'bytes_recv_mb': round(net.bytes_recv / (1024**2), 2),
                'packets_sent': net.packets_sent,
                'packets_recv': net.packets_recv,
                'errors_in': net.errin,
                'errors_out': net.errout,
                'bandwidth_sent_mbps': round(bytes_sent_per_sec * 8 / (1024**2), 2),  # Mbps
                'bandwidth_recv_mbps': round(bytes_recv_per_sec * 8 / (1024**2), 2),  # Mbps
                'available': True
            }
        except Exception as e:
            logger.error(f"Network monitoring error: {e}")
            return {'available': False}
    
    def get_disk_usage(self) -> Dict:
        """
        Get disk usage statistics
        
        Returns:
            Dict with disk usage details
        """
        try:
            disk = psutil.disk_usage('/')
            
            return {
                'percent': round(disk.percent, 1),
                'used_gb': round(disk.used / (1024**3), 2),
                'total_gb': round(disk.total / (1024**3), 2),
                'free_gb': round(disk.free / (1024**3), 2),
                'available': True
            }
        except Exception as e:
            logger.error(f"Disk monitoring error: {e}")
            return {'percent': 0, 'available': False}
    
    def get_temperature(self) -> Dict:
        """
        Get system temperature (if available)
        
        Returns:
            Dict with temperature readings
        """
        try:
            temps = psutil.sensors_temperatures()
            
            if not temps:
                return {'available': False}
            
            # Get CPU temperature
            cpu_temp = None
            if 'coretemp' in temps:
                cpu_temp = temps['coretemp'][0].current
            elif 'cpu_thermal' in temps:  # Raspberry Pi
                cpu_temp = temps['cpu_thermal'][0].current
            
            return {
                'cpu_celsius': round(cpu_temp, 1) if cpu_temp else None,
                'available': cpu_temp is not None
            }
        except Exception as e:
            return {'available': False}
    
    def get_uptime(self) -> float:
        """
        Get system uptime in seconds
        
        Returns:
            Uptime in seconds
        """
        return time.time() - self.start_time
    
    def get_process_info(self) -> Dict:
        """
        Get current process information
        
        Returns:
            Dict with process stats
        """
        try:
            process = psutil.Process()
            
            return {
                'pid': process.pid,
                'cpu_percent': round(process.cpu_percent(), 1),
                'memory_mb': round(process.memory_info().rss / (1024**2), 2),
                'threads': process.num_threads(),
                'available': True
            }
        except Exception as e:
            logger.error(f"Process monitoring error: {e}")
            return {'available': False}
    
    def get_all_metrics(self) -> Dict:
        """
        Get all system metrics at once
        
        Returns:
            Dict with all available metrics
        """
        return {
            'cpu': self.get_cpu_usage(),
            'memory': self.get_memory_usage(),
            'gpu': self.get_gpu_usage(),
            'battery': self.get_battery_status(),
            'network': self.get_network_stats(),
            'disk': self.get_disk_usage(),
            'temperature': self.get_temperature(),
            'process': self.get_process_info(),
            'uptime_seconds': round(self.get_uptime(), 1),
            'timestamp': time.time()
        }
    
    def get_health_status(self) -> Dict:
        """
        Get overall system health status
        
        Returns:
            Dict with health indicators
        """
        cpu = self.get_cpu_usage()
        memory = self.get_memory_usage()
        battery = self.get_battery_status()
        disk = self.get_disk_usage()
        
        # Determine health status
        issues = []
        
        if cpu['usage_percent'] > 90:
            issues.append("High CPU usage")
        if memory['percent'] > 90:
            issues.append("High memory usage")
        if battery['present'] and battery['percent'] < 20:
            issues.append("Low battery")
        if disk['percent'] > 90:
            issues.append("Low disk space")
        
        # Overall status
        if not issues:
            status = "healthy"
        elif len(issues) == 1:
            status = "warning"
        else:
            status = "critical"
        
        return {
            'status': status,
            'issues': issues,
            'timestamp': time.time()
        }


# Test function
def test_system_monitor():
    """Test system monitoring"""
    print("🔍 Testing System Monitor...\n")
    
    monitor = SystemMonitor()
    
    # Get all metrics
    metrics = monitor.get_all_metrics()
    
    print("=" * 60)
    print("SYSTEM METRICS")
    print("=" * 60)
    
    # CPU
    print(f"\n💻 CPU:")
    print(f"   Usage: {metrics['cpu']['usage_percent']}%")
    print(f"   Cores: {metrics['cpu']['physical_cores']} physical, {metrics['cpu']['logical_cores']} logical")
    if metrics['cpu'].get('frequency_mhz'):
        print(f"   Frequency: {metrics['cpu']['frequency_mhz']} MHz")
    
    # Memory
    print(f"\n🧠 Memory:")
    print(f"   Usage: {metrics['memory']['percent']}%")
    print(f"   Used: {metrics['memory']['used_gb']} GB / {metrics['memory']['total_gb']} GB")
    
    # GPU
    print(f"\n🎮 GPU:")
    if metrics['gpu']['available']:
        print(f"   Device: {metrics['gpu']['device_name']}")
        print(f"   Memory: {metrics['gpu']['memory_used_gb']} GB / {metrics['gpu']['memory_total_gb']} GB")
    else:
        print(f"   Not available")
    
    # Battery
    print(f"\n🔋 Battery:")
    if metrics['battery']['present']:
        print(f"   Level: {metrics['battery']['percent']}%")
        print(f"   Plugged in: {metrics['battery']['plugged_in']}")
        if metrics['battery']['time_left_minutes']:
            print(f"   Time left: {metrics['battery']['time_left_minutes']} minutes")
    else:
        print(f"   Not present (desktop/always plugged)")
    
    # Network
    print(f"\n🌐 Network:")
    print(f"   Sent: {metrics['network']['bytes_sent_mb']} MB")
    print(f"   Received: {metrics['network']['bytes_recv_mb']} MB")
    print(f"   Upload: {metrics['network']['bandwidth_sent_mbps']} Mbps")
    print(f"   Download: {metrics['network']['bandwidth_recv_mbps']} Mbps")
    
    # Disk
    print(f"\n💾 Disk:")
    print(f"   Usage: {metrics['disk']['percent']}%")
    print(f"   Free: {metrics['disk']['free_gb']} GB / {metrics['disk']['total_gb']} GB")
    
    # Health
    health = monitor.get_health_status()
    print(f"\n❤️  Health Status: {health['status'].upper()}")
    if health['issues']:
        print(f"   Issues: {', '.join(health['issues'])}")
    
    print(f"\n⏱️  Uptime: {metrics['uptime_seconds']:.1f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    test_system_monitor()
