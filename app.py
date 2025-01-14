from fastapi import FastAPI
from config.config import initiate_database, shutdown_database

from routes.user import router as UserRouter

app = FastAPI()

def include_routers():
  """ 
    Includes all application routers. 
  """
  app.include_router(UserRouter, prefix="/user")
  
@app.on_event("startup")
async def start_database():
  """
  Event handler for application startup.
  Initialize the database connection when the application starts.
  """
  await initiate_database()

@app.get("/")
async def read_root():
  """ """
  return {"message": "Olá Mundo!"}

@app.on_event("shutdown")
async def shutdown_db_client():
  """
  Event handler for application shutdown.
  This function closes the database connection when the application stops.
  """
  await shutdown_database()

include_routers()