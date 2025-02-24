from typing import Any, Union

from beanie import Document
from pydantic import BaseModel


class Favorite(Document):
    client_id: int
    product_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "client_id": 1,
                "product_id": 1,
            }
        }

    class Settings:
        name = "favorite"


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Union[str, Any]

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
