import { useState, useRef, useEffect } from "react";

const MOCK_RESPONSES = {
    en: [
        "To **register a startup in Tunisia**, follow these steps:\n\n1. **Choose your legal structure** (SARL, SA, SUARL, etc.)\n2. **Reserve your company name** at INNORPI (Institut National de la Normalisation)\n3. **Draft the company statutes** with a notary\n4. **Deposit capital** at a Tunisian bank\n5. **Register at the RNE** (Registre National des Entreprises)\n\nThe full process typically takes **3–7 business days**. The minimum capital for a SARL is 1,000 TND.",
        "**CNSS Employer Registration** is mandatory within **30 days** of hiring your first employee.\n\nRequired documents:\n- Company tax ID (Matricule Fiscal)\n- Employment contract copy\n- Employee's CIN (national ID)\n- D0 registration form\n\nSubmit at your local **CNSS regional office**. Registration is free of charge.",
        "For **monthly CNSS declarations**, employers must:\n\n- Submit **Form D1** each month detailing employee salaries\n- Deadline: **28th of each month**\n- Contribution rate: **~25.75%** of gross salary (shared employer/employee)\n- Late penalty: **1% per month** on unpaid amounts\n\nDeclarations can now be submitted online via the CNSS portal.",
    ],
    fr: [
        "Pour **créer une startup en Tunisie**, suivez ces étapes :\n\n1. **Choisir la forme juridique** (SARL, SA, SUARL, etc.)\n2. **Réserver le nom** à l'INNORPI\n3. **Rédiger les statuts** chez un notaire\n4. **Déposer le capital** dans une banque tunisienne\n5. **S'immatriculer au RNE**\n\nLe processus prend généralement **3 à 7 jours ouvrables**. Le capital minimum pour une SARL est de 1 000 TND.",
        "**L'affiliation CNSS employeur** est obligatoire dans les **30 jours** suivant l'embauche du premier salarié.\n\nDocuments requis :\n- Matricule fiscal de l'entreprise\n- Copie du contrat de travail\n- CIN de l'employé\n- Formulaire D0\n\nDépôt à l'**agence CNSS** de votre région. L'inscription est gratuite.",
        "Pour les **déclarations mensuelles CNSS** :\n\n- Soumettre le **formulaire D1** chaque mois\n- Date limite : **28 du mois**\n- Taux de cotisation : **~25,75%** du salaire brut\n- Pénalité de retard : **1% par mois**\n\nLes déclarations peuvent maintenant être soumises en ligne.",
    ],
    dar: [
        "باش **تسجل startup في تونس**، اتبع هاذي الخطوات:\n\n1. **اختار الشكل القانوني** (SARL، SA، SUARL...)\n2. **احجز اسم الشركة** في INNORPI\n3. **اكتب القانون الأساسي** عند الكاتب العدل\n4. **ودّع رأس المال** في بنك تونسي\n5. **سجّل في RNE**\n\nالعملية تاخذ عادةً **3 لـ7 أيام عمل**. رأس المال الأدنى للـ SARL هو 1000 دينار.",
        "**التسجيل في CNSS كمشغّل** إجباري في **30 يوم** من أول يوم توظيف.\n\nالوثائق المطلوبة:\n- الرقم الجبائي للشركة\n- نسخة من عقد العمل\n- بطاقة تعريف الموظف\n- استمارة D0\n\nقدّمها في **وكالة CNSS** القريبة منك. التسجيل مجاني.",
        "للـ **التصريح الشهري في CNSS**:\n\n- قدّم **استمارة D1** كل شهر\n- الأجل: **28 من كل شهر**\n- نسبة الاشتراك: **~25.75%** من الأجر الإجمالي\n- غرامة التأخير: **1% في الشهر**\n\nيمكنك التصريح أونلاين على بوابة CNSS.",
    ],
};

