from resources.resources import ResourceManager

resources = ResourceManager()


def get_default_client(id):
    return {
        "id": id,
        "name": f"Client {id}",
        "email": f"client{id}@example.com",
    }


def get_default_product(id):
    return {
        "id": id,
        "title": f"Product {id}",
        "price": 100.0,
        "image": f"https://site.com/product{id}.jpg",
        "brand": f"Brand {id}",
        "reviewScore": 9.1,
    }


def test_get_products(test_client):
    """
    Testa a listagem de produtos na primeira página.
    """
    id_to_get = 99991
    test_client.post("/product", json=get_default_product(id_to_get))
    response = test_client.get("/product", params={"page": 1})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status_code"] == 200
    assert json_response["response_type"] == resources.get("requests.success")
    assert (
        json_response["description"]
        == resources.get("product.product_retrived")
    )

    test_client.delete(f"/product/{id_to_get}")


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
    id_to_get = 99999100
    test_client.post("/product", json=get_default_product(id_to_get))
    response = test_client.get(f"/product/{id_to_get}")
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["status_code"] == 200
    assert json_response["response_type"] == resources.get("requests.success")
    assert (
        json_response["description"]
        == resources.get("product.product_retrived")
    )

    test_client.delete(f"/product/{id_to_get}")


def test_get_product_data_nonexistent(test_client):
    """
    Testa a tentativa de recuperar dados de um produto inexistente.
    """
    id_to_get = 999987
    test_client.delete(f"/product/{id_to_get}")
    response = test_client.get(f"/product/{id_to_get}")
    json_response = response.json()
    assert response.status_code == 404
    assert (
        json_response["detail"]
        == resources.get("product.product_not_exists")
    )


def test_add_product(test_client):
    """
    Testa a adição de um novo produto.
    """
    id_to_get = 99923
    test_client.delete(f"/product/{id_to_get}")
    response = test_client.post(
        "/product",
        json=get_default_product(id_to_get)
    )
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["response_type"] == resources.get("requests.success")
    assert (
        json_response["description"]
        == resources.get("product.product_creates_request")
    )

    test_client.delete(f"/product/{id_to_get}")


def test_add_existing_product(test_client):
    """
    Testa a adição de um produto já existente.
    """
    id_to_get = 9999823
    product_data = get_default_product(id_to_get)
    test_client.post("/product", json=product_data)
    response = test_client.post("/product", json=product_data)
    json_response = response.json()
    assert response.status_code == 409
    assert (
        json_response["detail"]
        == resources.get("product.product_already_exists")
    )
    test_client.delete(f"/product/{id_to_get}")


def test_delete_product(test_client):
    """
    Testa a exclusão de um produto existente.
    """
    id_to_delete = 999982
    test_client.delete(f"/product/{id_to_delete}")
    test_client.post("/product", json=get_default_product(id_to_delete))
    response = test_client.delete(f"/product/{id_to_delete}")
    json_response = response.json()
    assert json_response["status_code"] == 200
    assert json_response["response_type"] == resources.get("requests.success")
    assert (
        json_response["description"]
        == resources.get("product.product_removed").format(id_to_delete)
    )


def test_delete_nonexistent_product(test_client):
    """
    Testa a exclusão de um produto inexistente.
    """
    id_to_delete = 999998721
    response = test_client.delete(f"/product/{id_to_delete}")
    json_response = response.json()
    assert response.status_code == 404
    assert (
        json_response["detail"]
        == resources.get("product.id_not_exists").format(id_to_delete)
    )


def test_update_product(test_client):
    """
    Testa a atualização de um produto existente.
    """
    id_to_update = 99931223
    test_client.post("/product", json=get_default_product(id_to_update))
    update_data = {
        "name": "Updated Product",
        "price": 150.0,
    }
    response = test_client.put(f"/product/{id_to_update}", json=update_data)
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["status_code"] == 200
    assert json_response["response_type"] == resources.get("requests.success")
    assert (
        json_response["description"]
        == resources.get("product.product_updated").format(id_to_update)
    )
    test_client.delete(f"/product/{id_to_update}")


def test_update_nonexistent_product(test_client):
    """
    Testa a atualização de um produto inexistente.
    """
    id_to_update = 9999312313
    update_data = {
        "name": "Nonexistent Product",
        "description": "Does not exist",
        "price": 150.0,
    }
    response = test_client.put(f"/product/{id_to_update}", json=update_data)
    json_response = response.json()
    assert response.status_code == 404
    assert (
        json_response["detail"]
        == resources.get("product.product_not_found").format(id_to_update)
    )


def test_update_to_existing_product_id(test_client):
    """
    Testa a tentativa de atualizar um produto para um ID já existente.
    """
    id_original = 9999321
    id_to_update = 999931231
    test_client.delete(f"/product/{id_original}")
    test_client.post("/product", json=get_default_product(id_original))
    test_client.delete(f"/product/{id_to_update}")
    test_client.post("/product", json=get_default_product(id_to_update))

    update_data = {
        "id": id_to_update,
        "name": "Duplicate ID Product",
        "price": 333.0,
    }
    response = test_client.put(f"/product/{id_original}", json=update_data)
    json_response = response.json()
    assert response.status_code == 409
    assert (
        json_response["detail"]
        == resources.get("product.product_id_already_exists")
    )
    test_client.delete(f"/product/{id_original}")
    test_client.delete(f"/product/{id_to_update}")
