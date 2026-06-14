import sqlite3

from database.config import DATABASE_PATH


def cadastrar_aula(
    data,
    observacao=""
):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO aulas (
            data,
            observacao
        )
        VALUES (?, ?)
        """,
        (
            data,
            observacao
        )
    )

    conn.commit()

    conn.close()

    print(f"Aula {data} cadastrada com sucesso.")

def listar_aulas():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            data,
            observacao
        FROM aulas
        ORDER BY data
        """
    )

    aulas = cursor.fetchall()

    conn.close()

    return aulas

def buscar_aula_por_id(aula_id):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            data,
            observacao
        FROM aulas
        WHERE id = ?
        """,
        (aula_id,)
    )

    aula = cursor.fetchone()

    conn.close()

    return aula

def buscar_aula_por_data(data):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            data,
            observacao
        FROM aulas
        WHERE data = ?
        """,
        (data,)
    )

    aula = cursor.fetchone()

    conn.close()

    return aula