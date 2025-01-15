from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .jwt_handler import decode_jwt


def verify_jwt(jwtoken: str) -> bool:
    """
    Verifies the validity of a JWT token.
    Use jwt_handler.decode_jwt
    Args:
        jwtoken (str): The JWT token to be verified.
    Returns:
        bool: True if the token is valid, False otherwise.
    """
    if decode_jwt(jwtoken):
        return True
    else:
        return False


class JWTBearer(HTTPBearer):
    """
    A custom HTTPBearer class to handle JWT authentication.
    """

    def __init__(self):
        """
        Initializes the JWTBearer instance.
        """

        super(JWTBearer, self)

    async def __call__(self, request: Request):
        """
        Processes the incoming request and validates the JWT token.
        Args:
            request (Request): The incoming HTTP request.
        Returns:
            str: The JWT token if authentication is successful.
        Raises:
            HTTPException: Status code 403 if the authentication fails due to
            an invalid credentials scheme, invalid token or missing token.
        """

        credentials: HTTPAuthorizationCredentials = \
            await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication token"
                )

            if not verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token or expired token"
                )

            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid authorization token"
            )
