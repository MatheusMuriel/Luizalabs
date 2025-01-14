from fastapi import FastAPI
from config.config import initiate_database, shutdown_database

app = FastAPI()

def include_routers():
  app.include_router(auth.router)
  
@app.on_event("startup")
async def start_database():
  await initiate_database()

@app.get("/")
async def read_root():
  return {"message": "Olá Mundo!"}

@app.on_event("shutdown")
async def shutdown_db_client():
  await shutdown_database()

include_routers()