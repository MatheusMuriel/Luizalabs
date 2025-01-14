from fastapi import Body, APIRouter, HTTPException
from config.config import Settings

from auth.jwt_handler import sign_jwt

from models.user import UserLogin

router = APIRouter()

# Login 
@router.post("/login")
async def user_login(user_credentials: UserLogin = Body(...)):
  """ 
  Por ser uma demonstração estou usando o usuario e senha do .env  
  para não precisar fazer o esquema de cadastro, função de hash, e etc...
  """
  if (user_credentials.username == Settings().API_USER) and (user_credentials.password == Settings().API_PASS):
    return sign_jwt(user_credentials.username)
  
  raise HTTPException(status_code=403, detail="Incorrect username or password")


