import flet as ft
from datetime import date

from app.aluno_service import buscar_aluno_por_id, desativar_aluno, reativar_aluno
from app.relatorio_service import calcular_frequencia_ultimos_90_dias
import sqlite3
from database.config import DATABASE_PATH

from ui.tema import (
    COR_FUNDO, COR_FUNDO_SEC, COR_BORDA, COR_TEXTO, COR_TEXTO_SEC,
    FAIXA_CORES, RAIO, RAIO_LG,
)
from ui.components.widgets import (
    card, badge_faixa, badge_ativo, avatar,
    stat_card, btn, divisor, campo,
    input_texto, input_data, dropdown, alerta,
)

FAIXAS = ["Branca", "Cinza", "Amarela", "Laranja", "Verde", "Azul", "Roxa", "Marrom", "Preta"]
GRAUS  = ["0", "1", "2", "3", "4"]


def calcular_idade(nasc_str):
    try:
        nasc = date.fromisoformat(nasc_str)
        hoje = date.today()
        return hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
    except Exception:
        return None


class ViewPerfilAluno:
    def __init__(self, ctx, aluno_id=None, **kwargs):
        self.ctx = ctx
        self.aluno_id = aluno_id

    def build(self):
        a = buscar_aluno_por_id(self.aluno_id)
        freq = calcular_frequencia_ultimos_90_dias(self.aluno_id)

        nome    = a["nome"]
        faixa   = a["faixa"]
        graus   = a["graus"]
        ativo   = bool(a["ativo"])
        nasc    = a["data_nascimento"] or ""
        sexo_str = "Masculino" if a["sexo"] == "M" else "Feminino"

        def fmt_data(d):
            try:
                from datetime import datetime
                return datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y")
            except Exception:
                return d or "—"

        idade = calcular_idade(nasc)
        idade_str = f"{idade} anos" if idade else "—"

        # Coluna esquerda — dados
        info_rows = [
            ("Nascimento",        fmt_data(nasc)),
            ("Idade",             idade_str),
            ("Sexo",              sexo_str),
            ("Última graduação",  fmt_data(a["data_ultima_graduacao"] or "")),
            ("Status",            None),  # badge especial
        ]

        def info_item(lbl, val):
            if val is None:
                val_widget = badge_ativo(ativo)
            else:
                val_widget = ft.Text(val, size=13, color=COR_TEXTO)
            return ft.Column(
                controls=[
                    ft.Text(lbl, size=10, color=COR_TEXTO_SEC),
                    val_widget,
                ],
                spacing=2,
            )

        info_grid = ft.Row(
            controls=[
                ft.Column(
                    controls=[info_item(l, v) for l, v in info_rows[:3]],
                    spacing=12,
                    expand=True,
                ),
                ft.Column(
                    controls=[info_item(l, v) for l, v in info_rows[3:]],
                    spacing=12,
                    expand=True,
                ),
            ],
            spacing=16,
        )

        btn_toggle = btn(
            "Desativar" if ativo else "Reativar",
            on_click=self._toggle_ativo,
            icone=ft.Icons.PERSON_OFF_OUTLINED if ativo else ft.Icons.PERSON_OUTLINED,
            perigo=ativo,
        )

        col_esq = card(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            avatar(nome, tamanho=52, font_size=18),
                            ft.Column(
                                controls=[
                                    ft.Text(nome, size=16, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                                    badge_faixa(faixa, graus),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    divisor(),
                    info_grid,
                    divisor(),
                    ft.Row(
                        controls=[
                            btn("Editar cadastro",
                                on_click=lambda e: self.ctx["navegar"]("editar_aluno", aluno_id=self.aluno_id),
                                icone=ft.Icons.EDIT_OUTLINED),
                            btn_toggle,
                        ],
                        spacing=8,
                    ),
                ],
                spacing=0,
            ),
        )

        # Coluna direita — frequência
        obs = a["observacoes"] or "Nenhuma observação registrada."

        col_dir = card(
            ft.Column(
                controls=[
                    ft.Text("Frequência — últimos 90 dias", size=13, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                    ft.Container(height=12),
                    ft.Row(
                        controls=[
                            stat_card("Presença", f"{int(freq['frequencia'])}%"),
                            stat_card("Presenças", str(freq["presencas"])),
                            stat_card("Faltas", str(freq["faltas"])),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=16),
                    ft.Text("Justificadas", size=11, color=COR_TEXTO_SEC),
                    ft.Text(str(freq["justificadas"]), size=22, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                    divisor(),
                    ft.Text("Observações", size=13, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                    ft.Container(height=4),
                    ft.Text(obs, size=13, color=COR_TEXTO_SEC),
                ],
                spacing=0,
            ),
        )

        return ft.Column(
            controls=[
                ft.Container(
                    btn("Voltar à lista",
                        on_click=lambda e: self.ctx["navegar"]("lista_alunos"),
                        icone=ft.Icons.ARROW_BACK),
                    margin=ft.margin.only(bottom=16),
                ),
                ft.Row(
                    controls=[col_esq, col_dir],
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=0,
        )

    def _toggle_ativo(self, e):
        a = buscar_aluno_por_id(self.aluno_id)
        if a["ativo"]:
            # Pede motivo via dialog
            motivo_field = ft.TextField(
                label="Motivo da saída",
                text_style=ft.TextStyle(size=13),
                border_radius=RAIO,
            )

            def confirmar(ev):
                desativar_aluno(self.aluno_id, motivo_field.value or "")
                e.page.dialog.open = False
                e.page.update()
                self.ctx["navegar"]("perfil_aluno", aluno_id=self.aluno_id)

            def cancelar(ev):
                e.page.dialog.open = False
                e.page.update()

            e.page.dialog = ft.AlertDialog(
                title=ft.Text("Desativar aluno", size=15),
                content=ft.Column([motivo_field], tight=True),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.TextButton("Confirmar", on_click=confirmar),
                ],
            )
            e.page.dialog.open = True
            e.page.update()
        else:
            reativar_aluno(self.aluno_id)
            self.ctx["navegar"]("perfil_aluno", aluno_id=self.aluno_id)


class ViewEditarAluno:
    def __init__(self, ctx, aluno_id=None, **kwargs):
        self.ctx = ctx
        self.aluno_id = aluno_id
        self.aviso_ref = ft.Ref[ft.Container]()

    def build(self):
        a = buscar_aluno_por_id(self.aluno_id)

        self.f_nome    = input_texto(valor=a["nome"] or "")
        self.f_sexo    = dropdown(["Masculino", "Feminino"],
                                  valor="Masculino" if a["sexo"] == "M" else "Feminino")
        self.f_nasc    = input_data(valor=a["data_nascimento"] or "")
        self.f_faixa   = dropdown(FAIXAS, valor=a["faixa"])
        self.f_graus   = dropdown(GRAUS,  valor=str(a["graus"]))
        self.f_grad    = input_data(valor=a["data_ultima_graduacao"] or "")
        self.f_obs     = input_texto(valor=a["observacoes"] or "", multiline=True, min_lines=3)

        return ft.Column(
            controls=[
                ft.Container(
                    btn("Voltar ao perfil",
                        on_click=lambda e: self.ctx["navegar"]("perfil_aluno", aluno_id=self.aluno_id),
                        icone=ft.Icons.ARROW_BACK),
                    margin=ft.margin.only(bottom=16),
                ),
                ft.Container(ref=self.aviso_ref, visible=False),
                card(
                    ft.Column(
                        controls=[
                            ft.Row([campo("Nome completo", self.f_nome), campo("Sexo", self.f_sexo)], spacing=16),
                            ft.Row([campo("Data de nascimento", self.f_nasc)], spacing=16),
                            ft.Row([campo("Faixa", self.f_faixa), campo("Graus", self.f_graus)], spacing=16),
                            campo("Última graduação", self.f_grad),
                            campo("Observações", self.f_obs),
                            ft.Container(
                                btn("Salvar alterações",
                                    on_click=self._salvar,
                                    icone=ft.Icons.SAVE_OUTLINED,
                                    primario=True),
                                alignment=ft.alignment.center_right,
                            ),
                        ],
                        spacing=14,
                        width=540,
                    ),
                ),
            ],
            spacing=0,
        )

    def _salvar(self, e):
        try:
            sexo = "M" if self.f_sexo.value == "Masculino" else "F"
            conn = sqlite3.connect(DATABASE_PATH)
            cur  = conn.cursor()
            cur.execute(
                """UPDATE alunos SET nome=?, sexo=?, data_nascimento=?, faixa=?, graus=?,
                   data_ultima_graduacao=?, observacoes=? WHERE id=?""",
                (
                    self.f_nome.value,
                    sexo,
                    self.f_nasc.value or None,
                    self.f_faixa.value,
                    int(self.f_graus.value or 0),
                    self.f_grad.value or None,
                    self.f_obs.value,
                    self.aluno_id,
                )
            )
            conn.commit()
            conn.close()
            self.ctx["navegar"]("perfil_aluno", aluno_id=self.aluno_id)
        except Exception as ex:
            self.aviso_ref.current.content = alerta(f"Erro: {ex}", "perigo")
            self.aviso_ref.current.visible = True
            e.page.update()