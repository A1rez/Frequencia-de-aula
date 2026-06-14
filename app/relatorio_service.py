import sqlite3
from datetime import datetime
from datetime import timedelta

from database.config import DATABASE_PATH
from app.aluno_service import (
    listar_alunos_ativos,
    buscar_aluno_por_id
)

def calcular_frequencia_aluno(
    aluno_id,
    data_inicio,
    data_fim
):

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            status
        FROM presencas

        INNER JOIN aulas
            ON aulas.id = presencas.aula_id

        WHERE presencas.aluno_id = ?
          AND aulas.data BETWEEN ? AND ?
        """,
        (
            aluno_id,
            data_inicio,
            data_fim
        )
    )

    registros = cursor.fetchall()

    conn.close()

    presencas = 0
    faltas = 0
    justificadas = 0

    for registro in registros:

        status = registro[0]

        if status == "PRESENTE":
            presencas += 1

        elif status == "FALTA":
            faltas += 1

        elif status == "JUSTIFICADA":
            justificadas += 1

    total_avaliado = presencas + faltas

    if total_avaliado == 0:

        frequencia = 0

    else:

        frequencia = (
            presencas / total_avaliado
        ) * 100

    return {
        "presencas": presencas,
        "faltas": faltas,
        "justificadas": justificadas,
        "frequencia": round(
            frequencia,
            2
        )
    }

def calcular_frequencia_ultimos_90_dias(aluno_id):

    data_fim = datetime.today()

    data_inicio = data_fim - timedelta(days=90)

    return calcular_frequencia_aluno(
        aluno_id=aluno_id,
        data_inicio=data_inicio.strftime("%Y-%m-%d"),
        data_fim=data_fim.strftime("%Y-%m-%d")
    )

def possui_tempo_minimo_para_graduacao(aluno_id):

    aluno = buscar_aluno_por_id(aluno_id)

    data_ultima_graduacao = aluno[6]

    data_ultima_graduacao = datetime.strptime(
        data_ultima_graduacao,
        "%Y-%m-%d"
    )

    dias = (
        datetime.today() -
        data_ultima_graduacao
    ).days

    return dias >= 90

def listar_aptos_graduacao():

    aptos = []

    alunos = listar_alunos_ativos()

    for aluno in alunos:

        aluno_id = aluno[0]

        frequencia = (
            calcular_frequencia_ultimos_90_dias(
                aluno_id
            )
        )

        possui_tempo = (
            possui_tempo_minimo_para_graduacao(
                aluno_id
            )
        )

        if (
            frequencia["frequencia"] >= 50
            and possui_tempo
        ):

            dados_aluno = buscar_aluno_por_id(
                aluno_id
            )

            aptos.append(
                {
                    "id": dados_aluno[0],
                    "nome": dados_aluno[1],
                    "faixa": dados_aluno[4],
                    "graus": dados_aluno[5],
                    "frequencia": frequencia[
                        "frequencia"
                    ]
                }
            )

    return aptos

def listar_alunos_para_desativacao():

    alunos_para_desativacao = []

    alunos = listar_alunos_ativos()

    for aluno in alunos:

        aluno_id = aluno[0]

        frequencia = (
            calcular_frequencia_ultimos_90_dias(
                aluno_id
            )
        )

        if frequencia["frequencia"] < 30:

            dados_aluno = buscar_aluno_por_id(
                aluno_id
            )

            alunos_para_desativacao.append(
                {
                    "id": dados_aluno[0],
                    "nome": dados_aluno[1],
                    "faixa": dados_aluno[4],
                    "graus": dados_aluno[5],
                    "frequencia": frequencia[
                        "frequencia"
                    ]
                }
            )

    return alunos_para_desativacao