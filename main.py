from app.aluno_service import listar_alunos


if __name__ == "__main__":

    alunos = listar_alunos()

    for aluno in alunos:
        print(aluno)