import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import re

API_BASE = "https://bi-agent-production.up.railway.app"
st.set_page_config(
    page_title="NEXUS BI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --void: #03050A;
    --abyss: #080C14;
    --panel: #0D1220;
    --surface: #121828;
    --rim: #1A2235;
    --wire: #243048;
    --muted: #3A4A65;
    --ghost: #5A6E90;
    --fog: #8899BB;
    --ice: #C2D0E8;
    --snow: #E8EDF6;
    --acid: #00FFB3;
    --acid-glow: rgba(0,255,179,0.12);
    --plasma: #7B61FF;
    --plasma-glow: rgba(123,97,255,0.12);
    --amber: #FFB830;
    --amber-glow: rgba(255,184,48,0.10);
    --danger: #FF4D6A;
}

html, body, [data-testid="stAppViewContainer"] {
    background: #03050A !important;
    color: #E8EDF6 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stMain"] { background: #03050A !important; }
[data-testid="stHeader"] { background: transparent !important; display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
.stApp { background: #03050A !important; }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
    display: none !important; visibility: hidden !important;
}
[data-testid="block-container"] { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] > div { padding: 0 !important; }

.section-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    color: #00FFB3;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    display: block;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #E8EDF6;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.02em;
}
.section-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    color: #5A6E90;
    margin: 0 0 2.5rem 0;
}
.stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: #243048;
    border: 1px solid #243048;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 3rem;
}
.stat-cell { background: #0D1220; padding: 1.8rem 2rem; text-align: center; }
.stat-num { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800; color: #00FFB3; display: block; line-height: 1; }
.stat-label { font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: 0.15em; color: #5A6E90; text-transform: uppercase; margin-top: 6px; display: block; }
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 2rem; }
.chip { font-family: 'Space Mono', monospace; font-size: 11px; color: #8899BB; border: 1px solid #243048; padding: 6px 14px; border-radius: 20px; background: #0D1220; letter-spacing: 0.02em; }
.terminal-bar-outer { background: #0D1220; border: 1px solid #243048; border-radius: 12px 12px 0 0; overflow: hidden; }
.terminal-bar { background: #121828; border-bottom: 1px solid #243048; padding: 10px 16px; display: flex; align-items: center; gap: 8px; }
.t-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.terminal-label { font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: 0.15em; color: #3A4A65; text-transform: uppercase; margin-left: auto; }
.panel { background: #0D1220; border: 1px solid #243048; border-radius: 12px; overflow: hidden; }
.panel-head { background: #121828; border-bottom: 1px solid #243048; padding: 12px 18px; display: flex; align-items: center; gap: 10px; }
.panel-icon { width: 28px; height: 28px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 13px; }
.panel-icon-acid { background: rgba(0,255,179,0.12); color: #00FFB3; }
.panel-icon-plasma { background: rgba(123,97,255,0.12); color: #7B61FF; }
.panel-icon-amber { background: rgba(255,184,48,0.10); color: #FFB830; }
.panel-title { font-family: 'Space Mono', monospace; font-size: 11px; letter-spacing: 0.12em; color: #8899BB; text-transform: uppercase; }
.panel-body { padding: 18px; }
.sql-block { background: #080C14; border: 1px solid #1A2235; border-radius: 8px; padding: 16px; font-family: 'Space Mono', monospace; font-size: 12px; line-height: 1.7; color: #8899BB; overflow-x: auto; white-space: pre-wrap; word-break: break-word; }
.sql-kw { color: #7B61FF; font-weight: 700; }
.sql-str { color: #FFB830; }
.sql-num { color: #FF8FA3; }
.narration-text { font-family: 'DM Sans', sans-serif; font-size: 15px; font-weight: 300; line-height: 1.85; color: #C2D0E8; letter-spacing: 0.01em; }
.badge { display: inline-flex; align-items: center; gap: 6px; font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: 0.12em; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; }
.badge-safe { background: rgba(0,255,179,0.08); color: #00FFB3; border: 1px solid rgba(0,255,179,0.2); }
.badge-blocked { background: rgba(255,77,106,0.08); color: #FF4D6A; border: 1px solid rgba(255,77,106,0.2); }
.badge-rewritten { background: rgba(255,184,48,0.08); color: #FFB830; border: 1px solid rgba(255,184,48,0.2); }
.log-stream { background: #080C14; border: 1px solid #1A2235; border-radius: 8px; padding: 14px 16px; max-height: 220px; overflow-y: auto; }
.log-line { font-family: 'Space Mono', monospace; font-size: 11px; line-height: 1.9; color: #3A4A65; }
.log-intent { color: #7B61FF; }
.log-llm { color: #4ECDC4; }
.log-validate { color: #8899BB; }
.log-execute { color: #00FFB3; }
.log-narrate { color: #FFB830; }
.log-blocked { color: #FF4D6A; }
.log-retry { color: #FF8FA3; }
.log-error { color: #FF4D6A; }
.meter-wrap { display: flex; align-items: center; gap: 8px; margin-top: 6px; }
.meter-dot { width: 8px; height: 8px; border-radius: 50%; background: #243048; }
.meter-dot-active { background: #00FFB3; box-shadow: 0 0 8px #00FFB3; }
.meter-label { font-family: 'Space Mono', monospace; font-size: 10px; color: #5A6E90; letter-spacing: 0.1em; }
.divider { height: 1px; background: linear-gradient(90deg, transparent, #243048, transparent); margin: 4rem 0; }

[data-testid="stTextInput"] input, .stTextInput input {
    background: #080C14 !important; border: 1px solid #243048 !important;
    border-radius: 6px !important; color: #E8EDF6 !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 16px !important;
    padding: 14px 16px !important; caret-color: #00FFB3;
}
[data-testid="stTextInput"] input:focus {
    border-color: #00FFB3 !important;
    box-shadow: 0 0 0 3px rgba(0,255,179,0.12) !important; outline: none !important;
}
[data-testid="stTextInput"] label {
    color: #5A6E90 !important; font-family: 'Space Mono', monospace !important;
    font-size: 10px !important; letter-spacing: 0.15em !important; text-transform: uppercase !important;
}
.stButton button {
    background: #00FFB3 !important; color: #000 !important; border: none !important;
    border-radius: 4px !important; font-family: 'Space Mono', monospace !important;
    font-size: 12px !important; font-weight: 700 !important; letter-spacing: 0.08em !important;
    padding: 10px 24px !important; width: 100% !important;
}
.stButton button:hover { background: #00e6a0 !important; }
[data-testid="stDataFrame"] { background: #0D1220 !important; }
[data-testid="stDataFrame"] th { background: #121828 !important; color: #5A6E90 !important; font-family: 'Space Mono', monospace !important; font-size: 10px !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }
[data-testid="stDataFrame"] td { color: #C2D0E8 !important; font-family: 'DM Sans', sans-serif !important; font-size: 13px !important; }
[data-testid="stExpander"] { background: #0D1220 !important; border: 1px solid #243048 !important; border-radius: 8px !important; }
[data-testid="stExpander"] summary { font-family: 'Space Mono', monospace !important; font-size: 11px !important; color: #5A6E90 !important; letter-spacing: 0.1em !important; }
[data-testid="stDownloadButton"] button { background: transparent !important; color: #8899BB !important; border: 1px solid #243048 !important; font-size: 11px !important; padding: 8px 16px !important; }
[data-testid="stDownloadButton"] button:hover { border-color: #00FFB3 !important; color: #00FFB3 !important; }
[data-testid="stHorizontalBlock"] { gap: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)


HERO_HTML = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #03050A; overflow: hidden; }
.hero {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; min-height: 520px;
    position: relative; overflow: hidden; padding: 3rem 2rem;
}
.grid-bg {
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(0,255,179,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,179,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    -webkit-mask-image: radial-gradient(ellipse 80% 60% at 50% 50%, black 40%, transparent 100%);
    mask-image: radial-gradient(ellipse 80% 60% at 50% 50%, black 40%, transparent 100%);
}
.orb-1 {
    position: absolute; width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(123,97,255,0.10) 0%, transparent 70%);
    top: -100px; left: -100px; pointer-events: none;
}
.orb-2 {
    position: absolute; width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(0,255,179,0.07) 0%, transparent 70%);
    bottom: -60px; right: -80px; pointer-events: none;
}
.inner { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; }
.badge {
    font-family: 'Space Mono', monospace; font-size: 11px; letter-spacing: 0.18em;
    color: #00FFB3; border: 1px solid rgba(0,255,179,0.25); padding: 6px 18px;
    border-radius: 20px; background: rgba(0,255,179,0.05);
    margin-bottom: 2rem; text-transform: uppercase;
}
.title {
    font-family: 'Syne', sans-serif; font-size: clamp(48px, 10vw, 88px);
    font-weight: 800; line-height: 0.95; letter-spacing: -0.03em; text-align: center;
    background: linear-gradient(135deg, #E8EDF6 0%, #8899BB 60%, #3A4A65 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin-bottom: 0.3rem;
}
.accent {
    font-family: 'Syne', sans-serif; font-size: clamp(48px, 10vw, 88px);
    font-weight: 800; line-height: 0.95; letter-spacing: -0.03em; text-align: center;
    background: linear-gradient(90deg, #00FFB3 0%, #7B61FF 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    display: block; margin-bottom: 1.8rem;
}
.sub {
    font-family: 'DM Sans', sans-serif; font-size: 17px; font-weight: 300;
    color: #5A6E90; text-align: center; max-width: 480px;
    line-height: 1.7; margin-bottom: 2.5rem;
}
.btns { display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center; }
.btn-p {
    font-family: 'Space Mono', monospace; font-size: 12px; letter-spacing: 0.08em;
    background: #00FFB3; color: #000; border: none; padding: 13px 28px;
    border-radius: 4px; cursor: pointer; font-weight: 700;
}
.btn-s {
    font-family: 'Space Mono', monospace; font-size: 12px; letter-spacing: 0.08em;
    background: transparent; color: #8899BB; border: 1px solid #243048;
    padding: 13px 28px; border-radius: 4px; cursor: pointer;
}
.scroll-hint {
    position: absolute; bottom: 1.5rem; left: 50%; transform: translateX(-50%);
    display: flex; flex-direction: column; align-items: center; gap: 6px; opacity: 0.4;
}
.scroll-line {
    width: 1px; height: 36px;
    background: linear-gradient(to bottom, #00FFB3, transparent);
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:0.3} 50%{opacity:1} }
.scroll-label { font-family: 'Space Mono', monospace; font-size: 8px; letter-spacing: 0.2em; color: #00FFB3; text-transform: uppercase; }
</style>
</head>
<body>
<div class="hero">
    <div class="grid-bg"></div>
    <div class="orb-1"></div>
    <div class="orb-2"></div>
    <div class="inner">
        <div class="badge">&#x2B21; Natural Language BI &middot; Powered by LLM + MySQL</div>
        <div class="title">NEXUS</div>
        <span class="accent">INTELLIGENCE</span>
        <p class="sub">Ask anything in plain English. Get validated SQL, live query results, and AI-narrated business insights &mdash; instantly.</p>
        <div class="btns">
            <button class="btn-p">&rarr; Run a Query</button>
            <button class="btn-s">View Schema</button>
        </div>
    </div>
    <div class="scroll-hint">
        <div class="scroll-line"></div>
        <span class="scroll-label">scroll</span>
    </div>
</div>
</body>
</html>
"""

GUARDRAILS_HTML = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #03050A; padding: 0 3rem 2rem; }
.grid {
    display: grid; grid-template-columns: repeat(5, 1fr);
    gap: 1px; background: #243048;
    border: 1px solid #243048; border-radius: 10px; overflow: hidden;
}
.cell { background: #0D1220; padding: 1.4rem 1.2rem; }
.num { font-family: 'Space Mono', monospace; font-size: 22px; font-weight: 700; margin-bottom: 0.5rem; }
.name { font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 600; color: #E8EDF6; margin-bottom: 0.4rem; }
.desc { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #3A4A65; line-height: 1.6; }
</style>
</head>
<body>
<div class="grid">
    <div class="cell">
        <div class="num" style="color:#00FFB3">01</div>
        <div class="name">Intent Guard</div>
        <div class="desc">Regex blocks DROP, DELETE, ALTER, INSERT and other dangerous intents</div>
    </div>
    <div class="cell">
        <div class="num" style="color:#7B61FF">02</div>
        <div class="name">AST Validate</div>
        <div class="desc">sqlglot parses the AST &mdash; only SELECT statements pass</div>
    </div>
    <div class="cell">
        <div class="num" style="color:#FFB830">03</div>
        <div class="name">Table Allowlist</div>
        <div class="desc">Queries only allowed against 4 known schema tables</div>
    </div>
    <div class="cell">
        <div class="num" style="color:#FF8FA3">04</div>
        <div class="name">Length Limit</div>
        <div class="desc">SQL capped at 1,000 chars to block injection payloads</div>
    </div>
    <div class="cell">
        <div class="num" style="color:#4ECDC4">05</div>
        <div class="name">LIMIT Inject</div>
        <div class="desc">LIMIT 100 auto-appended if absent &mdash; no runaway scans</div>
    </div>
</div>
</body>
</html>
"""

CUBE_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#03050A; display:flex; justify-content:center; align-items:center; height:140px; }
.scene { width:80px; height:80px; perspective:300px; }
.cube { width:80px; height:80px; position:relative; transform-style:preserve-3d; animation:spin 8s linear infinite; }
@keyframes spin { from{transform:rotateX(15deg) rotateY(0deg)} to{transform:rotateX(15deg) rotateY(360deg)} }
.face {
    position:absolute; width:80px; height:80px;
    border:1px solid rgba(0,255,179,0.3);
    background:rgba(0,255,179,0.02);
    display:flex; align-items:center; justify-content:center;
    font-family:'Space Mono',monospace; font-size:11px;
    color:rgba(0,255,179,0.5); letter-spacing:0.1em;
}
.front  {transform:rotateY(0deg)   translateZ(40px)}
.back   {transform:rotateY(180deg) translateZ(40px)}
.left   {transform:rotateY(-90deg) translateZ(40px)}
.right  {transform:rotateY(90deg)  translateZ(40px)}
.top    {transform:rotateX(90deg)  translateZ(40px)}
.bottom {transform:rotateX(-90deg) translateZ(40px)}
</style>
</head>
<body>
<div class="scene">
    <div class="cube">
        <div class="face front">SQL</div>
        <div class="face back">BI</div>
        <div class="face left">AI</div>
        <div class="face right">ML</div>
        <div class="face top">&#x2B21;</div>
        <div class="face bottom">NL</div>
    </div>
</div>
</body>
</html>
"""


def colorize_sql(sql: str) -> str:
    kws = r'\b(SELECT|FROM|WHERE|JOIN|LEFT|RIGHT|INNER|OUTER|ON|GROUP\s+BY|ORDER\s+BY|HAVING|LIMIT|AS|AND|OR|NOT|IN|LIKE|IS|NULL|DISTINCT|COUNT|SUM|AVG|MIN|MAX|ROUND|COALESCE|CASE|WHEN|THEN|ELSE|END|WITH|UNION|ALL|BY)\b'
    sql_e = sql.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    sql_e = re.sub(kws, r'<span class="sql-kw">\1</span>', sql_e, flags=re.IGNORECASE)
    sql_e = re.sub(r"'([^']*)'", r'<span class="sql-str">\'\1\'</span>', sql_e)
    sql_e = re.sub(r'\b(\d+(\.\d+)?)\b', r'<span class="sql-num">\1</span>', sql_e)
    return sql_e


def log_class(line: str) -> str:
    l = line.upper()
    if "[INTENT" in l: return "log-intent"
    if "[LLM]" in l: return "log-llm"
    if "[VALIDATE]" in l: return "log-validate"
    if "[EXECUTE]" in l: return "log-execute"
    if "[NARRATE]" in l: return "log-narrate"
    if "[BLOCKED]" in l: return "log-blocked"
    if "[RETRY]" in l: return "log-retry"
    if "[ERROR]" in l or "[FAIL]" in l: return "log-error"
    return ""


def badge_html(status: str) -> str:
    cls = {"SAFE": "badge-safe", "BLOCKED": "badge-blocked", "REWRITTEN": "badge-rewritten"}.get(status, "badge-safe")
    dot = {"SAFE": "●", "BLOCKED": "■", "REWRITTEN": "◆"}.get(status, "●")
    return f'<span class="badge {cls}">{dot} {status}</span>'


# ── HERO ─────────────────────────────────────────────
components.html(HERO_HTML, height=540, scrolling=False)

# ── MAIN CONTENT ─────────────────────────────────────
st.markdown('<div style="padding: 0 3rem;">', unsafe_allow_html=True)

st.markdown("""
<div class="stats-row">
    <div class="stat-cell"><span class="stat-num">5</span><span class="stat-label">Guardrail Layers</span></div>
    <div class="stat-cell"><span class="stat-num">3×</span><span class="stat-label">Auto-Retry on Failure</span></div>
    <div class="stat-cell"><span class="stat-num">4</span><span class="stat-label">Schema Tables</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<span class="section-eyebrow">Query Interface</span>
<h2 class="section-title">Ask your data</h2>
<p class="section-sub">Plain English → Validated SQL → Live Results → AI Insight</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chip-row">
    <span class="chip">Top customers by revenue</span>
    <span class="chip">Monthly order volume 2024</span>
    <span class="chip">Products with low stock</span>
    <span class="chip">Orders by status</span>
    <span class="chip">Average order value by country</span>
    <span class="chip">Best-selling categories</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="terminal-bar-outer">
    <div class="terminal-bar">
        <span class="t-dot" style="background:#FF5F57"></span>
        <span class="t-dot" style="background:#FEBC2E"></span>
        <span class="t-dot" style="background:#28C840"></span>
        <span class="terminal-label">nexus · query terminal</span>
    </div>
</div>
""", unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1])
with col_input:
    question = st.text_input(
        "NATURAL LANGUAGE QUERY",
        placeholder="e.g.  What are the top 5 customers by total spend?",
        key="question_input",
        label_visibility="visible"
    )
with col_btn:
    st.markdown('<div style="padding-top:1.85rem;">', unsafe_allow_html=True)
    run_clicked = st.button("⬡  RUN", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── EXECUTION ────────────────────────────────────────
if run_clicked and question.strip():
    with st.spinner(""):
        try:
            res = requests.post(f"{API_BASE}/ask", json={"question": question.strip()}, timeout=30)
        except requests.exceptions.ConnectionError:
            st.markdown("""
            <div class="panel" style="padding:2rem; margin-top:1.5rem;">
                <span style="color:#FF4D6A; font-family:'Space Mono',monospace; font-size:12px;">
                    CONNECTION ERROR — Backend not reachable at localhost:8000<br>
                    <span style="color:#3A4A65;">Start the FastAPI server: python -m uvicorn backend.main:app --reload</span>
                </span>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

    if res.status_code == 200:
        data = res.json()
        sql = data.get("sql", "")
        cols = data.get("columns", [])
        results = data.get("results", [])
        narration = data.get("narration", "")
        status = data.get("guardrail_status", "SAFE")
        logs = data.get("logs", [])
        attempts = data.get("attempts", 1)

        meta_cols = st.columns([3, 1, 1])
        with meta_cols[0]:
            st.markdown('<span style="font-family:\'Space Mono\',monospace; font-size:10px; color:#5A6E90;">QUERY COMPLETE</span>', unsafe_allow_html=True)
        with meta_cols[1]:
            st.markdown(badge_html(status), unsafe_allow_html=True)
        with meta_cols[2]:
            dots_html = "".join([
                f'<div class="meter-dot {"meter-dot-active" if i < attempts else ""}"></div>'
                for i in range(3)
            ])
            st.markdown(f'<div class="meter-wrap">{dots_html}<span class="meter-label">{attempts}/3 attempt{"s" if attempts > 1 else ""}</span></div>', unsafe_allow_html=True)

        st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="panel">
                <div class="panel-head">
                    <div class="panel-icon panel-icon-plasma">&#x2387;</div>
                    <span class="panel-title">Generated SQL</span>
                </div>
                <div class="panel-body">
                    <div class="sql-block">{colorize_sql(sql)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            narration_formatted = narration.replace("\n", "<br>")
            st.markdown(f"""
            <div class="panel">
                <div class="panel-head">
                    <div class="panel-icon panel-icon-amber">&#x2726;</div>
                    <span class="panel-title">AI Business Insight</span>
                </div>
                <div class="panel-body">
                    <p class="narration-text">{narration_formatted}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

        if results and cols:
            st.markdown(f"""
            <div class="panel">
                <div class="panel-head">
                    <div class="panel-icon panel-icon-acid">&#x25C8;</div>
                    <span class="panel-title">Query Results</span>
                    <span style="margin-left:auto; font-family:'Space Mono',monospace; font-size:10px; color:#3A4A65;">{len(results)} rows</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            df = pd.DataFrame(results, columns=cols)
            st.dataframe(df, use_container_width=True, hide_index=True)

            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(label="↓ Export CSV", data=csv_data, file_name="nexus_results.csv", mime="text/csv", key="dl_csv")

        st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)
        with st.expander("EXECUTION LOGS", expanded=False):
            lines_html = "".join([f'<div class="log-line {log_class(line)}">{line}</div>' for line in logs])
            st.markdown(f'<div class="log-stream">{lines_html}</div>', unsafe_allow_html=True)

    else:
        try:
            err_detail = res.json().get("detail", {})
            err_msg = err_detail.get("message", str(err_detail)) if isinstance(err_detail, dict) else str(err_detail)
            err_status = err_detail.get("guardrail_status", "BLOCKED") if isinstance(err_detail, dict) else "BLOCKED"
            err_logs = err_detail.get("logs", []) if isinstance(err_detail, dict) else []
        except Exception:
            err_msg = res.text
            err_status = "ERROR"
            err_logs = []

        st.markdown(f"""
        <div class="panel" style="margin-top:1.5rem;">
            <div class="panel-head">
                <div class="panel-icon" style="background:rgba(255,77,106,0.1); color:#FF4D6A;">&#x2717;</div>
                <span class="panel-title">Query Blocked</span>
                <span style="margin-left:auto;">{badge_html(err_status)}</span>
            </div>
            <div class="panel-body">
                <p style="font-family:'Space Mono',monospace; font-size:12px; color:#FF4D6A; margin:0;">{err_msg}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if err_logs:
            with st.expander("LOGS", expanded=True):
                lines_html = "".join([f'<div class="log-line {log_class(l)}">{l}</div>' for l in err_logs])
                st.markdown(f'<div class="log-stream">{lines_html}</div>', unsafe_allow_html=True)

elif run_clicked and not question.strip():
    st.markdown('<div style="margin-top:1rem; font-family:\'Space Mono\',monospace; font-size:11px; color:#5A6E90;">Enter a question above to run a query.</div>', unsafe_allow_html=True)

# ── SCHEMA ───────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

components.html(CUBE_HTML, height=140, scrolling=False)

st.markdown("""
<span class="section-eyebrow">Schema Reference</span>
<h2 class="section-title">Data architecture</h2>
<p class="section-sub">Four relational tables — fully validated before every query.</p>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:#243048; border:1px solid #243048; border-radius:10px; overflow:hidden; margin:2rem 0;">
    <div style="background:#0D1220; padding:1.2rem; border-top:2px solid #00FFB3;">
        <div style="font-family:'Space Mono',monospace; font-size:11px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#00FFB3; margin-bottom:0.8rem;">customers</div>
        <div style="font-family:'DM Sans',sans-serif; font-size:11px; color:#3A4A65; line-height:1.8;">
            <span style="color:#8899BB;">&#9658; customer_id</span><br>name<br>email<br>city<br>country<br>created_at
        </div>
    </div>
    <div style="background:#0D1220; padding:1.2rem; border-top:2px solid #7B61FF;">
        <div style="font-family:'Space Mono',monospace; font-size:11px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#7B61FF; margin-bottom:0.8rem;">orders</div>
        <div style="font-family:'DM Sans',sans-serif; font-size:11px; color:#3A4A65; line-height:1.8;">
            <span style="color:#8899BB;">&#9658; order_id</span><br>customer_id<br>order_date<br>status<br>total_amount
        </div>
    </div>
    <div style="background:#0D1220; padding:1.2rem; border-top:2px solid #FFB830;">
        <div style="font-family:'Space Mono',monospace; font-size:11px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#FFB830; margin-bottom:0.8rem;">order_items</div>
        <div style="font-family:'DM Sans',sans-serif; font-size:11px; color:#3A4A65; line-height:1.8;">
            <span style="color:#8899BB;">&#9658; item_id</span><br>order_id<br>product_id<br>quantity<br>unit_price
        </div>
    </div>
    <div style="background:#0D1220; padding:1.2rem; border-top:2px solid #FF8FA3;">
        <div style="font-family:'Space Mono',monospace; font-size:11px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#FF8FA3; margin-bottom:0.8rem;">products</div>
        <div style="font-family:'DM Sans',sans-serif; font-size:11px; color:#3A4A65; line-height:1.8;">
            <span style="color:#8899BB;">&#9658; product_id</span><br>name<br>category<br>price<br>stock_quantity
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SECURITY ─────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown("""
<span class="section-eyebrow">Security Model</span>
<h2 class="section-title">Five guardrail layers</h2>
<p class="section-sub">Every query passes through a multi-stage validation pipeline before touching the database.</p>
""", unsafe_allow_html=True)

components.html(GUARDRAILS_HTML, height=160, scrolling=False)

# ── FOOTER ────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #243048; padding:2rem 0; display:flex; align-items:center; justify-content:space-between; margin-top:2rem;">
    <span style="font-family:'Space Mono',monospace; font-size:11px; color:#3A4A65;">&#x2B21; NEXUS BI v1.0.0</span>
    <span style="font-family:'Space Mono',monospace; font-size:11px; color:#3A4A65;">FastAPI · Groq · MySQL · Streamlit</span>
    <span style="font-family:'Space Mono',monospace; font-size:11px; color:#3A4A65;">localhost:8000/docs</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
