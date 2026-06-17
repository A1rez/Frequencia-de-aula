import flet as ft

from app.relatorio_service import listar_aptos_graduacao

from ui.tema import (
    COR_FUNDO, COR_FUNDO_SEC, COR_BORDA, COR_TEXTO, COR_TEXTO_SEC, RAIO_LG,
)
from ui.components.widgets import (
    card, badge_faixa, avatar, btn, alerta,
)


class ViewAptosGraduacao:
    def __init__(self, ctx, **kwargs):
        self.ctx = ctx

    def build(self):
        try:
            aptos = listar_aptos_graduacao()
        except Exception as ex:
            return ft.Text(f"Erro ao carregar: {ex}", color=COR_TEXTO_SEC)

        aviso = alerta(
            "Critérios: ≥ 50% de frequência nos últimos 90 dias "
            "e mínimo de 90 dias desde a última graduação.",
            "aviso",
        )

        if not aptos:
            conteudo = ft.Container(
                ft.Text(
                    "Nenhum aluno atinge os critérios no momento.",
                    size=13,
                    color=COR_TEXTO_SEC,
                ),
                padding=ft.padding.symmetric(vertical=32),
                alignment=ft.alignment.center,
            )
        else:
            linhas = []
            for a in aptos:
                aid = a["id"]
                freq = int(a.get("frequencia", 0))
                linha = ft.Container(
                    content=ft.Row(
                        controls=[
                            avatar(a["nome"]),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        a["nome"],
                                        size=13,
                                        weight=ft.FontWeight.W_500,
                                        color=COR_TEXTO,
                                    ),
                                    badge_faixa(a["faixa"], a["graus"]),
                                ],
                                spacing=3,
                                expand=True,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        f"{freq}%",
                                        size=16,
                                        weight=ft.FontWeight.W_500,
                                        color=COR_TEXTO,
                                    ),
                                    ft.Text("frequência", size=11, color=COR_TEXTO_SEC),
                                ],
                                spacing=2,
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                            ),
                            btn(
                                "Ver perfil",
                                on_click=lambda e, i=aid: self.ctx["navegar"](
                                    "perfil_aluno", aluno_id=i
                                ),
                                pequeno=True,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=10),
                    border=ft.border.only(bottom=ft.BorderSide(0.5, COR_BORDA)),
                )
                linhas.append(linha)

            if linhas:
                linhas[-1].border = None

            conteudo = ft.Column(controls=linhas, spacing=0)

        titulo = (
            f"{len(aptos)} aluno{'s' if len(aptos) != 1 else ''} "
            f"apto{'s' if len(aptos) != 1 else ''} para graduação"
            if aptos
            else "Aptos para graduação"
        )

        return ft.Column(
            controls=[
                aviso,
                card(
                    ft.Column(
                        controls=[
                            ft.Container(
                                ft.Text(
                                    titulo,
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    color=COR_TEXTO,
                                ),
                                margin=ft.margin.only(bottom=14),
                            ),
                            conteudo,
                        ],
                        spacing=0,
                    )
                ),
            ],
            spacing=0,
            expand=True,
        )