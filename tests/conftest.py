from pytest import fixture
from starlette.testclient import TestClient

from app import app, token_listener


@fixture(scope="session", autouse=True)
def test_client():
    app.dependency_overrides[token_listener] = lambda: {}
    with TestClient(app) as test_client:
        yield test_client
