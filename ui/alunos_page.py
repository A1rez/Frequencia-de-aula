import flet as ft

from app.aluno_service import (
    listar_alunos_ativos
)


def alunos_view(
    page,
    mostrar_menu_principal
):

    def voltar(e):

        mostrar_menu_principal(
            page
        )

    alunos = listar_alunos_ativos()

    controles = [
        ft.Text(
            "Lista de Alunos",
            size=24
        )
    ]

    for aluno in alunos:

        controles.append(
            ft.Text(
                aluno["nome"]
            )
        )

    controles.append(
        ft.ElevatedButton(
            "Voltar",
            on_click=voltar
        )
    )

    return ft.Column(
        controles
    )