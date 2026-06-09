# Handoff: Imprime Provas — Gerador de Provas

## Overview
**Imprime Provas** é um editor de provas (exames) com pré-visualização ao vivo e impressão.
O usuário (professor) cola/digita um roteiro em texto simples no painel da esquerda e vê, em
tempo real, uma folha A4 formatada à direita, exatamente como sairá na impressão. Um botão
**Imprimir** gera a saída limpa (apenas a prova, sem a interface).

## About the Design Files
Os arquivos deste pacote (`Imprime Provas.html`, `app.jsx`, `tweaks-panel.jsx`) são
**referências de design criadas em HTML** — um protótipo que demonstra o visual e o
comportamento pretendidos. **Não são código de produção para copiar diretamente.**

A tarefa é **recriar este design no ambiente do seu codebase** (React, Vue, Svelte, etc.),
usando os padrões, componentes e bibliotecas já estabelecidos. Se ainda não existir um
ambiente, escolha o framework mais adequado e implemente lá. O `app.jsx` usa React 18 via
Babel no navegador apenas para fins de protótipo — em produção, use o build do seu projeto.

## Fidelity
**Alta fidelidade (hifi).** Cores, tipografia, espaçamentos e estados finais estão definidos.
Recrie a UI fielmente usando as bibliotecas/padrões do seu codebase. Os valores exatos estão
em **Design Tokens** abaixo.

---

## Layout Geral

Aplicação de altura total da viewport (`height: 100%`), em coluna:

```
┌────────────────────────────────────────────────────────────┐
│ Header (60px)  ▢ Imprime Provas │ Editor de provas...        │
├──────────────────────────┬─────────────────────────────────┤
│ EDITOR (esquerda)        │ PREVIEW PANE (direita)           │
│ grid col: minmax(360px,  │ grid col: 1.18fr                 │
│   0.82fr)                │                                  │
│                          │  ┌─ canvas (scroll, cinza) ──┐   │
│  ROTEIRO   4 questões…    │  │   ┌─ folha A4 (branca) ─┐  │   │
│  ┌────────────────────┐  │  │   │  Prova de História  │  │   │
│  │ <textarea mono>    │  │  │   │  cabeçalho + campos │  │   │
│  │                    │  │  │   │  questões…          │  │   │
│  └────────────────────┘  │  │   └─────────────────────┘  │   │
│  [# Título][## Seção]…   │  └───────────────────────────┘   │
│                          │  Footer(76px): A4·prev  [Imprimir]│
└──────────────────────────┴─────────────────────────────────┘
```

- Workspace: `display:grid; grid-template-columns: minmax(360px, 0.82fr) 1.18fr;`
- Ambos os painéis com `min-height:0` para permitir scroll interno correto.

---

## Screens / Views

### 1. Header (barra superior)
- **Layout:** `display:flex; align-items:center; gap:18px; height:60px; padding:0 26px;`
  fundo branco, borda inferior `1px solid var(--hairline)`.
- **Marca:** quadrado 16×16, `border-radius:4px`, fundo Pine Blue, com anel interno branco
  (`box-shadow: inset 0 0 0 3px rgba(255,255,255,.85), 0 0 0 1px #297373`). Ao lado, nome
  "Imprime Provas" (Baskervville 21px, weight 700, `white-space:nowrap`).
- **Subtítulo:** "Editor de provas para impressão" — 14.5px, itálico, cor muted, separado por
  divisória vertical (`border-left:1px solid hairline; padding-left:18px`).

### 2. Editor (painel esquerdo)
- **Layout:** coluna flex, fundo branco, `border-right:1px solid hairline`,
  `padding:22px 24px 18px`.
- **Cabeçalho do painel:** linha com "ROTEIRO" (16px, 700, uppercase, letter-spacing .04em) à
  esquerda e contador à direita ("N questões · M caracteres", 13px, muted).
