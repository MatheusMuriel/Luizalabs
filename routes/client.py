from fastapi import APIRouter, Body, HTTPException

import database.client as DatabaseClient
from models.client import Client, Response, UpdateClientModel

router = APIRouter()


@router.get(
    path="/",
    response_description="Clientes retrieved",
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
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Clientes data retrieved successfully",
        "data": clients,
    }


@router.get(
    path="/{id}",
    response_description="Cliente data retrieved",
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
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Cliente data retrieved successfully",
            "data": client,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Cliente doesn't exist",
    }


# Create Cliente
@router.post(
    path="/",
    response_description="Cliente registrado",
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
            detail="Cliente with this email supplied already exists"
        )

    new_client = await DatabaseClient.add_client(client)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Cliente created successfully",
        "data": new_client,
    }


@router.delete(
    path="/{id}",
    response_description="Cliente data deleted from the database"
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
    deleted_client = await DatabaseClient.delete_client(id)
    if deleted_client:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Cliente with ID: {} removed".format(id),
            "data": deleted_client,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Cliente with id {0} doesn't exist".format(id),
        "data": False,
    }


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
    updated_client = await DatabaseClient.update_client_data(id, req.dict())
    if updated_client:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Cliente with ID: {id} updated",
            "data": updated_client,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"An error occurred. Cliente with ID: {id} not found",
        "data": False,
    }
