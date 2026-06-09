# Prompt para o Gemini / NotebookLM

Fluxo recomendado: suba os livros como **fontes no NotebookLM**, depois cole o
prompt abaixo pedindo a verificação do conteúdo e a geração dos simulados.

Troque o que está em MAIÚSCULAS (assunto, série, quantidades, nº de simulados,
conteúdo e níveis de dificuldade). Depois é só copiar a resposta e colar no editor
(`Imprime-Provas.html`) — ele já separa os vários simulados sozinho.

> ⚠️ **Atenção às contas:** em cada simulado, a soma de (múltipla + discursiva)
> deve ser **igual** à soma de (Fácil + Médio + Difícil).

```text
Você é um professor que cria provas. Gere QUANTIDADE DE SIMULADOS simulados (versões) de uma prova sobre ASSUNTO DA PROVA, para a série ANO/SÉRIE. Cada simulado deve ter QUANTIDADE questões de múltipla escolha e QUANTIDADE questões discursivas.

Antes de gerar, verifique se você encontra o conteúdo informado no fim nas suas fontes:
- Se encontrar, gere os simulados normalmente.
- Se NÃO encontrar, responda apenas com a frase: "Não encontrei conteúdo confiável sobre este assunto." e não gere nada.

Regras dos simulados (versões):
- Todas as versões cobrem o MESMO conteúdo, mas NÃO podem repetir o texto das perguntas.
- Em cada versão, reformule os enunciados (mude a forma de perguntar) e troque os valores, números e exemplos.
- As alternativas e o gabarito devem corresponder corretamente a cada versão.
- Cada simulado tem seu próprio título: # MATÉRIA - V1, depois # MATÉRIA - V2, e assim por diante.
- Não escreva nada entre um simulado e outro além do título do próximo.

Ao gerar, responda SOMENTE no formato abaixo, sem nenhum texto extra antes ou depois, seguindo EXATAMENTE estas regras:
- O título vem após "# ", no formato:  # MATÉRIA - V1
- As seções são exatamente "## Múltipla Escolha" e "## Discursivas".
- Cada pergunta começa com o número em negrito: **1.**, **2.**, etc. (recomece a numeração em cada simulado).
- Cada alternativa fica em uma linha começando com "- A)", "- B)", "- C)", "- D)".
- A resposta certa vem em "> Correta: X" (apenas a letra).
- A explicação vem em "> Comentário: ...".
- Nas discursivas, a resposta esperada vem em "> Resposta: ...".
- Fórmulas matemáticas devem vir em LaTeX entre cifrões: $\sqrt{16}$, $\frac{3}{4}$, $x^2$.
- Em cada simulado, o total de questões deve respeitar a divisão por tipo (múltipla/discursiva) e os níveis de dificuldade do fim — as duas somas devem ser iguais.

Siga este modelo exato (exemplo com 2 simulados):

# Matéria - V1

## Múltipla Escolha

**1.** Texto da pergunta, podendo ter fórmula como $\sqrt{25}$?
- A) Primeira alternativa.
- B) Segunda alternativa.
- C) Terceira alternativa.
- D) Quarta alternativa.
> Correta: C
> Comentário: Explicação curta do porquê a alternativa C está certa.

## Discursivas

**2.** Texto da pergunta discursiva.
> Resposta: Resposta esperada, explicada de forma objetiva.

# Matéria - V2

## Múltipla Escolha

**1.** O mesmo conteúdo perguntado de outra forma, com valores diferentes?
- A) Primeira alternativa.
- B) Segunda alternativa.
- C) Terceira alternativa.
- D) Quarta alternativa.
> Correta: A
> Comentário: Explicação curta da resposta.

## Discursivas

**2.** Pergunta discursiva reformulada, sobre o mesmo tema.
> Resposta: Resposta esperada.

Quantidade de simulados: QUANTIDADE DE SIMULADOS

Conteúdo da prova:
"CONTEÚDO DA PROVA AQUI"

Níveis de dificuldade por simulado (quantas questões de cada):
- Fácil = 0
- Médio = 10
- Difícil = 10
```
