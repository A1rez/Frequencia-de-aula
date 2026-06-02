import sqlite3
from pathlib import Path


DATABASE_PATH = "database/frequencia.db"
SCHEMA_PATH = "database/schema.sql"


def criar_banco():
    """
    Cria o banco de dados e as tabelas.
    """

    conn = sqlite3.connect(DATABASE_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as arquivo:
        schema = arquivo.read()

    conn.executescript(schema)

    conn.commit()
    conn.close()

    print("Banco criado com sucesso!")