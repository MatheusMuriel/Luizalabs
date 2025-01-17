from fastapi import APIRouter, Body, HTTPException

import database.client as DatabaseClient
import database.favorite as DatabaseFavorite
from models.client import Client, Response, UpdateClientModel
from resources.resources import ResourceManager

resources = ResourceManager()

router = APIRouter()


@router.get(
    path="/",
    response_description=resources.get("client.client_retrived"),
    response_model=Response
)
async def get_clients():
    """
    Retrieve all clients from the database.

    Returns:
        dict: A dictionary containing the status code, response type,
        description, and the list of all clients.
    """
    clients = await DatabaseClient.list_clients()
    clients = [client.dict() for client in clients]

    return Response(
        status_code=200,
        response_type=resources.get("requests.success"),
        description=resources.get("client.client_retrived"),
        data=clients
    )


@router.get(
    path="/{id}",
    response_description=resources.get("client.client_retrived"),
    response_model=Response
)
async def get_client_data(id: int):
    """
    Retrieve a specific client data by ID.

    Args:
        id (int): The ID of the client to retrieve.

    Returns:
        dict: A dictionary containing the status code, response type,
        description, and the client data if found, or an error message if not.
    """
    client = await DatabaseClient.get_client(id)
    if client:
        return Response(
            status_code=200,
            response_type=resources.get("requests.success"),
            description=resources.get("client.client_retrived"),
            data=client.dict()
        )
    raise HTTPException(
        status_code=404,
        detail=resources.get("client.client_not_found").format(id)
    )


@router.post(
    path="/",
    response_description=resources.get("client.client_created"),
    response_model=Response
)
async def add_client_data(client: Client = Body(...)):
    """
    Add a new client to the database.

    Args:
        cliente (Client): The cliente data to add.

    Raises:
        HTTPException: If a cliente with the same email already exists.

    Returns:
        dict: A dictionary containing the status code, response type,
        description, and the newly created cliente data.
    """
    client_exists = await Client.find_one(Client.email == client.email)
    if client_exists:
        raise HTTPException(
            status_code=409,
            detail=resources.get("client.client_already_exists")
        )

    new_client = await DatabaseClient.add_client(client)
    return Response(
        status_code=200,
        response_type=resources.get("requests.success"),
        description=resources.get("client.client_created"),
        data=new_client
    )


@router.delete(
    path="/{id}",
    response_description=resources.get("client.client_deleted"),
)
async def delete_client_data(id: int):
    """
    Delete a cliente from the database by ID.

    Args:
        id (int): The ID of the cliente to delete.

    Returns:
        dict: A dictionary containing the status code, response type,
        description, and a confirmation of deletion or an error
        message if not found.
    """

    # Antes de excluir o produto é necessário excluir os favoritos dele
    # Fazendo sem transação por não ter os replicasets configurados
    await DatabaseFavorite.delete_all_favorites(client_id=id)

    deleted_client = await DatabaseClient.delete_client(id)
    if deleted_client:
        return Response(
            status_code=200,
            response_type=resources.get("requests.success"),
            description=resources.get("client.client_removed").format(id),
            data=None
        )
    raise HTTPException(
        status_code=404,
        detail=resources.get("client.client_not_found").format(id)
    )


@router.put(
    path="/{id}",
    response_model=Response
)
async def update_client(id: int, req: UpdateClientModel = Body(...)):
    """
    Update a cliente's data in the database by ID.

    Args:
        id (int): The ID of the cliente to update.
        req (UpdateClientModel): The updated cliente data.

    Returns:
        dict: A dictionary containing the status code, response type,
        description, and the updated cliente data or an error
        message if not found.
    """
    updated_client = await DatabaseClient.update_client(id, req.dict())
    if updated_client:
        return Response(
            status_code=200,
            response_type=resources.get("requests.success"),
            description=resources.get("client.client_updated").format(id),
            data=updated_client.dict()
        )

    raise HTTPException(
        status_code=404,
        detail=resources.get("client.client_not_found").format(id)
    )
