from app.presenca_service import listar_presencas_da_aula

if __name__ == "__main__":

    presencas = listar_presencas_da_aula(1)

    for presenca in presencas:
        print(presenca)