- **Textarea (`.script-input`):** ocupa o espaço restante (`flex:1`), `resize:none`,
  `border:1px solid var(--line)`, `border-radius:10px`, fundo `#fcfcfb`, `padding:18px 20px`.
  **Fonte monoespaçada** 13.5px, `line-height:1.7`, `tab-size:2`.
  - **Foco:** borda Pine Blue + `box-shadow: 0 0 0 3px rgba(41,115,115,.12)`.
  - **Placeholder:** cor `#b7b7b6`.
- **Legenda (`.legend`):** chips de sintaxe abaixo do textarea — `display:flex; flex-wrap:wrap;
  gap:7px`. Cada chip: mono 11.5px, fundo `#f0f0ee`, borda hairline, `border-radius:6px`,
  `padding:4px 8px`. Conteúdo: `# Título`, `## Seção`, `Campo: valor`, `1. Questão`,
  `a) Alternativa`.

### 3. Preview Pane (painel direito)
- **Layout:** coluna flex, fundo Alabaster Grey (`#e3e3e3`).
- **Canvas (`.canvas`):** área de scroll (`overflow:auto`), `padding:38px 0 46px`,
  centraliza a folha (`display:flex; justify-content:center; align-items:flex-start`).
- **Folha A4 (`.paper`):** `width:210mm; max-width:calc(100% - 64px); min-height:297mm`,
  fundo branco, `padding:22mm 20mm 24mm`, `font-size:11pt; line-height:1.55`,
  cor texto `#111`, sombra `0 1px 2px rgba(0,0,0,.08), 0 18px 44px rgba(0,0,0,.16)`.
- **Footer (`.preview-footer`):** `height:76px; padding:0 30px`, fundo branco,
  `border-top:1px solid hairline`, `display:flex; justify-content:space-between; align-items:center`.
  - Esquerda: tag "A4 · Pré-visualização" (13px, muted).
  - Direita: **botão Imprimir** (ver Componentes).

### Componentes dentro da folha A4

**Cabeçalho da prova (`.pp-head`)** — `border-bottom:1.5px solid #111; padding-bottom:14px; margin-bottom:22px`:
- **Título** (`.pp-title`): `font-size:1.85em`, weight 700, `text-align:center`.
- **Meta** (`.pp-meta`): bloco centralizado, `font-size:0.92em`, `line-height:1.5`, cor `#333`.
  Cada item é `inline-block`, `margin:0 11px`, com rótulo em **negrito** ("Disciplina:", "Professor:" etc.).
- **Campos do aluno** (`.pp-fields`, opcional): `display:flex; align-items:flex-end; gap:18px`.
  - Cada campo: rótulo (0.88em, `#333`, `nowrap`) + linha de preenchimento (`border-bottom:1px solid #999; height:1.1em`). O campo "Nome" cresce (`flex:1`); os demais têm largura ~90px.
  - **Caixa de Nota** (opcional): rótulo + caixa `64×42px`, `border:1.5px solid #111; border-radius:3px`.

**Seção (`.pp-section`)** — `## Texto`:
- `font-size:1.05em`, weight 700, uppercase, letter-spacing .05em, cor `#111`,
  `border-left:3px solid var(--accent); padding-left:10px; margin:26px 0 12px`.

**Parágrafo de instrução (`.pp-text`)** — texto solto antes/entre questões:
- `color:#333; font-style:italic; margin:0 0 10px`.

**Questão (`.pp-q`)** — `margin:0 0 20px; break-inside:avoid`:
- **Enunciado (`.pp-q-stmt`):** `display:grid; grid-template-columns:auto 1fr; column-gap:9px; align-items:baseline`.
  - Número (`.pp-q-num`): weight 700, **cor = var(--accent)**.
  - Texto: `text-wrap:pretty`.
- **Alternativas (`.pp-opts`):** `<ol>` sem marcador, `padding-left:26px; display:flex; flex-direction:column; gap:6px`.
  - Cada `<li>`: `display:grid; grid-template-columns:1.5em 1fr; column-gap:6px; align-items:baseline`.
  - Marcador (`.pp-opt-mark`): letra "a)" "b)"… em weight 700.
