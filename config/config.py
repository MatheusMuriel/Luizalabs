from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict
import models as models

db_client: AsyncIOMotorClient = None

class Settings(BaseSettings):
  """
  A class to manage application settings using environment variables.

  Attributes:
    DATABASE_URL (str): The database connection URL.
    SECRET_KEY (str): The secret key for signing JWT tokens.
    EXPIRE_TIME (int): The expiration time for JWT tokens (in seconds).
    TOKEN_ALGORITHM (str): The algorithm used for signing JWT tokens.
    API_USER (str): Default username for API authentication.
    API_PASS (str): Default password for API authentication.
  """
  DATABASE_URL: str
  SECRET_KEY: str 
  EXPIRE_TIME: int
  TOKEN_ALGORITHM: str
  API_USER: str
  API_PASS: str
  model_config = SettingsConfigDict(env_file=".env")

async def initiate_database():
  """
  Initializes the database connection and sets up Beanie with the all models.
  """
  global db_client
  db_client = AsyncIOMotorClient(Settings().DATABASE_URL)
  await init_beanie(
    database=db_client.get_default_database(), document_models=models.__all__
  )
  print("Conexão com o banco de dados estabelecida.")

async def shutdown_database():
  """
  Closes the database connection.
  """
  global db_client
  db_client.close()
  print("Conexão com o banco de dados encerrada.")