const SUGGESTIONS = {
    en: ["How to register a startup?", "CNSS employer obligations", "Employee declaration steps", "Required documents for RNE", "Minimum capital for SARL"],
    fr: ["Comment créer une startup ?", "Obligations CNSS employeur", "Étapes déclaration employé", "Documents requis pour le RNE", "Capital minimum pour SARL"],
    dar: ["كيفاش نسجل startup؟", "التزامات CNSS المشغّل", "خطوات التصريح للموظف", "وثائق الـ RNE", "رأس المال الأدنى للـ SARL"],
};

const T = {
    en: { newChat: "New Chat", today: "Today", procedures: "Categories", startup: "Startup Creation", cnssEmp: "CNSS Employer", cnssEmployee: "CNSS Employee", analytics: "Analytics", settings: "Settings", placeholder: "Ask about startup or CNSS procedures...", send: "Send", typing: "Thinking...", suggested: "Suggested questions", logout: "Sign out", online: "AI Online", hint: "Press Enter to send · Shift+Enter for new line", welcome: "Hello! I'm your AI assistant for Tunisian startup and CNSS procedures.", welcomeSub: "Ask me anything about company registration, CNSS obligations, or legal requirements.", darkMode: "Dark mode", lightMode: "Light mode" },
    fr: { newChat: "Nouvelle conv.", today: "Aujourd'hui", procedures: "Catégories", startup: "Création Startup", cnssEmp: "CNSS Employeur", cnssEmployee: "CNSS Employé", analytics: "Analytiques", settings: "Paramètres", placeholder: "Posez votre question sur la startup ou le CNSS...", send: "Envoyer", typing: "Réflexion...", suggested: "Questions suggérées", logout: "Déconnexion", online: "IA En ligne", hint: "Entrée pour envoyer · Maj+Entrée pour nouvelle ligne", welcome: "Bonjour ! Je suis votre assistant IA pour les procédures startup et CNSS en Tunisie.", welcomeSub: "Posez-moi toutes vos questions sur l'enregistrement d'entreprise ou les obligations CNSS.", darkMode: "Mode sombre", lightMode: "Mode clair" },
    dar: { newChat: "محادثة جديدة", today: "اليوم", procedures: "التصنيفات", startup: "تأسيس Startup", cnssEmp: "CNSS مشغّل", cnssEmployee: "CNSS موظف", analytics: "الإحصائيات", settings: "الإعدادات", placeholder: "اسأل على إجراءات الـ Startup أو الـ CNSS...", send: "ارسل", typing: "يفكر...", suggested: "أسئلة مقترحة", logout: "خروج", online: "الذكاء متصل", hint: "Enter للإرسال · Shift+Enter لسطر جديد", welcome: "مرحبا! أنا مساعدك الذكي لإجراءات الـ Startup والـ CNSS في تونس.", welcomeSub: "اسألني على تسجيل الشركات أو التزامات CNSS أو المتطلبات القانونية.", darkMode: "وضع داكن", lightMode: "وضع فاتح" },
};

function parseMarkdown(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n\n/g, "</p><p>")
        .replace(/\n(\d+)\./g, "<br/>$1.")
        .replace(/\n-/g, "<br/>•");
}

