import { useEffect, useState } from 'react';
import { api } from './api';

type Resume = { id: number; filename: string; created_at: string };

const Icon = ({ children }: { children: string }) => (
  <span className="nav-icon" aria-hidden="true">{children}</span>
);

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [user, setUser] = useState<any>(null);
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [selected, setSelected] = useState<number | null>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const [job, setJob] = useState('');
  const [match, setMatch] = useState<any>(null);
  const [coach, setCoach] = useState('');
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState(false);
  const [active, setActive] = useState('overview');

  async function load() {
    try {
      const [u, r] = await Promise.all([api.get('/auth/me'), api.get('/resumes')]);
      setUser(u.data);
      setResumes(r.data);
    } catch {
      logout();
    }
  }

  useEffect(() => {
    if (token) load();
  }, [token]);

  function logout() {
    localStorage.removeItem('token');
    setToken('');
    setUser(null);
    setResumes([]);
    setAnalysis(null);
    setSelected(null);
    setMatch(null);
    setCoach('');
  }

  async function auth(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setMessage('');
    try {
      if (mode === 'register') {
        await api.post('/auth/register', { name, email, password });
        setMode('login');
        setMessage('Account created successfully. Please sign in.');
      } else {
        const r = await api.post('/auth/login', { email, password });
        localStorage.setItem('token', r.data.access_token);
        setToken(r.data.access_token);
      }
    } catch (e: any) {
      setMessage(e.response?.data?.detail || 'Authentication failed. Please try again.');
    } finally {
      setBusy(false);
    }
  }

  async function upload() {
    if (!file) return;
    setBusy(true);
    setMessage('');
    try {
      const data = new FormData();
      data.append('file', file);
      await api.post('/resumes', data);
      setFile(null);
      setMessage('Resume uploaded successfully.');
      await load();
    } catch (e: any) {
      setMessage(e.response?.data?.detail || 'Upload failed.');
    } finally {
      setBusy(false);
    }
  }

  async function analyze(id: number) {
    setBusy(true);
    setSelected(id);
    setMessage('');
    try {
      const r = await api.post(`/resumes/${id}/analyze`);
      setAnalysis(r.data);
      setMatch(null);
      setCoach('');
      setActive('analysis');
    } catch (e: any) {
      setMessage(e.response?.data?.detail || 'Analysis failed.');
    } finally {
      setBusy(false);
    }
  }

  async function del(id: number) {
    if (!confirm('Delete this resume?')) return;
    try {
      await api.delete(`/resumes/${id}`);
      setResumes(items => items.filter(item => item.id !== id));
      if (selected === id) {
        setSelected(null);
        setAnalysis(null);
        setMatch(null);
        setCoach('');
      }
    } catch (e: any) {
      setMessage(e.response?.data?.detail || 'Could not delete resume.');
    }
  }

  async function doMatch() {
    if (!selected) return;
    setBusy(true);
    try {
      setMatch((await api.post('/job-match', {
        resume_id: selected,
        job_description: job
      })).data);
    } catch (e: any) {
      setMessage(e.response?.data?.detail || 'Matching failed.');
    } finally {
      setBusy(false);
    }
  }

  async function doCoach() {
  if (!selected) return;
  setBusy(true);
  setMessage('');
  setCoach('');

  try {
    const response = await api.post(`/career-coach/${selected}`);
    setCoach(response.data.recommendations || 'No recommendations returned.');
  } catch (e: any) {
    setMessage(e.response?.data?.detail || 'Career coach unavailable.');
  } finally {
    setBusy(false);
  }
}

  const scrollTo = (id: string) => {
    setActive(id);
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  if (!token) {
    return (
      <div className="auth-shell">
        <section className="auth-visual">
          <div className="brand brand-light"><span className="brand-mark">C</span> careerlens</div>
          <div className="auth-pitch">
            <span className="eyebrow light-eyebrow">YOUR CAREER, IN FOCUS</span>
            <h1>Make your next move<br /><em>your best move.</em></h1>
            <p>Turn your resume into a clearer picture of your strengths, opportunities, and next steps.</p>
            <div className="auth-points">
              <span><b>01</b> Understand your resume</span>
              <span><b>02</b> Find your skill gaps</span>
              <span><b>03</b> Move forward with confidence</span>
            </div>
          </div>
          <div className="auth-foot">A little more clarity. A lot more possibility.</div>
          <div className="visual-orb orb-one" /><div className="visual-orb orb-two" />
        </section>
        <section className="auth-panel">
          <form className="auth-form" onSubmit={auth}>
            <div className="mobile-brand brand"><span className="brand-mark">C</span> careerlens</div>
            <span className="eyebrow">WELCOME TO CAREERLENS</span>
            <h2>{mode === 'login' ? 'Welcome back' : 'Create your account'}</h2>
            <p className="muted">{mode === 'login' ? 'Sign in to pick up where you left off.' : 'Create your workspace and start building your next chapter.'}</p>
            {mode === 'register' && (
              <label className="field-label">Full name
                <input value={name} onChange={e => setName(e.target.value)} placeholder="Your name" required />
              </label>
            )}
            <label className="field-label">Email address
              <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" required />
            </label>
            <label className="field-label">Password
              <input type="password" minLength={8} value={password} onChange={e => setPassword(e.target.value)} placeholder="At least 8 characters" required />
            </label>
            <button className="button button-primary button-wide" disabled={busy}>{busy ? 'Please wait…' : mode === 'login' ? 'Sign in' : 'Create account'} <span>→</span></button>
            {message && <p className="notice">{message}</p>}
            <p className="auth-switch">{mode === 'login' ? 'New to CareerLens?' : 'Already have an account?'} <button type="button" onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setMessage(''); }}>{mode === 'login' ? 'Create an account' : 'Sign in'}</button></p>
            <p className="auth-privacy">Your career workspace is private and secure.</p>
          </form>
        </section>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">C</span> careerlens</div>
        <div className="side-caption">WORKSPACE</div>
        <nav className="side-nav">
          <button className={active === 'overview' ? 'nav-link active' : 'nav-link'} onClick={() => scrollTo('overview')}><Icon>⌂</Icon> Overview</button>
          <button className={active === 'library' ? 'nav-link active' : 'nav-link'} onClick={() => scrollTo('library')}><Icon>▤</Icon> My resumes</button>
          <button className={active === 'matching' ? 'nav-link active' : 'nav-link'} onClick={() => scrollTo('matching')}><Icon>⌕</Icon> Job matching</button>
          <button className={active === 'coach' ? 'nav-link active' : 'nav-link'} onClick={() => scrollTo('coach')}><Icon>✧</Icon> Career coach</button>
        </nav>
        <div className="sidebar-bottom">
          <div className="profile-avatar">{(user?.name || 'U').slice(0, 1).toUpperCase()}</div>
          <div className="profile-info"><strong>{user?.name || 'User'}</strong><span>{user?.email}</span></div>
          <button className="logout-button" onClick={logout} title="Sign out">↗</button>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div><span className="eyebrow">YOUR PERSONAL CAREER SPACE</span><h1>Overview</h1></div>
          <div className="secure-pill"><span /> Private workspace</div>
        </header>

        <section id="overview" className="welcome-card">
          <div className="welcome-copy">
            <span className="eyebrow light-eyebrow">A CLEARER PATH STARTS HERE</span>
            <h2>Hello, {user?.name?.split(' ')[0] || 'there'} <span>✦</span></h2>
            <p>Small steps today can open up exciting opportunities tomorrow.</p>
            <button className="button button-white" onClick={() => scrollTo('library')}>Explore my resumes <span>→</span></button>
          </div>
          <div className="welcome-art" aria-hidden="true">
            <div className="art-ring ring-a" /><div className="art-ring ring-b" />
            <div className="art-card"><span>CAREER SNAPSHOT</span><b>Potential<br />in progress.</b><i>✦</i></div>
          </div>
        </section>

        {message && <div className="global-notice">{message}<button onClick={() => setMessage('')}>×</button></div>}

        <section className="stats-grid">
          <div className="stat-card"><div className="stat-icon violet">▤</div><span>Resumes uploaded</span><strong>{resumes.length}</strong><small>Your resume library</small></div>
          <div className="stat-card"><div className="stat-icon peach">◎</div><span>Selected resume</span><strong className="stat-word">{selected ? 'Ready' : '—'}</strong><small>{selected ? 'Ready for your next step' : 'Choose a resume to begin'}</small></div>
          <div className="stat-card"><div className="stat-icon mint">✧</div><span>Latest analysis</span><strong className="stat-word">{analysis ? 'Complete' : 'Pending'}</strong><small>{analysis ? 'Your insights are ready' : 'Upload and analyze a resume'}</small></div>
        </section>

        <section id="library" className="content-card section-card">
          <div className="section-heading">
            <div><span className="eyebrow">YOUR DOCUMENTS</span><h3>Resume library</h3><p>Keep your resumes organized and ready for new opportunities.</p></div>
            <span className="count-pill">{resumes.length} {resumes.length === 1 ? 'resume' : 'resumes'}</span>
          </div>
          <div className="upload-zone">
            <div className="upload-symbol">↑</div>
            <div className="upload-text"><strong>{file ? file.name : 'Add your resume'}</strong><span>{file ? 'Ready to upload' : 'Choose a PDF or DOCX file to get started'}</span></div>
            <label className="button button-outline upload-select">Browse files<input type="file" accept=".pdf,.docx" onChange={e => setFile(e.target.files?.[0] || null)} /></label>
            <button className="button button-primary" onClick={upload} disabled={!file || busy}>{busy ? 'Uploading…' : 'Upload resume'}</button>
          </div>
          <div className="resume-list">
            {resumes.map(r => (
              <div className="resume-row" key={r.id}>
                <div className="file-icon">PDF</div>
                <div className="resume-meta"><strong>{r.filename}</strong><span>Added {new Date(r.created_at).toLocaleDateString()}</span></div>
                {selected === r.id && <span className="selected-pill">Selected</span>}
                <button className="button button-soft" onClick={() => analyze(r.id)} disabled={busy}>{busy && selected === r.id ? 'Analyzing…' : 'Analyze resume'}</button>
                <button className="delete-button" onClick={() => del(r.id)} aria-label={`Delete ${r.filename}`}>×</button>
              </div>
            ))}
            {!resumes.length && <div className="empty-state"><div>▤</div><strong>Your library is waiting</strong><span>Upload your first resume to unlock your career insights.</span></div>}
          </div>
        </section>

        {analysis && (
          <section id="analysis" className="content-card section-card">
            <div className="section-heading"><div><span className="eyebrow">YOUR RESUME INSIGHTS</span><h3>Analysis overview</h3><p>An estimate based on the content extracted from your resume.</p></div><span className="selected-pill">Analysis ready</span></div>
            <div className="score-grid">
              <div className="score-card"><span>ATS estimate</span><strong>{analysis.ats_score}<small>/100</small></strong><div className="score-track"><i style={{ width: `${analysis.ats_score}%` }} /></div></div>
              <div className="score-card"><span>Readability</span><strong>{analysis.readability_score}<small>/100</small></strong><div className="score-track"><i style={{ width: `${analysis.readability_score}%` }} /></div></div>
            </div>
            <div className="insight-block"><h4>Detected skills</h4><div className="skill-list">{analysis.skills.map((s: string) => <span className="skill-chip" key={s}>{s}</span>)}</div></div>
            <div className="insight-columns">
              <div><h4><span className="dot green" /> Strengths</h4>{analysis.strengths.map((s: string) => <p className="insight-line" key={s}>{s}</p>)}</div>
              <div><h4><span className="dot amber" /> Areas to improve</h4>{analysis.weaknesses.map((s: string) => <p className="insight-line" key={s}>{s}</p>)}</div>
            </div>
            <p className="method-note">{analysis.methodology}</p>
          </section>
        )}

        <div className="tools-grid">
          <section id="matching" className="content-card tool-card">
            <div className="tool-heading"><div className="tool-icon peach">⌕</div><div><span className="eyebrow">FIND YOUR FIT</span><h3>Job description match</h3></div></div>
            <p className="tool-description">Compare your selected resume with a role and discover which skills align.</p>
            <textarea value={job} onChange={e => setJob(e.target.value)} rows={5} placeholder="Paste a job description here (at least 50 characters)…" />
            <button className="button button-primary" onClick={doMatch} disabled={!selected || job.trim().length < 50 || busy}>{busy ? 'Comparing…' : 'Compare resume'} <span>→</span></button>
            {!selected && <small className="helper-text">Analyze a resume first to enable matching.</small>}
            {match && <div className="match-result"><div className="match-score"><strong>{match.match_percentage}%</strong><span>skill match</span></div><div><b>Matched skills</b><p>{match.matched_skills.join(', ') || 'None detected'}</p><b>Skills to develop</b><p className="missing-skills">{match.missing_skills.join(', ') || 'None detected'}</p></div></div>}
          </section>

          <section id="coach" className="content-card tool-card">
            <div className="tool-heading"><div className="tool-icon violet">✧</div><div><span className="eyebrow">YOUR NEXT CHAPTER</span><h3>AI career coach</h3></div></div>
            <p className="tool-description">Get practical next steps and career guidance based on the skills in your resume.</p>
            <div className="coach-prompt"><span>✦</span><p>Turn your current experience into a plan for what comes next.</p></div>
            <button className="button button-primary" onClick={doCoach} disabled={!selected || busy}>{busy ? 'Generating…' : 'Generate career guidance'} <span>→</span></button>
            {!selected && <small className="helper-text">Analyze a resume first to enable career coaching.</small>}
            {coach && <div className="coach-result">{coach}</div>}
          </section>
        </div>

        <footer className="app-footer">Made for your next opportunity <span>✦</span><small>ATS scores are estimates, not official ATS results.</small></footer>
      </main>
    </div>
  );
}

export default App;
