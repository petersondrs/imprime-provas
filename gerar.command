#!/bin/bash
# =====================================================================
#  GERAR PROVAS  ->  De dois cliques neste arquivo para criar o PDF.
# =====================================================================

# Vai para a pasta onde este arquivo esta
cd "$(dirname "$0")" || exit 1

echo "Preparando o ambiente (so demora na primeira vez)..."

# Garante que as ferramentas necessarias estao instaladas
python3 -c "import reportlab" 2>/dev/null || python3 -m pip install --user reportlab
python3 -c "import matplotlib" 2>/dev/null || python3 -m pip install --user matplotlib

# Gera o PDF
python3 motor_provas.py

# Abre a pasta com os PDFs prontos
open provas 2>/dev/null

echo ""
echo "Pode fechar esta janela. (ou pressione ENTER)"
read -r _
