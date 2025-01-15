import time
from typing import Dict

import jwt

from config.config import Settings


def token_response(token: str):
    """
    Generates a response dictionary containing the access token.
    Args:
        token (str): The JWT token to include in the response.
    Returns:
        dict: A dictionary with the access token.
    """
    return {"access_token": token}


def sign_jwt(login: str) -> Dict[str, str]:
    """
    Singin and generates a JWT token for a given login.
    Args:
        login (str): The login for which the token is being generated.
    Returns:
        Dict[str, str]: A dictionary containing the signed JWT token.
    """
    payload = {
        "login": login,
        "expires": (time.time() + Settings().EXPIRE_TIME)
    }
    return token_response(
        jwt.encode(
            payload,
            Settings().SECRET_KEY,
            algorithm=Settings().TOKEN_ALGORITHM
        )
    )


def decode_jwt(token: str) -> dict:
    """
    Decodes and validates a JWT token.
    Args:
        token (str): The JWT token to decode.
    Returns:
        dict: The decoded token if valid and not expired,
        otherwise an empty dictionary.
    """
    decoded_token = jwt.decode(
        token.encode(),
        Settings().SECRET_KEY,
        algorithms=Settings().TOKEN_ALGORITHM
    )
    return decoded_token if decoded_token["expires"] >= time.time() else {}
