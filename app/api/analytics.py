from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api import deps
from app.models.stocks import AnalyticsMetric
from app.models.user import User

router = APIRouter()

@router.get("/overview")
def get_analytics_overview(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    # A dummy overview aggregation for the enterprise dashboard
    total_symbols = db.query(func.count(func.distinct(AnalyticsMetric.stock_symbol))).scalar()
    avg_volatility = db.query(func.avg(AnalyticsMetric.volatility)).scalar()
    return {"total_symbols_tracked": total_symbols, "average_market_volatility": avg_volatility}

@router.get("/market-trends")
def get_market_trends(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    trends = db.query(AnalyticsMetric).order_by(AnalyticsMetric.created_at.desc()).limit(10).all()
    return [{"symbol": t.stock_symbol, "moving_average": t.moving_average, "trend": "up" if t.moving_average and t.moving_average > 0 else "down"} for t in trends]

@router.get("/volatility")
def get_market_volatility(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    volatilities = db.query(AnalyticsMetric).order_by(AnalyticsMetric.volatility.desc()).limit(10).all()
    return [{"symbol": v.stock_symbol, "volatility": v.volatility} for v in volatilities]

@router.get("/volume")
def get_market_volume(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    volumes = db.query(AnalyticsMetric).order_by(AnalyticsMetric.trading_volume.desc()).limit(10).all()
    return [{"symbol": v.stock_symbol, "volume": v.trading_volume} for v in volumes]
