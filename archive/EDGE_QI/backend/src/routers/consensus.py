"""
Consensus API endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import ConsensusRound as ConsensusRoundModel
from ..schemas import ConsensusRound, ConsensusRoundCreate
from ..services.websocket_service import ws_service

router = APIRouter()


@router.get("/rounds", response_model=List[ConsensusRound])
async def list_consensus_rounds(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    List consensus rounds
    """
    rounds = db.query(ConsensusRoundModel).order_by(
        ConsensusRoundModel.timestamp.desc()
    ).offset(offset).limit(limit).all()
    
    return rounds


@router.get("/rounds/{round_id}", response_model=ConsensusRound)
async def get_consensus_round(round_id: int, db: Session = Depends(get_db)):
    """
    Get specific consensus round details
    """
    from fastapi import HTTPException
    
    round_data = db.query(ConsensusRoundModel).filter(
        ConsensusRoundModel.id == round_id
    ).first()
    
    if not round_data:
        raise HTTPException(status_code=404, detail=f"Consensus round {round_id} not found")
    
    return round_data


@router.post("/rounds", response_model=ConsensusRound, status_code=201)
async def create_consensus_round(
    consensus: ConsensusRoundCreate,
    db: Session = Depends(get_db)
):
    """
    Record a new consensus round
    """
    db_consensus = ConsensusRoundModel(
        **consensus.model_dump(),
        timestamp=datetime.utcnow()
    )
    
    db.add(db_consensus)
    db.commit()
    db.refresh(db_consensus)
    
    # Broadcast consensus update
    consensus_data = ConsensusRound.model_validate(db_consensus).model_dump()
    consensus_data['timestamp'] = consensus_data['timestamp'].isoformat()
    await ws_service.broadcast_consensus_update(consensus_data)
    
    # Log if there were Byzantine nodes detected
    if consensus.byzantine_nodes:
        await ws_service.broadcast_log({
            'level': 'warning',
            'source': 'consensus',
            'message': f'Byzantine nodes detected in round {consensus.round_number}: {", ".join(consensus.byzantine_nodes)}',
            'details': {'round_id': db_consensus.id, 'byzantine_nodes': consensus.byzantine_nodes}
        })
    
    return db_consensus


@router.get("/stats/summary")
async def consensus_summary(db: Session = Depends(get_db)):
    """
    Get consensus statistics summary
    """
    from sqlalchemy import func
    
    total_rounds = db.query(ConsensusRoundModel).count()
    successful_rounds = db.query(ConsensusRoundModel).filter(
        ConsensusRoundModel.success == True
    ).count()
    
    avg_duration = db.query(
        func.avg(ConsensusRoundModel.duration_ms)
    ).scalar() or 0
    
    avg_participants = db.query(
        func.avg(ConsensusRoundModel.participants)
    ).scalar() or 0
    
    # Get recent rounds
    recent_rounds = db.query(ConsensusRoundModel).order_by(
        ConsensusRoundModel.timestamp.desc()
    ).limit(10).all()
    
    return {
        'total_rounds': total_rounds,
        'successful_rounds': successful_rounds,
        'success_rate': round(successful_rounds / total_rounds * 100, 2) if total_rounds > 0 else 0,
        'average_duration_ms': round(avg_duration, 2),
        'average_participants': round(avg_participants, 1),
        'recent_rounds': [
            {
                'round_number': r.round_number,
                'success': r.success,
                'participants': r.participants,
                'duration_ms': r.duration_ms,
                'timestamp': r.timestamp.isoformat()
            }
            for r in recent_rounds
        ]
    }
