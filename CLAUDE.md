# CLAUDE.md — Imprime Provas

Contexto completo do projeto para novas sessões do Claude Code.

---

## O que é este projeto

**Imprime Provas** é uma ferramenta para professores criarem, pré-visualizarem e imprimirem provas escolares. O usuário (Peterson) **não é programador** — toda solução deve ser de dois cliques, sem terminal no dia a dia.

O conteúdo das provas é gerado pelo **Gemini / NotebookLM** (com livros e provas anteriores como fontes) e colado no editor. O app monta a prova formatada com gabarito em folha separada.

**Repositório GitHub:** `git@github.com:petersondrs/imprime-provas.git` — branch `main`.

---

## Dois modos de uso

| Arquivo | Como usar | Tecnologia |
|---|---|---|
| `Imprime-Provas.html` | Duplo clique → abre no navegador | HTML/CSS/JS puro, sem build |
| `gerar.command` + `motor_provas.py` | Duplo clique no macOS | Python, reportlab, matplotlib |

O arquivo HTML é o modo principal. O Python é legado/lote.

---

## Estrutura de arquivos

```
Imprime-Provas.html   ← app principal (single-file, sem dependências locais)
motor_provas.py       ← gerador PDF em Python (modo lote)
gerar.command         ← launcher macOS para o motor Python
PROMPT_GEMINI.md      ← prompt template completo para o NotebookLM
conteudo/             ← arquivos .md usados pelo motor Python
provas/               ← PDFs gerados (ignorados pelo git)
LEIA-ME.md            ← manual de uso para o professor
README.md             ← página do repositório GitHub
design_handoff_imprime_provas/ ← referência de design original
```

---

## Formato do roteiro (Markdown)

Este é o formato que o parser entende. O Gemini é instruído a gerar exatamente assim.

```markdown
# Matéria - V1

## Múltipla Escolha

**1.** Enunciado da questão, com fórmula opcional: $\sqrt{25}$?
- A) Primeira alternativa.
- B) Segunda alternativa.
- C) Alternativa correta.
- D) Quarta alternativa.
> Correta: C
> Comentário: Explicação curta da resposta.

## Discursivas

**2.** Enunciado da questão discursiva.
> Resposta: Resposta esperada.

[quebra de página]

# Matéria - V2

...
```

### Regras críticas do parser (não quebre isso)

| Elemento | Formato obrigatório | Por quê |
|---|---|---|
| Questão | `**1.**` ou `**2)**` — **com negrito** | Sem negrito, `1.` é tratado como sub-item de lista |
| Alternativa | `- A)` — **com hífen-espaço** | Sem hífen, `a)` é tratado como sub-item de lista |
| Gabarito múltipla | `> Correta: C` | Parser extrai só a letra |
| Comentário | `> Comentário: texto` | Vai para a página de gabarito |
| Discursiva | `> Resposta: texto` | Vai para a página de gabarito |
| Quebra de página | `[quebra de página]` | Vira `break-after: page` no print |
| Linha horizontal | `---` | Renderiza `<hr>` |
| Fórmulas | `$\sqrt{x}$` (LaTeX inline) | MathJax no HTML, matplotlib no Python |
| Sub-itens de lista | `1. item`, `a) item`, `( ) item` | Renderizam em linhas separadas (não viram opções) |

### Múltiplos simulados

O usuário cola a resposta inteira do Gemini (V1 + V2 + V3 ...) de uma vez. A função `splitSimulados()` divide pelo marcador `# Título` (um `#` simples). O app renderiza todas as provas primeiro, depois todos os gabaritos, separados por marcadores de quebra de página.

---

## Arquitetura do HTML (Imprime-Provas.html)

Single-file sem build. Tudo inline.

### Design tokens (CSS vars)
```css
--pine:      #297373   /* verde-azulado, botão "Exemplo de prompt" */
--coral:     #FF8552   /* laranja, botão "Gerar Prompt", bordas tool-btn */
--alabaster: #E3E3E3
--ink:       #010400
--serif:     'Baskervville', Georgia, serif
```

### Principais funções JS

| Função | O que faz |
|---|---|
| `parseExam(src)` | Converte string Markdown → objeto `{title, blocks[]}` |
| `splitSimulados(src)` | Divide roteiro com múltiplos simulados pelo `# Título` |
| `renderProva(doc)` | Gera HTML da prova (questões + opções) |
| `renderGabarito(doc)` | Gera HTML do gabarito (respostas) |
| `renderAll()` | Monta tudo em `.paper` único com separadores de quebra |
| `fmt(s)` | Formata texto: `\n`→`<br>`, `**bold**`, `*italic*`, protege fórmulas `$...$` |
| `buildGerarPrompt()` | Monta prompt preenchido a partir do modal "Gerar Prompt" |
| `insertToken(token)` | Insere texto na posição do cursor no textarea |

