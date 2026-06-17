import flet as ft
from ui.tema import (
    FAIXA_CORES, STATUS_CORES, STATUS_LABELS,
    COR_FUNDO, COR_FUNDO_SEC, COR_BORDA, COR_BORDA_FORTE,
    COR_TEXTO, COR_TEXTO_SEC, COR_TEXTO_HINT, COR_PRIMARIA,
    COR_SUCESSO_BG, COR_SUCESSO_TXT,
    COR_AVISO_BG, COR_AVISO_TXT,
    COR_PERIGO_BG, COR_PERIGO_TXT,
    RAIO, RAIO_LG,
)


def card(conteudo, padding=16, margem_baixo=0):
    return ft.Container(
        content=conteudo,
        bgcolor=COR_FUNDO,
        border=ft.border.all(0.5, COR_BORDA),
        border_radius=RAIO_LG,
        padding=padding,
        margin=ft.margin.only(bottom=margem_baixo),
    )


def secao_header(titulo, acoes=None):
    linha = ft.Row(
        controls=[
            ft.Text(titulo, size=14, weight=ft.FontWeight.W_500, color=COR_TEXTO),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    if acoes:
        linha.controls.append(ft.Row(controls=acoes, spacing=8))
    return ft.Container(content=linha, margin=ft.margin.only(bottom=14))


def badge_faixa(faixa, graus=0):
    cores = FAIXA_CORES.get(faixa, {"bg": "#F1EFE8", "texto": "#444441"})
    graus_str = " " + "●" * graus if graus > 0 else ""
    return ft.Container(
        content=ft.Text(
            f"{faixa}{graus_str}",
            size=11,
            weight=ft.FontWeight.W_500,
            color=cores["texto"],
        ),
        bgcolor=cores["bg"],
        border_radius=10,
        padding=ft.padding.symmetric(horizontal=8, vertical=2),
    )


def badge_status(status):
    cores = STATUS_CORES.get(status, STATUS_CORES["AUSENTE"])
    label = STATUS_LABELS.get(status, status)
    return ft.Container(
        content=ft.Text(label, size=11, weight=ft.FontWeight.W_500, color=cores["texto"]),
        bgcolor=cores["bg"],
        border=ft.border.all(0.5, cores["borda"]),
        border_radius=10,
        padding=ft.padding.symmetric(horizontal=8, vertical=2),
    )


def badge_ativo(ativo: bool):
    if ativo:
        return ft.Container(
            content=ft.Text("Ativo", size=11, weight=ft.FontWeight.W_500, color="#085041"),
            bgcolor="#E1F5EE",
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=8, vertical=2),
        )
    return ft.Container(
        content=ft.Text("Inativo", size=11, weight=ft.FontWeight.W_500, color="#444441"),
        bgcolor="#F1EFE8",
        border_radius=10,
        padding=ft.padding.symmetric(horizontal=8, vertical=2),
    )


def avatar(nome, tamanho=36, font_size=13):
    iniciais = "".join(p[0].upper() for p in nome.split()[:2])
    return ft.Container(
        content=ft.Text(iniciais, size=font_size, weight=ft.FontWeight.W_500, color=COR_TEXTO_SEC),
        width=tamanho,
        height=tamanho,
        bgcolor=COR_FUNDO_SEC,
        border_radius=tamanho // 2,
        alignment=ft.alignment.center,
    )


def stat_card(label, valor):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(label, size=11, color=COR_TEXTO_SEC),
                ft.Text(str(valor), size=22, weight=ft.FontWeight.W_500, color=COR_TEXTO),
            ],
            spacing=3,
        ),
        bgcolor=COR_FUNDO_SEC,
        border_radius=RAIO,
        padding=14,
        expand=True,
    )


