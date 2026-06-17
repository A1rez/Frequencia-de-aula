import flet as ft
from datetime import date

from database.config import DATABASE_PATH
from app.aula_service import cadastrar_aula, buscar_aula_por_data
from app.aluno_service import listar_alunos_ativos
from app.presenca_service import registrar_presenca

from ui.tema import (
    COR_FUNDO, COR_FUNDO_SEC, COR_BORDA, COR_BORDA_FORTE,
    COR_TEXTO, COR_TEXTO_SEC, COR_TEXTO_HINT,
    COR_PRIMARIA, RAIO, RAIO_LG,
    STATUS_CORES, STATUS_LABELS, FAIXA_CORES,
)
from ui.components.widgets import (
    card, secao_header, badge_faixa, avatar,
    alerta, campo, input_texto, input_data, btn, divisor,
)


class ViewRegistrarAula:
    def __init__(self, ctx, **kwargs):
        self.ctx = ctx
        self.presencas: dict[int, str] = {}
        self.alunos = []
        self.dropdowns: dict[int, ft.Dropdown] = {}
        self.aviso_ref = ft.Ref[ft.Container]()
        self.campo_data = input_data(valor=date.today().isoformat())
        self.campo_obs  = input_texto(hint="Ex.: treino especial, competição…")

    def build(self):
        self.alunos = listar_alunos_ativos()
        for a in self.alunos:
            self.presencas[a["id"]] = "AUSENTE"

        lista_chamada = self._build_lista_chamada()

        return ft.Column(
            controls=[
                ft.Container(ref=self.aviso_ref, visible=False),

                # Cabeçalho da aula
                card(
                    ft.Row(
                        controls=[
                            campo("Data da aula", self.campo_data),
                            campo("Observação (opcional)", self.campo_obs),
                        ],
                        spacing=16,
                    ),
                    margem_baixo=16,
                ),

                # Lista de chamada
                card(
                    ft.Column(
                        controls=[
                            secao_header(
                                "Lista de chamada",
                                acoes=[
                                    btn("Todos ausentes",  on_click=lambda e: self._marcar_todos("AUSENTE"),  pequeno=True),
                                    btn("Todos presentes", on_click=lambda e: self._marcar_todos("PRESENTE"), pequeno=True),
                                ],
                            ),
                            lista_chamada,
                            ft.Container(
                                content=btn(
                                    "Salvar chamada",
                                    on_click=self._salvar,
                                    icone=ft.Icons.SAVE_OUTLINED,
                                    primario=True,
                                ),
                                alignment=ft.alignment.center_right,
                                margin=ft.margin.only(top=16),
                            ),
                        ],
                        spacing=0,
                    ),
                ),
            ],
            spacing=0,
            expand=True,
        )

    def _build_lista_chamada(self):
        linhas = []
        for a in self.alunos:
            dd = ft.Dropdown(
                value="AUSENTE",
                options=[
                    ft.dropdown.Option("AUSENTE",     "Ausente"),
                    ft.dropdown.Option("PRESENTE",    "Presente"),
                    ft.dropdown.Option("JUSTIFICADO", "Justificado"),
                ],
                border_color=COR_BORDA,
                focused_border_color=COR_BORDA_FORTE,
                border_radius=RAIO,
                bgcolor=COR_FUNDO,
                text_style=ft.TextStyle(color=COR_TEXTO, size=13),
                content_padding=ft.padding.symmetric(horizontal=10, vertical=4),
                width=140,
                on_change=lambda e, aid=a["id"]: self._on_status_change(aid, e.control.value),
            )
            self.dropdowns[a["id"]] = dd

            linha = ft.Container(
                content=ft.Row(
                    controls=[
                        avatar(a["nome"]),
                        ft.Column(
                            controls=[
                                ft.Text(a["nome"], size=13, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                                badge_faixa(a["faixa"], a["graus"]),
                            ],
                            spacing=3,
                            expand=True,
                        ),
                        dd,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                padding=ft.padding.symmetric(vertical=10),
                border=ft.border.only(bottom=ft.BorderSide(0.5, COR_BORDA)),
            )
            linhas.append(linha)

        if linhas:
            linhas[-1].border = None

        return ft.Column(controls=linhas, spacing=0)

    def _on_status_change(self, aluno_id, status):
        self.presencas[aluno_id] = status

    def _marcar_todos(self, status):
        for aid, dd in self.dropdowns.items():
            dd.value = status
            self.presencas[aid] = status
        self.dropdowns[list(self.dropdowns.keys())[0]].page.update()

    def _salvar(self, e):
        data = self.campo_data.value.strip()
        obs  = self.campo_obs.value.strip()

        if not data:
            self._mostrar_aviso("Informe a data da aula.", "perigo")
            return

        try:
            cadastrar_aula(data, obs)
            aula = buscar_aula_por_data(data)
            aula_id = aula["id"]

            for aluno_id, status in self.presencas.items():
                registrar_presenca(aluno_id, aula_id, status)

            self.campo_obs.value = ""
            for dd in self.dropdowns.values():
                dd.value = "AUSENTE"
            for aid in self.presencas:
                self.presencas[aid] = "AUSENTE"

            self._mostrar_aviso("Aula registrada com sucesso!", "sucesso")
            e.page.update()

        except Exception as ex:
            self._mostrar_aviso(f"Erro ao salvar: {ex}", "perigo")

    def _mostrar_aviso(self, msg, tipo):
        from ui.components.widgets import alerta
        aviso = alerta(msg, tipo)
        aviso.visible = True
        self.aviso_ref.current.content = aviso
        self.aviso_ref.current.visible = True
        self.aviso_ref.current.page.update()

        import threading
        def esconder():
            import time; time.sleep(3)
            self.aviso_ref.current.visible = False
            try:
                self.aviso_ref.current.page.update()
            except Exception:
                pass
        threading.Thread(target=esconder, daemon=True).start()