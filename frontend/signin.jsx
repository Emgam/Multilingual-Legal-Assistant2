import { useState } from "react";

export default function SignIn({ onNavigate, lang, dark, toggleDark, setLang }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPass, setShowPass] = useState(false);
    const [loading, setLoading] = useState(false);

    const t = {
        en: {
            welcome: "Welcome back",
            sub: "Sign in to your StartupTN account",
            email: "Email address",
            emailPh: "you@example.com",
            password: "Password",
            remember: "Remember me",
            forgot: "Forgot password?",
            btn: "Sign In",
            noAccount: "Don't have an account?",
            signup: "Create account",
            or: "or",
            secure: "256-bit SSL encrypted",
            darkMode: "Dark",
            lightMode: "Light",
            feature1Title: "Startup Creation",
            feature1: "Complete step-by-step registration guide",
            feature2Title: "CNSS Procedures",
            feature2: "Social security obligations simplified",
            feature3Title: "Multilingual AI",
            feature3: "Ask in English, French or Darija",
        },
        fr: {
            welcome: "Bon retour",
            sub: "Connectez-vous à votre compte StartupTN",
            email: "Adresse e-mail",
            emailPh: "vous@exemple.com",
            password: "Mot de passe",
            remember: "Se souvenir",
            forgot: "Mot de passe oublié ?",
            btn: "Connexion",
            noAccount: "Pas de compte ?",
            signup: "Créer un compte",
            or: "ou",
            secure: "Chiffrement SSL 256 bits",
            darkMode: "Sombre",
            lightMode: "Clair",
            feature1Title: "Création Startup",
            feature1: "Guide complet d'enregistrement étape par étape",
            feature2Title: "Procédures CNSS",
            feature2: "Obligations sociales simplifiées",
            feature3Title: "IA Multilingue",
            feature3: "Posez vos questions en français, anglais ou darija",
        },
        dar: {
            welcome: "أهلاً بيك",
            sub: "ادخل لحسابك في StartupTN",
            email: "البريد الإلكتروني",
            emailPh: "you@example.com",
            password: "كلمة السر",
            remember: "تذكرني",
            forgot: "نسيت كلمة السر؟",
            btn: "ادخل",
            noAccount: "ماعندكش حساب؟",
            signup: "سجّل",
            or: "أو",
            secure: "مشفر ومحمي",
            darkMode: "داكن",
            lightMode: "فاتح",
            feature1Title: "تأسيس Startup",
            feature1: "دليل التسجيل خطوة بخطوة",
            feature2Title: "إجراءات CNSS",
            feature2: "الالتزامات الاجتماعية بطريقة بسيطة",
            feature3Title: "ذكاء اصطناعي متعدد اللغات",
            feature3: "اسأل بالعربي أو الفرنسي أو الإنجليزي",
        },
    }[lang];

    const isRtl = lang === "dar";

    const handleSubmit = (e) => {
        e.preventDefault();
        setLoading(true);
        setTimeout(() => { setLoading(false); onNavigate("chat"); }, 1200);
    };

    return (
        <div className={`root ${dark ? "dark" : "light"} ${isRtl ? "rtl" : ""}`}>
            <style>{css}</style>

            {/* Top Controls */}
            <div className="top-controls">
                <div className="lang-pills">
                    {[["en", "EN"], ["fr", "FR"], ["dar", "ع"]].map(([code, label]) => (
                        <button key={code} className={`pill ${lang === code ? "pill-active" : ""}`} onClick={() => setLang(code)}>{label}</button>
                    ))}
                </div>
                <button className="theme-toggle" onClick={toggleDark}>
                    {dark ? <SunSVG /> : <MoonSVG />}
                </button>
            </div>

            <div className="layout">
                {/* Left Hero Panel */}
                <aside className="hero-panel">
                    <div className="hero-inner">
                        <div className="brand">
                            <div className="brand-icon"><BotSVG /></div>
                            <span className="brand-name">StartupTN</span>
                        </div>
                        <p className="hero-headline">Your AI guide to<br /><em>Tunisian procedures</em></p>

                        <div className="feature-list">
                            {[
                                { icon: <RocketSVG />, title: t.feature1Title, desc: t.feature1, color: "#60a5fa" },
                                { icon: <ShieldSVG />, title: t.feature2Title, desc: t.feature2, color: "#34d399" },
                                { icon: <GlobeSVG />, title: t.feature3Title, desc: t.feature3, color: "#f472b6" },
                            ].map((f, i) => (
                                <div className="feature-item" key={i} style={{ animationDelay: `${i * 0.1 + 0.3}s` }}>
                                    <div className="feature-icon" style={{ color: f.color }}>{f.icon}</div>
                                    <div>
                                        <div className="feature-title">{f.title}</div>
                                        <div className="feature-desc">{f.desc}</div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        <div className="hero-blob hero-blob-1" />
                        <div className="hero-blob hero-blob-2" />
                    </div>
                </aside>

                {/* Right Form Panel */}
                <main className="form-panel">
                    <div className="form-box">
                        <div className="form-header">
                            <h1 className="form-title">{t.welcome}</h1>
                            <p className="form-subtitle">{t.sub}</p>
                        </div>

                        <form onSubmit={handleSubmit} className="form">
                            <div className="field">
                                <label className="label">{t.email}</label>
                                <div className="input-wrap">
                                    <span className="input-icon"><MailSVG /></span>
                                    <input
                                        type="email"
                                        className="input"
                                        placeholder={t.emailPh}
                                        value={email}
                                        onChange={e => setEmail(e.target.value)}
                                        dir={isRtl ? "rtl" : "ltr"}
                                        required
                                    />
                                </div>
                            </div>

                            <div className="field">
                                <label className="label">{t.password}</label>
                                <div className="input-wrap">
                                    <span className="input-icon"><LockSVG /></span>
                                    <input
                                        type={showPass ? "text" : "password"}
                                        className="input"
                                        placeholder="••••••••"
                                        value={password}
                                        onChange={e => setPassword(e.target.value)}
                                        required
                                    />
                                    <button type="button" className="eye-btn" onClick={() => setShowPass(s => !s)}>
                                        {showPass ? <EyeOffSVG /> : <EyeSVG />}
                                    </button>
                                </div>
                            </div>

                            <div className="form-row">
                                <label className="check-label">
                                    <input type="checkbox" className="check" />
                                    <span className="check-box" />
                                    {t.remember}
                                </label>
                                <button type="button" className="text-btn">{t.forgot}</button>
                            </div>

                            <button type="submit" className={`submit-btn ${loading ? "loading" : ""}`} disabled={loading}>
                                {loading ? <SpinnerSVG /> : t.btn}
                            </button>
                        </form>

                        <p className="switch-text">
                            {t.noAccount}{" "}
                            <button className="link-btn" onClick={() => onNavigate("signup")}>{t.signup}</button>
                        </p>

                        <div className="secure-row">
                            <LockTinySVG />
                            {t.secure}
                        </div>
                    </div>
                </main>
            </div>
        </div>
    );
}

// ── SVG Icons ──
const BotSVG = () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="11" rx="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /><circle cx="9" cy="16" r="1" fill="currentColor" /><circle cx="15" cy="16" r="1" fill="currentColor" /></svg>;
const RocketSVG = () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z" /><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z" /></svg>;
const ShieldSVG = () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /></svg>;
const GlobeSVG = () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10" /><line x1="2" y1="12" x2="22" y2="12" /><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" /></svg>;
const MailSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" /><polyline points="22,6 12,13 2,6" /></svg>;
const LockSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /></svg>;
const EyeSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" /></svg>;
const EyeOffSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" /><line x1="1" y1="1" x2="23" y2="23" /></svg>;
const LockTinySVG = () => <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><rect x="3" y="11" width="18" height="11" rx="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /></svg>;
const SunSVG = () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="5" /><line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" /><line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" /><line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" /><line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" /></svg>;
const MoonSVG = () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" /></svg>;
const SpinnerSVG = () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" style={{ animation: "spin 0.8s linear infinite" }}><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" /></svg>;

const css = `
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Instrument+Serif:ital@0;1&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  .root {
    --font: 'Plus Jakarta Sans', sans-serif;
    --serif: 'Instrument Serif', serif;
    --r: 12px;
    --r-sm: 8px;
    --r-lg: 20px;
    --t: 0.18s ease;
    font-family: var(--font);
    min-height: 100vh;
    position: relative;
  }

  .light {
    --bg: #f0f4ff;
    --card: #ffffff;
    --hero-from: #1e40af;
    --hero-to: #1d4ed8;
    --text: #0f172a;
    --text-2: #475569;
    --text-3: #94a3b8;
    --border: rgba(37,99,235,0.15);
    --input-bg: #f8faff;
    --accent: #2563eb;
    --accent-h: #1d4ed8;
    --accent-glow: rgba(37,99,235,0.25);
    background: var(--bg);
    color: var(--text);
  }

  .dark {
    --bg: #060d1f;
    --card: #0d1628;
    --hero-from: #0a1628;
    --hero-to: #0f1e3d;
    --text: #e2e8f0;
    --text-2: #94a3b8;
    --text-3: #475569;
    --border: rgba(99,148,255,0.12);
    --input-bg: #0f1e3d;
    --accent: #3b82f6;
    --accent-h: #2563eb;
    --accent-glow: rgba(59,130,246,0.3);
    background: var(--bg);
    color: var(--text);
  }

  /* TOP BAR */
  .top-controls {
    position: fixed;
    top: 18px;
    right: 20px;
    z-index: 100;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .rtl .top-controls { right: auto; left: 20px; }

  .lang-pills {
    display: flex;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 30px;
    padding: 3px;
    gap: 2px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  }
  .pill {
    padding: 5px 12px;
    border-radius: 20px;
    border: none;
    background: none;
    font-family: var(--font);
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-2);
    cursor: pointer;
    transition: all var(--t);
  }
  .pill-active { background: var(--accent); color: white; }
  .pill:not(.pill-active):hover { color: var(--text); }

  .theme-toggle {
    width: 36px; height: 36px;
    border-radius: 50%;
    border: 1px solid var(--border);
    background: var(--card);
    color: var(--text-2);
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: all var(--t);
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  }
  .theme-toggle:hover { color: var(--accent); border-color: var(--accent); }

  /* LAYOUT */
  .layout {
    display: grid;
    grid-template-columns: 440px 1fr;
    min-height: 100vh;
  }
  @media (max-width: 900px) {
    .layout { grid-template-columns: 1fr; }
    .hero-panel { display: none; }
  }

  /* HERO PANEL */
  .hero-panel {
    background: linear-gradient(160deg, var(--hero-from) 0%, var(--hero-to) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
  }
  .hero-inner {
    padding: 60px 48px;
    position: relative;
    z-index: 2;
  }
  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 40px;
  }
  .brand-icon {
    width: 40px; height: 40px;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    color: white;
    backdrop-filter: blur(8px);
  }
  .brand-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: white;
    letter-spacing: -0.3px;
  }
  .hero-headline {
    font-family: var(--serif);
    font-size: 2.4rem;
    line-height: 1.2;
    color: white;
    margin-bottom: 48px;
  }
  .hero-headline em {
    font-style: italic;
    color: rgba(255,255,255,0.7);
  }

  .feature-list { display: flex; flex-direction: column; gap: 20px; }
  .feature-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    animation: fadeUp 0.5s ease both;
  }
  .feature-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    backdrop-filter: blur(8px);
  }
  .feature-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: white;
    margin-bottom: 3px;
  }
  .feature-desc {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.55);
    line-height: 1.5;
  }

  .hero-blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    z-index: 1;
    pointer-events: none;
  }
  .hero-blob-1 {
    width: 350px; height: 350px;
    background: rgba(96,165,250,0.12);
    top: -100px; right: -100px;
  }
  .hero-blob-2 {
    width: 250px; height: 250px;
    background: rgba(167,139,250,0.1);
    bottom: -60px; left: -60px;
  }

  /* FORM PANEL */
  .form-panel {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 80px 40px 40px;
    background: var(--bg);
  }
  .form-box {
    width: 100%;
    max-width: 400px;
    animation: fadeUp 0.4s ease both;
  }
  .form-header { margin-bottom: 32px; }
  .form-title {
    font-size: 1.9rem;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.5px;
    margin-bottom: 6px;
  }
  .form-subtitle {
    font-size: 0.875rem;
    color: var(--text-2);
  }

  /* FORM ELEMENTS */
  .form { display: flex; flex-direction: column; gap: 18px; margin-bottom: 24px; }

  .field { display: flex; flex-direction: column; gap: 6px; }
  .label {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-2);
    letter-spacing: 0.2px;
  }

  .input-wrap {
    position: relative;
    display: flex;
    align-items: center;
  }
  .input-icon {
    position: absolute;
    left: 12px;
    color: var(--text-3);
    display: flex;
    pointer-events: none;
    transition: color var(--t);
  }
  .rtl .input-icon { left: auto; right: 12px; }
  .eye-btn {
    position: absolute;
    right: 12px;
    background: none;
    border: none;
    color: var(--text-3);
    cursor: pointer;
    display: flex;
    padding: 0;
    transition: color var(--t);
  }
  .eye-btn:hover { color: var(--accent); }
  .rtl .eye-btn { right: auto; left: 12px; }

  .input {
    width: 100%;
    padding: 11px 40px;
    border-radius: var(--r);
    border: 1.5px solid var(--border);
    background: var(--input-bg);
    color: var(--text);
    font-family: var(--font);
    font-size: 0.875rem;
    outline: none;
    transition: border-color var(--t), box-shadow var(--t);
  }
  .input::placeholder { color: var(--text-3); }
  .input:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-glow);
  }
  .input-wrap:focus-within .input-icon { color: var(--accent); }

  .form-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .check-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.8rem;
    color: var(--text-2);
    cursor: pointer;
    user-select: none;
  }
  .check { display: none; }
  .check-box {
    width: 16px; height: 16px;
    border-radius: 4px;
    border: 1.5px solid var(--border);
    background: var(--input-bg);
    position: relative;
    transition: all var(--t);
    flex-shrink: 0;
  }
  .check:checked + .check-box {
    background: var(--accent);
    border-color: var(--accent);
  }
  .check:checked + .check-box::after {
    content: '';
    position: absolute;
    left: 4px; top: 1px;
    width: 5px; height: 9px;
    border: 2px solid white;
    border-top: none;
    border-left: none;
    transform: rotate(45deg);
  }
  .text-btn {
    background: none; border: none;
    font-family: var(--font);
    font-size: 0.8rem;
    color: var(--accent);
    cursor: pointer;
    font-weight: 500;
    padding: 0;
  }
  .text-btn:hover { text-decoration: underline; }

  .submit-btn {
    width: 100%;
    padding: 13px;
    border-radius: var(--r);
    border: none;
    background: var(--accent);
    color: white;
    font-family: var(--font);
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    transition: all var(--t);
    letter-spacing: 0.2px;
    box-shadow: 0 4px 20px var(--accent-glow);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    min-height: 46px;
  }
  .submit-btn:hover:not(:disabled) {
    background: var(--accent-h);
    transform: translateY(-1px);
    box-shadow: 0 6px 24px var(--accent-glow);
  }
  .submit-btn:active:not(:disabled) { transform: translateY(0); }
  .submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }

  .switch-text {
    text-align: center;
    font-size: 0.85rem;
    color: var(--text-2);
    margin-bottom: 20px;
  }
  .link-btn {
    background: none; border: none;
    font-family: var(--font);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--accent);
    cursor: pointer;
    padding: 0;
  }
  .link-btn:hover { text-decoration: underline; }

  .secure-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    font-size: 0.72rem;
    color: var(--text-3);
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }`;
