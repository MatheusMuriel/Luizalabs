import pytest
from fastapi.testclient import TestClient

from app import app
from auth.jwt_bearer import verify_jwt
from resources.resources import ResourceManager

resources = ResourceManager()


@pytest.fixture
def client():
    return TestClient(app)


def test_login_success(client):
    """Testa um login bem-sucedido."""
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure(client):
    """Testa um login com credenciais inválidas."""
    response = client.post(
        "/auth/login",
        json={"username": "username_errado", "password": "password_errado"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": resources.get("auth.login_failure")}


def test_valid_token(client):
    """Testa um acesso com token valido."""
    response_login = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin"}
    )
    token = response_login.json()["access_token"]
    assert verify_jwt(token)
