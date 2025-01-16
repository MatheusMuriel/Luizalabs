from fastapi import Depends, FastAPI

from auth.jwt_bearer import JWTBearer
from config.config import initiate_database, shutdown_database

from routes.client import router as ClientRouter
from routes.product import router as ProductRouter
from routes.user import router as UserRouter
from routes.favorite import router as FavoriteRouter

app = FastAPI()
token_listener = JWTBearer()


def include_routers():
    """
    Includes all application routers with depends of token to use auth.
    """
    app.include_router(
        UserRouter,
        tags=["Auth"],
        prefix="/auth"
    )
    app.include_router(
        ClientRouter,
        tags=["Clients"],
        prefix="/client",
        dependencies=[Depends(token_listener)]
    )
    app.include_router(
        ProductRouter,
        tags=["Products"],
        prefix="/product",
        dependencies=[Depends(token_listener)]
    )
    app.include_router(
        FavoriteRouter,
        tags=["Favorites"],
        prefix="/favorite",
        dependencies=[Depends(token_listener)]
    )


@app.on_event("startup")
async def start_database():
    """
    Event handler for application startup.
    Initialize the database connection when the application starts.
    """
    await initiate_database()


@app.on_event("shutdown")
async def shutdown_db_client():
    """
    Event handler for application shutdown.
    This function closes the database connection when the application stops.
    """
    await shutdown_database()

include_routers()
