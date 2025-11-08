"""
Detection API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from ..database import get_db
from ..models import Detection as DetectionModel, EdgeNode
from ..schemas import Detection, DetectionCreate
from ..services.websocket_service import ws_service

router = APIRouter()


@router.get("/", response_model=List[Detection])
async def list_detections(
    node_id: Optional[str] = Query(None, description="Filter by node ID"),
    object_type: Optional[str] = Query(None, description="Filter by object type"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """
    List detections with optional filters
    """
    query = db.query(DetectionModel).order_by(DetectionModel.timestamp.desc())
    
    if node_id:
        query = query.filter(DetectionModel.node_id == node_id)
    
    if object_type:
        query = query.filter(DetectionModel.object_type == object_type)
    
    detections = query.offset(offset).limit(limit).all()
    return detections


@router.get("/{detection_id}", response_model=Detection)
async def get_detection(detection_id: int, db: Session = Depends(get_db)):
    """
    Get specific detection by ID
    """
    detection = db.query(DetectionModel).filter(DetectionModel.id == detection_id).first()
    
    if not detection:
        raise HTTPException(status_code=404, detail=f"Detection {detection_id} not found")
    
    return detection


@router.post("/", response_model=Detection, status_code=201)
async def create_detection(detection: DetectionCreate, db: Session = Depends(get_db)):
    """
    Record a new detection
    """
    # Verify node exists
    node = db.query(EdgeNode).filter(EdgeNode.id == detection.node_id).first()
    if not node:
        raise HTTPException(status_code=404, detail=f"Node {detection.node_id} not found")
    
    # Create detection record
    db_detection = DetectionModel(
        **detection.model_dump(),
        timestamp=datetime.utcnow()
    )
    
    db.add(db_detection)
    
    # Update node statistics
    node.total_detections += 1
    node.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_detection)
    
    # Broadcast detection
    detection_data = Detection.model_validate(db_detection).model_dump()
    detection_data['timestamp'] = detection_data['timestamp'].isoformat()
    await ws_service.broadcast_detection(detection_data)
    
    return db_detection


@router.get("/stats/summary")
async def detection_summary(
    time_range: str = Query("24h", description="Time range: 1h, 6h, 24h, 7d"),
    db: Session = Depends(get_db)
):
    """
    Get detection summary statistics
    """
    # Parse time range
    if time_range == '1h':
        time_delta = timedelta(hours=1)
    elif time_range == '6h':
        time_delta = timedelta(hours=6)
    elif time_range == '24h':
        time_delta = timedelta(hours=24)
    elif time_range == '7d':
        time_delta = timedelta(days=7)
    else:
        time_delta = timedelta(hours=24)
    
    start_time = datetime.utcnow() - time_delta
    
    # Get detections in time range
    detections = db.query(DetectionModel).filter(
        DetectionModel.timestamp >= start_time
    ).all()
    
    # Calculate statistics
    total = len(detections)
    by_type = {}
    by_node = {}
    total_confidence = 0
    
    for det in detections:
        # Count by type
        by_type[det.object_type] = by_type.get(det.object_type, 0) + 1
        
        # Count by node
        by_node[det.node_id] = by_node.get(det.node_id, 0) + 1
        
        # Sum confidence
        total_confidence += det.confidence
    
    avg_confidence = total_confidence / total if total > 0 else 0
    
    return {
        'total': total,
        'time_range': time_range,
        'average_confidence': round(avg_confidence, 4),
        'by_type': by_type,
        'by_node': by_node,
        'start_time': start_time.isoformat(),
        'end_time': datetime.utcnow().isoformat()
    }


@router.get("/recent/stream")
async def recent_detections_stream(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Get recent detections for live stream display
    """
    detections = db.query(DetectionModel).order_by(
        DetectionModel.timestamp.desc()
    ).limit(limit).all()
    
    return {
        'detections': [Detection.model_validate(d).model_dump() for d in detections],
        'count': len(detections),
        'timestamp': datetime.utcnow().isoformat()
    }
