"""
Logs API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..models import SystemLog
from ..schemas import Log, LogCreate
from ..services.websocket_service import ws_service

router = APIRouter()


@router.get("/", response_model=List[Log])
async def list_logs(
    level: Optional[str] = Query(None, description="Filter by level: info, warning, error, critical"),
    source: Optional[str] = Query(None, description="Filter by source"),
    node_id: Optional[str] = Query(None, description="Filter by node ID"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    List system logs with optional filters
    """
    query = db.query(SystemLog).order_by(SystemLog.timestamp.desc())
    
    if level:
        query = query.filter(SystemLog.level == level)
    
    if source:
        query = query.filter(SystemLog.source == source)
    
    if node_id:
        query = query.filter(SystemLog.node_id == node_id)
    
    logs = query.offset(offset).limit(limit).all()
    return logs


@router.post("/", response_model=Log, status_code=201)
async def create_log(log: LogCreate, db: Session = Depends(get_db)):
    """
    Create a new log entry
    """
    db_log = SystemLog(
        **log.model_dump(),
        timestamp=datetime.utcnow()
    )
    
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    # Broadcast log
    log_data = Log.model_validate(db_log).model_dump()
    log_data['timestamp'] = log_data['timestamp'].isoformat()
    await ws_service.broadcast_log(log_data)
    
    return db_log


@router.delete("/clear")
async def clear_logs(
    older_than_hours: int = Query(24, ge=1, description="Clear logs older than N hours"),
    db: Session = Depends(get_db)
):
    """
    Clear old logs
    """
    from datetime import timedelta
    
    cutoff_time = datetime.utcnow() - timedelta(hours=older_than_hours)
    
    deleted = db.query(SystemLog).filter(
        SystemLog.timestamp < cutoff_time
    ).delete()
    
    db.commit()
    
    return {
        'deleted': deleted,
        'message': f'Cleared {deleted} logs older than {older_than_hours} hours'
    }
