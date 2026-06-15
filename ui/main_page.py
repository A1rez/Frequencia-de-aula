import flet as ft
from ui.alunos_page import (
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

        ft.ElevatedButton(
            "Alunos",
            on_click=abrir_alunos
        ),

        ft.ElevatedButton("Aulas"),
        ft.ElevatedButton("Presenças"),
        ft.ElevatedButton("Relatórios")
    )

    page.update()

def main(page: ft.Page):

    page.title = "Controle de Frequência"

    mostrar_menu_principal(page)

ft.app(target=main)