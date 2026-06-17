import flet as ft
from datetime import date

from ui.tema import (
    COR_FUNDO, COR_FUNDO_SEC, COR_SIDEBAR, COR_BORDA,
    COR_TEXTO, COR_TEXTO_SEC, COR_TEXTO_HINT,
    COR_PRIMARIA, RAIO,
)
from ui.views.aulas.registrar_aula   import ViewRegistrarAula
from ui.views.aulas.historico_aulas  import ViewHistoricoAulas
from ui.views.aulas.editar_aula      import ViewEditarAula
from ui.views.alunos.cadastrar_aluno  import ViewCadastrarAluno
from ui.views.alunos.lista_alunos     import ViewListaAlunos
from ui.views.alunos.perfil_aluno     import ViewPerfilAluno, ViewEditarAluno
from ui.views.relatorios.relatorio_turma  import ViewRelatorioTurma
from ui.views.relatorios.aptos_graduacao  import ViewAptosGraduacao


ROTAS = [
    ("registrar_aula",   "Registrar aula",       ft.Icons.CALENDAR_MONTH_OUTLINED,  "Aulas"),
    ("historico_aulas",  "Histórico de aulas",    ft.Icons.HISTORY,                  "Aulas"),
    ("editar_aula",      "Editar aula",            ft.Icons.EDIT_OUTLINED,            "Aulas"),
    ("cadastrar_aluno",  "Cadastrar aluno",        ft.Icons.PERSON_ADD_OUTLINED,      "Alunos"),
    ("lista_alunos",     "Lista de alunos",        ft.Icons.PEOPLE_OUTLINED,          "Alunos"),
    ("perfil_aluno",     "Perfil do aluno",        ft.Icons.PERSON_OUTLINED,          "Alunos"),
    ("editar_aluno",     "Editar cadastro",        ft.Icons.EDIT_OUTLINED,            "Alunos"),
    ("relatorio_turma",  "Dados da turma",         ft.Icons.BAR_CHART_OUTLINED,       "Relatórios"),
    ("aptos_graduacao",  "Aptos para graduação",   ft.Icons.MILITARY_TECH_OUTLINED,   "Relatórios"),
]

# Rotas visíveis na sidebar (sem sub-views)
ROTAS_NAV = [
    ("registrar_aula",   "Registrar aula",       ft.Icons.CALENDAR_MONTH_OUTLINED,  "Aulas"),
    ("historico_aulas",  "Histórico de aulas",    ft.Icons.HISTORY,                  "Aulas"),
    ("cadastrar_aluno",  "Cadastrar aluno",        ft.Icons.PERSON_ADD_OUTLINED,      "Alunos"),
    ("lista_alunos",     "Lista de alunos",        ft.Icons.PEOPLE_OUTLINED,          "Alunos"),
    ("relatorio_turma",  "Dados da turma",         ft.Icons.BAR_CHART_OUTLINED,       "Relatórios"),
    ("aptos_graduacao",  "Aptos para graduação",   ft.Icons.MILITARY_TECH_OUTLINED,   "Relatórios"),
]


class FrequenciaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.rota_ativa = "registrar_aula"
        self.nav_items: dict[str, ft.Container] = {}
        self.area_conteudo = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)
        self._views: dict = {}

    def inicializar(self):
        p = self.page
        p.title = "Frequência — Jiu-jitsu"
        p.bgcolor = COR_FUNDO_SEC
        p.padding = 0
        p.window_width      = 1100
        p.window_height     = 740
        p.window_min_width  = 800
        p.window_min_height = 600
        p.theme = ft.Theme(color_scheme_seed="#1A1A1A", font_family="Roboto")

        sidebar = self._build_sidebar()

        conteudo_wrapper = ft.Container(
            content=ft.Column(
                controls=[self.area_conteudo],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
            padding=ft.padding.all(24),
        )

        layout = ft.Row(
            controls=[sidebar, conteudo_wrapper],
            expand=True,
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        p.add(layout)
        self._navegar("registrar_aula")

    # ── Sidebar ────────────────────────────────────────────────────────────

    def _build_sidebar(self):
        logo = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=28, height=8,
                        bgcolor="#1A1A1A",
                        border_radius=2,
                    ),
                    ft.Text("Frequência", size=15, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                    ft.Text("Jiu-jitsu", size=11, color=COR_TEXTO_SEC),
                ],
                spacing=3,
            ),
            padding=ft.padding.only(left=16, top=20, right=16, bottom=16),
            border=ft.border.only(bottom=ft.BorderSide(0.5, COR_BORDA)),
        )

        secoes_vistas = []
        secao_atual = None
        nav_controles = [logo]

        for rota, label, icone, secao in ROTAS_NAV:
            if secao != secao_atual:
                secao_atual = secao
                nav_controles.append(
                    ft.Container(
                        ft.Text(secao.upper(), size=10, weight=ft.FontWeight.W_500,
                                color=COR_TEXTO_HINT,
                                style=ft.TextStyle(letter_spacing=0.8)),
                        padding=ft.padding.only(left=16, top=12, bottom=4),
                    )
                )

            item = self._nav_item(rota, label, icone)
            self.nav_items[rota] = item
            nav_controles.append(item)

        nav_col = ft.Column(controls=nav_controles, spacing=0)

        return ft.Container(
            content=ft.Column(
                controls=[nav_col],
                expand=True,
            ),
            width=220,
            bgcolor=COR_SIDEBAR,
            border=ft.border.only(right=ft.BorderSide(0.5, COR_BORDA)),
            expand=False,
        )

    def _nav_item(self, rota, label, icone):
        def on_click(e, r=rota):
            self._navegar(r)

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icone, size=16, color=COR_TEXTO_SEC),
                    ft.Text(label, size=13, color=COR_TEXTO_SEC),
                ],
                spacing=8,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=7),
            on_click=on_click,
            ink=True,
            border_radius=0,
        )

    def _atualizar_nav_ativo(self, rota):
        # Mapear sub-rotas para suas rotas pai na sidebar
        pai_map = {
            "editar_aula":  "historico_aulas",
            "perfil_aluno": "lista_alunos",
            "editar_aluno": "lista_alunos",
        }
        rota_nav = pai_map.get(rota, rota)
        for r, item in self.nav_items.items():
            if r == rota_nav:
                item.bgcolor = COR_FUNDO_SEC
                row = item.content
                row.controls[0].color = COR_TEXTO
                row.controls[1].color = COR_TEXTO
                row.controls[1].weight = ft.FontWeight.W_500
            else:
                item.bgcolor = None
                row = item.content
                row.controls[0].color = COR_TEXTO_SEC
                row.controls[1].color = COR_TEXTO_SEC
                row.controls[1].weight = ft.FontWeight.W_400

    # ── Navegação ──────────────────────────────────────────────────────────

    def _navegar(self, rota, **kwargs):
        self.rota_ativa = rota
        self._atualizar_nav_ativo(rota)

        info = next((r for r in ROTAS if r[0] == rota), None)
        titulo  = info[1] if info else rota
        secao   = info[3] if info else ""
        hoje    = date.today().strftime("%d/%m/%Y")

        topbar = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(titulo, size=16, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                            ft.Text(secao,  size=12, color=COR_TEXTO_SEC),
                        ],
                        spacing=2,
                    ),
                    ft.Text(hoje, size=12, color=COR_TEXTO_SEC),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=COR_FUNDO,
            border=ft.border.only(bottom=ft.BorderSide(0.5, COR_BORDA)),
            padding=ft.padding.symmetric(horizontal=24, vertical=14),
            margin=ft.margin.only(bottom=20, left=-24, right=-24, top=-24),
        )

        view = self._get_view(rota, **kwargs)

        self.area_conteudo.controls = [topbar, view]
        self.page.update()

    def _get_view(self, rota, **kwargs):
        ctx = {"navegar": self._navegar}
        views_map = {
            "registrar_aula":  ViewRegistrarAula,
            "historico_aulas": ViewHistoricoAulas,
            "editar_aula":     ViewEditarAula,
            "cadastrar_aluno": ViewCadastrarAluno,
            "lista_alunos":    ViewListaAlunos,
            "perfil_aluno":    ViewPerfilAluno,
            "editar_aluno":    ViewEditarAluno,
            "relatorio_turma": ViewRelatorioTurma,
            "aptos_graduacao": ViewAptosGraduacao,
        }
        cls = views_map.get(rota)
        if cls:
            return cls(ctx, **kwargs).build()
        return ft.Text(f"View '{rota}' não encontrada.", color=COR_TEXTO_SEC)