export default function Chat({ onNavigate, lang, dark, toggleDark, setLang }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [typing, setTyping] = useState(false);
    const [started, setStarted] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const bottomRef = useRef(null);
    const textareaRef = useRef(null);
    const t = T[lang];
    const isRtl = lang === "dar";

    useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, typing]);

    const send = (text) => {
        const msg = (text || input).trim();
        if (!msg) return;
        setInput("");
        setStarted(true);
        if (textareaRef.current) { textareaRef.current.style.height = "auto"; }

        setMessages(m => [...m, { role: "user", text: msg, ts: now() }]);
        setTyping(true);

        setTimeout(() => {
            const pool = MOCK_RESPONSES[lang];
            const reply = pool[Math.floor(Math.random() * pool.length)];
            setTyping(false);
            setMessages(m => [...m, { role: "bot", text: reply, ts: now() }]);
        }, 1000 + Math.random() * 1000);
    };

    const now = () => new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

    const handleKey = (e) => {
        if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
    };

    const autoResize = () => {
        const ta = textareaRef.current;
        if (ta) { ta.style.height = "auto"; ta.style.height = Math.min(ta.scrollHeight, 130) + "px"; }
    };

    const catColors = ["#3b82f6", "#8b5cf6", "#06b6d4"];

    return (
        <div className={`chat-root ${dark ? "dark" : "light"} ${isRtl ? "rtl" : ""}`}>
            <style>{css}</style>

            {/* Mobile sidebar overlay */}
            {sidebarOpen && <div className="overlay" onClick={() => setSidebarOpen(false)} />}

            {/* ── Sidebar ── */}
            <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
                <div className="sb-top">
                    <div className="sb-logo">
                        <div className="sb-logo-icon"><BotSVG /></div>
                        <span className="sb-logo-text">StartupTN</span>
                    </div>
                    <button className="sb-new" onClick={() => { setMessages([]); setStarted(false); setSidebarOpen(false); }}>
                        <PlusSVG /> {t.newChat}
                    </button>
                </div>

                <div className="sb-section">
                    <div className="sb-section-label">{t.today}</div>
                    {["Startup registration steps", "CNSS employer guide", "RNE documents list"].map((item, i) => (
                        <div key={i} className={`sb-item ${i === 0 ? "sb-item-active" : ""}`}>{item}</div>
                    ))}
                </div>

                <div className="sb-section">
                    <div className="sb-section-label">{t.procedures}</div>
                    {[t.startup, t.cnssEmp, t.cnssEmployee].map((cat, i) => (
                        <div key={i} className="sb-cat">
                            <div className="sb-cat-dot" style={{ background: catColors[i] }} />
                            {cat}
                        </div>
                    ))}
                </div>

                <div className="sb-section">
                    <div className="sb-item sb-item-icon"><ChartSVG /> {t.analytics}</div>
                    <div className="sb-item sb-item-icon"><SettingsSVG /> {t.settings}</div>
                </div>

                <div className="sb-bottom">
                    <div className="sb-user">
                        <div className="avatar">A</div>
                        <div className="user-info">
                            <div className="user-name">Ahmed Ben Ali</div>
                            <div className="user-email">ahmed@example.com</div>
                        </div>
                        <button className="icon-btn sb-logout" onClick={() => onNavigate("signin")} title={t.logout}>
                            <LogoutSVG />
                        </button>
                    </div>
                </div>
            </aside>

            {/* ── Main ── */}
            <div className="chat-main">
                {/* Header */}
                <header className="chat-header">
                    <button className="hamburger" onClick={() => setSidebarOpen(s => !s)}><MenuSVG /></button>
                    <div className="header-center">
                        <div className="header-title">StartupTN</div>
                        <div className="online-badge"><div className="online-dot" />{t.online}</div>
                    </div>
                    <div className="header-right">
                        <div className="lang-pills">
                            {[["en", "EN"], ["fr", "FR"], ["dar", "ع"]].map(([code, label]) => (
                                <button key={code} className={`pill ${lang === code ? "pill-active" : ""}`} onClick={() => setLang(code)}>{label}</button>
                            ))}
                        </div>
                        <button className="theme-toggle" onClick={toggleDark} title={dark ? t.lightMode : t.darkMode}>
                            {dark ? <SunSVG /> : <MoonSVG />}
                        </button>
                    </div>
                </header>

                {/* Messages */}
                <div className="messages-area">
                    {!started ? (
                        <div className="welcome-screen">
                            <div className="welcome-bot-icon"><BotSVG /></div>
                            <h2 className="welcome-title">{t.welcome}</h2>
                            <p className="welcome-sub">{t.welcomeSub}</p>
                            <div className="chips-label">{t.suggested}</div>
                            <div className="chips">
                                {SUGGESTIONS[lang].map((q, i) => (
                                    <button key={i} className="chip" onClick={() => send(q)} style={{ animationDelay: `${i * 0.07}s` }}>{q}</button>
                                ))}
                            </div>
                        </div>
                    ) : (
                        <>
                            {messages.map((msg, i) => (
                                <div key={i} className={`msg-row ${msg.role} fade-in`}>
                                    <div className={`msg-avatar ${msg.role}`}>
                                        {msg.role === "bot" ? <BotSVG /> : <UserSVG />}
                                    </div>
                                    <div className="msg-body">
                                        <div
                                            className={`bubble ${msg.role}`}
                                            dangerouslySetInnerHTML={{ __html: `<p>${parseMarkdown(msg.text)}</p>` }}
                                        />
                                        <div className="msg-ts">{msg.ts}</div>
                                    </div>
                                </div>
                            ))}

                            {typing && (
                                <div className="msg-row bot fade-in">
                                    <div className="msg-avatar bot"><BotSVG /></div>
                                    <div className="msg-body">
                                        <div className="bubble bot typing-bubble">
                                            <div className="typing-dots">
                                                <div className="dot" /><div className="dot" /><div className="dot" />
                                            </div>
                                        </div>
                                        <div className="msg-ts">{t.typing}</div>
                                    </div>
                                </div>
                            )}
                            <div ref={bottomRef} />
                        </>
                    )}
                </div>

                {/* Quick suggestions after first message */}
                {started && messages.length > 0 && messages.length < 4 && (
                    <div className="quick-chips">
                        {SUGGESTIONS[lang].slice(0, 3).map((q, i) => (
                            <button key={i} className="chip chip-sm" onClick={() => send(q)}>{q}</button>
                        ))}
                    </div>
                )}

                {/* Input */}
                <div className="input-area">
                    <div className="input-box">
                        <textarea
                            ref={textareaRef}
                            rows={1}
                            placeholder={t.placeholder}
                            value={input}
                            onChange={e => { setInput(e.target.value); autoResize(); }}
                            onKeyDown={handleKey}
                            dir={isRtl ? "rtl" : "ltr"}
                            className="input-ta"
                        />
                        <div className="input-actions">
                            <button className="icon-btn mic-btn"><MicSVG /></button>
                            <button
                                className={`send-btn ${input.trim() ? "active" : ""}`}
                                onClick={() => send()}
                                disabled={!input.trim()}
                                title={t.send}
                            >
                                <SendSVG />
                            </button>
                        </div>
                    </div>
                    <div className="input-hint">{t.hint}</div>
                </div>
            </div>
        </div>
    );
}

