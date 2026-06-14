import sqlite3

from database.config import DATABASE_PATH


def registrar_presenca(
    aluno_id,
    aula_id,
    status
):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO presencas (
            aluno_id,
            aula_id,
            status
        )
        VALUES (?, ?, ?)
        """,
        (
            aluno_id,
            aula_id,
            status
        )
    )

    conn.commit()

    conn.close()

    print(
        f"Presença registrada: aluno={aluno_id}, aula={aula_id}"
    )

def listar_presencas():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            aluno_id,
            aula_id,
            status
        FROM presencas
        """
    )

    presencas = cursor.fetchall()

    conn.close()

    return presencas

def listar_presencas_da_aula(aula_id):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            alunos.nome,
            presencas.status
        FROM presencas

        INNER JOIN alunos
            ON alunos.id = presencas.aluno_id

        WHERE presencas.aula_id = ?
        ORDER BY alunos.nome
        """,
        (aula_id,)
    )

    resultado = cursor.fetchall()

    conn.close()

    return resultado

def listar_presencas_por_data(data):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            alunos.nome,
            presencas.status
        FROM presencas

        INNER JOIN alunos
            ON alunos.id = presencas.aluno_id

        INNER JOIN aulas
            ON aulas.id = presencas.aula_id

        WHERE aulas.data = ?

        ORDER BY alunos.nome
        """,
        (data,)
    )

    resultado = cursor.fetchall()

    conn.close()

    return resultado