- **Linhas de resposta (`.pp-lines`)** — para questões discursivas (sem alternativas):
  `padding-left:26px`, N linhas (`.pp-line`: `height:1.75em; border-bottom:1px solid #c7c7c7`).
  N é configurável (padrão 4).

> ⚠️ **Nota de implementação importante:** o layout de alternativas e enunciado usa **CSS Grid**
> (não flex). Flex com `align-items:baseline` faz itens multilinha **não crescerem em altura**,
> causando sobreposição de texto. Use grid `auto 1fr` para o enunciado e `1.5em 1fr` para as
> alternativas.

**Botão Imprimir (`.btn-print`)**:
- `display:inline-flex; align-items:center; gap:10px; padding:13px 28px; border-radius:10px; border:none`.
- Texto Baskervville 17px, weight 700, letter-spacing .02em, cor **branca**.
- Fundo = **var(--accent)** (padrão Coral Glow `#FF8552`). Ícone de impressora (SVG stroke branco, 18×18).
- Sombra: `0 2px 8px rgba(255,133,82,.32)`.
- **Hover:** `filter:brightness(1.04)`, sombra mais forte `0 4px 14px rgba(255,133,82,.42)`.
- **Active:** `transform:translateY(1px)`.
- **Ação:** `window.print()`.

---

## Interactions & Behavior
- **Edição ao vivo:** cada alteração no textarea re-parseia o roteiro e re-renderiza a folha imediatamente (estado controlado).
- **Contador:** nº de questões e de caracteres atualizam em tempo real no cabeçalho do editor.
- **Persistência:** o roteiro é salvo em `localStorage` (`ip_script`) a cada mudança e recarregado ao abrir. Se não houver nada salvo, carrega um roteiro de exemplo.
- **Imprimir:** chama `window.print()`. CSS de impressão esconde header, editor, footer e painel de tweaks; a folha ocupa a página inteira sem sombra/padding; `@page { size:A4; margin:16mm 15mm }`.
- **Sem alternativas → discursiva:** se uma questão não tem linhas `a)`/`b)`…, são renderizadas linhas em branco para resposta.
- **Estado vazio:** se o roteiro não gera blocos, a folha mostra "Cole o roteiro da prova à esquerda para visualizar aqui." (itálico, cinza, centralizado).

## Sintaxe do roteiro (parser)
O parser converte texto simples em estrutura. Regras (todas case-insensitive nos delimitadores):

| Sintaxe | Vira | Regex (referência) |
|---|---|---|
| `# Texto` (1ª no preâmbulo) | Título da prova | `^#\s+(.*)` |
| `## Texto` ou mais # | Seção | `^#{2,}\s+(.*)` |
| `Campo: valor` (antes da 1ª questão) | Item de meta (cabeçalho) | `^([^:]{2,40}):\s*(.+)$` |
| `1. Texto` / `1) Texto` / `1 - Texto` | Nova questão | `^\(?(\d+)\s*[.)\-]\s+(.*)` |
| `a) Texto` / `b. Texto` / `(c) Texto` | Alternativa (sob a questão atual) | `^\(?([a-eA-E])\s*[.)\-]\s+(.*)` |
| Linha solta após questão | Continuação do enunciado | — |
| Linha solta no preâmbulo (sem `:`) | Parágrafo de instrução | — |

- Questões são **renumeradas sequencialmente** na renderização (o número do texto é ignorado para a numeração exibida).
- Linhas em branco são ignoradas (apenas separadores).
- A estrutura de saída: `{ title, meta:[{key,value}], blocks:[…] }`, onde cada block é
  `{type:'section', text}` | `{type:'text', text}` | `{type:'question', statement, options:[string]}`.

