"""
Database initialization script
Creates all tables in the database
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.database import Base, engine
from src.models import EdgeNode, Detection, SystemMetric, ConsensusRound, SystemLog, Alert


def init_database():
    """Initialize database with all tables"""
    print("🔧 Initializing EDGE-QI Database...")
    print(f"📍 Database URL: {engine.url}")
    print("")
    
    try:
        # Create all tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tables created successfully:")
        for table in Base.metadata.sorted_tables:
            print(f"   - {table.name}")
        
        print("")
        print("✅ Database initialization complete!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    init_database()
