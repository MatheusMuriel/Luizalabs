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


def test_protected_route_without_token(client):
    """Testa o acesso a uma rota protegida sem token de autenticação."""
    response = client.get("/client")
    assert response.status_code == 403
    assert response.json() == {
        "detail": resources.get("auth.not_authenticated")
    }
