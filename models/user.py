from beanie import Document
from fastapi.security import HTTPBasicCredentials


class User(Document):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin",
            }
        }

    class Settings:
        name = "user"


class UserLogin(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {"username": "admin", "password": "admin"}
        }
