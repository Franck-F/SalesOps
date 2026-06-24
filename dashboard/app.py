# -*- coding: utf-8 -*-
"""Dashboard de pilotage SalesOps — MoveUp (prototype J4).
Design « MoveUp » (Poppins, crème/vert/lime) appliqué à Streamlit.
Lancer :  streamlit run dashboard/app.py   (depuis la racine du repo)."""
import sys
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import data as D  # noqa: E402
import importlib
importlib.reload(D)

# ---------- Palette ----------
CREAM, INK, MUTE = "#FFFDF8", "#2A432E", "#737D74"
LIME, OLIVE, LIGHT = "#AACB55", "#859356", "#D6E393"

st.set_page_config(page_title="MoveUp — Pilotage SalesOps", page_icon="./favicon.png",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stApp, button, input, select, textarea {
  font-family:'Poppins', system-ui, sans-serif; }
.stApp { background:#FFFDF8; color:#2A432E; }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display:none; }
[data-testid="stHeader"] { background:transparent; }
[data-testid="stSidebarCollapseButton"] { display:none; }
[data-testid="collapsedControl"] { display:none; }
button[title="View fullscreen"], [data-testid="StyledFullScreenButton"], [data-testid="stImage"] button { display:none !important; }
.block-container { padding-top:1.4rem; padding-bottom:3rem; max-width:1320px; }
::selection { background:rgba(170,203,85,0.35); }

/* ----- Sidebar sombre ----- */
[data-testid="stSidebar"] { background:#2A432E; position: relative !important; }
[data-testid="stSidebar"] * { color:#FFFDF8; }
[data-testid="stSidebar"] .block-container { padding-top:0rem; padding-bottom:160px; position: static !important; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { position: static !important; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div { position: static !important; }

.mu-sub { font-size:11px; letter-spacing:0.12em; text-transform:uppercase;
  color:rgba(255,253,248,0.5); margin:6px 0 14px; }
[data-testid="stSidebar"] hr { border-color:rgba(255,253,248,0.12); }
[data-testid="stSidebar"] [role="radiogroup"] { gap:4px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
  padding:10px 14px; border-radius:8px; border-left:3px solid transparent;
  font-size:14px; color:rgba(255,253,248,0.65); cursor:pointer; transition:all .2s ease; margin-bottom: 2px;}
[data-testid="stSidebar"] [role="radiogroup"] label p { display:flex; align-items:center; gap:10px; margin:0; }
[data-testid="stSidebar"] [role="radiogroup"] label p::before {
  content: ''; display:inline-block; width:18px; height:18px; background-color:currentColor;
  -webkit-mask-size:contain; -webkit-mask-repeat:no-repeat; -webkit-mask-position:center;
}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(1) p::before { -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='7' height='9' x='3' y='3' rx='1'/%3E%3Crect width='7' height='5' x='14' y='3' rx='1'/%3E%3Crect width='7' height='9' x='14' y='12' rx='1'/%3E%3Crect width='7' height='5' x='3' y='16' rx='1'/%3E%3C/svg%3E"); }
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(2) p::before { -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='6' x2='6' y1='3' y2='15'/%3E%3Ccircle cx='18' cy='6' r='3'/%3E%3Ccircle cx='6' cy='18' r='3'/%3E%3Cpath d='M18 9a9 9 0 0 1-9 9'/%3E%3C/svg%3E"); }
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(3) p::before { -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='22 7 13.5 15.5 8.5 10.5 2 17'/%3E%3Cpolyline points='16 7 22 7 22 13'/%3E%3C/svg%3E"); }
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(4) p::before { -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='9' cy='7' r='4'/%3E%3Cpath d='M22 21v-2a4 4 0 0 0-3-3.87'/%3E%3Cpath d='M16 3.13a4 4 0 0 1 0 7.75'/%3E%3C/svg%3E"); }
[data-testid="stSidebar"] [role="radiogroup"] label:nth-child(5) p::before { -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3Cpath d='M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z'/%3E%3Cpath d='M2 12h20'/%3E%3C/svg%3E"); }

[data-testid="stSidebar"] [role="radiogroup"] label p { color:#A8B2A9 !important; transition:color 0.2s; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover p { color:#FFFDF8 !important; }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
  background:rgba(170,203,85,0.16); border-left-color:#AACB55; }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p { color:#FFFDF8 !important; font-weight:600; }
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display:none; }
.mu-bottom-wrapper { position: absolute; bottom: 1.5rem; left: 1.5rem; right: 1.5rem; z-index: 999; }
.mu-salle { border:1px solid rgba(255,253,248,0.14); border-radius:12px; padding:16px; background:rgba(0,0,0,0.1); }
.mu-salle .k { font-size:10.5px; letter-spacing:0.1em; text-transform:uppercase; color:rgba(255,253,248,0.5); }
.mu-salle .v { font-size:14px; font-weight:600; margin-top:3px; }
.mu-salle .s { font-size:12px; color:rgba(255,253,248,0.55); margin-top:2px; }
.mu-user { display: flex; align-items: center; gap: 12px; margin-top: 12px; padding: 12px; border-radius: 12px; background: transparent; border: none; cursor: pointer; transition: all .2s; }
.mu-user:hover { background: rgba(255,253,248,0.05); }
.mu-avatar { width: 34px; height: 34px; border-radius: 50%; background: #AACB55; color: #2A432E; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; }
.mu-user-info { display: flex; flex-direction: column; }
.mu-name { font-size: 13px; font-weight: 600; color: #FFFDF8; line-height: 1.2; }
.mu-role { font-size: 11px; color: rgba(255,253,248,0.6); }

@keyframes slideUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes fillBar {
  from { width: 0; }
  to { width: var(--target-width); }
}
@keyframes chartPop {
  0% { opacity: 0; transform: scale(0.96) translateY(10px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}

/* ----- Cartes / éléments ----- */
.mu-card { background:#FFFDF8; border:1px solid color-mix(in srgb,#737D74 13%,transparent); box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  border-radius:16px; padding:24px; margin-bottom:16px; animation: slideUp 0.4s ease-out forwards; transition: all 0.25s ease; }
.mu-h2 { margin:0 0 4px; font-size:16px; font-weight:700; text-transform:uppercase;
  letter-spacing:0.01em; color:#2A432E; }
.mu-sub2 { margin:0 0 16px; font-size:13px; color:#737D74; }
.mu-kpigrid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; margin-bottom:24px; }
.mu-kpi { background:#FFFDF8; border:1px solid color-mix(in srgb,#737D74 15%,transparent); box-shadow: 0 4px 16px rgba(0,0,0,0.02);
  border-radius:16px; padding:22px; animation: slideUp 0.5s cubic-bezier(0.1, 0.8, 0.2, 1) forwards; transition: all 0.3s cubic-bezier(0.1, 0.8, 0.2, 1); position:relative; overflow:hidden; }

.mu-kpi::before { content:''; position:absolute; top:0; left:0; width:100%; height:4px; transition: height 0.3s ease; }
.mu-kpi:hover::before { height:6px; }

.mu-kpi.lime { background:linear-gradient(145deg, rgba(170,203,85,0.08) 0%, #FFFDF8 100%); border-color:rgba(170,203,85,0.2); }
.mu-kpi.lime::before { background:#AACB55; }
.mu-kpi.lime .icon { background:rgba(170,203,85,0.2); color:#5d7524; }

.mu-kpi.olive { background:linear-gradient(145deg, rgba(133,147,86,0.08) 0%, #FFFDF8 100%); border-color:rgba(133,147,86,0.2); }
.mu-kpi.olive::before { background:#859356; }
.mu-kpi.olive .icon { background:rgba(133,147,86,0.2); color:#424b26; }

.mu-kpi.dark { background:linear-gradient(145deg, #2A432E 0%, #223725 100%); border:none; box-shadow: 0 8px 24px rgba(42,67,46,0.15); }
.mu-kpi.dark::before { background:#AACB55; }
.mu-kpi.dark .l, .mu-kpi.dark .s { color:rgba(255,253,248,0.7); }
.mu-kpi.dark .v { color:#FFFDF8; }
.mu-kpi.dark .v .u { color:#AACB55; }
.mu-kpi.dark .icon { background:rgba(255,253,248,0.1); color:#AACB55; }

.mu-kpi.danger { background:linear-gradient(145deg, rgba(255,75,75,0.05) 0%, #FFFDF8 100%); border-color:rgba(255,75,75,0.15); }
.mu-kpi.danger::before { background:#FF4B4B; }
.mu-kpi.danger .icon { background:rgba(255,75,75,0.12); color:#D63232; }

.mu-kpi.accent { background:linear-gradient(135deg,rgba(42,67,46,0.04) 0%,rgba(42,67,46,0.01) 100%); border-color:rgba(42,67,46,0.2); }
.mu-kpi.accent::before { background:#2A432E; }

.mu-kpi .icon { position:absolute; top:18px; right:18px; width:34px; height:34px; border-radius:10px; display:flex; align-items:center; justify-content:center; backdrop-filter:blur(4px); }
.mu-kpi .icon svg { width:18px; height:18px; stroke-width:2; }
.mu-kpi .l { font-size:11px; letter-spacing:0.08em; text-transform:uppercase; color:#737D74; font-weight:600; padding-right: 30px; }
.mu-kpi .v { font-size:32px; font-weight:700; letter-spacing:-0.03em; margin-top:14px; line-height:1; white-space:nowrap; color:#2A432E; }
.mu-kpi .v .u { font-size:16px; color:#859356; font-weight:600; }
.mu-kpi .s { font-size:12px; color:#737D74; margin-top:10px; line-height:1.4; display:flex; align-items:center; gap:6px; }
.mu-kpi .s::before { content:''; display:inline-block; width:4px; height:4px; border-radius:50%; background:currentColor; opacity:0.5; }
.mu-grid2 { display:grid; grid-template-columns:minmax(0,1.25fr) minmax(0,1fr); gap:16px; }
.mu-grid2e { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.mu-grid3 { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.mu-grid4 { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }
.mu-mini { border:1px solid color-mix(in srgb,#737D74 13%,transparent); border-radius:14px; padding:18px; box-shadow: 0 2px 8px rgba(0,0,0,0.025); background:#FFFDF8; animation: slideUp 0.4s ease-out forwards; transition: all 0.25s cubic-bezier(0.1, 0.8, 0.2, 1); }
.mu-card:hover, .mu-kpi:hover, .mu-mini:hover { transform: translateY(-4px); box-shadow: 0 16px 40px rgba(42,67,46,0.1); z-index: 2; border-color: rgba(170,203,85,0.4); }

/* ----- Tables ----- */
.mu-table { width:100%; border-collapse:collapse; font-size:13px; text-align:right; }
.mu-table th { padding:12px 8px; font-weight:600; color:#737D74; font-size:10.5px; text-transform:uppercase; letter-spacing:0.06em; border-bottom:2px solid color-mix(in srgb,#737D74 20%,transparent); }
.mu-table th:first-child, .mu-table td:first-child { text-align:left; }
.mu-table td { padding:12px 8px; border-bottom:1px solid color-mix(in srgb,#737D74 12%,transparent); transition:background 0.2s ease; }
.mu-table tbody tr:hover td { background:color-mix(in srgb,#AACB55 12%,transparent); }
.mu-table tbody tr:last-child td { border-bottom:none; }
/* Animation des graphiques Plotly */
.stPlotlyChart { opacity: 0; animation: chartPop 0.8s cubic-bezier(0.1, 0.8, 0.2, 1) 0.1s forwards; }

/* @media queries for responsivness */
@media (max-width: 1024px) {
  .mu-kpigrid { grid-template-columns: repeat(3, 1fr); }
  .mu-grid4 { grid-template-columns: repeat(2, 1fr); }
  .mu-grid3 { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .mu-kpigrid { grid-template-columns: repeat(2, 1fr); }
  .mu-grid2, .mu-grid2e, .mu-grid3, .mu-grid4 { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
  .mu-kpigrid { grid-template-columns: 1fr; }
}

.mu-mini .l { font-size:11px; letter-spacing:0.05em; text-transform:uppercase; color:#737D74; font-weight:500; }
.mu-mini .v { font-size:25px; font-weight:700; color:#2A432E; margin-top:8px; line-height:1; }
.mu-mini .v .u { font-size:14px; color:#859356; }
.mu-mini .s { font-size:12px; color:#737D74; margin-top:8px; }
.mu-row { display:flex; justify-content:space-between; font-size:13px; margin-bottom:6px; }
.mu-track { height:26px; border-radius:6px; background:color-mix(in srgb,#737D74 8%,transparent); overflow:hidden; }
.mu-fill { height:100%; border-radius:6px; width: 0; animation: fillBar 1s cubic-bezier(0.1, 0.8, 0.2, 1) 0.2s forwards; }
.mu-callout { border-radius:0 12px 12px 0; padding:16px 18px; font-size:13.5px; line-height:1.6; }
.mu-tbl { width:100%; border-collapse:collapse; font-size:13.5px; }
.mu-tbl th { text-align:right; color:#737D74; font-size:11px; letter-spacing:0.05em;
  text-transform:uppercase; font-weight:600; padding:0 0 12px; }
.mu-tbl th:first-child, .mu-tbl td:first-child { text-align:left; }
.mu-tbl td { text-align:right; padding:13px 0; border-top:1px solid color-mix(in srgb,#737D74 15%,transparent); }
.mu-dark { background:linear-gradient(145deg, #2A432E, #223725); color:#FFFDF8; border-radius:12px; padding:26px; box-shadow: 0 8px 24px rgba(42,67,46,0.15); }
h1.mu-title { margin:0; font-size:32px; font-weight:700; letter-spacing:-0.03em;
  text-transform:uppercase; color:#2A432E; line-height:1; }
.mu-badge { display:inline-flex; align-items:center; gap:8px; background:linear-gradient(135deg, #D6E393, #AACB55); border-radius:8px;
  padding:8px 14px; font-size:12px; font-weight:600; letter-spacing:0.05em; text-transform:uppercase; color:#2A432E; box-shadow: 0 2px 8px rgba(170,203,85,0.2); }
</style>
""", unsafe_allow_html=True)


# ---------- Helpers ----------
def nb(x):
    return f"{x:,.0f}".replace(",", " ")


def pc(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


@st.cache_data
def get_data():
    return D.load_all()


def bar(label, value_txt, pct, color, h=24):
    return (f'<div style="margin-bottom:13px"><div class="mu-row">'
            f'<span style="font-weight:500">{label}</span><span style="color:{MUTE}">{value_txt}</span></div>'
            f'<div class="mu-track" style="height:{h}px"><div class="mu-fill" '
            f'style="--target-width:{pct:.1f}%;background:{color}"></div></div></div>')

d = get_data()

# ---------- Sidebar ----------
with st.sidebar:
    logo_path = Path(__file__).resolve().parent.parent / "logomoveup.png"
    if logo_path.exists():
        import base64
        with open(logo_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<div style="margin-top:-50px"><img src="data:image/png;base64,{b64}" width="180"></div>', unsafe_allow_html=True)
    st.markdown('<div class="mu-sub" style="margin-top:-10px;">Pilotage SalesOps</div>', unsafe_allow_html=True)
    st.markdown("---")
    tab = st.radio("nav", ["Vue d'ensemble", "Funnel & commercial",
                           "Acquisition / ROI", "Rétention / churn", "Audience web"], label_visibility="collapsed")

    st.markdown('<div class="mu-bottom-wrapper"><div class="mu-salle"><div class="k">Salle</div>'
                '<div class="v">MoveUp · Versailles</div><div class="s">1 000 m² · 1 200 adhérents</div></div>'
                '<div class="mu-user"><div class="mu-avatar">KF</div>'
                '<div class="mu-user-info"><div class="mu-name">Franck Koffi</div>'
                '<div class="mu-role">Admin SalesOps</div></div></div></div>', unsafe_allow_html=True)

# ---------- Header & Filtres ----------
hc = st.columns([2.5, 1.5])
with hc[0]:
    st.markdown('<h1 class="mu-title">Pilotage commercial.</h1>'
                f'<p style="margin:9px 0 0;font-size:14px;color:{MUTE}">Ce qu\'un Excel partagé ne '
                'montrait pas — leads, conversion, acquisition &amp; rétention, en un coup d\'œil.</p>',
                unsafe_allow_html=True)
with hc[1]:
    TODAY = pd.Timestamp("2026-06-23")
    periodes = {
        "2 dernières semaines": TODAY - pd.Timedelta(weeks=2),
        "4 dernières semaines": TODAY - pd.Timedelta(weeks=4),
        "8 dernières semaines": TODAY - pd.Timedelta(weeks=8),
        "12 dernières semaines": TODAY - pd.Timedelta(weeks=12),
        "Tout l'historique": None,
    }

    h_cols = st.columns([0.4, 2.5, 2.2])
    with h_cols[0]:
        st.markdown('<div style="margin-top:6px;text-align:right">'
                    '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#737D74" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
                    '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>'
                    '<line x1="16" y1="2" x2="16" y2="6"></line>'
                    '<line x1="8" y1="2" x2="8" y2="6"></line>'
                    '<line x1="3" y1="10" x2="21" y2="10"></line></svg></div>', unsafe_allow_html=True)
    with h_cols[1]:
        periode_sel = st.selectbox("Période d'analyse", list(periodes.keys()), index=1, label_visibility="collapsed")
    with h_cols[2]:
        st.markdown('<div style="text-align:right;margin-bottom:8px;margin-top:2px"><span class="mu-badge">'
                    '<span style="width:7px;height:7px;border-radius:50%;background:#859356"></span>'
                    'Modèle CIBLE</span></div>', unsafe_allow_html=True)
    
    start_date = periodes[periode_sel]
    fd = dict(d)
    if start_date:
        fd["lead"] = d["lead"][d["lead"]["date_creation"] >= start_date]
        fd["acquisition"] = d["acquisition"][d["acquisition"]["date"] >= start_date]
        if "audience" in d: fd["audience"] = d["audience"][d["audience"]["date"] >= start_date]
        if "pages" in d: fd["pages"] = d["pages"][d["pages"]["date"] >= start_date]

k = D.kpis(fd)
q = D.qualite_commerciale(fd)
roi = D.roi_canal(fd)
ch = D.churn_view(d)
em = D.email_kpis(fd)
ak = D.audience_kpis(fd)
lead = fd["lead"]
n_perdu = int((lead.statut_lead == "perdu").sum())
n_gagne = int((lead.statut_lead == "gagne").sum())
open_mask = lead.statut_lead.isin(["nouveau", "contacte", "visite", "essai"])
n_encours = int(open_mask.sum())
n_chauds = int((open_mask & (lead.score >= 70)).sum())

PLOT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", color=INK), margin=dict(l=8, r=8, t=8, b=8),
            xaxis=dict(showgrid=False, zeroline=False, showline=False, tickfont=dict(size=11)),
            yaxis=dict(gridcolor="rgba(115,125,116,0.12)", zeroline=False, showline=False, tickfont=dict(size=11)))

# ===================== VUE D'ENSEMBLE =====================
if tab == "Vue d'ensemble":
    kpis_html = '<div class="mu-kpigrid">'
    kpis_html += f'<div class="mu-kpi lime"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg></div><div class="l">MRR · revenu mensuel</div><div class="v">{nb(k["mrr"])} <span class="u">€</span></div><div class="s">Base abonnements actifs</div></div>'
    kpis_html += f'<div class="mu-kpi olive"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg></div><div class="l">ARPM · panier moyen</div><div class="v">{pc(k["arpm"])} <span class="u">€</span></div><div class="s">Essentiel 49 € · Premium 69 €</div></div>'
    kpis_html += f'<div class="mu-kpi dark"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg></div><div class="l">Adhérents actifs</div><div class="v">{nb(k["n_actifs"])}</div><div class="s">Capacité max 170 simultanés</div></div>'
    kpis_html += f'<div class="mu-kpi accent"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg></div><div class="l">Conversion lead → adhérent</div><div class="v">{pc(k["conv"]*100)} <span class="u">%</span></div><div class="s">{k["n_adh"]} adhésions / {k["n_leads"]} leads</div></div>'

    total_depense = roi["depense"].sum()
    total_adhesions_paid = roi["adhesions"].sum()
    global_cac = total_depense / total_adhesions_paid if total_adhesions_paid else 0.0
    ltv_cac_ratio = k["ltv"] / global_cac if global_cac > 0 else 0.0

    kpis_html += f'<div class="mu-kpi lime"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg></div><div class="l">LTV · Valeur à vie</div><div class="v">{nb(k["ltv"])} <span class="u">€</span></div><div class="s">Valeur client sur sa durée de vie</div></div>'
    kpis_html += f'<div class="mu-kpi olive"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg></div><div class="l">Ratio LTV:CAC</div><div class="v">{pc(ltv_cac_ratio)} <span class="u">x</span></div><div class="s">Retour long terme (cible &gt; 3x)</div></div>'
    kpis_html += f'<div class="mu-kpi danger"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg></div><div class="l">Risque churn élevé</div><div class="v">{k["risque_eleve"]}</div><div class="s" style="color:#D63232;font-weight:600">{round(100*k["risque_eleve"]/ch["total"])} % de la base · à cibler</div></div>'
    kpis_html += f'<div class="mu-kpi danger"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" /></svg></div><div class="l">Résiliations · 30 j</div><div class="v">{k["churn30"]}</div><div class="s" style="color:#D63232;font-weight:600">+ {ch["inactifs"]} inactifs &gt; 30 j</div></div>'
    kpis_html += '</div>'

    f = D.funnel(fd)
    fv = dict(zip(f.etape, f.volume))
    fcolors = {"Lead": LIME, "Contacté": LIME, "Visite": OLIVE, "Essai réalisé": OLIVE, "Adhésion": INK}

    st.markdown(kpis_html, unsafe_allow_html=True)
    g = st.columns([1.25, 1])
    with g[0]:
        f = D.funnel(fd)
        fcolors = {"Lead": LIME, "Contacté": LIME, "Visite": OLIVE, "Essai réalisé": OLIVE, "Adhésion": INK}
        bars = ('<div class="mu-card"><div style="display:flex;justify-content:space-between;align-items:baseline">'
                '<div class="mu-h2">Funnel de vente.</div>'
                f'<span style="font-size:11px;color:{MUTE}">mensuel · lead → adhésion</span></div>'
                '<div style="margin-top:18px">')
        for _, r in f.iterrows():
            pct = r.volume / k["n_leads"] * 100
            bars += bar(r.etape, f'{nb(r.volume)} · {pc(pct,0)} %', pct, fcolors.get(r.etape, OLIVE))
        bars += '</div></div>'
        st.markdown(bars, unsafe_allow_html=True)
    with g[1]:
        st.markdown(
            '<div class="mu-card"><div class="mu-h2">Qualité commerciale.</div><div class="mu-grid2e" style="margin-top:14px">'
            f'<div class="mu-mini"><div class="l">Speed-to-lead</div><div class="v">{q["speed_to_lead"]:.0f} <span class="u">h</span></div></div>'
            f'<div class="mu-mini"><div class="l">No-show essais</div><div class="v">{q["no_show"]:.0f} <span class="u">%</span></div></div>'
            f'<div class="mu-mini"><div class="l">Relance post-essai</div><div class="v">{q["relance"]:.0f} <span class="u">%</span></div></div>'
            f'<div class="mu-mini"><div class="l">Cycle moyen</div><div class="v">{q["cycle"]:.0f} <span class="u">j</span></div></div>'
            '</div><div class="mu-callout" style="margin-top:16px;border-left:2px solid #2A432E;'
            'background:color-mix(in srgb,#2A432E 4%,transparent)"><b>3 prospects chauds sur 4</b> qui font un '
            'essai ne sont jamais rappelés. Le premier levier de conversion est là.</div></div>',
            unsafe_allow_html=True)

    st.markdown('<div class="mu-card"><div class="mu-h2">Volume hebdomadaire.</div>'
                f'<div class="mu-sub2">Leads (lime) vs adhésions (vert foncé) par semaine.</div>', unsafe_allow_html=True)
    lh = D.leads_hebdo(fd)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=lh.semaine, y=lh.Leads, name="Leads", mode="lines",
                             line=dict(color=LIME, width=2.6), fill="tozeroy", fillcolor="rgba(170,203,85,0.14)"))
    fig.add_trace(go.Scatter(x=lh.semaine, y=lh["Adhésions"], name="Adhésions", mode="lines",
                             line=dict(color=INK, width=2.6)))
    fig.update_layout(height=240, legend=dict(orientation="h", y=1.15, x=1, xanchor="right",
                      bgcolor="rgba(0,0,0,0)"), **PLOT)
    fig.update_xaxes(showgrid=False, title=None)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(115,125,116,0.15)", zeroline=False, title=None)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    cac_ig = roi.loc[roi.canal == "instagram", "cac"].iloc[0]
    cac_gg = roi.loc[roi.canal == "google_ads", "cac"].iloc[0]
    st.markdown(
        '<div class="mu-grid3">'
        f'<div class="mu-card" style="border-left:3px solid #2A432E;margin:0"><div style="font-size:13px;font-weight:600;margin-bottom:7px">Réactivité</div>'
        f'<p style="margin:0;font-size:12.5px;color:{MUTE};line-height:1.5">Speed-to-lead à <b style="color:#2A432E">{q["speed_to_lead"]:.0f} h</b> : la joignabilité chute après quelques heures. Objectif &lt; 1 h.</p></div>'
        f'<div class="mu-card" style="border-left:3px solid #859356;margin:0"><div style="font-size:13px;font-weight:600;margin-bottom:7px">Acquisition</div>'
        f'<p style="margin:0;font-size:12.5px;color:{MUTE};line-height:1.5">Instagram convertit à <b style="color:#2A432E">{cac_ig:.0f} € de CAC</b> vs <b style="color:#2A432E">{cac_gg:.0f} €</b> sur Google Ads. Budget mal réparti.</p></div>'
        f'<div class="mu-card" style="border-left:3px solid #AACB55;margin:0"><div style="font-size:13px;font-weight:600;margin-bottom:7px">Rétention</div>'
        f'<p style="margin:0;font-size:12.5px;color:{MUTE};line-height:1.5">Seulement <b style="color:#2A432E">{ch["coaching"]:.0f} %</b> utilisent le coaching : fort potentiel d\'upsell sur les ~{100-ch["coaching"]:.0f} % restants.</p></div>'
        '</div>', unsafe_allow_html=True)

# ===================== FUNNEL & COMMERCIAL =====================
elif tab == "Funnel & commercial":
    f = D.funnel(fd)
    fcolors = {"Lead": LIME, "Contacté": LIME, "Visite": OLIVE, "Essai réalisé": OLIVE, "Adhésion": INK}
    g = st.columns([1.25, 1])
    with g[0]:
        steps = list(f.itertuples(index=False))
        gates = ["63 % contactés", "64 % visites", "55 % essais — point de fuite n°1", "61 % adhésions"]
        html = ('<div class="mu-card"><div class="mu-h2">Funnel détaillé.</div>'
                '<div class="mu-sub2">Conversion d\'étape en étape — où les prospects décrochent.</div>')
        for i, r in enumerate(steps):
            pct = r.volume / k["n_leads"] * 100
            col = fcolors.get(r.etape, OLIVE)
            html += (f'<div style="display:flex;align-items:center;gap:16px"><div style="width:120px;font-size:13px;font-weight:500">{r.etape}</div>'
                     f'<div style="flex:1"><div class="mu-track" style="height:30px"><div class="mu-fill" style="height:100%;--target-width:{pct:.1f}%;background:{col}"></div></div></div>'
                     f'<div style="width:46px;text-align:right;font-weight:700;font-size:15px">{nb(r.volume)}</div></div>')
            if i < len(gates):
                hot = ";color:#2A432E;font-weight:600" if i == 2 else f";color:{MUTE}"
                html += f'<div style="padding:5px 0 5px 136px;font-size:11px{hot}">↓ {gates[i]}</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)
    with g[1]:
        st.markdown(
            f'<div class="mu-dark"><div style="font-size:11px;letter-spacing:0.08em;text-transform:uppercase;color:rgba(255,253,248,0.6)">Opportunités perdues / mois</div>'
            f'<div style="font-size:40px;font-weight:700;margin-top:8px;line-height:1">{nb(k["n_leads"]-n_gagne)}</div>'
            f'<p style="margin:12px 0 0;font-size:12.5px;color:rgba(255,253,248,0.75);line-height:1.5">Sur {k["n_leads"]} leads, {n_gagne} deviennent adhérents. Plus de <b style="color:#AACB55">85 %</b> de l\'intérêt initial s\'évapore faute de relance structurée.</p></div>'
            f'<div class="mu-card" style="margin-top:16px"><div style="font-size:12px;letter-spacing:0.05em;text-transform:uppercase;color:{MUTE};margin-bottom:12px">Statut des leads</div>'
            f'<div style="display:flex;flex-direction:column;gap:9px;font-size:13px">'
            f'<div style="display:flex;justify-content:space-between"><span>Perdus</span><span style="font-weight:600">{n_perdu}</span></div>'
            f'<div style="display:flex;justify-content:space-between"><span>Gagnés</span><span style="font-weight:600;color:#859356">{n_gagne}</span></div>'
            f'<div style="display:flex;justify-content:space-between"><span>Nouveaux / en cours</span><span style="font-weight:600">{n_encours}</span></div>'
            f'<div style="height:1px;background:color-mix(in srgb,#737D74 18%,transparent);margin:3px 0"></div>'
            f'<div style="display:flex;justify-content:space-between"><span style="font-weight:600">Leads chauds ouverts</span><span style="font-weight:700">{n_chauds} · à relancer</span></div>'
            '</div></div>', unsafe_allow_html=True)

    sessions = ak["sessions"]
    conv_web = (k["n_leads"] / sessions * 100) if sessions > 0 else 0.0

    st.markdown(
        '<div class="mu-card"><div class="mu-h2">Qualité commerciale.</div><div class="mu-kpigrid" style="margin-top:14px;grid-template-columns:repeat(5,minmax(0,1fr))">'
        f'<div class="mu-mini"><div class="l">Conv. Visiteur → Lead</div><div class="v">{conv_web:.1f} <span class="u">%</span></div><div class="s">Micro-conversion web</div></div>'
        f'<div class="mu-mini"><div class="l">Speed-to-lead</div><div class="v">{q["speed_to_lead"]:.0f} <span class="u">h</span></div><div class="s" style="color:#2A432E;font-weight:500">Cible &lt; 1 h</div></div>'
        f'<div class="mu-mini"><div class="l">No-show essais</div><div class="v">{q["no_show"]:.0f} <span class="u">%</span></div><div class="s">Aucune confirmation auto</div></div>'
        f'<div class="mu-mini"><div class="l">Relance post-essai</div><div class="v">{q["relance"]:.0f} <span class="u">%</span></div><div class="s">{100-q["relance"]:.0f} % jamais rappelés</div></div>'
        f'<div class="mu-mini"><div class="l">Cycle de vente</div><div class="v">{q["cycle"]:.0f} <span class="u">j</span></div><div class="s">Lead → signature</div></div>'
        '</div></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="mu-card" style="border-left:3px solid #2A432E"><div style="font-size:13px;font-weight:600;margin-bottom:6px">Diagnostic</div>'
        f'<p style="margin:0;font-size:13px;color:{MUTE};line-height:1.55">Le funnel existe mais n\'est pas piloté : pas de critères de passage, '
        'pas de scénario de relance (J+1, J+3, post-essai), un seul commercial dépendant. Structurer la relance après l\'essai et automatiser '
        'les confirmations adresserait directement le no-show de 40 % et la conversion de 13,7 %.</p></div>', unsafe_allow_html=True)

# ===================== ACQUISITION / ROI =====================
elif tab == "Acquisition / ROI":
    g = st.columns(2)
    cac_max = roi["cac"].max()
    leads_max = roi["leads"].max()
    cbar = {"instagram": LIME, "google_ads": INK, "recommandation": LIGHT, "site_web": LIGHT}
    with g[0]:
        paid = roi[roi.cac.notna()]
        h = '<div class="mu-card"><div class="mu-h2">CAC par canal payant.</div><div class="mu-sub2">Coût d\'acquisition d\'un adhérent.</div>'
        for _, r in paid.iterrows():
            h += bar(r.canal.replace("_", " ").title(), f'{r.cac:.0f} €', r.cac / cac_max * 100, cbar.get(r.canal, OLIVE), 22)
        cac_ig = roi.loc[roi.canal == "instagram", "cac"].iloc[0]
        cac_gg = roi.loc[roi.canal == "google_ads", "cac"].iloc[0]
        h += (f'<div class="mu-callout" style="margin-top:8px;border-left:2px solid #AACB55;background:color-mix(in srgb,#AACB55 8%,transparent)">'
              f'Google Ads coûte <b>~{cac_gg/cac_ig:.1f}×</b> Instagram par adhérent. Réallouer le budget vers Instagram.</div></div>')
        st.markdown(h, unsafe_allow_html=True)
    with g[1]:
        h = '<div class="mu-card"><div class="mu-h2">Leads par canal.</div><div class="mu-sub2">Volume généré sur la période.</div>'
        for _, r in roi.sort_values("leads", ascending=False).iterrows():
            h += bar(r.canal.replace("_", " ").title(), f'{int(r.leads)}', r.leads / leads_max * 100, cbar.get(r.canal, OLIVE), 20)
        h += '</div>'
        st.markdown(h, unsafe_allow_html=True)

    rows = ""
    for _, r in roi.iterrows():
        dep = f'{nb(r.depense)} €' if r.depense else '0 €'
        cpl = f'{r.cpl:.0f} €' if pd.notna(r.cpl) else '—'
        cac = f'{r.cac:.0f} €' if pd.notna(r.cac) else '—'
        ctr = f'{r.ctr*100:.1f} %' if pd.notna(r.ctr) else '—'
        cpc = f'{r.cpc:.2f} €' if pd.notna(r.cpc) else '—'
        roas = f'{(r.adhesions * k["arpm"]) / r.depense:.1f}x' if r.depense > 0 else '—'
        ccol = "#859356" if r.canal == "instagram" else INK
        rows += (f'<tr><td style="font-weight:600"><span style="display:inline-flex;align-items:center;gap:8px">'
                 f'<span style="width:9px;height:9px;border-radius:2px;background:{cbar.get(r.canal,OLIVE)}"></span>{r.canal.replace("_"," ").title()}</span></td>'
                 f'<td>{dep}</td><td>{int(r.leads)}</td><td>{int(r.adhesions)}</td><td>{cpl}</td>'
                 f'<td style="font-weight:600;color:{ccol}">{cac}</td><td>{ctr}</td><td>{cpc}</td><td style="font-weight:600;color:#2A432E">{roas}</td><td>{pc(r.conv_pct)} %</td></tr>')

    valeur_lead = k["arpm"] * k["conv"]
    
    st.markdown(
        f'<div class="mu-card" style="display:flex;justify-content:space-between;align-items:center;padding:16px 24px;border-left:4px solid #AACB55">'
        f'<div style="display:flex;align-items:center;gap:24px">'
        f'<div><div style="font-size:11.5px;text-transform:uppercase;color:{MUTE};font-weight:600;letter-spacing:0.05em">Valeur d\'un lead (Max CPC)</div>'
        f'<div style="font-size:24px;font-weight:700;color:#2A432E;margin-top:2px">{valeur_lead:.1f} <span style="font-size:14px;color:#859356">€</span></div></div>'
        f'<div style="width:1px;height:36px;background:color-mix(in srgb,#737D74 20%,transparent)"></div>'
        f'<div><div style="font-size:12px;color:{MUTE};line-height:1.4">Valeur théorique = ARPM × Taux de conversion.<br>C\'est le coût maximal que vous pouvez payer par lead pour être rentable dès le premier mois.</div></div>'
        f'</div></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="mu-card"><div class="mu-h2">Performances par canal.</div>'
        '<table class="mu-tbl"><thead><tr><th>Canal</th><th>Dépense</th><th>Leads</th><th>Adhésions</th>'
        f'<th>CPL</th><th>CAC</th><th>CTR</th><th>CPC</th><th>ROAS</th><th>Conv.</th></tr></thead><tbody>{rows}</tbody></table></div>',
        unsafe_allow_html=True)
        
    st.markdown(
        '<div class="mu-card"><div class="mu-h2">Email & Newsletter.</div><div class="mu-grid3" style="margin-top:14px">'
        f'<div class="mu-mini"><div class="l">Taux d\'ouverture</div><div class="v">{em["ouvertures"]*100:.1f} <span class="u">%</span></div></div>'
        f'<div class="mu-mini"><div class="l">Taux de clic</div><div class="v">{em["clics"]*100:.1f} <span class="u">%</span></div></div>'
        f'<div class="mu-mini"><div class="l">Désabonnements</div><div class="v">{em["desabos"]}</div></div>'
        '</div></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="mu-grid2e">'
        f'<div class="mu-card" style="border-left:3px solid #AACB55;margin:0"><div style="font-size:13px;font-weight:600;margin-bottom:6px">Réallouer le payant</div>'
        f'<p style="margin:0;font-size:12.5px;color:{MUTE};line-height:1.5">Instagram est le canal le plus rentable. Basculer une partie du budget Google Ads vers Instagram améliorerait mécaniquement le ROI global.</p></div>'
        f'<div class="mu-card" style="border-left:3px solid #859356;margin:0"><div style="font-size:13px;font-weight:600;margin-bottom:6px">Activer l\'organique</div>'
        f'<p style="margin:0;font-size:12.5px;color:{MUTE};line-height:1.5">Recommandation + site web : 0 € de dépense pour 18 adhésions. Un programme de parrainage structuré démultiplierait ce canal gratuit.</p></div>'
        '</div>', unsafe_allow_html=True)

# ===================== RÉTENTION / CHURN =====================
elif tab == "Rétention / churn":
    g = st.columns([1, 1.4])
    with g[0]:
        st.markdown('<div class="mu-card"><div class="mu-h2">Risque de churn.</div>', unsafe_allow_html=True)
        seg = ch["seg"]
        fig = go.Figure(go.Pie(labels=list(seg.index), values=list(seg.values), hole=0.62, sort=False,
                        marker=dict(colors=[LIME, OLIVE, INK]), textinfo="label+value",
                        textfont=dict(family="Poppins", size=12)))
        fig.update_layout(height=300, showlegend=False, **PLOT)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
    with g[1]:
        st.markdown(
            '<div class="mu-card"><div class="mu-h2">Signaux de rétention.</div><div class="mu-grid2e" style="margin-top:14px">'
            f'<div class="mu-mini"><div class="l">Taux de Churn</div><div class="v">{k["churn_rate"]*100:.1f} <span class="u">%</span></div><div class="s">Mensuel</div></div>'
            f'<div class="mu-mini"><div class="l">Rétention</div><div class="v">{k["retention"]*100:.1f} <span class="u">%</span></div><div class="s">Cohorte active</div></div>'
            f'<div class="mu-mini"><div class="l">Inactifs &gt; 30 j</div><div class="v">{ch["inactifs"]}</div><div class="s">sans visite</div></div>'
            f'<div class="mu-mini"><div class="l">Risque élevé</div><div class="v">{int(seg.get("Élevé",0))}</div><div class="s">à cibler en priorité</div></div>'
            f'<div class="mu-mini"><div class="l">Utilisent le coaching</div><div class="v">{ch["coaching"]:.0f} <span class="u">%</span></div><div class="s">levier d\'upsell</div></div>'
            f'<div class="mu-mini"><div class="l">Abonnés Premium</div><div class="v">{ch["premium"]:.0f} <span class="u">%</span></div><div class="s">montée en gamme</div></div>'
            '</div><div class="mu-callout" style="margin-top:16px;border-left:2px solid #2A432E;background:color-mix(in srgb,#2A432E 4%,transparent)">'
            f'<b>{int(seg.get("Élevé",0))} adhérents à risque élevé</b> + <b>{ch["inactifs"]} inactifs</b> : cibles prioritaires de rétention. '
            f'Seulement {ch["coaching"]:.0f} % utilisent le coaching → fort potentiel d\'upsell.</div></div>', unsafe_allow_html=True)

    a = d["adherents"]
    st.markdown('<div class="mu-card"><h2 class="mu-h2">Base adhérents — exploration.</h2>', unsafe_allow_html=True)
    
    st.markdown('<p class="mu-sub2">trié par score de risque</p>', unsafe_allow_html=True)
    
    if "reset_filters" not in st.session_state:
        st.session_state.seg_filter = "Tous"
        st.session_state.formule_filter = "Toutes"
        st.session_state.commune_filter = "Toutes"
        st.session_state.search_filter = ""
        st.session_state.reset_filters = True

    def reset_form():
        st.session_state.seg_filter = "Tous"
        st.session_state.formule_filter = "Toutes"
        st.session_state.commune_filter = "Toutes"
        st.session_state.search_filter = ""

    f1, f2, f3, f4, f5 = st.columns([1.5, 1.5, 1.5, 2, 1])
    with f1:
        seg_filter = st.selectbox("Segment de risque", ["Tous", "Élevé", "Moyen", "Faible"], key="seg_filter")
    with f2:
        formules = ["Toutes"] + list(a["formule"].dropna().unique())
        form_filter = st.selectbox("Formule", formules, key="formule_filter")
    with f3:
        communes = ["Toutes"] + list(a["commune"].dropna().unique())
        com_filter = st.selectbox("Commune", communes, key="commune_filter")
    with f4:
        search_filter = st.text_input("Recherche", placeholder="Nom d'adhérent…", key="search_filter")
    with f5:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Réinitialiser", on_click=reset_form, use_container_width=True)

    filtered = a.copy()
    if seg_filter != "Tous": filtered = filtered[filtered["segment_risque"] == seg_filter]
    if form_filter != "Toutes": filtered = filtered[filtered["formule"] == form_filter]
    if com_filter != "Toutes": filtered = filtered[filtered["commune"] == com_filter]
    if search_filter:
        search_lower = search_filter.lower()
        full_name = filtered["prenom"].astype(str) + " " + filtered["nom"].astype(str)
        mask = full_name.str.lower().str.contains(search_lower, na=False)
        filtered = filtered[mask]

    st.caption(f"{len(filtered)} / {len(a)} adhérents")

    if not filtered.empty:
        display_df = pd.DataFrame()
        display_df["Adhérent"] = filtered["prenom"] + " " + filtered["nom"]
        display_df["Commune"] = filtered["commune"]
        display_df["Formule"] = filtered["formule"]
        display_df["Ancienneté"] = filtered["anciennete_mois"]
        display_df["Fréq/sem"] = filtered["frequence_hebdo"]
        display_df["Coaching"] = filtered["utilisation_coaching"]
        display_df["Niveau"] = filtered["segment_risque"]
        display_df["Taux"] = filtered["score_risque_churn"].astype(int).astype(str) + " %"
        
        display_df["_score"] = filtered["score_risque_churn"]
        display_df = display_df.sort_values("_score", ascending=False).drop(columns=["_score"])

        def style_risk(val):
            # Only style the Taux column, no background, just text color
            if not isinstance(val, str): return ""
            try:
                score = int(val.replace(" %", ""))
                if score >= 60: return "color: #FF4B4B; font-weight: bold;" # Élevé
                elif score >= 30: return "color: #FFA421; font-weight: bold;" # Moyen
                else: return "color: #859356; font-weight: bold;" # Faible
            except:
                return ""

        styled_df = display_df.style.map(style_risk, subset=["Taux"])
        st.dataframe(styled_df, hide_index=True, use_container_width=True, height=400)
    else:
        st.markdown(
            '<div style="text-align:center;padding:56px 24px;background:linear-gradient(135deg,rgba(115,125,116,0.04),transparent);'
            'border:1px dashed rgba(115,125,116,0.3);border-radius:16px;margin-top:8px">'
            '<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#A0AAB2" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:14px">'
            '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
            '<div style="font-size:15px;font-weight:600;color:#2A432E;margin-bottom:6px">Aucun résultat</div>'
            '<div style="font-size:13px;color:#737D74">Essayez de modifier vos filtres ou votre recherche.</div></div>',
            unsafe_allow_html=True)
    
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(label=" Télécharger la liste (CSV)", data=csv, file_name="adherents_risque.csv", mime="text/csv")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== AUDIENCE WEB =====================
elif tab == "Audience web":
    ak = D.audience_kpis(fd)
    ad = D.audience_device(fd)
    pt = D.pages_top(fd)
    
    def fmts(secs):
        if secs < 60: return f"{int(secs)} s"
        m = int(secs) // 60
        s = int(secs) % 60
        return f"{m} min {s:02d} s"

    html = f"""
    <div class="mu-kpigrid" style="grid-template-columns:repeat(3,minmax(0,1fr))">
        <div class="mu-kpi lime"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg></div><div class="l">Sessions</div><div class="v">{nb(ak['sessions'])}</div><div class="s">sur la période</div></div>
        <div class="mu-kpi olive"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg></div><div class="l">Utilisateurs</div><div class="v">{nb(ak['users'])}</div><div class="s">visiteurs uniques</div></div>
        <div class="mu-kpi accent"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 10h16M4 14h16M4 18h16" /></svg></div><div class="l">Pages vues</div><div class="v">{nb(int(ak['views']))}</div><div class="s">{ak['pages_session']:.1f} / session</div></div>
        <div class="mu-kpi dark"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg></div><div class="l">Durée moy. session</div><div class="v">{fmts(ak['duration_s'])}</div><div class="s">toutes sources</div></div>
        <div class="mu-kpi lime"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" /></svg></div><div class="l">Pages / session</div><div class="v">{ak['pages_session']:.1f}</div><div class="s">profondeur</div></div>
        <div class="mu-kpi danger"><div class="icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" /></svg></div><div class="l">Taux de rebond</div><div class="v">{ak['bounce_rate']*100:.0f}<span class="u"> %</span></div><div class="s">sessions 1 page</div></div>
    </div>
    
    <div class="mu-grid2e">
        <div class="mu-card">
            <h2 class="mu-h2">Par appareil.</h2>
            <p class="mu-sub2">Répartition des sessions.</p>
    """
    
    dev_colors = {"mobile": "#AACB55", "desktop": "#2A432E", "tablette": "#D6E393"}
    top_device = "mobile"
    top_pct = 0
    if not ad.empty:
        top_device = ad.iloc[0]["device"]
        top_pct = ad.iloc[0]["pct_sessions"]
        for _, r in ad.iterrows():
            d_name = r["device"]
            d_pct = r["pct_sessions"]
            d_dur = fmts(r["duree_s"])
            d_reb = r["rebond"] * 100
            color = dev_colors.get(d_name, "#D6E393")
            html += f'<div style="margin-bottom:15px"><div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px"><span style="font-weight:500;text-transform:capitalize">{d_name}</span><span style="color:#737D74">{d_pct:.0f} % · {d_dur} · rebond {d_reb:.0f} %</span></div><div style="height:22px;border-radius:3px;background:color-mix(in srgb,#737D74 8%,transparent)"><div style="height:100%;width:{d_pct:.1f}%;border-radius:3px;background:{color}"></div></div></div>'

    html += f"""
        </div>
        <div class="mu-card">
            <h2 class="mu-h2">Pages les plus vues.</h2>
            <table class="mu-table">
                <thead>
                    <tr><th>Page</th><th>Vues</th><th>Durée moy.</th><th>Sortie</th></tr>
                </thead>
                <tbody style="color:#2A432E">
    """
    
    top_conv_page = "Essai gratuit"
    if not pt.empty:
        for _, r in pt.head(8).iterrows():
            html += f'<tr><td style="font-weight:600;color:#2A432E">{r["page"]}</td><td>{nb(r["vues"])}</td><td style="color:#737D74">{fmts(r["duree_s"])}</td><td>{r["sortie"]*100:.0f} %</td></tr>'
            
    html += f"""
                </tbody>
            </table>
        </div>
    </div>
    
    <div style="background:#FFFDF8;border:1px solid color-mix(in srgb,#737D74 25%,transparent);border-radius:4px;border-left:3px solid #AACB55;padding:18px 20px">
        <div style="font-size:13px;font-weight:600;color:#2A432E;margin-bottom:6px">Lecture</div>
        <p style="margin:0;font-size:12.5px;color:#737D74;line-height:1.5">
            <b style="color:#2A432E">{top_pct:.0f} % du trafic est {top_device}</b>. 
            L'analyse des taux de sortie par page indique les prochains chantiers d'optimisation de la conversion.
        </p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

st.markdown(f'<div style="text-align:center;color:{MUTE};font-size:11px;margin-top:24px">'
            'MoveUp · Projet SalesOps Epitech · prototype Streamlit — données fictives.</div>', unsafe_allow_html=True)
