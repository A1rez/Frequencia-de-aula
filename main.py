from app.aluno_service import buscar_aluno_por_id

if __name__ == "__main__":

    aluno = buscar_aluno_por_id(1)

    print(aluno[1])
    print(aluno["faixa"])
    print(aluno["graus"])