from app.aula_service import listar_aulas

if __name__ == "__main__":

    aulas = listar_aulas()

    for aula in aulas:
        print(aula)