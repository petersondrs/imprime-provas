# Como gerar suas provas em PDF

Sistema simples: você escreve o conteúdo, dá dois cliques e sai o PDF pronto
para imprimir (com o gabarito comentado no final, em páginas separadas).

## O seu dia a dia (3 passos)

### 1. Crie o conteúdo no Gemini
- Abra o arquivo **`PROMPT_GEMINI.md`**, copie o prompt e cole no Gemini.
- Troque o assunto, a série e a quantidade de questões.
- O Gemini vai responder no formato certo.

### 2. Salve a resposta na pasta `conteudo`
- Copie a resposta do Gemini.
- Salve como um arquivo de texto com final **`.md`** dentro da pasta
  **`conteudo`** (ex.: `05-prova-matematica.md`).
- Dica: o número na frente do nome controla a ordem no PDF
  (`01-...`, `02-...`, `03-...`).
- Pode ter quantos arquivos quiser na pasta — cada um vira uma prova no PDF.

### 3. Gere o PDF
- Dê **dois cliques** em **`gerar.command`**.
- Uma janela preta vai abrir, trabalhar alguns segundos e a pasta **`provas`**
  vai abrir sozinha com o PDF pronto (o nome tem a data e a hora).

Pronto. É só imprimir.

## Matemática

Para raiz, fração, expoente etc., escreva a fórmula entre cifrões, em LaTeX
(o Gemini já faz isso sozinho se você usar o prompt):

| O que você quer | Como escrever | Como sai no PDF |
|---|---|---|
| Raiz quadrada | `$\sqrt{16}$` | raiz com o tracinho por cima |
| Fração | `$\frac{3}{4}$` | número em cima do outro |
| Expoente | `$x^2$` | x ao quadrado |
| Símbolos | `$\pi$`, `$\div$`, `$\neq$` | π, ÷, ≠ |

## As pastas e arquivos

| Item | Para que serve | Você mexe? |
|---|---|---|
| `conteudo/` | Onde ficam os arquivos `.md` das provas | ✅ Sim |
| `provas/` | Onde os PDFs prontos aparecem | só pega o PDF |
| `gerar.command` | O botão de gerar (dois cliques) | só clica |
| `PROMPT_GEMINI.md` | O prompt pronto para o Gemini | só copia |
| `motor_provas.py` | O motor que monta o PDF | ❌ Não |

## Se aparecer "não foi possível abrir" no primeiro duplo-clique

O macOS às vezes bloqueia arquivos novos. Resolve assim, só uma vez:
- Clique com o **botão direito** em `gerar.command` → **Abrir** → **Abrir**.

Depois disso, o duplo-clique normal funciona sempre.
