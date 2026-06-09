/* Imprime Provas — exam generator app (parser + editor + live paper preview) */

/* ---------- Sample script shown on first load ---------- */
const SAMPLE_SCRIPT = `# Prova de História — 8º Ano
Disciplina: História do Brasil
Professor: Ana Ribeiro
Valor: 10,0 pontos
Duração: 50 minutos

## Instruções
Leia com atenção cada questão antes de responder. Utilize caneta azul ou preta.
Não é permitido o uso de corretivo. Boa prova!

1. Qual foi o principal fator econômico que impulsionou as Grandes Navegações nos séculos XV e XVI?
a) A busca por especiarias e novas rotas comerciais para o Oriente
b) O desejo de explorar territórios polares
c) A invenção da imprensa por Gutenberg
d) A queda definitiva do Império Romano do Ocidente

2. (FUVEST) Em que ano teve início a Revolução Francesa?
a) 1789
b) 1822
c) 1500
d) 1945

## Parte II — Questões Discursivas
3. Explique, com suas próprias palavras, o que foi o Iluminismo e cite dois de seus principais pensadores.

4. Compare o sistema colonial português com o espanhol na América, destacando duas diferenças relevantes.`;

/* ---------- Parser ---------- */
function parseExam(src) {
  const lines = (src || '').split(/\r?\n/);
  let title = '';
  const meta = [];
  const blocks = [];
  let cur = null;
  let sawQuestion = false;

  const flush = () => { if (cur) { blocks.push(cur); cur = null; } };

  for (const raw of lines) {
    const line = raw.trim();
    if (!line) { continue; }
    let m;

    // Title — first single-hash line in the preamble
    if (!title && !sawQuestion && (m = line.match(/^#\s+(.*)/))) { title = m[1]; continue; }

    // Section heading
    if ((m = line.match(/^#{2,}\s+(.*)/))) { flush(); blocks.push({ type: 'section', text: m[1] }); continue; }

    // Question — "1." / "1)" / "1 -"
    if ((m = line.match(/^\(?(\d+)\s*[.)\-]\s+(.*)/))) {
      flush();
      sawQuestion = true;
      cur = { type: 'question', statement: m[2], options: [] };
      continue;
    }

    // Option — "a)" / "b." / "(c)" under a question
    if (cur && (m = line.match(/^\(?([a-eA-E])\s*[.)\-]\s+(.*)/))) {
      cur.options.push(m[2]);
      continue;
    }

    // Metadata "Key: value" in the preamble
    if (!sawQuestion && (m = line.match(/^([^:]{2,40}):\s*(.+)$/))) {
      meta.push({ key: m[1].trim(), value: m[2].trim() });
      continue;
    }

    // Continuation of a statement, or a stray preamble paragraph
    if (cur) { cur.statement += ' ' + line; }
    else { blocks.push({ type: 'text', text: line }); }
  }
  flush();
  return { title, meta, blocks };
}

/* ---------- Preview (the printed sheet) ---------- */
function Paper({ script, t }) {
  const doc = React.useMemo(() => parseExam(script), [script]);
  let qNum = 0;

  const letter = (i) => String.fromCharCode(97 + i);

  return (
    <div className="paper" style={{ fontSize: `${t.paperScale}em` }}>
      <header className="pp-head">
        <h1 className="pp-title">{doc.title || 'Prova'}</h1>
        {doc.meta.length > 0 && (
          <div className="pp-meta">
            {doc.meta.map((x, i) => (
              <span key={i} className="pp-meta-item"><b>{x.key}:</b> {x.value}</span>
            ))}
          </div>
        )}
        {t.showFields && (
          <div className="pp-fields">
            <div className="pp-field grow"><span>Nome</span><i /></div>
            <div className="pp-field"><span>Turma</span><i /></div>
            <div className="pp-field"><span>Data</span><i /></div>
            {t.showGrade && (
              <div className="pp-grade"><span>Nota</span><div className="pp-grade-box" /></div>
            )}
          </div>
        )}
      </header>

      <div className="pp-body">
        {doc.blocks.map((b, i) => {
          if (b.type === 'section') {
            return <h2 key={i} className="pp-section">{b.text}</h2>;
          }
          if (b.type === 'text') {
            return <p key={i} className="pp-text">{b.text}</p>;
          }
          qNum += 1;
          const hasOpts = b.options.length > 0;
          return (
            <div key={i} className="pp-q">
              <p className="pp-q-stmt">
                <span className="pp-q-num">{qNum}.</span>
                <span>{b.statement}</span>
              </p>
              {hasOpts ? (
                <ol className="pp-opts">
                  {b.options.map((o, j) => (
                    <li key={j}><span className="pp-opt-mark">{letter(j)})</span><span>{o}</span></li>
                  ))}
                </ol>
              ) : (
                <div className="pp-lines">
                  {Array.from({ length: t.answerLines }).map((_, k) => <span key={k} className="pp-line" />)}
                </div>
              )}
            </div>
          );
        })}
        {doc.blocks.length === 0 && (
          <p className="pp-empty">Cole o roteiro da prova à esquerda para visualizar aqui.</p>
        )}
      </div>
    </div>
  );
}

/* ---------- App shell ---------- */
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "accent": "#FF8552",
  "paperScale": 1,
  "showFields": true,
  "showGrade": true,
  "answerLines": 4
}/*EDITMODE-END*/;

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const [script, setScript] = React.useState(() => {
    return localStorage.getItem('ip_script') ?? SAMPLE_SCRIPT;
  });

  React.useEffect(() => {
    localStorage.setItem('ip_script', script);
  }, [script]);

  React.useEffect(() => {
    document.documentElement.style.setProperty('--accent', t.accent);
  }, [t.accent]);

  const onPrint = () => window.print();

  const charCount = script.length;
  const qCount = React.useMemo(
    () => parseExam(script).blocks.filter((b) => b.type === 'question').length,
    [script]
  );

  return (
    <div className="app">
      <header className="app-header">
        <div className="brand">
          <span className="brand-mark" />
          <span className="brand-name">Imprime Provas</span>
        </div>
        <span className="app-sub">Editor de provas para impressão</span>
      </header>

      <main className="workspace">
        <section className="editor">
          <div className="panel-head">
            <h2>Roteiro</h2>
            <span className="hint">{qCount} {qCount === 1 ? 'questão' : 'questões'} · {charCount} caracteres</span>
          </div>
          <textarea
            className="script-input"
            value={script}
            spellCheck={false}
            onChange={(e) => setScript(e.target.value)}
            placeholder={'# Título da prova\nProfessor: ...\n\n## Instruções\n...\n\n1. Enunciado da questão\na) alternativa\nb) alternativa'}
          />
          <div className="legend">
            <code># Título</code>
            <code>## Seção</code>
            <code>Campo: valor</code>
            <code>1. Questão</code>
            <code>a) Alternativa</code>
          </div>
        </section>

        <div className="preview-pane">
          <div className="canvas">
            <Paper script={script} t={t} />
          </div>
          <footer className="preview-footer">
            <span className="paper-tag">A4 · Pré-visualização</span>
            <button className="btn-print" onClick={onPrint}>
              <PrinterIcon />
              Imprimir
            </button>
          </footer>
        </div>
      </main>

      <TweaksPanel>
        <TweakSection label="Aparência da prova" />
        <TweakColor label="Cor de destaque" value={t.accent}
          options={['#FF8552', '#297373', '#39393A', '#010400']}
          onChange={(v) => setTweak('accent', v)} />
        <TweakSlider label="Tamanho do texto" value={t.paperScale} min={0.85} max={1.3} step={0.05}
          onChange={(v) => setTweak('paperScale', v)} />
        <TweakSection label="Cabeçalho e respostas" />
        <TweakToggle label="Campos do aluno" value={t.showFields}
          onChange={(v) => setTweak('showFields', v)} />
        <TweakToggle label="Caixa de nota" value={t.showGrade}
          onChange={(v) => setTweak('showGrade', v)} />
        <TweakSlider label="Linhas de resposta" value={t.answerLines} min={2} max={8} step={1}
          onChange={(v) => setTweak('answerLines', v)} />
      </TweaksPanel>
    </div>
  );
}

function PrinterIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
      strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M6 9V3h12v6" />
      <path d="M6 18H4a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-2" />
      <rect x="6" y="14" width="12" height="7" rx="1" />
    </svg>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
