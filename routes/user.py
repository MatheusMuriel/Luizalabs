from fastapi import APIRouter, Body, HTTPException

from auth.jwt_handler import sign_jwt
from config.config import Settings
from models.user import UserLogin
from resources.resources import ResourceManager

resources = ResourceManager()
router = APIRouter()


@router.post("/login")
async def user_login(user_credentials: UserLogin = Body(...)):
    """
    Handles user login by verifying credentials and returning a JWT token.

    This function checks if the provided username and password match the values
    stored in the application's settings.
    If valid, it generates and returns a signed JWT token.
    Args:
        user_credentials (UserLogin): The user's login credentials.
    Returns:
        dict: A dictionary containing the signed JWT token
        if authentication is successful.

    Raises:
        HTTPException: If the username or password is incorrect.
    """
    """ Por ser uma demonstração estou usando o usuario e senha do .env """
    """ para não precisar fazer o esquema de cadastro, função de hash, e etc"""
    if (
        user_credentials.username == Settings().API_USER
        and user_credentials.password == Settings().API_PASS
    ):
        return sign_jwt(user_credentials.username)

    raise HTTPException(
        status_code=401,
        detail=resources.get("auth.login_failure")
    )
