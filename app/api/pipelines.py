from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.pipeline import PipelineExecution
from app.models.user import User

router = APIRouter()

@router.get("/")
def get_pipelines(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get list of pipeline executions.
    """
    executions = db.query(PipelineExecution).order_by(PipelineExecution.started_at.desc()).limit(50).all()
    return executions

@router.get("/{id}")
def get_pipeline(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    execution = db.query(PipelineExecution).filter(PipelineExecution.id == id).first()
    if not execution:
        raise HTTPException(status_code=404, detail="Pipeline execution not found")
    return execution

@router.post("/restart")
def restart_pipeline(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    # Logic to hit Airflow API to trigger DAG
    return {"message": "Pipeline restart triggered"}
