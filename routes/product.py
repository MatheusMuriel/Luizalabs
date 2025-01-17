from fastapi import APIRouter, Body, HTTPException

import database.favorite as DatabaseFavorite
import database.product as DatabaseProduct
from models.product import Product, Response, UpdateProductModel
from resources.resources import ResourceManager

resources = ResourceManager()
router = APIRouter()


@router.get(
    "/",
    response_description=resources.get("requests.product_retrived_request"),
    response_model=Response
)
async def get_products(page: int):
    """
    Retrieve a paginated list of products.

    Args:
        page (int): The current page number.

    Returns:
        dict: A dictionary containing the status code, response type,
        description, and product data.
    """
    """
    Não colocado o tamanho da pagina pois não estava na documentação
    """
    products = await DatabaseProduct.list_products(page=page)
    return {
        "status_code": 200,
        "response_type": resources.get("requests.success"),
        "description": resources.get("product.product_retrived"),
        "data": products,
    }


@router.get(
    "/{id}",
    response_description=resources.get("product.product_retrived"),
    response_model=Response
)
async def get_product_data(id: int):
    """
    Retrieve data for a specific product by ID.

    Args:
        id (int): The ID of the product to retrieve.

    Returns:
        dict: A dictionary containing the status code, response type,
        description, and product data if the product exists. If not, an
        error message is returned.
    """

    product = await DatabaseProduct.get_product(id)
    if product:
        return {
            "status_code": 200,
            "response_type": resources.get("requests.success"),
            "description": resources.get("product.product_retrived"),
            "data": product,
        }
    raise HTTPException(
        status_code=404,
        detail=resources.get("product.product_not_exists")
    )


@router.post(
    "/",
    response_description=resources.get("product.product_created"),
    response_model=Response
)
async def add_product_data(product: Product = Body(...)):
    """
    Add a new product to the database.

    Args:
        product (Product): The product data to add.

    Returns:
        dict: A dictionary containing the status code, response type,
        description, and newly created product data.

    Raises:
        HTTPException: If a product with the same ID already exists.
"""

    product_exists = await Product.find_one(Product.id == product.id)
    if product_exists:
        raise HTTPException(
            status_code=409,
            detail=resources.get("product.product_already_exists")
        )

    new_product = await DatabaseProduct.add_product(product)
    return {
        "status_code": 201,
        "response_type": resources.get("requests.success"),
        "description": resources.get("product.product_creates_request"),
        "data": new_product,
    }


@router.delete(
    "/{id}",
    response_description=resources.get("product.product_deleted")
)
async def delete_product(id: int):
    """
    Delete a product from the database by ID.

    Args:
        id (int): The ID of the product to delete.

    Returns:
        dict: A dictionary containing the status code, response type,
        description, and a flag indicating whether the product was deleted.
    """

    # Antes de excluir o produto é necessário excluir os favoritos dele
    # Fazendo sem transação por não ter os replicasets configurados
    await DatabaseFavorite.delete_all_favorites(product_id=id)

    deleted_product = await DatabaseProduct.delete_product(id)
    if deleted_product:
        return {
            "status_code": 200,
            "response_type": resources.get("requests.success"),
            "description": resources.get("product.product_removed").format(id),
            "data": deleted_product,
        }
    raise HTTPException(
        status_code=404,
        detail=resources.get("product.id_not_exists").format(id),
    )


@router.put(
    "/{id_product}",
    response_model=Response
)
async def update_product(id_product: int, req: UpdateProductModel = Body(...)):
    """
    Update an existing product by ID.

    Args:
        id_product (int): The ID of the product to update.
        req (UpdateProductModel): The updated product data.

    Returns:
        dict: A dictionary containing the status code, response type,
        description, and updated product data if successful. If not, an
        error message is returned.
    """
    updated_product = await DatabaseProduct.update_product_data(
        id_product, req.dict()
    )
    if updated_product:
        return {
            "status_code": 200,
            "response_type": resources.get("requests.success"),
            "description": resources
            .get("product.product_updated")
            .format(id_product),
            "data": updated_product,
        }
    raise HTTPException(
        status_code=404,
        detail=resources.get("product.product_not_found").format(id_product),
    )
