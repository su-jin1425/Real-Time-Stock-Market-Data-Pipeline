from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.stocks import AnalyticsMetric

def get_auth_headers(client: TestClient) -> dict:
    try:
        client.post(
            "/api/v1/auth/register",
            json={"email": "analyticstest@example.com", "password": "securepassword"}
        )
    except:
        pass
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "analyticstest@example.com", "password": "securepassword"}
    )
    token = response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

def test_get_analytics_overview(client: TestClient, db_session: Session):
    db_session.add(AnalyticsMetric(stock_symbol="META", moving_average=300, volatility=5.0))
    db_session.add(AnalyticsMetric(stock_symbol="AMZN", moving_average=3400, volatility=15.0))
    db_session.commit()
    
    headers = get_auth_headers(client)
    response = client.get("/api/v1/analytics/overview", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_symbols_tracked"] == 2
    assert data["average_market_volatility"] == 10.0

def test_get_market_trends(client: TestClient, db_session: Session):
    headers = get_auth_headers(client)
    response = client.get("/api/v1/analytics/market-trends", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_volatility(client: TestClient, db_session: Session):
    headers = get_auth_headers(client)
    response = client.get("/api/v1/analytics/volatility", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_volume(client: TestClient, db_session: Session):
    headers = get_auth_headers(client)
    response = client.get("/api/v1/analytics/volume", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
