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


def test_get_favorites_existing_client(test_client):
    """
    Testa a listagem de favoritos de um cliente existente.
    """
    client_id = 9881

    # Create a user
    client_data = get_default_client(client_id)
    test_client.delete(f"/client/{client_id}")
    test_client.post("/client", json=client_data)

    # Get favorites
    response = test_client.get(f"/favorite/{client_id}")

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["response_type"] == resources.get("requests.success")
    assert (
        json_response["description"]
        == resources.get("favorites.retrieved")
    )

    # Delete the created user
    test_client.delete(f"/client/{client_id}")


def test_get_favorites_nonexistent_client(test_client):
    """
    Testa a tentativa de listar favoritos de um cliente inexistente.
    """
    client_id = 9999999
    response = test_client.get(f"/favorite/{client_id}")

    assert response.status_code == 404
    json_response = response.json()
    assert (
        json_response["detail"]
        == resources.get("client.not_found").format(client_id)
    )


def test_add_favorite(test_client):
    """
    Testa a adição de um produto aos favoritos de um cliente.
    """
    client_id = 99982
    product_id = 99982

    # Prepare the instances
    test_client.delete(f"/client/{client_id}")
    test_client.post("/client", json=get_default_client(client_id))
    test_client.delete(f"/product/{product_id}")
    test_client.post("/product", json=get_default_product(product_id))
    test_client.delete("/favorite/", params={
        "client_id": client_id, "product_id": product_id
    })

    # Add the favorite
    response = test_client.post("/favorite/", params={
        "client_id": client_id, "product_id": product_id
    })

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["response_type"] == resources.get("requests.success")
    assert (
        json_response["description"]
        == resources.get("favorites.added").format(product_id)
    )

    # Delete the created instances
    test_client.delete(f"/client/{client_id}")
    test_client.delete(f"/product/{product_id}")
    test_client.delete("/favorite/", params={
        "client_id": client_id, "product_id": product_id
    })


def test_delete_favorite_existing(test_client):
    """
    Testa a exclusão de um produto dos favoritos de um cliente.
    """
    client_id = 9998
    product_id = 9998
    # Prepare the instances
    test_client.delete(f"/client/{client_id}")
    test_client.post("/client", json=get_default_client(client_id))
    test_client.delete(f"/product/{product_id}")
    test_client.post("/product", json=get_default_product(product_id))
    test_client.post("/favorite/", params={
        "client_id": client_id, "product_id": product_id
    })

    response = test_client.delete("/favorite/", params={
        "client_id": client_id, "product_id": product_id
    })

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["response_type"] == resources.get("requests.success")
    assert (
        json_response["description"]
        == resources.get("favorites.removed").format(product_id)
    )

    test_client.delete(f"/client/{client_id}")
    test_client.delete(f"/product/{product_id}")


def test_delete_favorite_nonexistent(test_client):
    """
    Testa a tentativa de exclusão de um favorito inexistente.
    """
    client_id = 999999
    product_id = 999999
    test_client.delete("/favorite/", params={
        "client_id": client_id, "product_id": product_id
    })
    response = test_client.delete("/favorite/", params={
        "client_id": client_id, "product_id": product_id
    })

    assert response.status_code == 404
    json_response = response.json()
    assert (
        json_response["detail"]
        == resources.get("favorites.not_found_for_product").format(product_id)
    )
