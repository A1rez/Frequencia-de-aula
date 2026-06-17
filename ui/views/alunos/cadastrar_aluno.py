import flet as ft
from datetime import date

from app.aluno_service import cadastrar_aluno

from ui.tema import COR_FUNDO, COR_BORDA, COR_TEXTO, COR_TEXTO_SEC, RAIO, RAIO_LG
from ui.components.widgets import (
    card, campo, input_texto, input_data, dropdown, btn, alerta,
)

FAIXAS = ["Branca", "Cinza", "Amarela", "Laranja", "Verde", "Azul", "Roxa", "Marrom", "Preta"]
GRAUS  = ["0", "1", "2", "3", "4"]


class ViewCadastrarAluno:
    def __init__(self, ctx, **kwargs):
        self.ctx = ctx
        self.aviso_ref = ft.Ref[ft.Container]()
        self._init_campos()

    def _init_campos(self):
        hoje = date.today().isoformat()
        self.f_nome    = input_texto(hint="Nome completo")
        self.f_sexo    = dropdown(["Masculino", "Feminino"])
        self.f_nasc    = input_data()
        self.f_faixa   = dropdown(FAIXAS)
        self.f_graus   = dropdown(GRAUS)
        self.f_grad    = input_data(valor=hoje)
        self.f_obs     = input_texto(hint="Lesões, contatos de emergência, informações relevantes…",
                                     multiline=True, min_lines=3)

    def build(self):
        return ft.Column(
            controls=[
                ft.Container(ref=self.aviso_ref, visible=False),
                card(
                    ft.Column(
                        controls=[
                            ft.Row([
                                campo("Nome completo *", self.f_nome),
                                campo("Sexo", self.f_sexo),
                            ], spacing=16),
                            ft.Row([
                                campo("Data de nascimento", self.f_nasc),
                            ], spacing=16),
                            ft.Row([
                                campo("Faixa", self.f_faixa),
                                campo("Graus", self.f_graus),
                            ], spacing=16),
                            campo("Última graduação", self.f_grad),
                            campo("Observações", self.f_obs),
                            ft.Row(
                                controls=[
                                    btn("Limpar", on_click=self._limpar),
                                    btn("Cadastrar",
                                        on_click=self._cadastrar,
                                        icone=ft.Icons.PERSON_ADD_OUTLINED,
                                        primario=True),
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
                data_nascimento=self.f_nasc.value or None,
                faixa=self.f_faixa.value,
                graus=int(self.f_graus.value or 0),
                data_ultima_graduacao=self.f_grad.value or None,
                observacoes=self.f_obs.value.strip(),
            )
            self._mostrar_aviso(f"Aluno '{nome}' cadastrado com sucesso!", "sucesso")
            self._limpar(e)
        except Exception as ex:
            self._mostrar_aviso(f"Erro ao cadastrar: {ex}", "perigo")

    def _limpar(self, e=None):
        self.f_nome.value    = ""
        self.f_nasc.value    = ""
        self.f_faixa.value   = "Branca"
        self.f_graus.value   = "0"
        self.f_obs.value     = ""
        if e:
            e.page.update()

    def _mostrar_aviso(self, msg, tipo):
        self.aviso_ref.current.content = alerta(msg, tipo)
        self.aviso_ref.current.visible = True
        self.aviso_ref.current.page.update()

        import threading, time
        def esconder():
            time.sleep(3)
            self.aviso_ref.current.visible = False
            try: self.aviso_ref.current.page.update()
            except Exception: pass
        threading.Thread(target=esconder, daemon=True).start()