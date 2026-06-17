import flet as ft
from datetime import datetime

from app.aula_service import listar_aulas
from app.presenca_service import listar_presencas_da_aula

from ui.tema import (
    COR_FUNDO, COR_FUNDO_SEC, COR_BORDA, COR_TEXTO, COR_TEXTO_SEC, RAIO_LG, STATUS_CORES
)
from ui.components.widgets import (
    card, secao_header, badge_status, btn, input_texto,
)

DIAS_PT = {0: "Segunda", 1: "Terça", 2: "Quarta",
           3: "Quinta",  4: "Sexta", 5: "Sábado", 6: "Domingo"}

def _badge_count(count: int, status: str):
    cores = STATUS_CORES.get(status, {})
    return ft.Container(
        content=ft.Text(
            str(count),
            size=12,
            weight=ft.FontWeight.W_500,
            color=cores.get("texto", "#444441"),
        ),
        bgcolor=cores.get("bg", "#F1EFE8"),
        border=ft.border.all(0.5, cores.get("borda", COR_BORDA)),
        border_radius=10,
        padding=ft.padding.symmetric(horizontal=10, vertical=2),
    )

class ViewHistoricoAulas:
    def __init__(self, ctx, **kwargs):
        self.ctx = ctx
        self.filtro = ""
        self.lista_ref = ft.Ref[ft.Column]()

    def build(self):
        self.aulas = sorted(listar_aulas(), key=lambda a: a["data"], reverse=True)

        campo_busca = ft.TextField(
            hint_text="Buscar por data…",
            hint_style=ft.TextStyle(color=COR_TEXTO_SEC, size=13),
            text_style=ft.TextStyle(color=COR_TEXTO, size=13),
            border_color=COR_BORDA,
            border_radius=8,
            bgcolor=COR_FUNDO,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=7),
            width=200,
            on_change=self._filtrar,
        )

        return ft.Column(
            controls=[
                card(
                    ft.Column(
                        controls=[
                            secao_header("Aulas registradas", acoes=[campo_busca]),
                            self._build_cabecalho(),
                            ft.Column(ref=self.lista_ref, controls=self._build_linhas(self.aulas), spacing=0),
                        ],
                        spacing=0,
                    )
                ),
            ],
            expand=True,
        )

    def _build_cabecalho(self):
        cols = ["Data", "Dia", "Presentes", "Ausentes", "Justificados", "Observação", ""]
        widths = [90, 80, 90, 80, 100, None, 80]
        cells = []
        for i, col in enumerate(cols):
            cells.append(
                ft.Container(
                    ft.Text(col.upper(), size=10, weight=ft.FontWeight.W_500, color=COR_TEXTO_SEC),
                    width=widths[i],
                    expand=(widths[i] is None),
                )
            )
        return ft.Container(
            content=ft.Row(controls=cells, spacing=0),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border=ft.border.only(bottom=ft.BorderSide(0.5, COR_BORDA)),
        )

    def _build_linhas(self, aulas):
        if not aulas:
            return [ft.Container(
                ft.Text("Nenhuma aula registrada.", size=13, color=COR_TEXTO_SEC),
                padding=ft.padding.symmetric(vertical=24),
                alignment=ft.alignment.center,
            )]

        linhas = []
        for a in aulas:
            presencas = listar_presencas_da_aula(a["id"])
            pres  = sum(1 for p in presencas if p["status"] == "PRESENTE")
            aus   = sum(1 for p in presencas if p["status"] == "AUSENTE")
            just  = sum(1 for p in presencas if p["status"] == "JUSTIFICADO")

            try:
                dt  = datetime.strptime(a["data"], "%Y-%m-%d")
                data_fmt = dt.strftime("%d/%m/%Y")
                dia = DIAS_PT.get(dt.weekday(), "")
            except Exception:
                data_fmt = a["data"]
                dia = ""

            aula_id = a["id"]
            linha = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(ft.Text(data_fmt, size=13, color=COR_TEXTO), width=90),
                        ft.Container(ft.Text(dia, size=13, color=COR_TEXTO_SEC), width=80),
                        ft.Container(_badge_count(pres, "PRESENTE"),    width=90),
                        ft.Container(_badge_count(aus,  "AUSENTE"),     width=80),
                        ft.Container(_badge_count(just, "JUSTIFICADO"), width=100),
                        ft.Container(
                            ft.Text(a["observacao"] or "—", size=12, color=COR_TEXTO_SEC, overflow=ft.TextOverflow.ELLIPSIS),
                            expand=True,
                        ),
                        ft.Container(
                            btn("Editar", on_click=lambda e, aid=aula_id: self._editar(aid),
                                icone=ft.Icons.EDIT_OUTLINED, pequeno=True),
                            width=80,
                        ),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=12, vertical=9),
                border=ft.border.only(bottom=ft.BorderSide(0.5, COR_BORDA)),
                ink=True,
            )
            linhas.append(linha)

        if linhas:
            linhas[-1].border = None
        return linhas

    def _filtrar(self, e):
        self.filtro = e.control.value.strip()
        filtradas = [a for a in self.aulas if self.filtro in a["data"]] if self.filtro else self.aulas
        self.lista_ref.current.controls = self._build_linhas(filtradas)
        e.page.update()

    def _editar(self, aula_id):
        self.ctx["navegar"]("editar_aula", aula_id=aula_id)