from fastapi import FastAPI
from config.config import initiate_database

app = FastAPI()

@app.get("/")
async def read_root():
  return {"message": "Olá Mundo!"}
