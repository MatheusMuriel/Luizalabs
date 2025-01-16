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


def test_get_all_clients(test_client):
    """
    Testa a listagem de todos os clientes.
    """
    id_to_get = 9992
    client_data = {
        "id": id_to_get,
        "name": "Client 1",
        "email": f"client{id_to_get}@example.com",
    }
    test_client.delete(f"/client/{id_to_get}")
    test_client.post("/client", json=client_data)
    response = test_client.get("/client")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["response_type"] == resources.get("requests.success")
    assert (
        json_response["description"]
        == resources.get("client.client_retrived")
    )
    test_client.delete(f"/client/{id_to_get}")


def test_get_client_data_existing(test_client):
    """
    Testa a recuperação de dados de um cliente existente.
    """
    id_to_get = 9992
    client_data = {
        "id": id_to_get,
        "name": "Client 1",
        "email": f"client{id_to_get}@example.com",
    }
    test_client.delete(f"/client/{id_to_get}")
    test_client.post("/client", json=client_data)
    response = test_client.get("/client/1")
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["response_type"] == resources.get("requests.success")
    assert (
        json_response["description"]
        == resources.get("client.client_retrived")
    )

    test_client.delete(f"/client/{id_to_get}")


def test_get_client_data_nonexistent(test_client):
    """
    Testa a tentativa de recuperar dados de um cliente inexistente.
    """
    id_to_get = 9990
    response = test_client.get(f"/client/{id_to_get}")
    json_response = response.json()
    assert response.status_code == 404
    assert (
        json_response["detail"]
        == resources.get("client.client_not_found").format(id_to_get)
    )


def test_add_client(test_client):
    """
    Testa a adição de um novo cliente.
    """
    id_to_add = 99911
    client_data = {
        "id": id_to_add,
        "name": "Client 1",
        "email": "client1@example.com",
    }
    test_client.delete(f"/client/{id_to_add}")
    response = test_client.post("/client", json=client_data)
    json_response = response.json()
    assert response.status_code == 200
    assert json_response["response_type"] == resources.get("requests.success")
    assert (
        json_response["description"]
        == resources.get("client.client_created")
    )


def test_add_existing_client(test_client):
    """
    Testa a adição de um cliente já existente.
    """
    client_data = {
        "id": 1,
        "name": "Client 1",
        "email": "client1@example.com",
    }
    test_client.post("/client", json=client_data)
    response = test_client.post("/client", json=client_data)
    json_response = response.json()
    assert response.status_code == 409
    assert (
        json_response["detail"]
        == resources.get("client.client_already_exists")
    )


def test_delete_client(test_client):
    """
    Testa a exclusão de um cliente existente.
    """
    id_to_delete = 99911
    client_data = {
        "id": id_to_delete,
        "name": "Client 1",
        "email": f"client{99911}@example.com",
    }
    test_client.delete(f"/client/{id_to_delete}")
    test_client.post("/client", json=client_data)

    response = test_client.delete(f"/client/{id_to_delete}")
    json_response = response.json()

    assert json_response["status_code"] == 200
    assert json_response["response_type"] == resources.get("requests.success")
    assert (
        json_response["description"]
        == resources.get("client.client_removed").format(id_to_delete)
    )
    test_client.delete(f"/client/{id_to_delete}")


def test_delete_nonexistent_client(test_client):
    """
    Testa a exclusão de um cliente inexistente.
    """
    id_to_delete = 999
    test_client.delete(f"/client/{id_to_delete}")
    response = test_client.delete(f"/client/{id_to_delete}")
    json_response = response.json()
    assert response.status_code == 404
    assert (
        json_response["detail"]
        == resources.get("client.client_not_found").format(id_to_delete)
    )


def test_update_client(test_client):
    """
    Testa a atualização de um cliente existente.
    """
    id_to_update = 9992
    # Garantindo que não existe um cliente com o ID a ser atualizado
    test_client.delete(f"/client/{id_to_update}")

    # Adicionando um cliente com o ID a ser atualizado
    client_data = {
        "id": id_to_update,
        "name": "Client 1",
        "email": f"client{id_to_update}@example.com",
    }
    test_client.post("/client", json=client_data)

    # Atualizando o cliente
    new_name = "Updated Client"
    new_email = "updatedclient@example.com"
    update_data = {
        "name": new_name,
        "email": new_email,
    }
    response = test_client.put(f"/client/{id_to_update}", json=update_data)
    json_response = response.json()
    # Verificando se a resposta foi bem-sucedida
    assert response.status_code == 200
    assert json_response["response_type"] == resources.get("requests.success")

    # Verificando se os dados foram atualizados
    assert json_response["data"]["name"] == new_name
    assert json_response["data"]["email"] == new_email
    assert (
        json_response["description"]
        == resources.get("client.client_updated").format(id_to_update)
    )

    # Fazendo um get do zero para verificar se os dados foram atualizados
    response = test_client.get(f"/client/{id_to_update}")
    json_response = response.json()
    assert json_response["data"]["name"] == new_name
    assert json_response["data"]["email"] == new_email

    test_client.delete(f"/client/{id_to_update}")


def test_update_nonexistent_client(test_client):
    """
    Testa a atualização de um cliente inexistente.
    """
    id_to_update = 9993
    test_client.delete(f"/client/{id_to_update}")
    update_data = {
        "name": "Nonexistent Client",
        "email": "nonexistent@example.com",
    }
    response = test_client.put(f"/client/{id_to_update}", json=update_data)
    json_response = response.json()
    assert response.status_code == 404
    assert (
        json_response["detail"]
        == resources.get("client.client_not_found").format(id_to_update)
    )
