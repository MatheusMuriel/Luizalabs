import pytest
from fastapi.testclient import TestClient

from app import app
from resources.resources import ResourceManager

resources = ResourceManager()


@pytest.fixture
def client():
    return TestClient(app)


def test_login_success(client):
    """Testa um login bem-sucedido."""
    response = client.post(
        "/user/login",
        json={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure(client):
    """Testa um login com credenciais inválidas."""
    response = client.post(
        "/user/login",
        json={"username": "username_errado", "password": "password_errado"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": resources.get("auth.login_failure")}
