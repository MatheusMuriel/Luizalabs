from typing import List, Union

from models.client import Client, ClientProjection

client_collection = Client


async def list_clients() -> List[Client]:
    clients = \
        await client_collection.find_all().project(ClientProjection).to_list()
    return clients


async def add_client(new_client: Client) -> Client:
    client = await new_client.create()
    return client


async def get_client(id: int) -> Client:
    client = await client_collection.get(id)
    if client:
        return client


async def delete_client(id: int) -> bool:
    client = await client_collection.get(id)
    if client:
        await client.delete()
        return True


async def update_client(
    id: int,
    data: dict
) -> Union[bool, Client]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {
        "$set": {field: value for field, value in des_body.items()}
    }
    client = await client_collection.get(id)
    if client:
        await client.update(update_query)
        return client
    return False
