from typing import List, Union

from models.client import Client

client_collection = Client


async def list_clients() -> List[Client]:
    """
    Lists all available clients.

    Returns:
        List[Client]: A list of Client objects representing
        all clients in the collection.
    """
    clients = await client_collection.find_all().to_list()
    return clients


async def get_client(id: int) -> Client:
    """
    Retrieves a specific client by ID.

    Args:
        id (int): The ID of the client to retrieve.

    Returns:
        Client: The Client object corresponding to the provided ID, if found.
    """
    client = await client_collection.get(id)

    if client:
        return client


async def add_client(new_client: Client) -> Client:
    """
    Adds a new client to the collection.

    Args:
        new_client (Client): The Client object representing
        the client to be added.

    Returns:
        Client: The Client object that was created.
    """
    client = await new_client.create()
    return client


async def delete_client(id: int) -> bool:
    """
    Removes a client from the collection by ID.

    Args:
        id (int): The ID of the client to be removed.

    Returns:
        bool: True if the client was found and removed, False otherwise.
    """
    client = await client_collection.get(id)
    if client:
        await client.delete()
        return True


async def update_client(
    id: int,
    data: dict
) -> Union[bool, Client]:
    """
    Updates the information of an existing client.

    Args:
        id (int): The ID of the client to be updated.
        data (dict): A dictionary containing the fields and values to update.

    Returns:
        Union[bool, Client]: The updated Client object if the operation is
        successful, or False if the client is not found.
    """
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {
        "$set": {field: value for field, value in des_body.items()}
    }
    client = await client_collection.get(id)
    if client:
        await client.update(update_query)
        return client
    return False
