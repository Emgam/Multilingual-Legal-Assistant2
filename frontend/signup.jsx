import { useState } from "react";

export default function SignUp({ onNavigate, lang, dark, toggleDark, setLang }) {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [showPass, setShowPass] = useState(false);
    const [loading, setLoading] = useState(false);
    const [strength, setStrength] = useState(0);

    const t = {
        en: {
            title: "Create account",
            sub: "Join StartupTN — it's free",
            name: "Full name",
            namePh: "Ahmed Ben Ali",
            email: "Email address",
            emailPh: "you@example.com",
            password: "Password",
            confirm: "Confirm password",
            terms: "I agree to the",
            termsLink: "Terms & Privacy Policy",
            btn: "Get Started",
            hasAccount: "Already have an account?",
            login: "Sign in",
            secure: "Your data is protected",
            passWeak: "Weak",
            passFair: "Fair",
            passGood: "Good",
            passStrong: "Strong",
        },
        fr: {
            title: "Créer un compte",
            sub: "Rejoignez StartupTN — c'est gratuit",
            name: "Nom complet",
            namePh: "Ahmed Ben Ali",
            email: "Adresse e-mail",
            emailPh: "vous@exemple.com",
            password: "Mot de passe",
            confirm: "Confirmer le mot de passe",
            terms: "J'accepte les",
            termsLink: "Conditions et Politique de confidentialité",
            btn: "Commencer",
            hasAccount: "Déjà un compte ?",
            login: "Se connecter",
            secure: "Vos données sont protégées",
            passWeak: "Faible",
            passFair: "Moyen",
            passGood: "Bien",
            passStrong: "Fort",
        },
        dar: {
            title: "سجّل حساب جديد",
            sub: "انضم لـ StartupTN — مجاني",
            name: "الاسم الكامل",
            namePh: "أحمد بن علي",
            email: "البريد الإلكتروني",
            emailPh: "you@example.com",
            password: "كلمة السر",
            confirm: "تأكيد كلمة السر",
            terms: "وافق على",
            termsLink: "الشروط وسياسة الخصوصية",
            btn: "ابدأ",
            hasAccount: "عندك حساب؟",
            login: "ادخل",
            secure: "بياناتك محمية",
            passWeak: "ضعيف",
            passFair: "متوسط",
            passGood: "جيد",
            passStrong: "قوي",
        },
    }[lang];

    const isRtl = lang === "dar";

    const checkStrength = (val) => {
        let s = 0;
        if (val.length >= 8) s++;
        if (/[A-Z]/.test(val)) s++;
        if (/[0-9]/.test(val)) s++;
        if (/[^A-Za-z0-9]/.test(val)) s++;
        setStrength(s);
    };

    const strengthLabels = [t.passWeak, t.passFair, t.passGood, t.passStrong];
    const strengthColors = ["#ef4444", "#f97316", "#eab308", "#22c55e"];

    const handleSubmit = (e) => {
        e.preventDefault();
        setLoading(true);
        setTimeout(() => { setLoading(false); onNavigate("chat"); }, 1300);
    };

    return (
        <div className={`root ${dark ? "dark" : "light"} ${isRtl ? "rtl" : ""}`}>
            <style>{css}</style>

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
                {/* Hero */}
                <aside className="hero-panel">
                    <div className="hero-inner">
                        <div className="brand">
                            <div className="brand-icon"><BotSVG /></div>
                            <span className="brand-name">StartupTN</span>
                        </div>
                        <p className="hero-headline">Start your<br /><em>Tunisian journey</em><br />today</p>

                        <div className="steps">
                            {[
                                { n: "01", text: "Create your free account" },
                                { n: "02", text: "Ask about startup or CNSS procedures" },
                                { n: "03", text: "Get instant AI-powered answers" },
                            ].map((s, i) => (
                                <div className="step" key={i} style={{ animationDelay: `${i * 0.12 + 0.2}s` }}>
                                    <div className="step-num">{s.n}</div>
                                    <div className="step-text">{s.text}</div>
                                </div>
                            ))}
                        </div>

                        <div className="hero-blob hero-blob-1" />
                        <div className="hero-blob hero-blob-2" />
                        <div className="hero-grid" />
                    </div>
                </aside>

                {/* Form */}
                <main className="form-panel">
                    <div className="form-box">
                        <div className="form-header">
                            <h1 className="form-title">{t.title}</h1>
                            <p className="form-subtitle">{t.sub}</p>
                        </div>

                        <form onSubmit={handleSubmit} className="form">
                            <div className="field-row">
                                <div className="field">
                                    <label className="label">{t.name}</label>
                                    <div className="input-wrap">
                                        <span className="input-icon"><UserSVG /></span>
                                        <input className="input" type="text" placeholder={t.namePh} value={name}
                                            onChange={e => setName(e.target.value)} dir={isRtl ? "rtl" : "ltr"} required />
                                    </div>
                                </div>
                                <div className="field">
                                    <label className="label">{t.email}</label>
                                    <div className="input-wrap">
                                        <span className="input-icon"><MailSVG /></span>
                                        <input className="input" type="email" placeholder={t.emailPh} value={email}
                                            onChange={e => setEmail(e.target.value)} dir={isRtl ? "rtl" : "ltr"} required />
                                    </div>
                                </div>
                            </div>

                            <div className="field">
                                <label className="label">{t.password}</label>
                                <div className="input-wrap">
                                    <span className="input-icon"><LockSVG /></span>
                                    <input className="input" type={showPass ? "text" : "password"} placeholder="••••••••"
                                        value={password}
                                        onChange={e => { setPassword(e.target.value); checkStrength(e.target.value); }} required />
                                    <button type="button" className="eye-btn" onClick={() => setShowPass(s => !s)}>
                                        {showPass ? <EyeOffSVG /> : <EyeSVG />}
                                    </button>
                                </div>
                                {password && (
                                    <div className="strength-wrap">
                                        <div className="strength-bars">
                                            {[1, 2, 3, 4].map(i => (
                                                <div key={i} className="strength-bar"
                                                    style={{ background: i <= strength ? strengthColors[strength - 1] : "var(--border)" }} />
                                            ))}
                                        </div>
                                        <span className="strength-label" style={{ color: strengthColors[strength - 1] || "var(--text-3)" }}>
                                            {strengthLabels[strength - 1] || ""}
                                        </span>
                                    </div>
                                )}
                            </div>

                            <div className="field">
                                <label className="label">{t.confirm}</label>
                                <div className="input-wrap">
                                    <span className="input-icon"><LockSVG /></span>
                                    <input className="input" type="password" placeholder="••••••••"
                                        value={confirm} onChange={e => setConfirm(e.target.value)} required />
                                    {confirm && (
                                        <span className="match-icon">
                                            {confirm === password ? <CheckSVG /> : <XSVGIcon />}
                                        </span>
                                    )}
                                </div>
                            </div>

                            <label className="terms-label">
                                <input type="checkbox" className="check" required />
                                <span className="check-box" />
                                <span>{t.terms} <button type="button" className="text-btn">{t.termsLink}</button></span>
                            </label>

                            <button type="submit" className={`submit-btn ${loading ? "loading" : ""}`} disabled={loading}>
                                {loading ? <SpinnerSVG /> : t.btn}
                            </button>
                        </form>

                        <p className="switch-text">
                            {t.hasAccount}{" "}
                            <button className="link-btn" onClick={() => onNavigate("signin")}>{t.login}</button>
                        </p>

                        <div className="secure-row">
                            <ShieldSVG />
                            {t.secure}
                        </div>
                    </div>
                </main>
            </div>
        </div>
    );
}

