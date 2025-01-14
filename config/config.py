from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict
import models as models

db_client: AsyncIOMotorClient = None

class Settings(BaseSettings):
  DATABASE_URL: str
  #secret_key: str 
  model_config = SettingsConfigDict(env_file=".env")

async def initiate_database():
  global db_client
  db_client = AsyncIOMotorClient(Settings().DATABASE_URL)
  await init_beanie(
    database=db_client.get_default_database(), document_models=models.__all__
  )
  print("Conexão com o banco de dados estabelecida.")

async def shutdown_database():
  global db_client
  db_client.close()
  print("Conexão com o banco de dados encerrada.")

