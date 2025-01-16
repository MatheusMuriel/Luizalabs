import pytest
# from fastapi.testclient import TestClient
# from app import app, token_listener
from resources.resources import ResourceManager
# import database.product as DatabaseProduct

# import asyncio
# from beanie import init_beanie
# from motor.motor_asyncio import AsyncIOMotorClient
# from config.config import initiate_database, shutdown_database
# from models.product import Product  # Substitua pelo caminho correto do modelo
# from tests.conftest import test_client
# from httpx import AsyncClient

resources = ResourceManager()


def test_get(test_client):
    response = test_client.get("/product/1")
    assert response.status_code == 200
    # //Add assertions as needed


def test_create_X(test_client):
    response = test_client.post("/product/", json={
            "id": 13,
            "title": "Teste",
            "price": 100.00,
            "image": "https://site.com/foto.jpg",
            "brand": "Marka",
            "reviewScore": 9.4,
        }
    )
    assert response.status_code == 201
    # //Add assertions as needed


def test_get_products(test_client):
    """
    Testa a listagem de produtos na primeira página.
    """
    response = test_client.get("/product", params={"page": 1})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status_code"] == 200
    assert json_response["response_type"] == resources.get("requests.success")
    assert json_response["description"] == resources.get("product.product_retrived")


def test_get_invalid_page(test_client):
    """
    Testa a tentativa de acessar uma página inválida.
    """
    response = test_client.get("/product", params={"page": 999})
    json_response = response.json()
    assert response.status_code == 404
    assert json_response["detail"] == resources.get("product.out_of_pages")


def test_get_product_data_existing(test_client):
    """
    Testa a recuperação de dados de um produto existente.
    """
    response = test_client.get("/product/1")
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["status_code"] == 200
    assert json_response["response_type"] == resources.get("requests.success")
    assert json_response["description"] == resources.get("product.product_retrived")


def test_get_product_data_nonexistent(test_client):
    """
    Testa a tentativa de recuperar dados de um produto inexistente.
    """
    response = test_client.get("/product/999")
    json_response = response.json()
    assert response.status_code == 404
    assert json_response["detail"] == resources.get("product.product_not_exists")


def test_add_existing_product(test_client):
    """
    Testa a adição de um produto já existente.
    """
    product_data = {
        "id": 1,
        "title": "Teste",
        "price": 100.00,
        "image": "https://site.com/foto.jpg",
        "brand": "Marka",
        "reviewScore": 9.4,
    }
    response = test_client.post("/product", json=product_data)
    json_response = response.json()
    assert response.status_code == 409
    assert json_response["detail"] == resources.get("product.product_already_exists")


def test_delete_product(test_client):
    """
    Testa a exclusão de um produto existente.
    """
    id_to_delete = 1
    response = test_client.delete(f"/product/{id_to_delete}")
    json_response = response.json()
    assert json_response["status_code"] == 200
    assert json_response["response_type"] == resources.get("requests.success")
    assert json_response["description"] == resources.get("product.product_removed").format(id_to_delete)


def test_delete_nonexistent_product(test_client):
    """
    Testa a exclusão de um produto inexistente.
    """
    id_to_delete = 999
    response = test_client.delete(f"/product/{id_to_delete}")
    json_response = response.json()
    assert json_response["status_code"] == 404
    assert json_response["response_type"] == resources.get("requests.error")
    assert json_response["description"] == resources.get("product.id_not_exists").format(id_to_delete)


def test_update_product(test_client):
    """
    Testa a atualização de um produto existente.
    """
    update_data = {
        "name": "Updated Product",
        "price": 150.0,
    }
    response = test_client.put("/product/2", json=update_data)
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["status_code"] == 200
    assert json_response["response_type"] == resources.get("requests.success")
    assert json_response["description"] == resources.get("product.product_updated").format(2)


def test_update_nonexistent_product(test_client):
    """
    Testa a atualização de um produto inexistente.
    """
    id_to_update = 999
    update_data = {
        "name": "Nonexistent Product",
        "description": "Does not exist",
        "price": 150.0,
    }
    response = test_client.put(f"/product/{id_to_update}", json=update_data)
    json_response = response.json()
    assert response.status_code == 404
    assert json_response["detail"] == resources.get("product.product_not_found").format(id_to_update)


def test_update_to_existing_product_id(test_client):
    """
    Testa a tentativa de atualizar um produto para um ID já existente.
    """
    id_original = 3
    id_to_update = 2
    update_data = {
        "id": id_to_update,
        "name": "Duplicate ID Product",
        "price": 333.0,
    }
    response = test_client.put(f"/product/{id_original}", json=update_data)
    json_response = response.json()
    assert response.status_code == 409
    assert json_response["detail"] == resources.get("product.product_id_already_exists")
