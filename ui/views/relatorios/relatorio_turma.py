import flet as ft
from datetime import date, timedelta

from app.aluno_service import listar_alunos_ativos, buscar_aluno_por_id
from app.relatorio_service import (
    calcular_frequencia_ultimos_90_dias,
    calcular_estatisticas_turma,
    aulas_por_mes,
    participacao_por_dia_semana,
    listar_ranking_participacao,
)

from ui.tema import (
    COR_FUNDO, COR_FUNDO_SEC, COR_BORDA, COR_TEXTO, COR_TEXTO_SEC,
    COR_PRIMARIA, RAIO, RAIO_LG,
)
from ui.components.widgets import (
    card, stat_card, badge_faixa, avatar,
    barra_horizontal, btn, divisor,
)

MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
         "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


class ViewRelatorioTurma:
    def __init__(self, ctx, **kwargs):
        self.ctx = ctx

    def build(self):
        try:
            stats    = calcular_estatisticas_turma()
            ranking  = listar_ranking_participacao()
            por_dia  = participacao_por_dia_semana()
            por_mes  = aulas_por_mes()
            alunos   = listar_alunos_ativos()
        except Exception as ex:
            return ft.Text(f"Erro ao carregar relatório: {ex}", color=COR_TEXTO_SEC)

        # Idade média
        idades = []
        for a in alunos:
            dado = buscar_aluno_por_id(a["id"])
            nasc = dado["data_nascimento"]
            if nasc:
                try:
                    from datetime import date as d_cls
                    nasc_d = d_cls.fromisoformat(nasc)
                    hoje = d_cls.today()
                    idade = hoje.year - nasc_d.year - ((hoje.month, hoje.day) < (nasc_d.month, nasc_d.day))
                    idades.append(idade)
                except Exception:
                    pass
        idade_media = round(sum(idades) / len(idades)) if idades else 0

        # ── Stats ──────────────────────────────────────────────────────────
        stats_row = ft.Row(
            controls=[
                stat_card("Alunos ativos",      str(stats["alunos_ativos"])),
                stat_card("Frequência média",   f"{int(stats['presenca_media'])}%"),
                stat_card("Idade média",         f"{idade_media} anos"),
                stat_card("Masculino / Feminino", f"{stats['masculino']}/{stats['feminino']}"),
            ],
            spacing=12,
        )

        # ── Frequência por dia ─────────────────────────────────────────────
        max_dia = max(por_dia.values(), default=1)
        barras_dia = ft.Column(
            controls=[
                barra_horizontal(dia[:3], round(val, 1), max_dia)
                for dia, val in por_dia.items()
            ],
            spacing=8,
        )

        # ── Aulas por mês ──────────────────────────────────────────────────
        max_mes = max(por_mes.values(), default=1)
        barras_mes = ft.Column(
            controls=[
                barra_horizontal(
                    MESES[int(mes.split("-")[1]) - 1] + " " + mes.split("-")[0][2:],
                    val, max_mes
                )
                for mes, val in sorted(por_mes.items())[-8:]
            ],
            spacing=8,
        )

        grafs_row = ft.Row(
            controls=[
                card(
                    ft.Column(
                        controls=[
                            ft.Text("Presença por dia da semana",
                                    size=13, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                            ft.Text("Média de alunos presentes (últimos 90 dias)",
                                    size=11, color=COR_TEXTO_SEC),
                            ft.Container(height=12),
                            barras_dia,
                        ],
                        spacing=2,
                    ),
                    padding=16,
                ),
                card(
                    ft.Column(
                        controls=[
                            ft.Text("Aulas por mês",
                                    size=13, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                            ft.Text("Total de aulas registradas por mês",
                                    size=11, color=COR_TEXTO_SEC),
                            ft.Container(height=12),
                            barras_mes,
                        ],
                        spacing=2,
                    ),
                    padding=16,
                ),
            ],
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        # ── Ranking ────────────────────────────────────────────────────────
        ranking_linhas = []
        for i, r in enumerate(ranking, 1):
            linha = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            ft.Text(str(i), size=13, weight=ft.FontWeight.W_500, color=COR_TEXTO_SEC),
                            width=24,
                        ),
                        avatar(r["nome"], tamanho=32, font_size=12),
                        ft.Column(
                            controls=[
                                ft.Text(r["nome"], size=13, color=COR_TEXTO),
                                badge_faixa(r["faixa"], r["graus"]),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Container(
                                bgcolor=COR_PRIMARIA,
                                border_radius=4,
                                width=int(r["frequencia"] * 1.2),
                                height=8,
                            ),
                            bgcolor=COR_FUNDO_SEC,
                            border_radius=4,
                            width=120,
                            height=8,
                        ),
                        ft.Text(f"{int(r['frequencia'])}%", size=13, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(vertical=8, horizontal=0),
                border=ft.border.only(bottom=ft.BorderSide(0.5, COR_BORDA)),
            )
            ranking_linhas.append(linha)

        if ranking_linhas:
            ranking_linhas[-1].border = None

        ranking_card = card(
            ft.Column(
                controls=[
                    ft.Text("Ranking de presença — últimos 90 dias",
                            size=13, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                    ft.Container(height=14),
                    *ranking_linhas,
                ],
                spacing=0,
            )
        )

        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Visão geral da turma", size=14, weight=ft.FontWeight.W_500, color=COR_TEXTO),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    margin=ft.margin.only(bottom=14),
                ),
                stats_row,
                ft.Container(height=16),
                grafs_row,
                ft.Container(height=16),
                ranking_card,
            ],
            spacing=0,
            expand=True,
        )