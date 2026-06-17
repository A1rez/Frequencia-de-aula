import flet as ft
from datetime import date, datetime

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
        self.presencas: dict = {}
        self.alunos = []
        self.dropdowns: dict = {}
        self.aviso_container = ft.Container(visible=False)
        self._data_selecionada = date.today()
        self.campo_obs = ft.TextField(
            hint_text="Ex.: treino especial, competição…",
            hint_style=ft.TextStyle(color=COR_TEXTO_SEC, size=13),
            text_style=ft.TextStyle(color=COR_TEXTO, size=13),
            border_color=COR_BORDA,
            focused_border_color=COR_BORDA_FORTE,
            border_radius=RAIO,
            bgcolor=COR_FUNDO,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
        )
 
    def build(self):
        self.alunos = listar_alunos_ativos()
        for a in self.alunos:
            self.presencas[a["id"]] = "FALTA"
 
        # Botão de data com ícone de calendário
        self.data_btn_text = ft.Text(
            self._data_selecionada.strftime("%d/%m/%Y"),
            size=13,
            color=COR_TEXTO,
        )
        self.data_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(name=ft.icons.CALENDAR_MONTH_OUTLINED, size=16, color=COR_TEXTO_SEC),
                    self.data_btn_text,
                ],
                spacing=8,
                tight=True,
            ),
            bgcolor=COR_FUNDO,
            border=ft.border.all(0.5, COR_BORDA),
            border_radius=RAIO,
            padding=ft.padding.symmetric(horizontal=10, vertical=9),
            on_click=self._abrir_calendario,
            ink=True,
        )
 
        # DatePicker (adicionado ao overlay da page depois)
        self.date_picker = ft.DatePicker(
            value=datetime.combine(self._data_selecionada, datetime.min.time()),
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2030, 12, 31),
            on_change=self._on_data_change,
        )
 
        lista_chamada = self._build_lista_chamada()
 
        return ft.Column(
            controls=[
                self.aviso_container,
                card(
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("Data da aula", size=11, weight=ft.FontWeight.W_500, color=COR_TEXTO_SEC),
                                    self.data_btn,
                                ],
                                spacing=4,
                                expand=True,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Observação (opcional)", size=11, weight=ft.FontWeight.W_500, color=COR_TEXTO_SEC),
                                    self.campo_obs,
                                ],
                                spacing=4,
                                expand=True,
                            ),
                        ],
                        spacing=16,
                    ),
                    margem_baixo=16,
                ),
                card(
                    ft.Column(
                        controls=[
                            secao_header(
                                "Lista de chamada",
                                acoes=[
                                    btn("Todos ausentes",  on_click=lambda e: self._marcar_todos("FALTA"),  pequeno=True),
                                    btn("Todos presentes", on_click=lambda e: self._marcar_todos("PRESENTE"), pequeno=True),
                                ],
                            ),
                            lista_chamada,
                            ft.Container(
                                content=btn(
                                    "Salvar chamada",
                                    on_click=self._salvar,
                                    icone=ft.icons.SAVE_OUTLINED,
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
 
    def _abrir_calendario(self, e):
        # Adiciona o picker ao overlay se ainda não estiver lá
        if self.date_picker not in e.page.overlay:
            e.page.overlay.append(self.date_picker)
        self.date_picker.open = True
        e.page.update()
 
    def _on_data_change(self, e):
        if e.control.value:
            self._data_selecionada = e.control.value.date() if hasattr(e.control.value, 'date') else e.control.value
            self.data_btn_text.value = self._data_selecionada.strftime("%d/%m/%Y")
            try:
                e.page.update()
            except Exception:
                pass
 
    def _build_lista_chamada(self):
        linhas = []
        for a in self.alunos:
            dd = ft.Dropdown(
                value="FALTA",
                options=[
                    ft.dropdown.Option("FALTA",     "Falta"),
                    ft.dropdown.Option("PRESENTE",    "Presente"),
                    ft.dropdown.Option("JUSTIFICADA", "Justificado"),
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
        if self.dropdowns:
            list(self.dropdowns.values())[0].page.update()
 
    def _salvar(self, e):
        data_iso = self._data_selecionada.isoformat()
        try:
            cadastrar_aula(data_iso, self.campo_obs.value.strip())
            aula = buscar_aula_por_data(data_iso)
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
        self.aviso_container.content = alerta(msg, tipo)
        self.aviso_container.visible = True
        try:
            self.aviso_container.page.update()
        except Exception:
            pass
        import threading, time
        def esconder():
            time.sleep(3)
            self.aviso_container.visible = False
            try:
                self.aviso_container.page.update()
            except Exception:
                pass
        threading.Thread(target=esconder, daemon=True).start()