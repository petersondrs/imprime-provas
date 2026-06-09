# -*- coding: utf-8 -*-
# =====================================================================
#  MOTOR DE PROVAS  ->  NAO PRECISA MEXER NESTE ARQUIVO
# ---------------------------------------------------------------------
#  Ele le todos os arquivos .md da pasta "conteudo" e gera um PDF unico
#  na pasta "provas", com as provas primeiro e o gabarito comentado no
#  final, em paginas separadas.
#
#  Como escrever o conteudo: veja o arquivo PROMPT_GEMINI.md e o
#  arquivo de exemplo dentro da pasta "conteudo".
# =====================================================================

import os
import re
import glob
import shutil
import datetime
import unicodedata

# --- Matematica (formulas em LaTeX entre $...$) ---
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Geracao do PDF ---
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.utils import ImageReader

# ---------------------------------------------------------------------
# Pastas do projeto
# ---------------------------------------------------------------------
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_CONTEUDO = os.path.join(PASTA_BASE, "conteudo")
PASTA_SAIDA = os.path.join(PASTA_BASE, "provas")
PASTA_TMP = os.path.join(PASTA_BASE, ".formulas_temp")


# =====================================================================
#  PARTE 1 - LEITURA DOS ARQUIVOS DE CONTEUDO (.md)
# =====================================================================

def _sem_acentos(texto):
    """Deixa o texto minusculo e sem acentos, para comparacoes."""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower().strip()


def _detectar_opcao(linha):
    """Reconhece uma alternativa (A, B, C, D...). Retorna 'A) texto' ou None."""
    m = re.match(r"^[-*]\s*([A-Ea-e])\s*[\)\.\-:]\s*(.*)", linha)
    if m:
        return f"{m.group(1).upper()}) {m.group(2).strip()}"
    m = re.match(r"^([A-Ea-e])\s*[\)\.]\s+(.*)", linha)
    if m:
        return f"{m.group(1).upper()}) {m.group(2).strip()}"
    return None


def _detectar_pergunta(linha):
    """Reconhece o inicio de uma pergunta numerada. Retorna o texto ou None."""
    t = linha.lstrip("*").strip()
    m = re.match(r"^(\d+)\s*[\.\)]\s*(.*)", t)
    if m:
        return m.group(2).strip().lstrip("*").strip()
    return None


def _tratar_meta(linha, atual):
    """Trata linhas que comecam com '>' (Correta / Comentario / Resposta)."""
    if atual is None:
        return
    corpo = linha.lstrip(">").strip()
    if ":" in corpo:
        chave, valor = corpo.split(":", 1)
    else:
        chave, valor = corpo, ""
    chave = _sem_acentos(chave)
    valor = valor.strip()

    if "correta" in chave or "gabarito" in chave:
        letra = re.search(r"[A-Ea-e]", valor)
        atual["r"] = letra.group(0).upper() if letra else valor
    elif "coment" in chave:
        atual["c"] = valor
    elif "resposta" in chave or "espera" in chave:
        atual["resp"] = valor


def carregar_simulado(caminho):
    """Le um arquivo .md e devolve a estrutura de um simulado."""
    with open(caminho, encoding="utf-8") as f:
        linhas = f.readlines()

    nome_arquivo = os.path.splitext(os.path.basename(caminho))[0]
    sim = {"titulo": nome_arquivo, "multiplas": [], "discursivas": []}
    modo = None       # "multipla" ou "discursiva"
    atual = None      # pergunta sendo lida no momento

    def fechar():
        nonlocal atual
        if atual is None:
            return
        if atual["_tipo"] == "discursiva":
            sim["discursivas"].append(atual)
        else:
            sim["multiplas"].append(atual)
        atual = None

    for raw in linhas:
        s = raw.strip()
        if not s:
            continue

        # Titulo principal:  # Titulo
        if s.startswith("#") and not s.startswith("##"):
            sim["titulo"] = s.lstrip("#").strip()
            continue

        # Cabecalho de secao:  ## Multipla Escolha  /  ## Discursivas
        if s.startswith("##"):
            fechar()
            cab = _sem_acentos(s.lstrip("#"))
            if "discurs" in cab:
                modo = "discursiva"
            elif "multip" in cab or "objetiv" in cab or "escolha" in cab:
                modo = "multipla"
            continue

        # Alternativa de multipla escolha
        opcao = _detectar_opcao(s)
        if opcao is not None and atual is not None and atual["_tipo"] == "multipla":
            atual["o"].append(opcao)
            continue

        # Metadados (Correta / Comentario / Resposta)
        if s.startswith(">"):
            _tratar_meta(s, atual)
            continue

        # Inicio de uma nova pergunta
        pergunta = _detectar_pergunta(s)
        if pergunta is not None:
            fechar()
            tipo = modo if modo else "multipla"
            atual = {"_tipo": tipo, "q": pergunta, "o": [],
                     "r": "", "c": "", "resp": ""}
            continue

        # Qualquer outra linha = continuacao do texto da pergunta atual
        if atual is not None:
            atual["q"] += " " + s

    fechar()
    return sim


