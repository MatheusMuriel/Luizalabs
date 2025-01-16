from fastapi import APIRouter, HTTPException, Body

import database.favorite as DatabaseFavorite
from models.favorite import Favorite, Response
from models.client import Client
from models.product import Product
from resources.resources import ResourceManager

resources = ResourceManager()
router = APIRouter()


@router.get(
    "/{client_id}",
    response_description=resources.get("favorites.retrieved"),
    response_model=Response,
)
async def get_favorites(client_id: int):
    """
    Retrieve a list of favorite products for a client.

    Args:
        client_id (int): The ID of the client.

    Returns:
        list[Favorite]: List of favorite products.
    """
    client = await Client.find_one({"id": client_id})
    if not client:
        raise HTTPException(
            status_code=404,
            detail=resources.get("client.not_found").format(client_id),
        )

    favorites = await DatabaseFavorite.get_favorites(client=client_id)
    return {
        "status_code": 200,
        "response_type": resources.get("requests.success"),
        "description": resources.get("favorites.retrieved"),
        "data": favorites,
    }


@router.post(
    "/",
    response_description=resources.get("favorites.added"),
    response_model=Response,
)
async def add_favorite(client_id: int, product_id: int):
    """
    Add a product to a client's favorites.

    Args:
        client_id (int): The ID of the client.
        product_id (int): The ID of the product.

    Returns:
        Response: The result of the operation.
    """
    # client = await Client.find_one({"id": client_id})
    # if not client:
    #     raise HTTPException(
    #         status_code=404,
    #         detail=resources.get("client.not_found").format(client_id),
    #     )

    # product = await Product.find_one({"id": product_id})
    # if not product:
    #     raise HTTPException(
    #         status_code=404,
    #         detail=resources.get("product.not_found").format(product_id),
    #     )

    # existing_favorite = await Favorite.find_one(
    #     {"client_id": client_id, "product_id": product_id}
    # )
    # if existing_favorite:
    #     raise HTTPException(
    #         status_code=409,
    #         detail=resources.get("favorites.already_exists").format(product_id)
    #     )

    new_favorite = await DatabaseFavorite.add_favorite(
        client_id=client_id,
        product_id=product_id
    )
    
    print(new_favorite)

    return {
        "status_code": 200,
        "response_type": resources.get("requests.success"),
        "description": resources.get("favorites.added").format(product_id),
        "data": new_favorite,
    }


@router.delete(
    "/",
    response_description=resources.get("favorites.removed"),
    response_model=Response,
)
async def delete_favorite(client_id: int, product_id: int):
    """
    Remove a product from a client's favorites.

    Args:
        client_id (int): The ID of the client.
        product_id (int): The ID of the product.

    Returns:
        Response: The result of the operation.
    """
    response = await DatabaseFavorite.delete_favorite(
        client_id=client_id,
        product_id=product_id
    )
    return response
