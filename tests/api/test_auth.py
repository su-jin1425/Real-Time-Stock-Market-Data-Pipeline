from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_register_existing_user(client: TestClient):
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={"email": "test2@example.com", "password": "securepassword"}
    )
    # Register again
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test2@example.com", "password": "securepassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_user(client: TestClient):
    # Setup user
    client.post(
        "/api/v1/auth/register",
        json={"email": "testlogin@example.com", "password": "securepassword"}
    )
    # Login
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testlogin@example.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wrong@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 400
