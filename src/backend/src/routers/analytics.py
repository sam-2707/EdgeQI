"""
Analytics API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.system_service import get_analytics_data
from ..schemas import AnalyticsResponse

router = APIRouter()


@router.get("/data", response_model=AnalyticsResponse)
async def analytics_data(
    time_range: str = Query("24h", description="Time range: 1h, 6h, 24h, 7d"),
    db: Session = Depends(get_db)
):
    """
    Get analytics data for all charts
    
    Returns data for:
    - Traffic trends
    - Performance metrics
    - Detection distribution
    - Bandwidth comparison
    - Energy efficiency
    - Node activity
    """
    return await get_analytics_data(db, time_range)


@router.get("/traffic")
async def traffic_analytics(
    time_range: str = Query("24h"),
    db: Session = Depends(get_db)
):
    """
    Get traffic analytics data
    """
    data = await get_analytics_data(db, time_range)
    return {
        'traffic_trends': data['traffic_trends'],
        'time_range': time_range
    }


@router.get("/performance")
async def performance_analytics(
    time_range: str = Query("24h"),
    db: Session = Depends(get_db)
):
    """
    Get performance analytics data
    """
    data = await get_analytics_data(db, time_range)
    return {
        'performance_metrics': data['performance_metrics'],
        'time_range': time_range
    }


@router.get("/distribution")
async def distribution_analytics(
    time_range: str = Query("24h"),
    db: Session = Depends(get_db)
):
    """
    Get detection distribution analytics
    """
    data = await get_analytics_data(db, time_range)
    return {
        'detection_distribution': data['detection_distribution'],
        'time_range': time_range
    }
