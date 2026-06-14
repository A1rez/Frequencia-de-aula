from app.relatorio_service import (
    listar_alunos_para_desativacao
)

if __name__ == "__main__":

    alunos = listar_alunos_para_desativacao()

    for aluno in alunos:
        print(aluno)