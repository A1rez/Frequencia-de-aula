import flet as ft

from app.aluno_service import (
    listar_alunos_ativos,
    buscar_aluno_por_id
)
from ui.pages.perfil_page import perfil_page


def alunos_view(
    page,
    mostrar_menu_principal
):

    def voltar(e):

        mostrar_menu_principal(
            page
        )

    def mostrar_lista_alunos(page):

        page.controls.clear()

        page.add(
            alunos_view(
                page,
                mostrar_menu_principal
            )
        )
        page.update()
    
    def abrir_perfil(aluno):

        def handler(e):

            aluno_completo = buscar_aluno_por_id(
                aluno["id"]
            )
 
            page.controls.clear()

            page.add(
                perfil_page(
                    page,
                    aluno,
                    mostrar_lista_alunos
                )
            )
            page.update()

        return handler

    #alunos = listar_alunos_ativos()

    controles = [
        ft.Text(
            "Lista de Alunos",
            size=24
        )
    ]

    for aluno in alunos:

        controles.append(
            ft.TextButton(
                aluno["nome"],
                on_click=abrir_perfil(aluno)
            )
        )

    controles.append(
        ft.Button(
            "Voltar",
            on_click=voltar
        )
    )

    return ft.Column(
        controles
    )