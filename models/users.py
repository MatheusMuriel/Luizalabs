from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class User(Document):
  login: str
  password: str

  class Config:
    json_schema_extra = {
      "example": {
        "login": "admin",
        "password": "admin",
      }
    }

  class Settings:
    name = "user"


class UserSignIn(HTTPBasicCredentials):
  class Config:
    json_schema_extra = {
      "example": {"login": "admin", "password": "admin"}
    }
