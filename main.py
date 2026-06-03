from app.aluno_service import (
    buscar_aluno_por_id,
    reativar_aluno
)

if __name__ == "__main__":

    reativar_aluno(1)

    aluno = buscar_aluno_por_id(1)

    print(aluno)