def barra_frequencia(pct: int, largura=90):
    return ft.Row(
        controls=[
            ft.Container(
                content=ft.Container(
                    bgcolor=COR_PRIMARIA,
                    border_radius=4,
                    width=(largura * pct / 100),
                    height=8,
                ),
                bgcolor=COR_FUNDO_SEC,
                border_radius=4,
                width=largura,
                height=8,
            ),
            ft.Text(f"{pct}%", size=12, color=COR_TEXTO_SEC),
        ],
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def barra_horizontal(label, valor, max_valor, sufixo=""):
    pct = int(valor / max_valor * 100) if max_valor > 0 else 0
    return ft.Row(
        controls=[
            ft.Container(
                ft.Text(label, size=12, color=COR_TEXTO_SEC, text_align=ft.TextAlign.RIGHT),
                width=70,
            ),
            ft.Container(
                content=ft.Container(
                    bgcolor=COR_PRIMARIA,
                    border_radius=4,
                    width=pct * 2.2,
                    height=8,
                ),
                bgcolor=COR_FUNDO_SEC,
                border_radius=4,
                expand=True,
                height=8,
            ),
            ft.Container(
                ft.Text(f"{valor}{sufixo}", size=12, color=COR_TEXTO_SEC),
                width=36,
            ),
        ],
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def alerta(mensagem, tipo="sucesso"):
    cores = {
        "sucesso": (COR_SUCESSO_BG, COR_SUCESSO_TXT, "#5DCAA5"),
        "aviso":   (COR_AVISO_BG,   COR_AVISO_TXT,   "#EF9F27"),
        "perigo":  (COR_PERIGO_BG,  COR_PERIGO_TXT,  "#E24B4A"),
    }
    bg, txt, borda = cores.get(tipo, cores["sucesso"])
    return ft.Container(
        content=ft.Text(mensagem, size=13, color=txt),
        bgcolor=bg,
        border=ft.border.all(0.5, borda),
        border_radius=RAIO,
        padding=ft.padding.symmetric(horizontal=14, vertical=10),
        margin=ft.margin.only(bottom=14),
    )


def campo(label, control):
    return ft.Column(
        controls=[
            ft.Text(label, size=11, weight=ft.FontWeight.W_500, color=COR_TEXTO_SEC),
            control,
        ],
        spacing=4,
        expand=True,
    )


def input_texto(hint="", valor="", on_change=None, multiline=False, min_lines=1):
    return ft.TextField(
        value=valor,
        hint_text=hint,
        hint_style=ft.TextStyle(color=COR_TEXTO_HINT, size=13),
        text_style=ft.TextStyle(color=COR_TEXTO, size=13),
        border_color=COR_BORDA,
        focused_border_color=COR_BORDA_FORTE,
        border_radius=RAIO,
        bgcolor=COR_FUNDO,
        content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
        on_change=on_change,
        multiline=multiline,
        min_lines=min_lines,
        max_lines=4 if multiline else 1,
    )


def input_data(valor="", on_change=None):
    return ft.TextField(
        value=valor,
        hint_text="AAAA-MM-DD",
        hint_style=ft.TextStyle(color=COR_TEXTO_HINT, size=13),
        text_style=ft.TextStyle(color=COR_TEXTO, size=13),
        border_color=COR_BORDA,
        focused_border_color=COR_BORDA_FORTE,
        border_radius=RAIO,
        bgcolor=COR_FUNDO,
        content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
        on_change=on_change,
    )


def dropdown(opcoes, valor=None, on_change=None):
    return ft.Dropdown(
        value=valor or (opcoes[0] if opcoes else None),
        options=[ft.dropdown.Option(o) for o in opcoes],
        border_color=COR_BORDA,
        focused_border_color=COR_BORDA_FORTE,
        border_radius=RAIO,
        bgcolor=COR_FUNDO,
        text_style=ft.TextStyle(color=COR_TEXTO, size=13),
        content_padding=ft.padding.symmetric(horizontal=10, vertical=4),
        on_change=on_change,
    )


def btn(texto, on_click=None, icone=None, primario=False, perigo=False, pequeno=False):
    if primario:
        bg, txt, borda = COR_PRIMARIA, "#FFFFFF", COR_PRIMARIA
    elif perigo:
        bg, txt, borda = COR_PERIGO_BG, COR_PERIGO_TXT, "#E24B4A"
    else:
        bg, txt, borda = COR_FUNDO, COR_TEXTO, COR_BORDA

    pad = ft.padding.symmetric(horizontal=10, vertical=4) if pequeno else ft.padding.symmetric(horizontal=14, vertical=7)
    font_size = 12 if pequeno else 13

    controles = []
    if icone:
        controles.append(ft.Icon(icone, size=15, color=txt))
    controles.append(ft.Text(texto, size=font_size, color=txt, weight=ft.FontWeight.W_400))

    return ft.Container(
        content=ft.Row(controles, spacing=5, tight=True),
        bgcolor=bg,
        border=ft.border.all(0.5, borda),
        border_radius=RAIO,
        padding=pad,
        on_click=on_click,
        ink=True,
    )


def divisor():
    return ft.Container(
        bgcolor=COR_BORDA,
        height=0.5,
        margin=ft.margin.symmetric(vertical=14),
    )