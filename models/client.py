from typing import Any, Optional

from beanie import Document
from pydantic import BaseModel, EmailStr


class Client(Document):
    id: int
    name: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Hortelã Leopoldo Muriel",
                "email": "hortela_leopoldo@muriel.dev"
            }
        }

    class Settings:
        name = "clients"


class ClientProjection(BaseModel):
    id: int
    name: str
    email: EmailStr


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data",
            }
        }


class UpdateClientModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

    class Collection:
        name = "cliente"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Tete Popoldo Muriel",
                "email": "tete@popoldo.cat"
            }
        }
