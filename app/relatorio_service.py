import sqlite3
from datetime import datetime
from datetime import timedelta

from database.config import DATABASE_PATH
from app.aluno_service import (
    listar_alunos_ativos,
    buscar_aluno_por_id
)
from app.aula_service import listar_aulas

def calcular_frequencia_aluno(
    aluno_id,
    data_inicio,
    data_fim
):

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

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

def listar_ranking_participacao():

    ranking = []

    alunos = listar_alunos_ativos()

    for aluno in alunos:

        aluno_id = aluno["id"]

        frequencia = (
            calcular_frequencia_ultimos_90_dias(
                aluno_id
            )
        )

        ranking.append(
            {
                "id": aluno["id"],
                "nome": aluno["nome"],
                "faixa": aluno["faixa"],
                "graus": aluno["graus"],
                "frequencia": frequencia[
                    "frequencia"
                ]
            }
        )

    ranking.sort(
        key=lambda x: x["frequencia"],
        reverse=True
    )

    return ranking

def calcular_estatisticas_turma():

    alunos = listar_alunos_ativos()

    quantidade_alunos = len(alunos)

    masculinos = 0
    femininos = 0

    soma_frequencias = 0

    for aluno in alunos:

        dados_aluno = buscar_aluno_por_id(
            aluno["id"]
        )

        if dados_aluno["sexo"] == "M":
            masculinos += 1

        elif dados_aluno["sexo"] == "F":
            femininos += 1

        frequencia = (
            calcular_frequencia_ultimos_90_dias(
                aluno["id"]
            )
        )

        soma_frequencias += (
            frequencia["frequencia"]
        )

    if quantidade_alunos > 0:

        presenca_media = (
            soma_frequencias /
            quantidade_alunos
        )

    else:

        presenca_media = 0

    return {
        "alunos_ativos": quantidade_alunos,
        "masculino": masculinos,
        "feminino": femininos,
        "presenca_media": round(
            presenca_media,
            2
        )
    }

def aulas_por_mes():

    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            strftime('%Y-%m', data) as mes,
            COUNT(*) as quantidade
        FROM aulas
        GROUP BY mes
        ORDER BY mes
        """
    )

    resultado = cursor.fetchall()

    conn.close()

    return {
        linha["mes"]: linha["quantidade"]
        for linha in resultado
    }

def contar_presentes_aula(aula_id):

    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) as total
        FROM presencas
        WHERE aula_id = ?
        AND status = 'PRESENTE'
        """,
        (aula_id,)
    )

    resultado = cursor.fetchone()

    conn.close()

    return resultado["total"]

from datetime import datetime

def participacao_por_dia_semana():

    aulas = listar_aulas()

    dias = {
        "Segunda": [],
        "Terça": [],
        "Quarta": [],
        "Quinta": [],
        "Sexta": [],
        "Sábado": [],
        "Domingo": []
    }

    mapa_dias = {
        0: "Segunda",
        1: "Terça",
        2: "Quarta",
        3: "Quinta",
        4: "Sexta",
        5: "Sábado",
        6: "Domingo"
    }

    for aula in aulas:

        data = datetime.strptime(
            aula["data"],
            "%Y-%m-%d"
        )

        dia_semana = mapa_dias[
            data.weekday()
        ]

        presentes = contar_presentes_aula(
            aula["id"]
        )

        dias[dia_semana].append(
            presentes
        )

    resultado = {}

    for dia, valores in dias.items():

        if valores:

            resultado[dia] = round(
                sum(valores) / len(valores),
                2
            )

    return resultado