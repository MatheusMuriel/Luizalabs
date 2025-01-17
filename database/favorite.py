from fastapi import HTTPException
from typing import Optional
from database.client import client_collection
from database.product import product_collection
from models.favorite import Favorite
from resources.resources import ResourceManager

resources = ResourceManager()
favorites_collection = Favorite


async def get_favorites(client_id: int) -> list[Favorite]:
    """
    Retrieves the list of favorite products for a client.

    Args:
        client (Client): The client whose favorites will be retrieved.

    Returns:
        list[Favorite]: List of favorite products
    """

    # Verify if the client exists
    client = await client_collection.find_one({"_id": client_id})
    if not client:
        raise HTTPException(
            status_code=404,
            detail=resources.get("client.not_found").format(client_id),
        )

    favorites = await favorites_collection\
        .find({"client_id": client_id}).to_list()

    return favorites


async def add_favorite(client_id: int, product_id: int) -> Favorite:
    """
    Adds a product to the client's list of favorites.

    Args:
        client (Client): The client adding the favorite.
        product (Product): The product to be added as a favorite.

    Returns:
        Favorite: The favorite inclued
    """

    # Validate if the client exists
    client_exists = await client_collection.get(client_id)
    if not client_exists:
        raise HTTPException(
            status_code=404,
            detail=resources.get("favorites.client_not_found")
            .format(client_id)
        )

    # Validate if the product exists
    product_exists = await product_collection.get(product_id)
    if not product_exists:
        raise HTTPException(
            status_code=404,
            detail=resources.get("favorites.products_not_found")
            .format(product_id)
        )

    # Check if the favorite already exists
    existing_favorite = await favorites_collection.find_one(
        {"client_id": client_id, "product_id": product_id}
    )
    if existing_favorite:
        raise HTTPException(
            status_code=409,
            detail=resources.get("favorites.already_exists")
            .format(product_id)
        )

    # Create the favorite
    new_favorite = Favorite(client_id=client_id, product_id=product_id)
    await new_favorite.create()
    return new_favorite


async def delete_favorite(client_id: int, product_id: int) -> bool:
    """
    Removes a product from the client's list of favorites.

    Args:
        client (Client): The client removing the favorite.
        product (Product): The product to be removed from favorites.

    Returns:
        bool: The result of the operation.
    """

    # Check if the favorite exists
    favorite_to_delete = await favorites_collection.find_one(
        {"client_id": client_id, "product_id": product_id}
    )
    if not favorite_to_delete:
        raise HTTPException(
            status_code=404,
            detail=resources.get("favorites.not_found_for_product")
            .format(product_id)
        )

    # Remove the favorite
    await favorite_to_delete.delete()

    return True


async def delete_all_favorites(
    client_id: Optional[int] = None,
    product_id: Optional[int] = None
) -> bool:
    """
    Removes all products from the clientes or products from the favorites list.

    Args:
        client (Client): The client removing the favorite.
        product (Product): The product to be removed from favorites.

    Returns:
        bool: The result of the operation.
    """

    # Antes de excluir o produto é necessário excluir os favoritos dele
    # Fazendo sem transação por não ter os replicasets configurados
    query = {}
    if client_id:
        query = {"client_id": client_id}
    elif product_id:
        query = {"product_id": product_id}

    favorites = await favorites_collection.find_many(query).to_list()
    for favorite in favorites:
        await favorite.delete()

    return True
