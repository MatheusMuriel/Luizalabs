# import pytest
from pytest import fixture
from starlette.testclient import TestClient
from config.config import db_client
# from database.product import product_collection
from app import app, token_listener

# @fixture(scope="session")
# def test_X():
#     return {
#         "_id": "10",
#         "name": "test",
#         "description": "test",
#         "type": "single value",
#         "crt_at": "2022-06-27T12:23:15.143Z",
#         "upd_at": "2022-06-27T12:23:15.143Z"
#     }

# # test_Y and test_Z fixtures should be like test_X


@fixture(scope="session", autouse=True)
def test_client():
    app.dependency_overrides[token_listener] = lambda: {}
    with TestClient(app) as test_client:
        yield test_client

    # db = db_client
    # Here, delete any objects you have created for your tests
    # db[product_collection].delete_one({
    #             "id": 1,
    #             "title": "Teste",
    #             "price": 100.00,
    #             "image": "https://site.com/foto.jpg",
    #             "brand": "Marka",
    #             "reviewScore": 9.4,
    #         }
    # )
