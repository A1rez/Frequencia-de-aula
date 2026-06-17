import flet as ft

# Paleta de faixas
FAIXA_CORES = {
    "Branca":  {"bg": "#F1EFE8", "texto": "#444441"},
    "Cinza/ranco":   {"bg": "#B4B2A9", "texto": "#F1EFE8"},
    "Cinza":   {"bg": "#B4B2A9", "texto": "#2C2C2A"},
    "Cinza/Preto":   {"bg": "#B4B2A9", "texto": "#000000"},
    "Amarela": {"bg": "#FAC775", "texto": "#633806"},
    "Amarela/Preto": {"bg": "#FAC775", "texto": "#000000"},
    "Laranja": {"bg": "#F0997B", "texto": "#4A1B0C"},
    "Laranja/Preto": {"bg": "#F0997B", "texto": "#000000"},
    "Verde":   {"bg": "#5DCAA5", "texto": "#04342C"},
    "Azul":    {"bg": "#378ADD", "texto": "#042C53"},
    "Roxa":    {"bg": "#7F77DD", "texto": "#26215C"},
    "Marrom":  {"bg": "#854F0B", "texto": "#FAC775"},
    "Preta":   {"bg": "#2C2C2A", "texto": "#D3D1C7"},
}

FAIXAS = list(FAIXA_CORES.keys())

# Status de presença
STATUS_CORES = {
    "PRESENTE":    {"bg": "#EAF3DE", "texto": "#27500A", "borda": "#5DCAA5"},
    "AUSENTE":     {"bg": "#FCEBEB", "texto": "#791F1F", "borda": "#E24B4A"},
    "JUSTIFICADO": {"bg": "#FAEEDA", "texto": "#633806", "borda": "#EF9F27"},
}

STATUS_LABELS = {
    "PRESENTE":    "Presente",
    "AUSENTE":     "Ausente",
    "JUSTIFICADO": "Justificado",
}

DIAS_PT = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
MESES   = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
           "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

# Cores base
COR_FUNDO        = "#FFFFFF"
COR_FUNDO_SEC    = "#F5F5F3"
COR_BORDA        = "#E0DED8"
COR_BORDA_FORTE  = "#C0BEB8"
COR_TEXTO        = "#1A1A1A"
COR_TEXTO_SEC    = "#6B6B68"
COR_TEXTO_HINT   = "#9B9B98"
COR_PRIMARIA     = "#1A1A1A"
COR_SIDEBAR      = "#FAFAF8"
COR_DESTAQUE     = "#1A1A1A"

COR_SUCESSO_BG   = "#EAF3DE"
COR_SUCESSO_TXT  = "#27500A"
COR_AVISO_BG     = "#FAEEDA"
COR_AVISO_TXT    = "#633806"
COR_PERIGO_BG    = "#FCEBEB"
COR_PERIGO_TXT   = "#791F1F"
COR_INFO_BG      = "#E6F1FB"
COR_INFO_TXT     = "#042C53"

RAIO = 8
RAIO_LG = 12