from typing import Any, Optional, Union, List

from beanie import Document
from pydantic import BaseModel, EmailStr, Field


class Client(Document):
    id: int = Field(alias="_id")
    name: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "João Silva",
                "email": "joao.silva@example.com"
            }
        }

    class Settings:
        name = "clients"


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Union[Any, List[Any]]]

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": {
                    "id": 1,
                    "name": "João Silva",
                    "email": "joao.silva@example.com"
                }
            }
        }


class UpdateClientModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Silvão Joilva",
                "email": "silva.joao@exemple.com"
            }
        }