# =====================================================================
#  PARTE 2 - MATEMATICA: transforma $formula$ em imagem
# =====================================================================

_cache_formulas = {}


def _renderizar_formula(formula):
    """Desenha uma formula LaTeX como imagem PNG e devolve (caminho, larg, alt)."""
    if formula in _cache_formulas:
        return _cache_formulas[formula]

    os.makedirs(PASTA_TMP, exist_ok=True)
    indice = len(_cache_formulas)
    caminho = os.path.join(PASTA_TMP, f"formula_{indice}.png")

    dpi = 300
    fonte = 14
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, f"${formula}$", fontsize=fonte)
    fig.savefig(caminho, dpi=dpi, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)

    px_l, px_a = ImageReader(caminho).getSize()
    # converte pixels -> pontos e ajusta para acompanhar o texto de 10pt
    fator = (72.0 / dpi) * (10.0 / fonte)
    larg = px_l * fator
    alt = px_a * fator

    _cache_formulas[formula] = (caminho, larg, alt)
    return _cache_formulas[formula]


def _escapar(texto):
    """Protege caracteres especiais e converte **negrito** do Markdown."""
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    texto = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texto)   # **negrito**
    texto = re.sub(r"\*(.+?)\*", r"<i>\1</i>", texto)       # *itálico*
    return texto


def montar_texto(texto):
    """Monta o texto final para o PDF, trocando $formula$ por imagens."""
    partes = re.split(r"(\$[^$]*\$)", texto)
    saida = []
    for parte in partes:
        if len(parte) >= 2 and parte.startswith("$") and parte.endswith("$"):
            formula = parte[1:-1].strip()
            if not formula:
                continue
            caminho, larg, alt = _renderizar_formula(formula)
            saida.append(
                f'<img src="{caminho}" width="{larg:.1f}" '
                f'height="{alt:.1f}" valign="middle"/>'
            )
        else:
            saida.append(_escapar(parte))
    return "".join(saida)


# =====================================================================
#  PARTE 3 - MONTAGEM DO PDF
# =====================================================================

