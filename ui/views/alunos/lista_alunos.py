import flet as ft

from app.aluno_service import listar_alunos
from app.relatorio_service import calcular_frequencia_ultimos_90_dias

from ui.tema import (
    COR_FUNDO, COR_FUNDO_SEC, COR_BORDA, COR_TEXTO, COR_TEXTO_SEC,
    COR_PRIMARIA, RAIO,
)
from ui.components.widgets import (
    card, badge_faixa, badge_ativo, avatar,
    barra_frequencia, btn,
)


class ViewListaAlunos:
    def __init__(self, ctx, **kwargs):
        self.ctx = ctx
        self.filtro = "todos"
        self.busca  = ""
        self.lista_ref = ft.Ref[ft.Column]()

    def build(self):
        self.alunos = listar_alunos()

        campo_busca = ft.TextField(
            hint_text="Buscar aluno…",
            hint_style=ft.TextStyle(color=COR_TEXTO_SEC, size=13),
            text_style=ft.TextStyle(color=COR_TEXTO, size=13),
            border_color=COR_BORDA,
            border_radius=8,
            bgcolor=COR_FUNDO,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=7),
            width=200,
            on_change=self._buscar,
        )

        self.count_text = ft.Text("", size=14, weight=ft.FontWeight.W_500, color=COR_TEXTO)

        self.filtro_btns = {
            "todos":    self._filtro_btn("Todos",    "todos",    ativo=True),
            "ativos":   self._filtro_btn("Ativos",   "ativos"),
            "inativos": self._filtro_btn("Inativos", "inativos"),
        }

        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.count_text,
                        campo_busca,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(controls=list(self.filtro_btns.values()), spacing=8),
                card(
                    ft.Column(
                        controls=[
                            self._build_cabecalho(),
                            ft.Column(ref=self.lista_ref, controls=[], spacing=0),
                        ],
                        spacing=0,
                    )
                ),
            ],
            spacing=12,
            expand=True,
        )

    def _filtro_btn(self, label, filtro, ativo=False):
        def on_click(e, f=filtro):
            self.filtro = f
            for k, b in self.filtro_btns.items():
                b.bgcolor = COR_PRIMARIA if k == f else None
                b.border  = ft.border.all(0.5, COR_BORDA if k != f else COR_PRIMARIA)
                t = b.content
                t.color = "#FFFFFF" if k == f else COR_TEXTO_SEC
            self._atualizar_lista(e.page)

        return ft.Container(
            content=ft.Text(label, size=12, color="#FFFFFF" if ativo else COR_TEXTO_SEC),
            bgcolor=COR_PRIMARIA if ativo else None,
            border=ft.border.all(0.5, COR_PRIMARIA if ativo else COR_BORDA),
            border_radius=RAIO,
            padding=ft.padding.symmetric(horizontal=12, vertical=5),
            on_click=on_click,
            ink=True,
        )

    def _build_cabecalho(self):
        cols  = ["Nome", "Faixa", "Graus", "Status", "Frequência (90d)", ""]
        widths = [None, 120, 60, 80, 150, 80]
        cells = []
        for i, col in enumerate(cols):
            cells.append(ft.Container(
                ft.Text(col.upper(), size=10, weight=ft.FontWeight.W_500, color=COR_TEXTO_SEC),
                width=widths[i], expand=(widths[i] is None),
            ))
        return ft.Container(
            content=ft.Row(controls=cells, spacing=0),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border=ft.border.only(bottom=ft.BorderSide(0.5, COR_BORDA)),
        )

    def _build_linhas(self, alunos):
        if not alunos:
            return [ft.Container(
                ft.Text("Nenhum aluno encontrado.", size=13, color=COR_TEXTO_SEC),
                padding=ft.padding.symmetric(vertical=24),
                alignment=ft.alignment.center,
            )]

        linhas = []
        for a in alunos:
            try:
                freq = calcular_frequencia_ultimos_90_dias(a["id"])
                pct  = freq["frequencia"]
            except Exception:
                pct = 0

            aid = a["id"]
            linha = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Row(
                            controls=[avatar(a["nome"]), ft.Text(a["nome"], size=13, color=COR_TEXTO)],
                            spacing=8,
                            expand=True,
                        ),
                        ft.Container(badge_faixa(a["faixa"], a["graus"]), width=120),
                        ft.Container(ft.Text(str(a["graus"]), size=13, color=COR_TEXTO_SEC), width=60),
                        ft.Container(badge_ativo(bool(a["ativo"])), width=80),
                        ft.Container(barra_frequencia(int(pct)), width=150),
                        ft.Container(
                            btn("Ver perfil",
                                on_click=lambda e, i=aid: self.ctx["navegar"]("perfil_aluno", aluno_id=i),
                                pequeno=True),
                            width=80,
                        ),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=12, vertical=9),
                border=ft.border.only(bottom=ft.BorderSide(0.5, COR_BORDA)),
                on_click=lambda e, i=aid: self.ctx["navegar"]("perfil_aluno", aluno_id=i),
                ink=True,
            )
            linhas.append(linha)

        if linhas:
            linhas[-1].border = None
        return linhas

    def _filtrar(self):
        lista = self.alunos
        if self.filtro == "ativos":
            lista = [a for a in lista if a["ativo"]]
        elif self.filtro == "inativos":
            lista = [a for a in lista if not a["ativo"]]
        if self.busca:
            lista = [a for a in lista if self.busca.lower() in a["nome"].lower()]
        return lista

    def _atualizar_lista(self, page):
        filtrados = self._filtrar()
        self.count_text.value = f"{len(filtrados)} aluno{'s' if len(filtrados) != 1 else ''}"
        self.lista_ref.current.controls = self._build_linhas(filtrados)
        page.update()

    def _buscar(self, e):
        self.busca = e.control.value
        self._atualizar_lista(e.page)

    # Inicializa a lista ao construir
    def build(self):
        self.alunos = listar_alunos()
        campo_busca = ft.TextField(
            hint_text="Buscar aluno…",
            hint_style=ft.TextStyle(color=COR_TEXTO_SEC, size=13),
            text_style=ft.TextStyle(color=COR_TEXTO, size=13),
            border_color=COR_BORDA,
            border_radius=8,
            bgcolor=COR_FUNDO,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=7),
            width=200,
            on_change=self._buscar,
        )

        self.count_text = ft.Text(
            f"{len(self.alunos)} alunos", size=14, weight=ft.FontWeight.W_500, color=COR_TEXTO
        )

        self.filtro_btns = {
            "todos":    self._filtro_btn("Todos",    "todos",    ativo=True),
            "ativos":   self._filtro_btn("Ativos",   "ativos"),
            "inativos": self._filtro_btn("Inativos", "inativos"),
        }

        linhas_iniciais = self._build_linhas(self.alunos)

        return ft.Column(
            controls=[
                ft.Row(
                    controls=[self.count_text, campo_busca],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(controls=list(self.filtro_btns.values()), spacing=8),
                card(
                    ft.Column(
                        controls=[
                            self._build_cabecalho(),
                            ft.Column(ref=self.lista_ref, controls=linhas_iniciais, spacing=0),
                        ],
                        spacing=0,
                    )
                ),
            ],
            spacing=12,
            expand=True,
        )