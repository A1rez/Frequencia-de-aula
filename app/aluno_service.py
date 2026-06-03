import sqlite3


from database.config import DATABASE_PATH


def cadastrar_aluno(
    nome,
    sexo,
    data_nascimento,
    faixa,
    graus,
    data_ultima_graduacao,
    observacoes=""
):
    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO alunos (
            nome,
            sexo,
            data_nascimento,
            faixa,
            graus,
            data_ultima_graduacao,
            observacoes,
            ativo,
            data_cadastro
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 1, DATE('now'))
        """,
        (
            nome,
            sexo,
            data_nascimento,
            faixa,
            graus,
            data_ultima_graduacao,
            observacoes
        )
    )

    conn.commit()
    conn.close()

    print(f"Aluno '{nome}' cadastrado com sucesso!")

def listar_alunos():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nome,
            faixa,
            graus,
            ativo
        FROM alunos
        """
    )

    alunos = cursor.fetchall()

    conn.close()

    return alunos