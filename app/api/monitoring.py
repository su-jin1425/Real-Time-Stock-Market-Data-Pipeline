from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.pipeline import MonitoringMetric
from app.models.user import User

router = APIRouter()

@router.get("/metrics")
def get_monitoring_metrics(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    metrics = db.query(MonitoringMetric).order_by(MonitoringMetric.created_at.desc()).limit(100).all()
    return metrics

@router.get("/streams")
def get_stream_health(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    return {
        "kafka_status": "healthy",
        "spark_streaming_status": "active",
        "active_partitions": 3
    }
