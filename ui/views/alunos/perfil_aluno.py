import flet as ft
from datetime import date, datetime

from app.aluno_service import buscar_aluno_por_id, desativar_aluno, reativar_aluno
from app.relatorio_service import calcular_frequencia_ultimos_90_dias
import sqlite3
from database.config import DATABASE_PATH

from ui.tema import (
    COR_FUNDO, COR_BORDA, COR_BORDA_FORTE, COR_TEXTO, COR_TEXTO_SEC,
     RAIO, 
)
from ui.components.widgets import (
    card, badge_faixa, badge_ativo, avatar,
    stat_card, btn, divisor, campo,
    input_texto, dropdown, alerta,
)

FAIXAS = ["Branca", "Cinza/Branco", "Cinza", "Cinza/Preto", "Amarela", "Amarela/Preto", "Laranja", "Laranja/Preto", "Verde", "Azul", "Roxa", "Marrom", "Preta"]
GRAUS  = ["0", "1", "2", "3", "4"]


def _calcular_idade(nasc_str):
    try:
        nasc = date.fromisoformat(nasc_str)
        hoje = date.today()
        return hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
    except Exception:
        return None
 
 
def _fmt_data(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return d or "—"
 
 
def _campo_data_calendario(label, valor_iso=None, primeiro_ano=1940, ultimo_ano=2030):
    """Retorna (coluna_widget, getter_fn, date_picker)"""
    data_ref = [None]
    if valor_iso:
        try:
            data_ref[0] = date.fromisoformat(valor_iso)
        except Exception:
            pass
 
    texto = ft.Text(
        data_ref[0].strftime("%d/%m/%Y") if data_ref[0] else "Selecionar data",
        size=13,
        color=COR_TEXTO if data_ref[0] else COR_TEXTO_SEC,
    )
 
    picker = ft.DatePicker(
        value=datetime.combine(data_ref[0], datetime.min.time()) if data_ref[0] else None,
        first_date=datetime(primeiro_ano, 1, 1),
        last_date=datetime(ultimo_ano, 12, 31),
    )
 
    botao = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(name=ft.icons.CALENDAR_MONTH_OUTLINED, size=16, color=COR_TEXTO_SEC),
                texto,
            ],
            spacing=8, tight=True,
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
 
 
# ── Perfil ──────────────────────────────────────────────────────────────────
 
