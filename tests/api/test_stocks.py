from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.stocks import StockPrice, AnalyticsMetric
from datetime import datetime

def get_auth_headers(client: TestClient) -> dict:
    # Register and login to get token
    client.post(
        "/api/v1/auth/register",
        json={"email": "stocktest@example.com", "password": "securepassword"}
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "stocktest@example.com", "password": "securepassword"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_stocks_empty(client: TestClient):
    headers = get_auth_headers(client)
    response = client.get("/api/v1/stocks/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"stocks": []}

def test_get_stock_by_symbol(client: TestClient, db_session: Session):
    # Seed DB
    db_session.add(StockPrice(stock_symbol="AAPL", price=150.0, volume=100))
    db_session.commit()
    
    headers = get_auth_headers(client)
    response = client.get("/api/v1/stocks/AAPL", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["price"] == 150.0

def test_get_stock_history(client: TestClient, db_session: Session):
    db_session.add(StockPrice(stock_symbol="GOOGL", price=2800.0, volume=10))
    db_session.add(StockPrice(stock_symbol="GOOGL", price=2810.0, volume=15))
    db_session.commit()
    
    headers = get_auth_headers(client)
    response = client.get("/api/v1/stocks/GOOGL/history", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["price"] in [2800.0, 2810.0]

def test_get_stock_analytics(client: TestClient, db_session: Session):
    db_session.add(AnalyticsMetric(
        stock_symbol="TSLA",
        moving_average=800.5,
        volatility=12.4,
        trading_volume=5000
    ))
    db_session.commit()
    
    headers = get_auth_headers(client)
    response = client.get("/api/v1/stocks/TSLA/analytics", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "TSLA"
    assert data["moving_average"] == 800.5
