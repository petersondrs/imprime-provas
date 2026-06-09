# Imprime Provas

Ferramenta para criar e imprimir provas (exames) de forma simples, a partir de um
roteiro em texto. Pensada para professores — sem necessidade de programar.

Há **duas formas de usar**, que compartilham o mesmo formato de conteúdo:

## 1. Editor no navegador (recomendado) — `Imprime-Provas.html`

Dois cliques no arquivo `Imprime-Provas.html` abrem um editor com **pré-visualização
ao vivo** de uma folha A4 e botão **Imprimir** (salva em PDF pela impressão do navegador).

- Digite/cole o roteiro à esquerda e veja a prova montada à direita.
- O **gabarito** vem no mesmo roteiro e é impresso em **folha separada**.
- **Matemática** em LaTeX entre cifrões: `$\sqrt{16}$`, `$\frac{3}{4}$`.
- Botão **Exemplo de prompt**: gera o prompt pronto para o Gemini criar o conteúdo.
- Botões **Quebra de página** e **Inserir linha** para ajustar o layout.
- Ajustes: cor de destaque, tamanho do texto e linhas das discursivas.

## 2. Gerador em PDF (lote) — `gerar.command` + `motor_provas.py`

Lê os arquivos `.md` da pasta `conteudo/` e gera **um PDF** na pasta `provas/`, com
as provas primeiro e o gabarito comentado no final, em páginas separadas.

- Dois cliques em `gerar.command` (macOS).
- Usa `reportlab` (PDF) e `matplotlib` (fórmulas) — instalados automaticamente na 1ª vez.

## Formato do conteúdo

```markdown
# Matéria - V1

## Múltipla Escolha

**1.** Enunciado da questão, com fórmula como $\sqrt{25}$?
- A) alternativa
- B) alternativa
- C) alternativa
- D) alternativa
> Correta: C
> Comentário: explicação da resposta.

## Discursivas

**2.** Pergunta discursiva.
> Resposta: resposta esperada.
```

Veja **`PROMPT_GEMINI.md`** para o prompt que gera esse formato automaticamente, e
**`LEIA-ME.md`** para o passo a passo de uso.

## Estrutura

| Caminho | Para que serve |
|---|---|
| `Imprime-Provas.html` | Editor no navegador + impressão |
| `motor_provas.py` | Motor que gera o PDF em lote |
| `gerar.command` | Atalho de dois cliques (macOS) para o motor |
| `conteudo/` | Roteiros das provas em `.md` |
| `provas/` | PDFs gerados (não versionados) |
| `PROMPT_GEMINI.md` | Prompt pronto para o Gemini |
| `LEIA-ME.md` | Manual de uso |
| `design_handoff_imprime_provas/` | Referência de design da interface |