## State Management
- `script: string` — conteúdo do textarea (fonte única da verdade; sincronizado com localStorage).
- `t` (tweaks) — objeto de configuração (ver Tweaks). Persistido pelo painel.
- Derivados (memoizados a partir de `script`): documento parseado, contagem de questões.
- A folha NÃO mantém estado próprio — é função pura de `(script, tweaks)`.

## Tweaks / Configurações (painel de ajustes)
No protótipo, um painel flutuante expõe controles. No seu app, exponha como preferências ou props:
- `accent` (cor de destaque): padrão `#FF8552`. Opções sugeridas: `#FF8552`, `#297373`, `#39393A`, `#010400`. Afeta número da questão, borda da seção e botão Imprimir.
- `paperScale` (tamanho do texto da folha): 0.85–1.3, passo 0.05, padrão 1. Aplicado como `font-size:{n}em` na `.paper`.
- `showFields` (campos do aluno): bool, padrão true.
- `showGrade` (caixa de nota): bool, padrão true.
- `answerLines` (linhas p/ discursivas): 2–8, padrão 4.

---

## Design Tokens

### Cores (paleta da marca)
| Token | Hex | Uso |
|---|---|---|
| Black | `#010400` | Texto principal (`--ink`) |
| Pine Blue | `#297373` | Marca, foco de inputs, opção de accent |
| Coral Glow | `#FF8552` | Accent padrão / CTA Imprimir |
| Alabaster Grey | `#E3E3E3` | Fundo do canvas de pré-visualização |
| Graphite | `#39393A` | Texto secundário / opção de accent |

### Tokens derivados (UI)
| Variável | Valor |
|---|---|
| `--accent` | `#FF8552` (configurável) |
| `--app-bg` | `#fafaf9` |
| `--panel` | `#ffffff` |
| `--canvas-bg` | `#e3e3e3` |
| `--ink` | `#010400` |
| `--muted` | `#6c6c6d` |
| `--line` | `rgba(1,4,0,0.14)` |
| `--hairline` | `rgba(1,4,0,0.08)` |
| Texto na folha | `#111` |
| Linhas de resposta | `#c7c7c7` |
| Linhas de campo | `#999` |

### Tipografia
- **Família principal (UI + folha):** `Baskervville`, Google Fonts.
  `<link href="https://fonts.googleapis.com/css2?family=Baskervville:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">`
  Fallback: `Georgia, 'Times New Roman', serif`.
- **Textarea (roteiro):** monoespaçada do sistema (`ui-monospace, Menlo, Consolas, monospace`), 13.5px, line-height 1.7.
- **Escala (UI):** marca 21px/700 · "ROTEIRO" 16px/700 uppercase · hint 13px · subtítulo 14.5px itálico · botão 17px/700.
- **Escala (folha, base 11pt):** título 1.85em/700 · meta 0.92em · seção 1.05em/700 uppercase · campos 0.88em · linha de resposta altura 1.75em.

### Raio / Sombra / Espaçamento
- Border radius: inputs/cards 10px, chips 6px, caixa de nota 3px.
- Sombra da folha: `0 1px 2px rgba(0,0,0,.08), 0 18px 44px rgba(0,0,0,.16)`.
- Sombra do botão: `0 2px 8px rgba(255,133,82,.32)` → hover `0 4px 14px rgba(255,133,82,.42)`.
- Padding da folha: `22mm 20mm 24mm`. Margem de impressão: `16mm 15mm` (A4).

## Assets
- Nenhuma imagem externa. O ícone de impressora é um SVG inline (stroke `currentColor`, 18×18, strokeWidth 1.7).
- Fonte Baskervville carregada via Google Fonts (link acima).

## Files
- `Imprime Provas.html` — shell, todo o CSS (layout + folha + regras de impressão) e carregamento de scripts.
- `app.jsx` — parser (`parseExam`), componente `Paper` (folha), `App` (estado + textarea + footer), defaults de tweaks, ícone de impressora.
- `tweaks-panel.jsx` — painel de ajustes do protótipo (pode ser descartado/substituído pelo sistema de preferências do seu app).
