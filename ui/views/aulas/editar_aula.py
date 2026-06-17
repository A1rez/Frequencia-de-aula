import flet as ft
import sqlite3
from datetime import datetime

from database.config import DATABASE_PATH
from app.aula_service import buscar_aula_por_id
from app.aluno_service import listar_alunos_ativos
from app.presenca_service import listar_presencas_da_aula

from ui.tema import (
    COR_FUNDO, COR_FUNDO_SEC, COR_BORDA, COR_BORDA_FORTE,
    COR_TEXTO, COR_TEXTO_SEC, COR_TEXTO_HINT, RAIO,
)
from ui.components.widgets import (
    card, secao_header, badge_faixa, avatar,
    campo, input_data, input_texto, btn, alerta,
)


class ViewEditarAula:
    def __init__(self, ctx, aula_id=None, **kwargs):
        self.ctx = ctx
        self.aula_id = aula_id
        self.presencas: dict[int, str] = {}
        self.dropdowns: dict[int, ft.Dropdown] = {}
        self.aviso_ref = ft.Ref[ft.Container]()

    def build(self):
        aula   = buscar_aula_por_id(self.aula_id)
        alunos = listar_alunos_ativos()
        presencas_aula = {p["aluno_id"]: p["status"]
                          for p in self._listar_presencas_completas()}

        for a in alunos:
            self.presencas[a["id"]] = presencas_aula.get(a["id"], "AUSENTE")

        try:
            dt = datetime.strptime(aula["data"], "%Y-%m-%d")
            titulo = f"Editando aula de {dt.strftime('%d/%m/%Y')}"
        except Exception:
            titulo = "Editar aula"

        self.campo_data = input_data(valor=aula["data"])
        self.campo_obs  = input_texto(valor=aula["observacao"] or "")

        lista = self._build_lista(alunos)

        return ft.Column(
            controls=[
                # Botão voltar
                ft.Container(
                    btn("Voltar ao histórico",
                        on_click=lambda e: self.ctx["navegar"]("historico_aulas"),
                        icone=ft.Icons.ARROW_BACK),
                    margin=ft.margin.only(bottom=16),
                ),

                ft.Container(ref=self.aviso_ref, visible=False),

                card(
                    ft.Row(
                        controls=[
                            campo("Data da aula", self.campo_data),
                            campo("Observação", self.campo_obs),
                        ],
                        spacing=16,
                    ),
                    margem_baixo=16,
                ),

                card(
                    ft.Column(
                        controls=[
                            secao_header(titulo),
                            lista,
                            ft.Container(
                                btn("Salvar alterações",
                                    on_click=self._salvar,
                                    icone=ft.Icons.SAVE_OUTLINED,
                                    primario=True),
                                alignment=ft.alignment.center_right,
                                margin=ft.margin.only(top=16),
                            ),
                        ],
                        spacing=0,
                    )
                ),
            ],
            spacing=0,
        )

    def _listar_presencas_completas(self):
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT aluno_id, status FROM presencas WHERE aula_id = ?",
            (self.aula_id,)
        )
        resultado = [dict(r) for r in cur.fetchall()]
        conn.close()
        return resultado

    def _build_lista(self, alunos):
        linhas = []
        for a in alunos:
            status_atual = self.presencas.get(a["id"], "AUSENTE")
            dd = ft.Dropdown(
                value=status_atual,
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
                on_change=lambda e, aid=a["id"]: self._on_change(aid, e.control.value),
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

    def _on_change(self, aluno_id, status):
        self.presencas[aluno_id] = status

    def _salvar(self, e):
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cur  = conn.cursor()
            cur.execute(
                "UPDATE aulas SET data=?, observacao=? WHERE id=?",
                (self.campo_data.value, self.campo_obs.value, self.aula_id)
            )
            for aluno_id, status in self.presencas.items():
                cur.execute(
                    """INSERT INTO presencas (aluno_id, aula_id, status)
                       VALUES (?, ?, ?)
                       ON CONFLICT(aluno_id, aula_id)
                       DO UPDATE SET status=excluded.status""",
                    (aluno_id, self.aula_id, status)
                )
            conn.commit()
            conn.close()
            self.ctx["navegar"]("historico_aulas")
        except Exception as ex:
            self._mostrar_aviso(f"Erro: {ex}", "perigo")

    def _mostrar_aviso(self, msg, tipo):
        from ui.components.widgets import alerta
        self.aviso_ref.current.content = alerta(msg, tipo)
        self.aviso_ref.current.visible = True
        self.aviso_ref.current.page.update()