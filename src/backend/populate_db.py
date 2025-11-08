"""
Populate database with mock data for testing
"""
import sys
import random
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.database import SessionLocal
from src.models import EdgeNode, Detection, SystemMetric, ConsensusRound, SystemLog


def create_mock_nodes(db, count=5):
    """Create mock edge nodes"""
    print(f"Creating {count} mock edge nodes...")
    
    nodes = []
    for i in range(count):
        node = EdgeNode(
            id=f"edge-node-{i+1}",
            name=f"Edge Node {i+1}",
            status=random.choice(['active', 'idle']) if i < count-1 else 'fault',
            location=f"Location {i+1}",
            cpu_usage=random.uniform(20, 80),
            memory_usage=random.uniform(30, 70),
            gpu_usage=random.uniform(10, 90),
            network_status='good' if i < count-1 else 'poor',
            energy_consumption=random.uniform(50, 150),
            ip_address=f"192.168.1.{10+i}",
            port=8080 + i,
            capabilities={"detection": True, "tracking": True, "yolo": "v8"},
            total_detections=random.randint(100, 1000),
            average_latency=random.uniform(10, 100),
            uptime=random.uniform(50, 100),
            last_heartbeat=datetime.utcnow() - timedelta(seconds=random.randint(0, 60))
        )
        db.add(node)
        nodes.append(node)
    
    db.commit()
    print(f"✅ Created {count} nodes")
    return nodes


def create_mock_detections(db, nodes, count=50):
    """Create mock detections"""
    print(f"Creating {count} mock detections...")
    
    object_types = ['car', 'person', 'bicycle', 'motorcycle', 'bus', 'truck', 'traffic_light']
    
    for i in range(count):
        detection = Detection(
            timestamp=datetime.utcnow() - timedelta(minutes=random.randint(0, 120)),
            node_id=random.choice(nodes).id,
            stream_id=f"stream-{random.randint(1, 3)}",
            object_type=random.choice(object_types),
            confidence=random.uniform(0.7, 0.99),
            bbox={
                "x": random.randint(0, 1000),
                "y": random.randint(0, 1000),
                "width": random.randint(50, 200),
                "height": random.randint(50, 200)
            },
            location=f"Location {random.randint(1, 5)}",
            consensus_verified=random.choice([True, False]),
            consensus_confidence=random.uniform(0.8, 1.0),
            metadata={"frame": i, "source": "yolov8"}
        )
        db.add(detection)
    
    db.commit()
    print(f"✅ Created {count} detections")


def create_mock_metrics(db, count=20):
    """Create mock system metrics"""
    print(f"Creating {count} mock system metrics...")
    
    for i in range(count):
        metric = SystemMetric(
            timestamp=datetime.utcnow() - timedelta(minutes=i*5),
            total_nodes=5,
            active_nodes=random.randint(3, 5),
            idle_nodes=random.randint(0, 2),
            fault_nodes=random.randint(0, 1),
            total_detections=random.randint(50, 200),
            detections_per_second=random.uniform(0.5, 5.0),
            average_latency=random.uniform(20, 80),
            average_cpu=random.uniform(30, 70),
            average_memory=random.uniform(40, 80),
            bandwidth_saved=random.uniform(10, 100),
            energy_saved=random.uniform(0.5, 5.0),
            metadata={}
        )
        db.add(metric)
    
    db.commit()
    print(f"✅ Created {count} metrics")


def create_mock_consensus_rounds(db, count=10):
    """Create mock consensus rounds"""
    print(f"Creating {count} mock consensus rounds...")
    
    for i in range(count):
        success = random.choice([True, True, True, False])  # 75% success rate
        round_data = ConsensusRound(
            round_number=i + 1,
            timestamp=datetime.utcnow() - timedelta(minutes=i*2),
            success=success,
            participants=random.randint(3, 5),
            duration_ms=random.randint(50, 200),
            votes={
                f"node-{j}": random.choice(['accept', 'reject'])
                for j in range(1, random.randint(4, 6))
            },
            result={"consensus": "reached" if success else "failed", "value": random.randint(1, 100)},
            byzantine_nodes=[] if success else [f"node-{random.randint(1, 5)}"],
            fault_tolerance_level=random.uniform(0.7, 1.0)
        )
        db.add(round_data)
    
    db.commit()
    print(f"✅ Created {count} consensus rounds")


def create_mock_logs(db, count=30):
    """Create mock system logs"""
    print(f"Creating {count} mock logs...")
    
    log_levels = ['info', 'warning', 'error']
    sources = ['api', 'detection', 'consensus', 'system', 'network']
    messages = [
        "System started successfully",
        "Node heartbeat received",
        "Detection processed",
        "Consensus round completed",
        "High CPU usage detected",
        "Network latency increased",
        "Byzantine node detected",
        "Cache cleared",
        "Database connection restored",
        "Alert triggered"
    ]
    
    for i in range(count):
        log = SystemLog(
            timestamp=datetime.utcnow() - timedelta(minutes=i*2),
            level=random.choice(log_levels),
            source=random.choice(sources),
            message=random.choice(messages),
            node_id=f"edge-node-{random.randint(1, 5)}" if random.random() > 0.3 else None,
            category=random.choice(['system', 'detection', 'consensus', 'network']),
            details={"mock": True, "index": i}
        )
        db.add(log)
    
    db.commit()
    print(f"✅ Created {count} logs")


def populate_database():
    """Main function to populate database"""
    print("🌱 Populating EDGE-QI Database with Mock Data")
    print("=" * 50)
    print("")
    
    db = SessionLocal()
    
    try:
        # Create mock data
        nodes = create_mock_nodes(db, count=5)
        create_mock_detections(db, nodes, count=50)
        create_mock_metrics(db, count=20)
        create_mock_consensus_rounds(db, count=10)
        create_mock_logs(db, count=30)
        
        print("")
        print("=" * 50)
        print("✅ Database population complete!")
        print("")
        print("📊 Summary:")
        print(f"   - 5 Edge Nodes")
        print(f"   - 50 Detections")
        print(f"   - 20 System Metrics")
        print(f"   - 10 Consensus Rounds")
        print(f"   - 30 System Logs")
        
    except Exception as e:
        print(f"❌ Error populating database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    populate_database()