### localStorage
- `ip_script` — roteiro atual do editor
- `ip_tweaks` — configurações (cor, tamanho de texto, linhas discursiva)

### Botões da interface

**Header:**
- `Gerar Prompt` (laranja/coral) — abre modal para montar prompt preenchido
- `Exemplo de prompt` (verde/pine) — exibe o template raw para referência
- `Ajustes` (ícone gear) — cor de destaque, tamanho do texto, linhas discursiva

**Barra de ferramentas (abaixo do textarea):**
- `Quebra de página` — insere `[quebra de página]` na posição do cursor
- `Inserir linha` — insere `---`
- `Quebra de linha` — insere `\n`

**Preview:**
- `Imprimir` — abre diálogo de impressão (salvar como PDF via navegador)

### Modal "Gerar Prompt"

Campos do formulário e o que substituem no prompt:

| Campo | Substitui no prompt |
|---|---|
| Conteúdo da prova (obrigatório) | `"CONTEÚDO AQUI"` |
| Tipo (select: Prova/Teste/Simulado/Exercícios) | `PROVA ou TESTE` |
| Etapa (texto) | `ETAPA X` |
| N de simulados (número) | `Gere QUANTIDADE simulados` e `Qtd. de simulados: QUANTIDADE` |
| Fontes NotebookLM (vírgula) | `"Etapa ETAPA - TIPO MATÉRIA (ANO).pdf"` |

Os demais `QUANTIDADE` (nº de questões), `ASSUNTO`, `ANO/SÉRIE` permanecem em maiúsculas para o professor preencher manualmente no Gemini.

---

## Fluxo de uso do professor (dia a dia)

1. Recebe o conteúdo que cairá na próxima prova
2. Abre `Imprime-Provas.html` → clica **Gerar Prompt**
3. Preenche o modal (conteúdo, tipo, etapa, fontes) → **Copiar prompt**
4. Cola no **NotebookLM** (que tem os livros e provas anteriores como fontes)
5. Cola a resposta no editor → visualiza a prova montada ao vivo
6. Ajusta com os botões de quebra de página/linha se necessário
7. Clica **Imprimir** → salva como PDF

### Convenção de nome de arquivo das provas anteriores

```
Etapa 2 - Prova Historia (2025).pdf
Etapa 3 - Teste Matematica (2024).pdf
```

O prompt instrui o Gemini a buscar arquivos com esse padrão nas fontes para analisar o estilo do professor.

---

## Prompt do Gemini (PROMPT_GEMINI.md)

O prompt existe em **dois lugares** — sempre atualizar os dois juntos:
1. `PROMPT_GEMINI.md` — arquivo standalone para referência
2. `const PROMPT_EXEMPLO` no `Imprime-Provas.html` — usado pelo modal e botão "Exemplo de prompt"

O prompt faz duas etapas antes de gerar:
1. **Verificação de conteúdo**: confirma se o assunto pedido existe nas fontes
2. **Análise de anos anteriores**: busca provas anteriores nas fontes para replicar o estilo do professor (formato, verbos de comando, pontuação por questão)

---

## Motor Python (motor_provas.py)

Lê arquivos `.md` da pasta `conteudo/`, gera PDF em `provas/` com `reportlab`. Fórmulas LaTeX são renderizadas como imagens PNG via `matplotlib` e embutidas no PDF.

Função equivalente ao `fmt()` do JS: `_escapar()` em `motor_provas.py` — mantê-las sincronizadas quando houver mudanças de formatação (negrito, itálico, etc.).

---

## Regras para futuras sessões

1. **Alterações no parser** (questões, alternativas, formatação): atualizar `Imprime-Provas.html` **e** `motor_provas.py`.
2. **Alterações no prompt**: atualizar `PROMPT_GEMINI.md` **e** `const PROMPT_EXEMPLO` no HTML.
3. **Sempre commitar e fazer push** ao final de cada conjunto de mudanças.
4. **Nunca exigir terminal do Peterson** para uso normal — qualquer operação nova deve ser de dois cliques.
5. **Testar no navegador** após mudanças no HTML antes de declarar pronto.
6. **Sintaxe JS**: rodar `node -e "..."` para verificar o bloco `<script>` antes do commit.
