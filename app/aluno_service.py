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
    conn.row_factory = sqlite3.Row

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
    conn.row_factory = sqlite3.Row

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

def buscar_aluno_por_id(aluno_id):

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nome,
            sexo,
            data_nascimento,
            faixa,
            graus,
            data_ultima_graduacao,
            observacoes,
            ativo
        FROM alunos
        WHERE id = ?
        """,
        (aluno_id,)
    )

    aluno = cursor.fetchone()

    conn.close()

    return aluno

def listar_alunos_ativos():

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nome,
            faixa,
            graus
        FROM alunos
        WHERE ativo = 1
        ORDER BY nome
        """
    )

    alunos = cursor.fetchall()

    conn.close()

    return alunos

def desativar_aluno(aluno_id, motivo_saida):

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE alunos
        SET
            ativo = 0,
            data_saida = DATE('now'),
            motivo_saida = ?
        WHERE id = ?
        """,
        (
            motivo_saida,
            aluno_id
        )
    )

    conn.commit()

    conn.close()

    print(f"Aluno {aluno_id} desativado com sucesso.")

def reativar_aluno(aluno_id):

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE alunos
        SET
            ativo = 1,
            data_saida = NULL,
            motivo_saida = NULL
        WHERE id = ?
        """,
        (aluno_id,)
    )

    conn.commit()

    conn.close()

    print(f"Aluno {aluno_id} reativado com sucesso.")