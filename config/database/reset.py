from config.config import initiate_database, shutdown_database
from models.client import Client
from models.product import Product
from models.favorite import Favorite


async def reset_database():
    await initiate_database()

    # Removendo todos os dados das coleções
    await Client.delete_all()
    await Product.delete_all()
    await Favorite.delete_all()

    print("Todas as coleções foram limpas com sucesso.")

    await shutdown_database()
