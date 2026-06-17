import flet as ft
from datetime import date, datetime

from app.aluno_service import cadastrar_aluno

from ui.tema import COR_FUNDO, COR_BORDA, COR_TEXTO, COR_TEXTO_SEC, RAIO
from ui.components.widgets import (
    card, campo, input_texto,  dropdown, btn, alerta,
)

FAIXAS = ["Branca", "Cinza/Branco", "Cinza", "Cinza/Preto", "Amarela", "Amarela/Preto", "Laranja", "Laranja/Preto", "Verde", "Azul", "Roxa", "Marrom", "Preta"]
GRAUS  = ["0", "1", "2", "3", "4"]


def _campo_data_com_calendario(label, valor_inicial=None):
    """Retorna (container_campo, getter_fn, date_picker)"""
    data_ref = [valor_inicial]  # lista para mutabilidade no closure
 
    texto = ft.Text(
        valor_inicial.strftime("%d/%m/%Y") if valor_inicial else "Selecionar data",
        size=13,
        color=COR_TEXTO if valor_inicial else COR_TEXTO_SEC,
    )
 
    picker = ft.DatePicker(
        value=datetime.combine(valor_inicial, datetime.min.time()) if valor_inicial else None,
        first_date=datetime(2008, 1, 1),
        last_date=datetime(2100, 12, 31),
    )
 
    botao = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(name=ft.icons.CALENDAR_MONTH_OUTLINED, size=16, color=COR_TEXTO_SEC),
                texto,
            ],
            spacing=8,
            tight=True,
        ),
        bgcolor=COR_FUNDO,
        border=ft.border.all(0.5, COR_BORDA),
        border_radius=RAIO,
        padding=ft.padding.symmetric(horizontal=10, vertical=9),
        ink=True,
    )
 
    def abrir(e):
        if picker not in e.page.overlay:
            e.page.overlay.append(picker)
        picker.open = True
        e.page.update()
 
    def on_change(e):
        if e.control.value:
            d = e.control.value.date() if hasattr(e.control.value, 'date') else e.control.value
            data_ref[0] = d
            texto.value = d.strftime("%d/%m/%Y")
            texto.color = COR_TEXTO
            try:
                e.page.update()
            except Exception:
                pass
 
    picker.on_change = on_change
    botao.on_click   = abrir
 
    def getter():
        return data_ref[0].isoformat() if data_ref[0] else None
 
    coluna = ft.Column(
        controls=[
            ft.Text(label, size=11, weight=ft.FontWeight.W_500, color=COR_TEXTO_SEC),
            botao,
        ],
        spacing=4,
        expand=True,
    )
 
    return coluna, getter, picker
 
 
class ViewCadastrarAluno:
    def __init__(self, ctx, **kwargs):
        self.ctx = ctx
        self.aviso_container = ft.Container(visible=False)
        self._pickers = []
        self._init_campos()
 
    def _init_campos(self):
        self.f_nome  = input_texto(hint="Nome completo")
        self.f_sexo  = dropdown(["Masculino", "Feminino"])
        self.f_faixa = dropdown(FAIXAS)
        self.f_graus = dropdown(GRAUS)
        self.f_obs   = input_texto(
            hint="Lesões, contatos de emergência, informações relevantes…",
            multiline=True, min_lines=3,
        )
 
        col_nasc, self._get_nasc, self._picker_nasc = _campo_data_com_calendario("Data de nascimento")
        col_grad, self._get_grad, self._picker_grad = _campo_data_com_calendario("Última graduação", date.today())
        self._col_nasc = col_nasc
        self._col_grad = col_grad
        self._pickers  = [self._picker_nasc, self._picker_grad]
 
    def build(self):
        return ft.Column(
            controls=[
                self.aviso_container,
                card(
                    ft.Column(
                        controls=[
                            ft.Row([campo("Nome completo *", self.f_nome), campo("Sexo", self.f_sexo)], spacing=16),
                            ft.Row([self._col_nasc], spacing=16),
                            ft.Row([campo("Faixa", self.f_faixa), campo("Graus", self.f_graus)], spacing=16),
                            self._col_grad,
                            campo("Observações", self.f_obs),
                            ft.Row(
                                controls=[
                                    btn("Limpar",    on_click=self._limpar),
                                    btn("Cadastrar", on_click=self._cadastrar,
                                        icone=ft.icons.PERSON_ADD_OUTLINED, primario=True),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                                spacing=8,
                            ),
                        ],
                        spacing=14,
                        width=540,
                    ),
                ),
            ],
            spacing=0,
            expand=True,
        )
 
    def _cadastrar(self, e):
        nome = self.f_nome.value.strip()
        if not nome:
            self._mostrar_aviso("Nome é obrigatório.", "perigo")
            return
        sexo = "M" if self.f_sexo.value == "Masculino" else "F"
        try:
            cadastrar_aluno(
                nome=nome,
                sexo=sexo,
                data_nascimento=self._get_nasc(),
                faixa=self.f_faixa.value,
                graus=int(self.f_graus.value or 0),
                data_ultima_graduacao=self._get_grad(),
                observacoes=self.f_obs.value.strip(),
            )
            self._mostrar_aviso(f"Aluno '{nome}' cadastrado com sucesso!", "sucesso")
            self._limpar(e)
        except Exception as ex:
            self._mostrar_aviso(f"Erro ao cadastrar: {ex}", "perigo")
 
    def _limpar(self, e=None):
        self.f_nome.value  = ""
        self.f_faixa.value = "Branca"
        self.f_graus.value = "0"
        self.f_obs.value   = ""
        if e:
            e.page.update()
 
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