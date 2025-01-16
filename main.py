import uvicorn
import sys
from config.database.populate import populate_database
from config.database.reset import reset_database

if __name__ == "__main__":
    # Verifica argumentos passados na linha de comando
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "--db_populate":
            print("Iniciando a população do banco de dados...")
            import asyncio
            asyncio.run(populate_database())
        elif command == "--db_reset":
            print("Limpando o banco de dados...")
            import asyncio
            asyncio.run(reset_database())
        else:
            print(f"Comando '{command}' não reconhecido.")
            print("Opções disponíveis: db_populate, db_reset.")
    else:
        # Comportamento padrão
        uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
