# Prompt mágico para o Gemini

Copie **todo o texto abaixo da linha** e cole no Gemini. Troque apenas o que
está em MAIÚSCULAS (assunto, série e quantidade de questões). O Gemini vai
responder já no formato certo — depois é só copiar a resposta dele e salvar
como um arquivo `.md` dentro da pasta `conteudo`.

---

Você é um professor que cria provas. Gere uma prova sobre **ASSUNTO DA PROVA**,
para a série **ANO/SÉRIE**, com **QUANTIDADE** questões de múltipla escolha e
**QUANTIDADE** questões discursivas.

Responda **somente** no formato Markdown abaixo, sem nenhum texto extra antes ou
depois, seguindo EXATAMENTE estas regras:

- O título vem após `# `.
- As seções são exatamente `## Multipla Escolha` e `## Discursivas`.
- Cada pergunta começa com o número em negrito: `**1.**`, `**2.**`, etc.
- Cada alternativa fica em uma linha começando com `- A)`, `- B)`, `- C)`, `- D)`.
- A resposta certa vem em `> Correta: X` (apenas a letra).
- A explicação vem em `> Comentario: ...`.
- Nas discursivas, a resposta esperada vem em `> Resposta: ...`.
- **Fórmulas matemáticas** (raiz, fração, expoente, etc.) devem vir escritas em
  LaTeX entre cifrões, assim: `$\sqrt{16}$`, `$\frac{3}{4}$`, `$x^2$`.

Use este modelo como referência exata:

```markdown
# Título da Prova

## Multipla Escolha

**1.** Texto da pergunta, podendo ter fórmula como $\sqrt{25}$?
- A) Primeira alternativa.
- B) Segunda alternativa.
- C) Terceira alternativa.
- D) Quarta alternativa.
> Correta: C
> Comentario: Explicação curta do porquê a alternativa C está certa.

**2.** Outra pergunta...
- A) ...
- B) ...
- C) ...
- D) ...
> Correta: A
> Comentario: ...

## Discursivas

**16.** Texto da pergunta discursiva.
> Resposta: Resposta esperada, explicada de forma objetiva.
```
