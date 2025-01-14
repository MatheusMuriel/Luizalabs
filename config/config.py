from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict
import models as models


class Settings(BaseSettings):
  DATABASE_URL: str
  model_config = SettingsConfigDict(env_file=".env")

async def initiate_database():
  client = AsyncIOMotorClient(Settings().DATABASE_URL)
  await init_beanie(
    database=client.get_default_database(), document_models=models.__all__
  )
