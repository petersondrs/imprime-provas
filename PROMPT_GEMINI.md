# Prompt para o Gemini / NotebookLM

Suba os livros **e as provas/testes de anos anteriores** como fontes no NotebookLM,
depois cole o prompt abaixo. Substitua tudo em MAIÚSCULAS e copie a resposta para o
editor `Imprime-Provas.html`.

> ⚠️ Em cada simulado: (múltipla + discursiva) deve ser **igual** a (Fácil + Médio + Difícil).

```text
Você é um professor que cria provas. Gere QUANTIDADE simulados sobre ASSUNTO, para ANO/SÉRIE, com QUANTIDADE questões de múltipla escolha e QUANTIDADE discursivas cada.

Verifique nas fontes se o conteúdo do fim existe:
- Se sim: gere normalmente.
- Se não: responda só "Não encontrei conteúdo confiável sobre este assunto." e pare.

Análise de anos anteriores:
Busque nas fontes "Etapa ETAPA - TIPO MATÉRIA (ANO).pdf". Se encontrar, analise antes de gerar:
- O conteúdo cobrado é o mesmo pedido agora?
- O professor é o mesmo? (veja cabeçalho/rodapé)
- Há padrão no formato e estrutura das perguntas?
- Quais verbos de comando ele usa? (ex.: "Cite...", "Explique...", "Assinale...")
- Há pontuação por questão? Se sim, use a mesma distribuição.
Se encontrar padrões, ajuste tom, vocabulário e formato ao estilo do professor — mas siga o conteúdo pedido agora. Sem arquivos anteriores, ignore esta etapa.

Regras dos simulados:
- Mesmo conteúdo em todas as versões, mas SEM repetir enunciados.
- Reformule perguntas e troque valores/exemplos a cada versão.
- Gabarito e alternativas devem corresponder a cada versão.
- Título de cada simulado: # MATÉRIA - V1, # MATÉRIA - V2, etc.
- Nada entre simulados além do próximo título.

Formato obrigatório (responda SOMENTE assim, sem texto extra):
- Seções: ## Múltipla Escolha  e  ## Discursivas
- Perguntas em negrito: **1.**, **2.**, etc. (reinicie a cada simulado)
- Alternativas: - A)  - B)  - C)  - D)
- Resposta certa: > Correta: X  (só a letra)
- Explicação: > Comentário: ...
- Discursivas: > Resposta: ...
- Fórmulas LaTeX entre cifrões: $\sqrt{16}$, $\frac{3}{4}$, $x^2$
- Total de questões = soma dos níveis de dificuldade

Modelo (replique esta estrutura para cada simulado):

# Matéria - V1

## Múltipla Escolha

**1.** Enunciado da questão, com fórmula se necessário: $\sqrt{25}$?
- A) Alternativa.
- B) Alternativa.
- C) Alternativa correta.
- D) Alternativa.
> Correta: C
> Comentário: Explicação curta.

## Discursivas

**2.** Enunciado da questão discursiva.
> Resposta: Resposta esperada.

Qtd. de simulados: QUANTIDADE
Conteúdo: "CONTEÚDO AQUI"
Dificuldade: Fácil = 0 / Médio = 10 / Difícil = 10
Tipo: PROVA ou TESTE
Etapa: ETAPA X
```
