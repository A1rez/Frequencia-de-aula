import flet as ft
from ui.pages.alunos_page import (
    alunos_view
)

def mostrar_menu_principal(page):

    def abrir_alunos(e):
        page.controls.clear()
        
        page.add(
            alunos_view(
                page,
                mostrar_menu_principal
            )
        )

        page.update()

    page.controls.clear()

    page.add(
        ft.Text(
            "Controle de Frequência",
            size=24
        ),

        ft.Button(
            "Alunos",
            on_click=abrir_alunos
        ),

        ft.Button("Aulas"),
        ft.Button("Presenças"),
        ft.Button("Relatórios")
    )

    page.update()

def main(page: ft.Page):

    page.title = "Controle de Frequência"

    mostrar_menu_principal(page)

ft.app(target=main)