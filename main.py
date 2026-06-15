from app.relatorio_service import (
    participacao_por_dia_semana
)

if __name__ == "__main__":

    resultado = (
        participacao_por_dia_semana()
    )

    print(resultado)