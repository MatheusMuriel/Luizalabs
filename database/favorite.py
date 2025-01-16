from typing import Union
from fastapi import HTTPException

from models.favorite import Favorite, Response
from models.client import Client
from models.product import Product
from resources.resources import ResourceManager

from database.client import client_collection
from database.product import product_collection

resources = ResourceManager()
favorites_collection = Favorite


async def get_favorites(client: Client) -> list[Favorite]:
    """
    Retrieves the list of favorite products for a client.

    Args:
        client (Client): The client whose favorites will be retrieved.

    Returns:
        Union[list[Favorite], Response]: List of favorite products
        or an error response.
    """

    # # Validate if the client exists
    # client_exists = await Client.find_one({"id": client.id})
    # if not client_exists:
    #     raise HTTPException(
    #         status_code=404,
    #         detail=resources.get("favorites.client_not_found")
    #         .format(client.id)
    #     )

    # Retrieve favorites
    favorites = await favorites_collection.find({"client_id": client.id}).to_list()

    return favorites


async def add_favorite(client_id: Client, product_id: Product) -> Response:
    """
    Adds a product to the client's list of favorites.

    Args:
        client (Client): The client adding the favorite.
        product (Product): The product to be added as a favorite.

    Returns:
        Response: The result of the operation.
    """

    # Validate if the client exists
    client_exists = await client_collection.get(client_id)
    if not client_exists:
        raise HTTPException(
            status_code=404,
            detail=resources.get("favorites.client_not_found").format(client_id)
        )

    # Validate if the product exists
    product_exists = await product_collection.get(product_id)
    if not product_exists:
        raise HTTPException(
            status_code=404,
            detail=resources.get("favorites.products_not_found").format(product_id)
        )

    # Check if the favorite already exists
    existing_favorite = await favorites_collection.find_one(
        {"client_id": client_id, "product_id": product_id}
    )
    if existing_favorite:
        raise HTTPException(
            status_code=409,
            detail=resources.get("favorites.already_exists").format(product_id)
        )
    
    # Create the favorite
    new_favorite = Favorite(client_id=client_id, product_id=product_id)
    await new_favorite.create()
    new_favorite = new_favorite.dict().pop("id")
    return new_favorite


async def delete_favorite(client_id: Client, product_id: Product) -> Response:
    """
    Removes a product from the client's list of favorites.

    Args:
        client (Client): The client removing the favorite.
        product (Product): The product to be removed from favorites.

    Returns:
        Response: The result of the operation.
    """

    # Check if the favorite exists
    favorite_to_delete = await favorites_collection.find_one(
        {"client_id": client_id, "product_id": product_id}
    )
    if not favorite_to_delete:
        raise HTTPException(
            status_code=404,
            detail=resources.get("favorites.not_found_for_product").format(product_id)
        )

    # Remove the favorite
    await favorite_to_delete.delete()

    return Response(
        status_code=200,
        response_type=resources.get("requests.success"),
        description=resources.get("favorites.removed").format(product_id),
        data=favorite_to_delete
    )
