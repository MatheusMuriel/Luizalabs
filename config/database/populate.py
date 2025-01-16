import random

from config.config import initiate_database, shutdown_database
from models.client import Client
from models.favorite import Favorite
from models.product import Product


async def populate_database():
    await initiate_database()

    # Listas estáticas de nomes e emails para clients
    names = [
        "João Silva", "Maria Oliveira", "Carlos Souza", "Ana Pereira",
        "Pedro Lima", "Rafael Almeida", "Luciana Mendes", "Bruno Rocha",
        "Fernanda Dias", "Gabriel Santos", "Isabela Costa", "Thiago Martins",
        "Camila Farias", "Renato Lima", "Carla Torres", "Marcelo Ribeiro",
        "Juliana Alves", "Rodrigo Silva", "Vanessa Mendes", "Eduardo Gomes",
        "Aline Rocha", "Fábio Santos", "Patrícia Moura", "André Almeida",
        "Larissa Costa", "Vitor Carvalho", "Beatriz Sousa", "Felipe Fernandes",
        "Sofia Ribeiro", "Lucas Martins", "Mariana Oliveira", "Diego Torres",
        "Daniela Mendes", "Alexandre Santos", "Natália Costa", "Rafael Vieira",
        "Carolina Dias", "Murilo Alves", "Amanda Farias", "Ricardo Gomes",
        "Gabriela Torres", "Fernando Moura", "Bianca Almeida", "Leonardo Lima",
        "Tatiana Sousa", "César Fernandes", "Viviane Ribeiro",
        "Rogério Martins", "Elaine Oliveira", "Maurício Dias"
    ]
    mail = "@example.com"

    client_emails = [
        # List comprehension não tão compreensivel só por diverdir rs.
        f"{n.split()[0].lower()}.{n.split()[1].lower()}{mail}" for n in names
    ]

    # Construindo a lista de clients
    clients = [
        Client(id=i+1, name=names[i], email=client_emails[i])
        for i in range(len(names))
    ]
    await Client.insert_many(clients)

    # Listas estáticas de títulos e marcas para produtos
    product_titles = [
        "Smartphone Galaxy", "Notebook Pro", "Smart TV", "Fone de Ouvido",
        "Câmera DSLR", "Monitor 4K", "Teclado Mecânico", "Mouse Gamer",
        "Smartwatch", "Cadeira Gamer", "Tablet X", "Impressora Laser",
        "HD Externo", "Pen Drive", "Carregador Universal", "Fonte Gamer",
        "Placa de Vídeo", "Processador X", "Memória RAM", "Placa Mãe",
        "Geladeira Frost Free", "Máquina de Lavar", "Micro-ondas",
        "Fogão 4 Bocas", "Aspirador Robô", "Ventilador Turbo",
        "Ar Condicionado Split", "Purificador de Água", "Liquidificador Power",
        "Batedeira Compacta", "Sanduicheira", "Cafeteira Elétrica",
        "Forno Elétrico", "Máquina de Pão", "Fritadeira Sem Óleo",
        "Grill Elétrico", "Panela Elétrica", "Panela de Pressão", "Cooktop",
        "Cortador de Cabelo", "Barbeador Elétrico", "Prancha Alisadora",
        "Secador de Cabelo", "Aparelho de Som", "Caixa de Som Bluetooth",
        "Home Theater", "Projetor Multimídia", "Drone X", "Camera de Ação"
    ]
    product_brands = [
        "Samsung", "Apple", "LG", "Sony", "Canon",
        "Dell", "Logitech", "Razer", "Garmin", "DXRacer",
        "Asus", "HP", "Seagate", "SanDisk", "Anker",
        "Corsair", "Nvidia", "AMD", "Kingston", "Gigabyte",
        "Brastemp", "Consul", "Panasonic", "Electrolux", "Philco",
        "Mondial", "Springer", "Esmaltec", "Arno", "Britânia",
        "Black+Decker", "Oster", "Cuisinart", "Hamilton Beach", "Tramontina",
        "Mallory", "Philips", "Panasonic", "JBL", "Sony",
        "Bose", "Pioneer", "Yamaha", "DJI", "GoPro"
    ]

    # Construindo a lista de produtos
    products = [
        Product(
            id=i+1,
            title=product_titles[i % len(product_titles)],
            price=round(random.uniform(10.0, 1000.0), 2),
            image=f"https://example.com/image{i+1}.jpg",
            brand=product_brands[i % len(product_brands)],
            reviewScore=round(random.uniform(1.0, 5.0), 1)
        )
        for i in range(100)  # Criando 100 produtos
    ]
    await Product.insert_many(products)

    # Populando favorites
    favorites = []
    # Seleciona 30 usuários aleatórios
    users_with_favorites = random.sample(clients, 30)

    for client in users_with_favorites:
        # 10 produtos favoritos aleatórios por usuário
        product_ids = random.sample(range(1, 101), k=10)
        favorites.extend([
            Favorite(client_id=client.id, product_id=product_id)
            for product_id in product_ids
        ])

    await Favorite.insert_many(favorites)

    print("Dados populados com sucesso.")
    await shutdown_database()