const BotSVG = () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="11" rx="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /><circle cx="9" cy="16" r="1" fill="currentColor" /><circle cx="15" cy="16" r="1" fill="currentColor" /></svg>;
const UserSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" /></svg>;
const MailSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" /><polyline points="22,6 12,13 2,6" /></svg>;
const LockSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /></svg>;
const EyeSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" /></svg>;
const EyeOffSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" /><line x1="1" y1="1" x2="23" y2="23" /></svg>;
const CheckSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2.5"><polyline points="20 6 9 17 4 12" /></svg>;
const XSVGIcon = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ef4444" strokeWidth="2.5"><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg>;
const ShieldSVG = () => <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /></svg>;
const SunSVG = () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="5" /><line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" /><line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" /><line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" /><line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" /></svg>;
const MoonSVG = () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" /></svg>;
const SpinnerSVG = () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" style={{ animation: "spin 0.8s linear infinite" }}><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" /></svg>;

const css = `
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Instrument+Serif:ital@0;1&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  .root {
    --font: 'Plus Jakarta Sans', sans-serif;
    --serif: 'Instrument Serif', serif;
    --r: 12px; --r-sm: 8px;
    --t: 0.18s ease;
    font-family: var(--font);
    min-height: 100vh;
    position: relative;
  }
  .light {
    --bg: #f0f4ff; --card: #ffffff;
    --hero-from: #1e3a8a; --hero-to: #2563eb;
    --text: #0f172a; --text-2: #475569; --text-3: #94a3b8;
    --border: rgba(37,99,235,0.15); --input-bg: #f8faff;
    --accent: #2563eb; --accent-h: #1d4ed8; --accent-glow: rgba(37,99,235,0.25);
    background: var(--bg); color: var(--text);
  }
  .dark {
    --bg: #060d1f; --card: #0d1628;
    --hero-from: #060d1f; --hero-to: #0f1e3d;
    --text: #e2e8f0; --text-2: #94a3b8; --text-3: #475569;
    --border: rgba(99,148,255,0.12); --input-bg: #0f1e3d;
    --accent: #3b82f6; --accent-h: #2563eb; --accent-glow: rgba(59,130,246,0.3);
    background: var(--bg); color: var(--text);
  }

  .top-controls { position: fixed; top: 18px; right: 20px; z-index: 100; display: flex; align-items: center; gap: 8px; }
  .rtl .top-controls { right: auto; left: 20px; }
  .lang-pills { display: flex; background: var(--card); border: 1px solid var(--border); border-radius: 30px; padding: 3px; gap: 2px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
  .pill { padding: 5px 12px; border-radius: 20px; border: none; background: none; font-family: var(--font); font-size: 0.75rem; font-weight: 600; color: var(--text-2); cursor: pointer; transition: all var(--t); }
  .pill-active { background: var(--accent); color: white; }
  .theme-toggle { width: 36px; height: 36px; border-radius: 50%; border: 1px solid var(--border); background: var(--card); color: var(--text-2); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all var(--t); box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
  .theme-toggle:hover { color: var(--accent); border-color: var(--accent); }

  .layout { display: grid; grid-template-columns: 400px 1fr; min-height: 100vh; }
  @media (max-width: 900px) { .layout { grid-template-columns: 1fr; } .hero-panel { display: none; } }

  .hero-panel { background: linear-gradient(160deg, var(--hero-from) 0%, var(--hero-to) 100%); display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; }
  .hero-inner { padding: 60px 40px; position: relative; z-index: 2; width: 100%; }
  .brand { display: flex; align-items: center; gap: 10px; margin-bottom: 40px; }
  .brand-icon { width: 40px; height: 40px; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; }
  .brand-name { font-size: 1.1rem; font-weight: 700; color: white; }
  .hero-headline { font-family: var(--serif); font-size: 2.2rem; line-height: 1.25; color: white; margin-bottom: 48px; }
  .hero-headline em { font-style: italic; color: rgba(255,255,255,0.65); }

  .steps { display: flex; flex-direction: column; gap: 16px; }
  .step { display: flex; align-items: center; gap: 16px; animation: fadeUp 0.5s ease both; }
  .step-num { width: 32px; height: 32px; border-radius: 50%; border: 1.5px solid rgba(255,255,255,0.3); color: rgba(255,255,255,0.8); font-size: 0.72rem; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .step-text { font-size: 0.85rem; color: rgba(255,255,255,0.7); }

  .hero-blob { position: absolute; border-radius: 50%; filter: blur(60px); z-index: 1; pointer-events: none; }
  .hero-blob-1 { width: 300px; height: 300px; background: rgba(96,165,250,0.1); top: -80px; right: -80px; }
  .hero-blob-2 { width: 220px; height: 220px; background: rgba(167,139,250,0.08); bottom: -50px; left: -50px; }
  .hero-grid { position: absolute; inset: 0; z-index: 1; background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px); background-size: 40px 40px; }

  .form-panel { display: flex; align-items: center; justify-content: center; padding: 80px 40px 40px; background: var(--bg); }
  .form-box { width: 100%; max-width: 420px; animation: fadeUp 0.4s ease both; }
  .form-header { margin-bottom: 28px; }
  .form-title { font-size: 1.8rem; font-weight: 800; color: var(--text); letter-spacing: -0.5px; margin-bottom: 5px; }
  .form-subtitle { font-size: 0.875rem; color: var(--text-2); }

  .form { display: flex; flex-direction: column; gap: 16px; margin-bottom: 20px; }

  .field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  @media (max-width: 500px) { .field-row { grid-template-columns: 1fr; } }

  .field { display: flex; flex-direction: column; gap: 6px; }
  .label { font-size: 0.8rem; font-weight: 600; color: var(--text-2); }

  .input-wrap { position: relative; display: flex; align-items: center; }
  .input-icon { position: absolute; left: 12px; color: var(--text-3); display: flex; pointer-events: none; transition: color var(--t); }
  .rtl .input-icon { left: auto; right: 12px; }
  .eye-btn { position: absolute; right: 12px; background: none; border: none; color: var(--text-3); cursor: pointer; display: flex; padding: 0; transition: color var(--t); }
  .eye-btn:hover { color: var(--accent); }
  .match-icon { position: absolute; right: 12px; display: flex; }
  .rtl .eye-btn, .rtl .match-icon { right: auto; left: 12px; }

  .input { width: 100%; padding: 11px 40px; border-radius: var(--r); border: 1.5px solid var(--border); background: var(--input-bg); color: var(--text); font-family: var(--font); font-size: 0.875rem; outline: none; transition: border-color var(--t), box-shadow var(--t); }
  .input::placeholder { color: var(--text-3); }
  .input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-glow); }
  .input-wrap:focus-within .input-icon { color: var(--accent); }

  .strength-wrap { display: flex; align-items: center; gap: 8px; margin-top: 6px; }
  .strength-bars { display: flex; gap: 4px; flex: 1; }
  .strength-bar { height: 3px; flex: 1; border-radius: 2px; transition: background 0.3s; }
  .strength-label { font-size: 0.72rem; font-weight: 600; min-width: 40px; }

  .terms-label { display: flex; align-items: flex-start; gap: 10px; font-size: 0.8rem; color: var(--text-2); cursor: pointer; user-select: none; line-height: 1.5; }
  .check { display: none; }
  .check-box { width: 16px; height: 16px; border-radius: 4px; border: 1.5px solid var(--border); background: var(--input-bg); position: relative; transition: all var(--t); flex-shrink: 0; margin-top: 2px; }
  .check:checked + .check-box { background: var(--accent); border-color: var(--accent); }
  .check:checked + .check-box::after { content: ''; position: absolute; left: 4px; top: 1px; width: 5px; height: 9px; border: 2px solid white; border-top: none; border-left: none; transform: rotate(45deg); }
  .text-btn { background: none; border: none; font-family: var(--font); font-size: 0.8rem; color: var(--accent); cursor: pointer; font-weight: 500; padding: 0; }
  .text-btn:hover { text-decoration: underline; }

  .submit-btn { width: 100%; padding: 13px; border-radius: var(--r); border: none; background: var(--accent); color: white; font-family: var(--font); font-size: 0.9rem; font-weight: 700; cursor: pointer; transition: all var(--t); letter-spacing: 0.2px; box-shadow: 0 4px 20px var(--accent-glow); display: flex; align-items: center; justify-content: center; gap: 8px; min-height: 46px; }
  .submit-btn:hover:not(:disabled) { background: var(--accent-h); transform: translateY(-1px); box-shadow: 0 6px 24px var(--accent-glow); }
  .submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }

  .switch-text { text-align: center; font-size: 0.85rem; color: var(--text-2); margin-bottom: 16px; }
  .link-btn { background: none; border: none; font-family: var(--font); font-size: 0.85rem; font-weight: 600; color: var(--accent); cursor: pointer; padding: 0; }
  .link-btn:hover { text-decoration: underline; }
  .secure-row { display: flex; align-items: center; justify-content: center; gap: 5px; font-size: 0.72rem; color: var(--text-3); }

  @keyframes fadeUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
  @keyframes spin { to { transform: rotate(360deg); } }
`;