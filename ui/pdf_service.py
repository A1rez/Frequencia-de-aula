import flet as ft
import os
import sqlite3
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

VERDE  = colors.HexColor("#27500A")
FUNDO_VERDE = colors.HexColor("#EAF3DE")
VERMELHO = colors.HexColor("#791F1F")
FUNDO_VERM = colors.HexColor("#FCEBEB")
AMARELO = colors.HexColor("#633806")
FUNDO_AMAR = colors.HexColor("#FAEEDA")
CINZA   = colors.HexColor("#6B6B68")
ESCURO  = colors.HexColor("#1A1A1A")
BORDA   = colors.HexColor("#E0DED8")

MESES = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

styles = getSampleStyleSheet()
titulo_style  = ParagraphStyle("titulo",  parent=styles["Normal"], fontSize=18, textColor=ESCURO, spaceAfter=4)
subtit_style  = ParagraphStyle("subtit",  parent=styles["Normal"], fontSize=10, textColor=CINZA,  spaceAfter=16)
secao_style   = ParagraphStyle("secao",   parent=styles["Normal"], fontSize=12, textColor=ESCURO, spaceBefore=14, spaceAfter=6, fontName="Helvetica-Bold")
normal_style  = ParagraphStyle("normal",  parent=styles["Normal"], fontSize=9,  textColor=ESCURO)
pequeno_style = ParagraphStyle("pequeno", parent=styles["Normal"], fontSize=8,  textColor=CINZA)


def _caminho_pdf(nome):
    desktop = os.path.join(os.path.expanduser("~"), r"C:\Users\jeyso\Downloads")
    if not os.path.exists(desktop):
        desktop = os.path.expanduser("~")
    return os.path.join(desktop, nome)


def _notificar(page, msg, sucesso=True):
    snack = ft.SnackBar(
        content=ft.Text(msg, color="#FFFFFF"),
        bgcolor="#27500A" if sucesso else "#791F1F",
        open=True,
    )
    page.overlay.append(snack)
    page.update()


def gerar_pdf_relatorio(stats, ranking, por_dia, meses_dados, idade_media, page):
    try:
        from app.relatorio_service import calcular_frequencia_ultimos_90_dias
        caminho = _caminho_pdf(f"relatorio_turma_{date.today()}.pdf")
        doc = SimpleDocTemplate(caminho, pagesize=A4,
                                leftMargin=2*cm, rightMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        story = []

        # Cabeçalho
        story.append(Paragraph("Relatório da Turma", titulo_style))
        story.append(Paragraph(f"Gerado em {date.today().strftime('%d/%m/%Y')}", subtit_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=BORDA, spaceAfter=12))

        # Estatísticas gerais
        story.append(Paragraph("Visão Geral", secao_style))
        dados_stats = [
            ["Alunos ativos", "Frequência média", "Idade média", "Masc. / Fem."],
            [
                str(stats["alunos_ativos"]),
                f"{int(stats['presenca_media'])}%",
                f"{idade_media} anos",
                f"{stats['masculino']}/{stats['feminino']}",
            ],
        ]
        t = Table(dados_stats, colWidths=[4.2*cm]*4)
        t.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#F5F5F3")),
            ("TEXTCOLOR",   (0,0), (-1,0), CINZA),
            ("FONTSIZE",    (0,0), (-1,0), 8),
            ("FONTSIZE",    (0,1), (-1,1), 16),
            ("FONTNAME",    (0,1), (-1,1), "Helvetica-Bold"),
            ("ALIGN",       (0,0), (-1,-1), "CENTER"),
            ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0,1), (-1,1), [colors.white]),
            ("BOX",         (0,0), (-1,-1), 0.5, BORDA),
            ("INNERGRID",   (0,0), (-1,-1), 0.5, BORDA),
            ("TOPPADDING",  (0,0), (-1,-1), 8),
            ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 16))

        # Presença por dia da semana
        story.append(Paragraph("Presença por dia da semana (média de presentes)", secao_style))
        max_dia = max(por_dia.values(), default=1)
        dias_dados = [
            [dia[:3], f"{round(val,1)}", f"{'█' * int(val/max_dia*20)}"]
            for dia, val in por_dia.items()
        ]
        t2 = Table([["Dia", "Média", ""]] + dias_dados, colWidths=[2.5*cm, 2*cm, 12.3*cm])
        t2.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#F5F5F3")),
            ("TEXTCOLOR",    (0,0), (-1,0), CINZA),
            ("FONTSIZE",     (0,0), (-1,-1), 8),
            ("TEXTCOLOR",    (2,1), (2,-1), ESCURO),
            ("ALIGN",        (1,0), (1,-1), "RIGHT"),
            ("BOX",          (0,0), (-1,-1), 0.5, BORDA),
            ("LINEBELOW",    (0,0), (-1,-2), 0.3, BORDA),
            ("TOPPADDING",   (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ]))
        story.append(t2)
        story.append(Spacer(1, 16))

        # Aulas por mês
        story.append(Paragraph("Aulas por mês (últimos 12 meses)", secao_style))
        max_mes = max((v for _, v in meses_dados), default=1)
        meses_rows = [
            [MESES[int(m.split("-")[1])-1] + "/" + m.split("-")[0][2:],
             str(v),
             f"{'█' * int(v/max_mes*20)}"]
            for m, v in meses_dados
        ]
        t3 = Table([["Mês", "Aulas", ""]] + meses_rows, colWidths=[2.5*cm, 2*cm, 12.3*cm])
        t3.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#F5F5F3")),
            ("TEXTCOLOR",    (0,0), (-1,0), CINZA),
            ("FONTSIZE",     (0,0), (-1,-1), 8),
            ("ALIGN",        (1,0), (1,-1), "RIGHT"),
            ("BOX",          (0,0), (-1,-1), 0.5, BORDA),
            ("LINEBELOW",    (0,0), (-1,-2), 0.3, BORDA),
            ("TOPPADDING",   (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ]))
        story.append(t3)
        story.append(Spacer(1, 16))

        # Ranking
        story.append(Paragraph("Ranking de Presença — últimos 90 dias", secao_style))
        ranking_rows = [["#", "Nome", "Faixa", "Presenças", "Justif.", "Faltas", "Freq."]]
        for i, r in enumerate(ranking, 1):
            freq_det = calcular_frequencia_ultimos_90_dias(r["id"])
            ranking_rows.append([
                str(i),
                r["nome"],
                r["faixa"],
                str(freq_det["presencas"]),
                str(freq_det["justificadas"]),
                str(freq_det["faltas"]),
                f"{int(r['frequencia'])}%",
            ])
        t4 = Table(ranking_rows, colWidths=[0.8*cm, 5.5*cm, 2.2*cm, 1.8*cm, 1.5*cm, 1.5*cm, 1.5*cm])
        t4.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#F5F5F3")),
            ("TEXTCOLOR",    (0,0), (-1,0), CINZA),
            ("FONTSIZE",     (0,0), (-1,-1), 8),
            ("ALIGN",        (0,0), (0,-1), "CENTER"),
            ("ALIGN",        (3,0), (-1,-1), "CENTER"),
            ("BOX",          (0,0), (-1,-1), 0.5, BORDA),
            ("LINEBELOW",    (0,0), (-1,-2), 0.3, BORDA),
            ("TOPPADDING",   (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",(0,0), (-1,-1), 5),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#FAFAF8")]),
        ]))
        story.append(t4)

        doc.build(story)
        _notificar(page, f"PDF salvo em: {caminho}")
    except Exception as ex:
        _notificar(page, f"Erro ao gerar PDF: {ex}", sucesso=False)