const BotSVG = () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="11" rx="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /><circle cx="9" cy="16" r="1" fill="currentColor" /><circle cx="15" cy="16" r="1" fill="currentColor" /></svg>;
const UserSVG = () => <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" /></svg>;
const PlusSVG = () => <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" /></svg>;
const SendSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" /></svg>;
const MicSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" /><path d="M19 10v2a7 7 0 0 1-14 0v-2" /><line x1="12" y1="19" x2="12" y2="23" /><line x1="8" y1="23" x2="16" y2="23" /></svg>;
const LogoutSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><polyline points="16 17 21 12 16 7" /><line x1="21" y1="12" x2="9" y2="12" /></svg>;
const ChartSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" /><line x1="6" y1="20" x2="6" y2="14" /></svg>;
const SettingsSVG = () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" /></svg>;
const MenuSVG = () => <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="18" x2="21" y2="18" /></svg>;
const SunSVG = () => <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="5" /><line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" /><line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" /><line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" /><line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" /></svg>;
const MoonSVG = () => <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" /></svg>;

const css = `
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  .chat-root {
    --font: 'Plus Jakarta Sans', sans-serif;
    --r: 12px; --r-sm: 8px; --r-lg: 18px;
    --t: 0.18s ease;
    --sb-width: 260px;
    font-family: var(--font);
    display: grid;
    grid-template-columns: var(--sb-width) 1fr;
    height: 100vh;
    overflow: hidden;
  }
  .light {
    --bg: #f0f4ff; --card: #ffffff; --sb-bg: #ffffff;
    --text: #0f172a; --text-2: #475569; --text-3: #94a3b8;
    --border: rgba(37,99,235,0.12); --input-bg: #f4f7ff;
    --accent: #2563eb; --accent-h: #1d4ed8; --accent-glow: rgba(37,99,235,0.2);
    --bubble-bot: #f0f4ff; --bubble-user: #2563eb;
    --bubble-bot-border: rgba(37,99,235,0.1);
    background: var(--bg); color: var(--text);
  }
  .dark {
    --bg: #060d1f; --card: #0d1628; --sb-bg: #080f20;
    --text: #e2e8f0; --text-2: #94a3b8; --text-3: #475569;
    --border: rgba(99,148,255,0.1); --input-bg: #0d1628;
    --accent: #3b82f6; --accent-h: #2563eb; --accent-glow: rgba(59,130,246,0.25);
    --bubble-bot: #0f1e3d; --bubble-user: #2563eb;
    --bubble-bot-border: rgba(59,130,246,0.12);
    background: var(--bg); color: var(--text);
  }

  /* ── Sidebar ── */
  .sidebar {
    background: var(--sb-bg);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 0;
    transition: transform 0.25s ease;
    flex-shrink: 0;
  }
  .sidebar::-webkit-scrollbar { width: 0; }

  @media (max-width: 860px) {
    .chat-root { grid-template-columns: 1fr; }
    .sidebar {
      position: fixed; top: 0; left: 0; z-index: 200;
      width: var(--sb-width);
      transform: translateX(-100%);
      box-shadow: 4px 0 24px rgba(0,0,0,0.15);
    }
    .sidebar.open { transform: translateX(0); }
    .rtl .sidebar { left: auto; right: 0; transform: translateX(100%); }
    .rtl .sidebar.open { transform: translateX(0); }
  }
  .overlay {
    position: fixed; inset: 0; z-index: 190;
    background: rgba(0,0,0,0.4);
    backdrop-filter: blur(2px);
  }

  .sb-top { padding: 20px 14px 14px; display: flex; flex-direction: column; gap: 12px; }
  .sb-logo { display: flex; align-items: center; gap: 10px; padding: 0 4px; }
  .sb-logo-icon { width: 32px; height: 32px; background: linear-gradient(135deg, #2563eb, #1d4ed8); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0; }
  .sb-logo-text { font-size: 1rem; font-weight: 700; color: var(--text); letter-spacing: -0.3px; }

  .sb-new { display: flex; align-items: center; gap: 8px; padding: 9px 14px; border-radius: var(--r); background: var(--accent); color: white; border: none; font-family: var(--font); font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: background var(--t); }
  .sb-new:hover { background: var(--accent-h); }

  .sb-section { padding: 10px 8px; border-top: 1px solid var(--border); margin-top: 4px; }
  .sb-section-label { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: var(--text-3); padding: 6px 6px 8px; }
  .sb-item { padding: 8px 10px; border-radius: var(--r-sm); font-size: 0.8rem; color: var(--text-2); cursor: pointer; transition: all var(--t); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .sb-item:hover { background: var(--input-bg); color: var(--text); }
  .sb-item-active { background: rgba(37,99,235,0.08); color: var(--accent); font-weight: 500; }
  .sb-item-icon { display: flex; align-items: center; gap: 8px; }
  .sb-cat { display: flex; align-items: center; gap: 10px; padding: 8px 10px; border-radius: var(--r-sm); font-size: 0.8rem; color: var(--text-2); cursor: pointer; transition: all var(--t); }
  .sb-cat:hover { background: var(--input-bg); color: var(--text); }
  .sb-cat-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }

  .sb-bottom { margin-top: auto; padding: 12px; border-top: 1px solid var(--border); }
  .sb-user { display: flex; align-items: center; gap: 10px; padding: 8px; border-radius: var(--r); cursor: pointer; transition: background var(--t); }
  .sb-user:hover { background: var(--input-bg); }
  .avatar { width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #3b82f6, #1d4ed8); display: flex; align-items: center; justify-content: center; color: white; font-size: 0.78rem; font-weight: 700; flex-shrink: 0; }
  .user-info { flex: 1; min-width: 0; }
  .user-name { font-size: 0.8rem; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .user-email { font-size: 0.68rem; color: var(--text-3); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .sb-logout { color: var(--text-3) !important; }
  .sb-logout:hover { color: #ef4444 !important; background: rgba(239,68,68,0.08) !important; }

  /* ── Main ── */
  .chat-main { display: flex; flex-direction: column; height: 100vh; overflow: hidden; }

  .chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 20px;
    border-bottom: 1px solid var(--border);
    background: var(--card);
    gap: 12px;
    flex-shrink: 0;
    min-height: 60px;
  }
  .hamburger { background: none; border: none; color: var(--text-2); cursor: pointer; display: flex; padding: 4px; border-radius: var(--r-sm); transition: all var(--t); }
  .hamburger:hover { background: var(--input-bg); color: var(--text); }
  @media (min-width: 861px) { .hamburger { display: none; } }

  .header-center { display: flex; flex-direction: column; align-items: center; flex: 1; }
  .header-title { font-size: 0.9rem; font-weight: 700; color: var(--text); letter-spacing: -0.2px; }
  .online-badge { display: flex; align-items: center; gap: 5px; font-size: 0.68rem; color: var(--text-3); }
  .online-dot { width: 6px; height: 6px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 0 2px rgba(34,197,94,0.2); animation: pulse 2s infinite; }
  @keyframes pulse { 0%,100%{opacity:1}50%{opacity:0.5} }

  .header-right { display: flex; align-items: center; gap: 8px; }
  .lang-pills { display: flex; background: var(--input-bg); border: 1px solid var(--border); border-radius: 24px; padding: 3px; gap: 2px; }
  .pill { padding: 4px 10px; border-radius: 18px; border: none; background: none; font-family: var(--font); font-size: 0.72rem; font-weight: 600; color: var(--text-2); cursor: pointer; transition: all var(--t); }
  .pill-active { background: var(--accent); color: white; }
  .theme-toggle { width: 34px; height: 34px; border-radius: 50%; border: 1px solid var(--border); background: var(--input-bg); color: var(--text-2); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all var(--t); }
  .theme-toggle:hover { color: var(--accent); border-color: var(--accent); }

  /* ── Messages ── */
  .messages-area { flex: 1; overflow-y: auto; padding: 28px 20px; display: flex; flex-direction: column; gap: 16px; scroll-behavior: smooth; }
  .messages-area::-webkit-scrollbar { width: 4px; }
  .messages-area::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }

  /* Welcome */
  .welcome-screen { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 20px; margin: auto; max-width: 540px; width: 100%; }
  .welcome-bot-icon { width: 52px; height: 52px; border-radius: 14px; background: linear-gradient(135deg, #2563eb, #1d4ed8); display: flex; align-items: center; justify-content: center; color: white; margin: 0 auto 18px; box-shadow: 0 8px 24px var(--accent-glow); }
  .welcome-bot-icon svg { width: 24px; height: 24px; }
  .welcome-title { font-size: 0.95rem; font-weight: 600; color: var(--text); margin-bottom: 8px; line-height: 1.5; }
  .welcome-sub { font-size: 0.85rem; color: var(--text-2); margin-bottom: 28px; line-height: 1.6; }
  .chips-label { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: var(--text-3); margin-bottom: 12px; }
  .chips { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; }
  .chip { padding: 8px 14px; border-radius: 20px; border: 1.5px solid var(--border); background: var(--card); color: var(--text-2); font-family: var(--font); font-size: 0.8rem; cursor: pointer; transition: all var(--t); animation: fadeUp 0.4s ease both; }
  .chip:hover { border-color: var(--accent); color: var(--accent); background: rgba(37,99,235,0.05); }
  .chip-sm { padding: 6px 12px; font-size: 0.76rem; }

  /* Message rows */
  .msg-row { display: flex; gap: 10px; align-items: flex-end; max-width: 680px; }
  .msg-row.user { flex-direction: row-reverse; margin-left: auto; }
  .msg-row.bot { margin-right: auto; }
  .rtl .msg-row.user { flex-direction: row; margin-right: auto; margin-left: 0; }
  .rtl .msg-row.bot { flex-direction: row-reverse; }

  .msg-avatar { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-bottom: 18px; }
  .msg-avatar.bot { background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; }
  .msg-avatar.user { background: var(--input-bg); color: var(--text-2); border: 1.5px solid var(--border); }

  .msg-body { display: flex; flex-direction: column; gap: 3px; max-width: calc(100% - 40px); }
  .msg-row.user .msg-body { align-items: flex-end; }
  .msg-row.bot .msg-body { align-items: flex-start; }

  .bubble { padding: 12px 16px; border-radius: 16px; font-size: 0.875rem; line-height: 1.6; }
  .bubble.user { background: var(--bubble-user); color: white; border-bottom-right-radius: 4px; }
  .bubble.bot { background: var(--bubble-bot); color: var(--text); border: 1px solid var(--bubble-bot-border); border-bottom-left-radius: 4px; }
  .rtl .bubble.user { border-bottom-right-radius: 16px; border-bottom-left-radius: 4px; }
  .rtl .bubble.bot { border-bottom-left-radius: 16px; border-bottom-right-radius: 4px; }
  .bubble p { margin-bottom: 6px; } .bubble p:last-child { margin-bottom: 0; }
  .bubble strong { font-weight: 700; }

  .typing-bubble { min-width: 60px; }
  .typing-dots { display: flex; gap: 5px; align-items: center; height: 18px; }
  .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--text-3); animation: bounce 1.2s infinite; }
  .dot:nth-child(2) { animation-delay: 0.2s; }
  .dot:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce { 0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-6px)} }

  .msg-ts { font-size: 0.67rem; color: var(--text-3); }

  /* Quick chips */
  .quick-chips { padding: 0 20px 12px; display: flex; gap: 7px; flex-wrap: wrap; flex-shrink: 0; }

  /* Input */
  .input-area { padding: 14px 20px 18px; border-top: 1px solid var(--border); background: var(--card); flex-shrink: 0; }
  .input-box { display: flex; align-items: flex-end; gap: 8px; padding: 10px 10px 10px 16px; border-radius: var(--r-lg); border: 1.5px solid var(--border); background: var(--input-bg); transition: border-color var(--t), box-shadow var(--t); }
  .input-box:focus-within { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-glow); }
  .input-ta { flex: 1; background: none; border: none; outline: none; resize: none; font-family: var(--font); font-size: 0.875rem; color: var(--text); line-height: 1.5; max-height: 130px; padding: 2px 0; }
  .input-ta::placeholder { color: var(--text-3); }
  .input-actions { display: flex; gap: 5px; align-items: center; padding-bottom: 2px; }
  .icon-btn { width: 34px; height: 34px; border-radius: var(--r-sm); border: none; background: none; color: var(--text-3); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all var(--t); flex-shrink: 0; }
  .icon-btn:hover { color: var(--accent); background: rgba(37,99,235,0.08); }
  .send-btn { width: 34px; height: 34px; border-radius: var(--r-sm); border: none; background: var(--border); color: var(--text-3); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all var(--t); flex-shrink: 0; }
  .send-btn.active { background: var(--accent); color: white; box-shadow: 0 3px 12px var(--accent-glow); }
  .send-btn.active:hover { background: var(--accent-h); }
  .send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
  .input-hint { font-size: 0.68rem; color: var(--text-3); text-align: center; margin-top: 8px; }
  .rtl .input-hint { direction: rtl; }

  @keyframes fadeUp { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
  .fade-in { animation: fadeUp 0.25s ease both; }
`;