from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.stocks import StockPrice, AnalyticsMetric
from app.models.user import User

router = APIRouter()

@router.get("/")
def get_stocks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve list of stocks.
    """
    stocks = db.query(StockPrice.stock_symbol).distinct().offset(skip).limit(limit).all()
    return {"stocks": [stock[0] for stock in stocks]}

@router.get("/{symbol}")
def get_stock_by_symbol(
    symbol: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get latest stock price for a symbol.
    """
    stock = db.query(StockPrice).filter(StockPrice.stock_symbol == symbol).order_by(StockPrice.timestamp.desc()).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return {"symbol": stock.stock_symbol, "price": stock.price, "volume": stock.volume, "timestamp": stock.timestamp}

@router.get("/{symbol}/history")
def get_stock_history(
    symbol: str,
    db: Session = Depends(deps.get_db),
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get history for a specific stock.
    """
    history = db.query(StockPrice).filter(StockPrice.stock_symbol == symbol).order_by(StockPrice.timestamp.desc()).limit(limit).all()
    return [{"price": h.price, "volume": h.volume, "timestamp": h.timestamp} for h in history]

@router.get("/{symbol}/analytics")
def get_stock_analytics(
    symbol: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get real-time analytics for a specific stock.
    """
    analytics = db.query(AnalyticsMetric).filter(AnalyticsMetric.stock_symbol == symbol).order_by(AnalyticsMetric.created_at.desc()).first()
    if not analytics:
        raise HTTPException(status_code=404, detail="Analytics not found for this stock")
    return {
        "symbol": analytics.stock_symbol,
        "moving_average": analytics.moving_average,
        "volatility": analytics.volatility,
        "trading_volume": analytics.trading_volume,
        "calculated_at": analytics.created_at
    }