def gerar_pdf_aptos(aptos, page):
    try:
        caminho = _caminho_pdf(f"aptos_graduacao_{date.today()}.pdf")
        doc = SimpleDocTemplate(caminho, pagesize=A4,
                                leftMargin=2*cm, rightMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        story = []

        story.append(Paragraph("Alunos Aptos para Graduação", titulo_style))
        story.append(Paragraph(f"Gerado em {date.today().strftime('%d/%m/%Y')}", subtit_style))
        story.append(Paragraph(
            "Critérios: ≥ 50% de frequência nos últimos 90 dias e mínimo de 90 dias desde a última graduação.",
            ParagraphStyle("aviso", parent=styles["Normal"], fontSize=9,
                           textColor=AMARELO, backColor=FUNDO_AMAR,
                           borderPadding=8, spaceAfter=16),
        ))
        story.append(HRFlowable(width="100%", thickness=0.5, color=BORDA, spaceAfter=12))

        if not aptos:
            story.append(Paragraph("Nenhum aluno atinge os critérios no momento.", normal_style))
        else:
            rows = [["Nome", "Faixa", "Graus", "Última Graduação", "Frequência"]]
            for a in aptos:
                try:
                    from datetime import datetime
                    grad_fmt = datetime.strptime(
                        a.get("data_ultima_graduacao",""), "%Y-%m-%d"
                    ).strftime("%d/%m/%Y")
                except Exception:
                    grad_fmt = a.get("data_ultima_graduacao", "—")
                rows.append([
                    a["nome"],
                    a["faixa"],
                    str(a["graus"]),
                    grad_fmt,
                    f"{int(a.get('frequencia', 0))}%",
                ])
            t = Table(rows, colWidths=[5.5*cm, 2.5*cm, 1.5*cm, 3.5*cm, 2.8*cm])
            t.setStyle(TableStyle([
                ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#F5F5F3")),
                ("TEXTCOLOR",    (0,0), (-1,0), CINZA),
                ("FONTSIZE",     (0,0), (-1,-1), 9),
                ("ALIGN",        (2,0), (-1,-1), "CENTER"),
                ("BOX",          (0,0), (-1,-1), 0.5, BORDA),
                ("LINEBELOW",    (0,0), (-1,-2), 0.3, BORDA),
                ("TOPPADDING",   (0,0), (-1,-1), 6),
                ("BOTTOMPADDING",(0,0), (-1,-1), 6),
                ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#FAFAF8")]),
            ]))
            story.append(t)
            story.append(Spacer(1, 12))
            story.append(Paragraph(
                f"Total: {len(aptos)} aluno{'s' if len(aptos) != 1 else ''} apto{'s' if len(aptos) != 1 else ''}.",
                pequeno_style,
            ))

        doc.build(story)
        _notificar(page, f"PDF salvo em: {caminho}")
    except Exception as ex:
        _notificar(page, f"Erro ao gerar PDF: {ex}", sucesso=False)