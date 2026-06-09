from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.db.base_class import Base

class PipelineExecution(Base):
    __tablename__ = "pipeline_executions"

    id = Column(Integer, primary_key=True, index=True)
    workflow_name = Column(String, index=True, nullable=False)
    execution_status = Column(String, nullable=False)
    started_at = Column(DateTime(timezone=True), default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

class DataQualityLog(Base):
    __tablename__ = "data_quality_logs"

    id = Column(Integer, primary_key=True, index=True)
    validation_type = Column(String, index=True, nullable=False)
    validation_status = Column(String, nullable=False)
    log_payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

class MonitoringMetric(Base):
    __tablename__ = "monitoring_metrics"

    id = Column(Integer, primary_key=True, index=True)
    pipeline_latency = Column(Float, nullable=True)
    kafka_throughput = Column(Float, nullable=True)
    spark_processing_time = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
