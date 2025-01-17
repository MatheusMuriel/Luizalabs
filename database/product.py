from math import ceil
from typing import Union

from fastapi import HTTPException

from models.product import PaginatedProducts, Product
from resources.resources import ResourceManager

resources = ResourceManager()
product_collection = Product


async def list_products(page: int, page_size: int = 10) -> PaginatedProducts:
    """
    List products with pagination.

    Args:
        page (int): The current page number.
        page_size (int, optional): The number of items per page.
        Default is 10.

    Returns:
        PaginatedProducts: Paginated product data.

    Raises:
        HTTPException: If the requested page exceeds the total number of pages.
    """
    total_items = await product_collection.count()
    total_pages = ceil(total_items / page_size)
    to_skip = (page - 1) * page_size

    if page > total_pages:
        raise HTTPException(
            status_code=404,
            detail=resources.get("product.out_of_pages")
        )

    products = (
        await product_collection
        .find()
        .skip(to_skip)
        .limit(page_size)
        .to_list()
    )
    return PaginatedProducts(
        current_page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        products=products,
    )


async def get_product(id: int) -> Product:
    """
    Get a product by its ID.

    Args:
        id (int): The ID of the product.

    Returns:
        Product: The product with the specified ID, if it exists.
    """

    product = await product_collection.get(id)
    if product:
        return product
    else:
        raise HTTPException(
            status_code=404,
            detail=resources.get("product.product_not_exists")
        )


async def add_product(new_product: Product) -> Product:
    """
    Add a new product to the collection.

    Args:
        new_product (Product): The product to add.

    Returns:
        Product: The newly added product.
    """
    product = await new_product.create()
    return product


async def delete_product(id: int) -> bool:
    """
    Delete a product by its ID.

    Args:
        id (int): The ID of the product to delete.

    Returns:
        bool: True if the product was deleted, False otherwise.
    """

    product = await product_collection.get(id)
    if product:
        await product.delete()
        return True


async def update_product_data(
    id_product: int, data: dict
) -> Union[bool, Product]:
    """
    Update a product's data by its ID.

    Args:
        id_product (int): The ID of the product to update.
        data (dict): The updated data for the product.

    Returns:
        Union[bool, Product]: The updated product if successful, or
        False if the product does not exist.
    """
    if data["id"]:
        if await product_collection.get(data["id"]):
            raise HTTPException(
                status_code=409,
                detail=resources.get("product.product_id_already_exists")
            )

    product = await product_collection.get(id_product)
    if product:
        des_body = {k: v for k, v in data.items() if v is not None}
        update_query = {
            "$set": {
                field: value for field, value in des_body.items()
            }
        }
        await product.update(update_query)
        return product
    return False
