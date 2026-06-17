import flet as ft
from ui.app import FrequenciaApp


def main(page: ft.Page):
    app = FrequenciaApp(page)
    app.inicializar()


ft.app(target=main)