def gerar_pdf(simulados, nome_arquivo):
    doc = SimpleDocTemplate(nome_arquivo, pagesize=A4,
                            rightMargin=20, leftMargin=20,
                            topMargin=20, bottomMargin=20)

    titulo_style = ParagraphStyle(name="Titulo", fontName="Helvetica-Bold",
                                  fontSize=14, spaceAfter=13, alignment=TA_LEFT)
    subtitulo_style = ParagraphStyle(name="Subtitulo", fontName="Helvetica-Bold",
                                     fontSize=12, spaceAfter=8, spaceBefore=10)
    pergunta_style = ParagraphStyle(name="Pergunta", fontName="Helvetica-Bold",
                                    fontSize=10, spaceAfter=5, spaceBefore=10,
                                    alignment=TA_JUSTIFY, leading=15)
    opcao_style = ParagraphStyle(name="Opcao", fontName="Helvetica",
                                 fontSize=10, leftIndent=15, spaceAfter=3, leading=14)
    gabarito_style = ParagraphStyle(name="Gabarito", fontName="Helvetica",
                                    fontSize=10, spaceAfter=5,
                                    alignment=TA_JUSTIFY, leading=14)
    label_style = ParagraphStyle(name="Bold", fontName="Helvetica-Bold",
                                 fontSize=11, spaceAfter=5)

    story = []

    # ---- PROVAS ----
    for sim in simulados:
        story.append(Paragraph(montar_texto(sim["titulo"]), titulo_style))
        story.append(Spacer(1, 10))

        numero = 1  # numeracao automatica e continua

        if sim["multiplas"]:
            story.append(Paragraph("PARTE 1: Multipla Escolha", subtitulo_style))
            for m in sim["multiplas"]:
                bloco = [Paragraph(f"{numero}. " + montar_texto(m["q"]), pergunta_style)]
                for op in m["o"]:
                    bloco.append(Paragraph(montar_texto(op), opcao_style))
                bloco.append(Spacer(1, 5))
                story.append(KeepTogether(bloco))
                m["_n"] = numero
                numero += 1
            story.append(Spacer(1, 10))

        if sim["discursivas"]:
            story.append(Paragraph("PARTE 2: Questoes Discursivas", subtitulo_style))
            for d in sim["discursivas"]:
                bloco = [Paragraph(f"{numero}. " + montar_texto(d["q"]), pergunta_style)]
                for _ in range(4):
                    bloco.append(HRFlowable(width="100%", thickness=0.5, spaceAfter=15))
                bloco.append(Spacer(1, 10))
                story.append(KeepTogether(bloco))
                d["_n"] = numero
                numero += 1

        story.append(PageBreak())

    # ---- GABARITO (no final, em paginas separadas) ----
    story.append(Paragraph("GABARITO COMENTADO DOS SIMULADOS", titulo_style))
    story.append(PageBreak())

    for i, sim in enumerate(simulados):
        if i > 0:
            story.append(PageBreak())

        bloco = [Paragraph(montar_texto(sim["titulo"]), subtitulo_style)]

        if sim["multiplas"]:
            bloco.append(Paragraph("Multipla Escolha:", label_style))
            for m in sim["multiplas"]:
                txt = f"<b>{m['_n']}. {m['r']}</b>"
                if m["c"]:
                    txt += " - " + montar_texto(m["c"])
                bloco.append(Paragraph(txt, gabarito_style))

        if sim["discursivas"]:
            bloco.append(Spacer(1, 10))
            bloco.append(Paragraph("Discursivas (Expectativa de Resposta):", label_style))
            for d in sim["discursivas"]:
                txt = f"<b>{d['_n']}.</b> " + montar_texto(d["resp"])
                bloco.append(Paragraph(txt, gabarito_style))

        story.append(KeepTogether(bloco))

    doc.build(story)


# =====================================================================
#  PARTE 4 - PROGRAMA PRINCIPAL
# =====================================================================

def main():
    print("=" * 55)
    print("  GERADOR DE PROVAS EM PDF")
    print("=" * 55)

    if not os.path.isdir(PASTA_CONTEUDO):
        os.makedirs(PASTA_CONTEUDO, exist_ok=True)

    # limpa imagens de formulas de execucoes anteriores
    if os.path.isdir(PASTA_TMP):
        shutil.rmtree(PASTA_TMP, ignore_errors=True)

    arquivos = sorted(glob.glob(os.path.join(PASTA_CONTEUDO, "*.md")))
    if not arquivos:
        print("\n[!] Nenhum arquivo .md encontrado na pasta 'conteudo'.")
        print("    Coloque ali os arquivos das provas (gerados pelo Gemini) e rode de novo.")
        return

    simulados = []
    for caminho in arquivos:
        nome = os.path.basename(caminho)
        try:
            sim = carregar_simulado(caminho)
            qtd = len(sim["multiplas"]) + len(sim["discursivas"])
            print(f"  - Lido: {nome}  ({qtd} questoes)")
            simulados.append(sim)
        except Exception as e:
            print(f"  [!] Problema ao ler '{nome}': {e}")

    if not simulados:
        print("\n[!] Nenhuma prova valida para gerar.")
        return

    os.makedirs(PASTA_SAIDA, exist_ok=True)
    carimbo = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    saida = os.path.join(PASTA_SAIDA, f"Provas_{carimbo}.pdf")

    try:
        gerar_pdf(simulados, saida)
    except Exception as e:
        print(f"\n[!] Erro ao gerar o PDF: {e}")
        return

    print("\n" + "=" * 55)
    print("  PRONTO! PDF gerado com sucesso:")
    print(f"  {saida}")
    print("=" * 55)


if __name__ == "__main__":
    main()
