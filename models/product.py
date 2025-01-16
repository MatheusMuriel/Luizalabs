from typing import Any, List, Optional, Union

from beanie import Document, Indexed
from pydantic import BaseModel


class Product(Document):
    """
    Represents a product document in the database.

    Attributes:
        id (int): The unique identifier for the product.
        title (str): The title of the product.
        price (float): The price of the product.
        image (str): The URL to the product's image.
        brand (str): The brand of the product.
        reviewScore (Optional[float]): The review score of the product.
    """

    id: Indexed(int)
    title: str
    price: float
    image: str
    brand: str
    reviewScore: Optional[float]

    class Config:
        """
        Pydantic configuration for additional settings,
        including an example schema.
        """
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Teste",
                "price": 100.00,
                "image": "https://site.com/foto.jpg",
                "brand": "Marka",
                "reviewScore": 9.4,
            }
        }

    class Settings:
        """
        Beanie-specific settings for the Product document.

        Attributes:
            name (str): The name of the collection in the database.
        """
        name = "product"


class PaginatedProducts(BaseModel):
    """
    Represents a paginated response for a list of products.

    Attributes:
        current_page (int): The current page number in the paginated results.
        page_size (int): The number of items per page.
        total_pages (int): The total number of pages available.
        total_items (int): The total number of items available.
        products (List[Product]): The list of products for the current page.
    """
    current_page: int
    page_size: int
    total_pages: int
    total_items: int
    products: List[Product]

    class Config:
        """
        Pydantic configuration for additional settings.
        """
        json_schema_extra = {
            "example": {
                "current_page": 1,
                "page_size": 10,
                "total_pages": 5,
                "total_items": 50,
                "data": [
                    {
                        "id": 1,
                        "title": "Teste",
                        "price": 100.00,
                        "image": "https://site.com/foto.jpg",
                        "brand": "Marka",
                        "reviewScore": 9.4,
                    },
                    {
                        "id": 2,
                        "title": "Outro Product",
                        "price": 200.00,
                        "image": "https://site.com/foto.jpg",
                        "brand": "Outra Marca",
                        "reviewScore": 8.7,
                    },
                ],
            }
        }


class UpdateProductModel(BaseModel):
    """
    Represents a model for updating product information.

    Attributes:
        id (Optional[int]): The unique identifier of the product.
        title (Optional[str]): The title of the product.
        price (Optional[float]): The price of the product.
        image (Optional[str]): The URL of the product's image.
        brand (Optional[str]): The brand of the product.
        reviewScore (Optional[float]): The review score of the product.
    """
    id: Union[int, None] = None
    title: Union[str, None] = None
    price: Union[float, None] = None
    image: Union[str, None] = None
    brand: Union[str, None] = None
    reviewScore: Union[float, None] = None

    class Collection:
        """
        Specifies the name of the database collection.
        """
        name = "product"

    class Config:
        """
        Pydantic configuration for additional settings
        """
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Teste",
                "price": "100,00",
                "image": "https://site.com/foto.jpg",
                "brand": "Marka",
                "reviewScore": "9,4",
            }
        }


class Response(BaseModel):
    """
    Represents a generic response model.

    Attributes:
        status_code (int): The HTTP status code of the response.
        response_type (str): The type of response (e.g., "success", "error").
        description (str): A brief description of the response.
        data (Union[Any, List[Product]]): The data returned in the response,
        which can be of any type or a list of Product instances.
    """

    status_code: int
    response_type: str
    description: str
    data: Union[Any, List[Product]]

    class Config:
        """
        json_schema_extra: Includes an example schema for this model.
        """
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data",
            }
        }
