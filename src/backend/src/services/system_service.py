"""
System service for metrics and health checks
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict, Any
from ..models import EdgeNode, Detection, SystemMetric, ConsensusRound, SystemLog
from ..schemas import SystemMetrics


async def get_system_metrics(db: Session) -> Dict[str, Any]:
    """Get current system metrics"""
    
    # Get node statistics
    total_nodes = db.query(EdgeNode).count()
    active_nodes = db.query(EdgeNode).filter(EdgeNode.status == 'active').count()
    idle_nodes = db.query(EdgeNode).filter(EdgeNode.status == 'idle').count()
    fault_nodes = db.query(EdgeNode).filter(EdgeNode.status == 'fault').count()
    
    # Get detection statistics
    total_detections = db.query(Detection).count()
    
    # Get recent detections (last minute)
    one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
    recent_detections = db.query(Detection).filter(
        Detection.timestamp >= one_minute_ago
    ).count()
    detections_per_second = recent_detections / 60.0
    
    # Get average metrics from active nodes
    avg_metrics = db.query(
        func.avg(EdgeNode.cpu_usage).label('avg_cpu'),
        func.avg(EdgeNode.memory_usage).label('avg_memory'),
        func.avg(EdgeNode.average_latency).label('avg_latency'),
        func.sum(EdgeNode.energy_consumption).label('total_energy')
    ).filter(EdgeNode.status == 'active').first()
    
    average_cpu = float(avg_metrics.avg_cpu or 0.0)
    average_memory = float(avg_metrics.avg_memory or 0.0)
    average_latency = float(avg_metrics.avg_latency or 0.0)
    
    # Calculate savings (mock calculation - replace with actual logic)
    bandwidth_saved = total_detections * 0.5  # MB
    energy_saved = total_detections * 0.001  # kWh
    
    metrics = {
        'total_nodes': total_nodes,
        'active_nodes': active_nodes,
        'idle_nodes': idle_nodes,
        'fault_nodes': fault_nodes,
        'total_detections': total_detections,
        'detections_per_second': round(detections_per_second, 2),
        'average_latency': round(average_latency, 2),
        'average_cpu': round(average_cpu, 2),
        'average_memory': round(average_memory, 2),
        'bandwidth_saved': round(bandwidth_saved, 2),
        'energy_saved': round(energy_saved, 3),
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Store metrics in database
    metric_record = SystemMetric(**metrics)
    db.add(metric_record)
    db.commit()
    
    return metrics


async def get_node_summary(db: Session) -> Dict[str, Any]:
    """Get node summary statistics"""
    
    nodes = db.query(EdgeNode).all()
    
    summary = {
        'total': len(nodes),
        'active': sum(1 for n in nodes if n.status == 'active'),
        'idle': sum(1 for n in nodes if n.status == 'idle'),
        'fault': sum(1 for n in nodes if n.status == 'fault'),
        'total_detections': sum(n.total_detections for n in nodes),
        'average_cpu': round(sum(n.cpu_usage for n in nodes) / len(nodes), 2) if nodes else 0.0,
        'average_memory': round(sum(n.memory_usage for n in nodes) / len(nodes), 2) if nodes else 0.0,
        'total_energy': round(sum(n.energy_consumption for n in nodes), 2)
    }
    
    return summary


async def check_system_health(db: Session) -> Dict[str, str]:
    """Check health of system components"""
    
    health = {
        'database': 'healthy',
        'mqtt': 'unknown',
        'redis': 'unknown'
    }
    
    # Check database
    try:
        db.execute('SELECT 1')
        health['database'] = 'healthy'
    except Exception as e:
        health['database'] = 'unhealthy'
        print(f"Database health check failed: {e}")
    
    # MQTT and Redis checks would go here
    # For now, we'll mark them as unknown
    
    return health


async def get_analytics_data(db: Session, time_range: str = '24h') -> Dict[str, Any]:
    """Get analytics data for charts"""
    
    # Parse time range
    if time_range == '1h':
        time_delta = timedelta(hours=1)
        bucket_size = 5  # 5 minute buckets
    elif time_range == '6h':
        time_delta = timedelta(hours=6)
        bucket_size = 15  # 15 minute buckets
    elif time_range == '24h':
        time_delta = timedelta(hours=24)
        bucket_size = 60  # 1 hour buckets
    elif time_range == '7d':
        time_delta = timedelta(days=7)
        bucket_size = 360  # 6 hour buckets
    else:
        time_delta = timedelta(hours=24)
        bucket_size = 60
    
    start_time = datetime.utcnow() - time_delta
    
    # Get metrics from database
    metrics = db.query(SystemMetric).filter(
        SystemMetric.timestamp >= start_time
    ).order_by(SystemMetric.timestamp).all()
    
    # Traffic trends
    traffic_trends = [
        {
            'time': m.timestamp.strftime('%H:%M'),
            'detections': m.total_detections,
            'dps': m.detections_per_second
        }
        for m in metrics
    ]
    
    # Performance metrics
    performance_metrics = [
        {
            'time': m.timestamp.strftime('%H:%M'),
            'latency': m.average_latency,
            'cpu': m.average_cpu,
            'memory': m.average_memory
        }
        for m in metrics
    ]
    
    # Detection distribution (by object type)
    detection_distribution = db.query(
        Detection.object_type,
        func.count(Detection.id).label('count')
    ).filter(
        Detection.timestamp >= start_time
    ).group_by(Detection.object_type).all()
    
    detection_dist = [
        {'name': dt[0], 'value': dt[1]}
        for dt in detection_distribution
    ]
    
    # Bandwidth comparison
    bandwidth_comparison = [
        {
            'time': m.timestamp.strftime('%H:%M'),
            'saved': m.bandwidth_saved,
            'used': m.bandwidth_saved * 0.3  # Mock data
        }
        for m in metrics
    ]
    
    # Energy efficiency
    energy_efficiency = [
        {
            'time': m.timestamp.strftime('%H:%M'),
            'saved': m.energy_saved,
            'consumed': m.energy_saved * 2  # Mock data
        }
        for m in metrics
    ]
    
    # Node activity
    node_activity = db.query(
        EdgeNode.name,
        EdgeNode.total_detections,
        EdgeNode.uptime,
        EdgeNode.energy_consumption
    ).all()
    
    node_act = [
        {
            'node': na[0],
            'detections': na[1],
            'uptime': na[2],
            'energy': na[3]
        }
        for na in node_activity
    ]
    
    return {
        'traffic_trends': traffic_trends,
        'performance_metrics': performance_metrics,
        'detection_distribution': detection_dist,
        'bandwidth_comparison': bandwidth_comparison,
        'energy_efficiency': energy_efficiency,
        'node_activity': node_act
    }