class ViewPerfilAluno:
    def __init__(self, ctx, aluno_id=None, **kwargs):
        self.ctx = ctx
        self.aluno_id = aluno_id
 
    def build(self):
        a    = buscar_aluno_por_id(self.aluno_id)
        freq = calcular_frequencia_ultimos_90_dias(self.aluno_id)
 
        nome  = a["nome"]
        faixa = a["faixa"]
        graus = a["graus"]
        ativo = bool(a["ativo"])
        nasc  = a["data_nascimento"] or ""
        idade = _calcular_idade(nasc)
 
        def info_item(lbl, val_widget):
            return ft.Column(
                controls=[ft.Text(lbl, size=10, color=COR_TEXTO_SEC), val_widget],
                spacing=2,
            )
 
        info_rows = [
            info_item("Nascimento",       ft.Text(_fmt_data(nasc), size=13, color=COR_TEXTO)),
            info_item("Idade",            ft.Text(f"{idade} anos" if idade else "—", size=13, color=COR_TEXTO)),
            info_item("Sexo",             ft.Text("Masculino" if a["sexo"] == "M" else "Feminino", size=13, color=COR_TEXTO)),
            info_item("Última graduação", ft.Text(_fmt_data(a["data_ultima_graduacao"] or ""), size=13, color=COR_TEXTO)),
            info_item("Status",           badge_ativo(ativo)),
        ]
 
        info_grid = ft.Row(
            controls=[
                ft.Column(controls=info_rows[:3], spacing=12, expand=True),
                ft.Column(controls=info_rows[3:], spacing=12, expand=True),
            ],
            spacing=16,
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
                                icone=ft.icons.EDIT_OUTLINED),
                            btn(
                                "Desativar" if ativo else "Reativar",
                                on_click=self._toggle_ativo,
                                icone=ft.icons.PERSON_OFF_OUTLINED if ativo else ft.icons.PERSON_OUTLINED,
                                perigo=ativo,
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=0,
            ),
        )
 
        col_dir = card(
            ft.Column(
                controls=[
                    ft.Text("Frequência — últimos 90 dias", size=13, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                    ft.Container(height=12),
                    ft.Row(
                        controls=[
                            stat_card("Presença",  f"{int(freq['frequencia'])}%"),
                            stat_card("Presenças", str(freq["presencas"])),
                            stat_card("Faltas",    str(freq["faltas"])),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=8),
                    ft.Row(controls=[stat_card("Justificadas", str(freq["justificadas"]))], spacing=8),
                    divisor(),
                    ft.Text("Observações", size=13, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                    ft.Container(height=4),
                    ft.Text(a["observacoes"] or "Nenhuma observação registrada.", size=13, color=COR_TEXTO_SEC),
                ],
                spacing=0,
            ),
        )
 
        return ft.Column(
            controls=[
                ft.Container(
                    btn("Voltar à lista",
                        on_click=lambda e: self.ctx["navegar"]("lista_alunos"),
                        icone=ft.icons.ARROW_BACK),
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
            # Dialog para pedir motivo
            motivo_field = ft.TextField(
                label="Motivo da saída (opcional)",
                text_style=ft.TextStyle(size=13),
                border_color=COR_BORDA,
                focused_border_color=COR_BORDA_FORTE,
                border_radius=RAIO,
            )
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Desativar aluno", size=15),
                content=ft.Container(
                    content=motivo_field,
                    width=360,
                    padding=ft.padding.only(top=8),
                ),
                actions=[
                    ft.TextButton(
                        "Cancelar",
                        on_click=lambda ev: self._fechar_dialog(ev, dlg),
                    ),
                    ft.TextButton(
                        "Confirmar",
                        on_click=lambda ev: self._confirmar_desativar(ev, motivo_field, dlg),
                    ),
                ],
            )
            e.page.open(dlg)
        else:
            reativar_aluno(self.aluno_id)
            self.ctx["navegar"]("perfil_aluno", aluno_id=self.aluno_id)
 
    def _fechar_dialog(self, e, dlg):
        e.page.close(dlg)
        '''e.page.dialog.open = False
        e.page.update()'''
 
    def _confirmar_desativar(self, e, motivo_field, dlg):
        desativar_aluno(self.aluno_id, motivo_field.value or "")
        e.page.close(dlg)
        '''e.page.dialog.open = False
        e.page.update()'''
        self.ctx["navegar"]("perfil_aluno", aluno_id=self.aluno_id)
 
 
# ── Editar aluno ─────────────────────────────────────────────────────────────
 
class ViewEditarAluno:
    def __init__(self, ctx, aluno_id=None, **kwargs):
        self.ctx = ctx
        self.aluno_id = aluno_id
        self.aviso_container = ft.Container(visible=False)
 
    def build(self):
        a = buscar_aluno_por_id(self.aluno_id)
 
        self.f_nome  = input_texto(valor=a["nome"] or "")
        self.f_sexo  = dropdown(["Masculino", "Feminino"],
                                valor="Masculino" if a["sexo"] == "M" else "Feminino")
        self.f_faixa = dropdown(FAIXAS, valor=a["faixa"])
        self.f_graus = dropdown(GRAUS,  valor=str(a["graus"]))
        self.f_obs   = input_texto(valor=a["observacoes"] or "", multiline=True, min_lines=3)
 
        # Campos de data com calendário
        col_nasc, self._get_nasc, self._picker_nasc = _campo_data_calendario(
            "Data de nascimento",
            valor_iso=a["data_nascimento"],
            primeiro_ano=1940, ultimo_ano=2020,
        )
        col_grad, self._get_grad, self._picker_grad = _campo_data_calendario(
            "Última graduação",
            valor_iso=a["data_ultima_graduacao"],
            primeiro_ano=2000, ultimo_ano=2030,
        )
 
        return ft.Column(
            controls=[
                ft.Container(
                    btn("Voltar ao perfil",
                        on_click=lambda e: self.ctx["navegar"]("perfil_aluno", aluno_id=self.aluno_id),
                        icone=ft.icons.ARROW_BACK),
                    margin=ft.margin.only(bottom=16),
                ),
                self.aviso_container,
                card(
                    ft.Column(
                        controls=[
                            ft.Row([campo("Nome completo", self.f_nome), campo("Sexo", self.f_sexo)], spacing=16),
                            ft.Row([col_nasc], spacing=16),
                            ft.Row([campo("Faixa", self.f_faixa), campo("Graus", self.f_graus)], spacing=16),
                            col_grad,
                            campo("Observações", self.f_obs),
                            ft.Container(
                                btn("Salvar alterações",
                                    on_click=self._salvar,
                                    icone=ft.icons.SAVE_OUTLINED,
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
                    self._get_nasc(),
                    self.f_faixa.value,
                    int(self.f_graus.value or 0),
                    self._get_grad(),
                    self.f_obs.value,
                    self.aluno_id,
                )
            )
            conn.commit()
            conn.close()
            self.ctx["navegar"]("perfil_aluno", aluno_id=self.aluno_id)
        except Exception as ex:
            self.aviso_container.content = alerta(f"Erro: {ex}", "perigo")
            self.aviso_container.visible = True
            e.page.update()