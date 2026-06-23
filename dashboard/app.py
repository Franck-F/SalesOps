# -*- coding: utf-8 -*-
"""Dashboard de pilotage SalesOps — MoveUp (prototype J4).
Design « MoveUp » (Poppins, crème/vert/lime) appliqué à Streamlit.
Lancer :  streamlit run dashboard/app.py   (depuis la racine du repo)."""
import sys
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).resolve().parent))
import data as D  # noqa: E402

# ---------- Palette ----------
CREAM, INK, MUTE = "#FFFDF8", "#2A432E", "#737D74"
LIME, OLIVE, LIGHT = "#AACB55", "#859356", "#D6E393"

st.set_page_config(page_title="MoveUp — Pilotage SalesOps", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stApp, button, input, select, textarea {
  font-family:'Poppins', system-ui, sans-serif; }
.stApp { background:#FFFDF8; color:#2A432E; }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display:none; }
[data-testid="stHeader"] { background:transparent; }
.block-container { padding-top:1.4rem; padding-bottom:3rem; max-width:1320px; }
::selection { background:rgba(170,203,85,0.35); }

/* ----- Sidebar sombre ----- */
[data-testid="stSidebar"] { background:#2A432E; }
[data-testid="stSidebar"] * { color:#FFFDF8; }
[data-testid="stSidebar"] .block-container { padding-top:1.5rem; }
.mu-logo { font-weight:700; font-size:20px; letter-spacing:-0.03em; text-transform:uppercase; }
.mu-logo span { color:#AACB55; }
.mu-sub { font-size:11px; letter-spacing:0.12em; text-transform:uppercase;
  color:rgba(255,253,248,0.5); margin:6px 0 14px; }
[data-testid="stSidebar"] hr { border-color:rgba(255,253,248,0.12); }
[data-testid="stSidebar"] [role="radiogroup"] { gap:4px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
  padding:9px 12px; border-radius:4px; border-left:2px solid transparent;
  font-size:14px; color:rgba(255,253,248,0.65); cursor:pointer; transition:.15s; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover { color:#fff; }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
  background:rgba(170,203,85,0.16); color:#FFFDF8; border-left-color:#AACB55; font-weight:600; }
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display:none; }
.mu-salle { border:1px solid rgba(255,253,248,0.14); border-radius:6px; padding:13px; margin-top:18px; }
.mu-salle .k { font-size:10.5px; letter-spacing:0.1em; text-transform:uppercase; color:rgba(255,253,248,0.5); }
.mu-salle .v { font-size:14px; font-weight:600; margin-top:3px; }
.mu-salle .s { font-size:12px; color:rgba(255,253,248,0.55); margin-top:2px; }

/* ----- Cartes / éléments ----- */
.mu-card { background:#FFFDF8; border:1px solid color-mix(in srgb,#737D74 25%,transparent);
  border-radius:4px; padding:22px; margin-bottom:16px; }
.mu-h2 { margin:0 0 4px; font-size:16px; font-weight:700; text-transform:uppercase;
  letter-spacing:-0.01em; color:#2A432E; }
.mu-sub2 { margin:0 0 16px; font-size:12px; color:#737D74; }
.mu-kpigrid { display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:13px; margin-bottom:22px; }
.mu-kpi { background:#FFFDF8; border:1px solid color-mix(in srgb,#737D74 25%,transparent);
  border-radius:4px; padding:16px; }
.mu-kpi.accent { border-left:3px solid #2A432E; }
.mu-kpi .l { font-size:10px; letter-spacing:0.07em; text-transform:uppercase; color:#737D74; font-weight:500; }
.mu-kpi .v { font-size:26px; font-weight:700; letter-spacing:-0.02em; margin-top:9px; line-height:1; white-space:nowrap; }
.mu-kpi .v .u { font-size:15px; color:#859356; }
.mu-kpi .s { font-size:11px; color:#737D74; margin-top:8px; }
.mu-grid2 { display:grid; grid-template-columns:minmax(0,1.25fr) minmax(0,1fr); gap:16px; }
.mu-grid2e { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.mu-grid3 { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
.mu-grid4 { display:grid; grid-template-columns:repeat(4,1fr); gap:13px; }
.mu-mini { border:1px solid color-mix(in srgb,#737D74 18%,transparent); border-radius:4px; padding:14px; }
.mu-mini .l { font-size:10px; letter-spacing:0.05em; text-transform:uppercase; color:#737D74; }
.mu-mini .v { font-size:23px; font-weight:700; color:#2A432E; margin-top:6px; line-height:1; }
.mu-mini .v .u { font-size:13px; color:#859356; }
.mu-mini .s { font-size:11px; color:#737D74; margin-top:7px; }
.mu-row { display:flex; justify-content:space-between; font-size:12.5px; margin-bottom:5px; }
.mu-track { height:24px; border-radius:3px; background:color-mix(in srgb,#737D74 8%,transparent); }
.mu-fill { height:100%; border-radius:3px; }
.mu-callout { border-radius:0 4px 4px 0; padding:13px 15px; font-size:12.5px; line-height:1.5; }
.mu-tbl { width:100%; border-collapse:collapse; font-size:13px; }
.mu-tbl th { text-align:right; color:#737D74; font-size:10px; letter-spacing:0.05em;
  text-transform:uppercase; font-weight:500; padding:0 0 10px; }
.mu-tbl th:first-child, .mu-tbl td:first-child { text-align:left; }
.mu-tbl td { text-align:right; padding:11px 0; border-top:1px solid color-mix(in srgb,#737D74 18%,transparent); }
.mu-dark { background:#2A432E; color:#FFFDF8; border-radius:4px; padding:22px; }
h1.mu-title { margin:0; font-size:29px; font-weight:700; letter-spacing:-0.03em;
  text-transform:uppercase; color:#2A432E; line-height:1; }
.mu-badge { display:inline-flex; align-items:center; gap:7px; background:#D6E393; border-radius:4px;
  padding:8px 12px; font-size:11px; font-weight:600; letter-spacing:0.05em; text-transform:uppercase; color:#2A432E; }
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


d = get_data()

PLOT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", color=INK), margin=dict(l=8, r=8, t=8, b=8))


def bar(label, value_txt, pct, color, h=24):
    return (f'<div style="margin-bottom:13px"><div class="mu-row">'
            f'<span style="font-weight:500">{label}</span><span style="color:{MUTE}">{value_txt}</span></div>'
            f'<div class="mu-track" style="height:{h}px"><div class="mu-fill" '
            f'style="width:{pct:.1f}%;background:{color}"></div></div></div>')


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="mu-logo">MoveUp<span>.</span></div>'
                '<div class="mu-sub">Pilotage SalesOps</div>', unsafe_allow_html=True)
    st.markdown("---")
    tab = st.radio("nav", ["Vue d'ensemble", "Funnel & commercial",
                           "Acquisition / ROI", "Rétention / churn"], label_visibility="collapsed")
    st.markdown("---")
    periode = st.selectbox("Période", ["12 semaines", "8 semaines", "4 semaines", "Juin 2026"])
    st.markdown('<div class="mu-salle"><div class="k">Salle</div>'
                '<div class="v">MoveUp · Versailles</div>'
                '<div class="s">1 000 m² · 1 200 adhérents</div></div>', unsafe_allow_html=True)

# ---------- Filtrage période (flux) — stocks (MRR/adhérents/churn) inchangés ----------
fd = D.filter_period(d, periode)
k = D.kpis(fd)
q = D.qualite_commerciale(fd)
roi = D.roi_canal(fd)
ch = D.churn_view(d)
lead = fd["lead"]
n_perdu = int((lead.statut_lead == "perdu").sum())
n_gagne = int((lead.statut_lead == "gagne").sum())
open_mask = lead.statut_lead.isin(["nouveau", "contacte", "visite", "essai"])
n_encours = int(open_mask.sum())
n_chauds = int((open_mask & (lead.score >= 70)).sum())

# ---------- Header ----------
hc = st.columns([3, 1])
with hc[0]:
    st.markdown('<h1 class="mu-title">Pilotage commercial.</h1>'
                f'<p style="margin:9px 0 0;font-size:14px;color:{MUTE}">Ce qu\'un Excel partagé ne '
                'montrait pas — leads, conversion, acquisition &amp; rétention, en un coup d\'œil.</p>',
                unsafe_allow_html=True)
with hc[1]:
    st.markdown('<div style="text-align:right;margin-top:6px"><span class="mu-badge">'
                '<span style="width:7px;height:7px;border-radius:50%;background:#859356"></span>'
                'Modèle CIBLE · fictif</span></div>', unsafe_allow_html=True)

# ---------- KPI row (toujours visible) ----------
kpis_html = '<div class="mu-kpigrid">'
kpis_html += f'<div class="mu-kpi"><div class="l">MRR · revenu mensuel</div><div class="v">{nb(k["mrr"])} <span class="u">€</span></div><div class="s">Base abonnements actifs</div></div>'
kpis_html += f'<div class="mu-kpi"><div class="l">ARPM · panier moyen</div><div class="v">{pc(k["arpm"])} <span class="u">€</span></div><div class="s">Essentiel 49 € · Premium 69 €</div></div>'
kpis_html += f'<div class="mu-kpi"><div class="l">Adhérents actifs</div><div class="v">{nb(k["n_actifs"])}</div><div class="s">Capacité max 170 simultanés</div></div>'
kpis_html += f'<div class="mu-kpi"><div class="l">Conversion lead → adhérent</div><div class="v">{pc(k["conv"]*100)} <span class="u">%</span></div><div class="s">{k["n_adh"]} adhésions / {k["n_leads"]} leads</div></div>'
kpis_html += f'<div class="mu-kpi accent"><div class="l">Risque de churn estimé</div><div class="v">{k["risque_eleve"]}</div><div class="s" style="color:#2A432E;font-weight:600">{round(100*k["risque_eleve"]/ch["total"])} % de la base · à cibler</div></div>'
kpis_html += f'<div class="mu-kpi accent"><div class="l">Résiliations · 30 j</div><div class="v">{k["churn30"]}</div><div class="s" style="color:#2A432E;font-weight:600">+ {ch["inactifs"]} inactifs &gt; 30 j</div></div>'
kpis_html += '</div>'

f = D.funnel(fd)
fv = dict(zip(f.etape, f.volume))
fcolors = {"Lead": LIME, "Contacté": LIME, "Visite": OLIVE, "Essai réalisé": OLIVE, "Adhésion": INK}

# ===================== VUE D'ENSEMBLE =====================
if tab == "Vue d'ensemble":
    st.markdown(kpis_html, unsafe_allow_html=True)
    g = st.columns([1.25, 1])
    with g[0]:
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
                     f'<div style="flex:1"><div class="mu-track" style="height:30px"><div class="mu-fill" style="height:100%;width:{pct:.1f}%;background:{col}"></div></div></div>'
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

    st.markdown(
        '<div class="mu-card"><div class="mu-h2">Qualité commerciale.</div><div class="mu-grid4" style="margin-top:14px">'
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
        dep = f'{nb(r.depense)} €' if r.depense else '0 € · organique'
        cpl = f'{r.cpl:.0f} €' if r.cpl == r.cpl else '—'
        cac = f'{r.cac:.0f} €' if r.cac == r.cac else '—'
        ccol = "#859356" if r.canal == "instagram" else INK
        rows += (f'<tr><td style="font-weight:600"><span style="display:inline-flex;align-items:center;gap:8px">'
                 f'<span style="width:9px;height:9px;border-radius:2px;background:{cbar.get(r.canal,OLIVE)}"></span>{r.canal.replace("_"," ").title()}</span></td>'
                 f'<td>{dep}</td><td>{int(r.leads)}</td><td>{int(r.adhesions)}</td><td>{cpl}</td>'
                 f'<td style="font-weight:600;color:{ccol}">{cac}</td><td>{pc(r.conv_pct)} %</td></tr>')
    st.markdown(
        '<div class="mu-card"><div class="mu-h2">ROI par canal.</div>'
        '<table class="mu-tbl"><thead><tr><th>Canal</th><th>Dépense</th><th>Leads</th><th>Adhésions</th>'
        f'<th>CPL</th><th>CAC</th><th>Conv.</th></tr></thead><tbody>{rows}</tbody></table></div>',
        unsafe_allow_html=True)
    st.markdown(
        '<div class="mu-grid2e">'
        f'<div class="mu-card" style="border-left:3px solid #AACB55;margin:0"><div style="font-size:13px;font-weight:600;margin-bottom:6px">Réallouer le payant</div>'
        f'<p style="margin:0;font-size:12.5px;color:{MUTE};line-height:1.5">Instagram est le canal le plus rentable. Basculer une partie du budget Google Ads vers Instagram améliorerait mécaniquement le ROI global.</p></div>'
        f'<div class="mu-card" style="border-left:3px solid #859356;margin:0"><div style="font-size:13px;font-weight:600;margin-bottom:6px">Activer l\'organique</div>'
        f'<p style="margin:0;font-size:12.5px;color:{MUTE};line-height:1.5">Recommandation + site web : 0 € de dépense pour 18 adhésions. Un programme de parrainage structuré démultiplierait ce canal gratuit.</p></div>'
        '</div>', unsafe_allow_html=True)

# ===================== RÉTENTION / CHURN =====================
else:
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
            f'<div class="mu-mini"><div class="l">Inactifs &gt; 30 j</div><div class="v">{ch["inactifs"]}</div><div class="s">sans visite</div></div>'
            f'<div class="mu-mini"><div class="l">Risque élevé</div><div class="v">{int(seg.get("Élevé",0))}</div><div class="s">à cibler en priorité</div></div>'
            f'<div class="mu-mini"><div class="l">Utilisent le coaching</div><div class="v">{ch["coaching"]:.0f} <span class="u">%</span></div><div class="s">levier d\'upsell</div></div>'
            f'<div class="mu-mini"><div class="l">Abonnés Premium</div><div class="v">{ch["premium"]:.0f} <span class="u">%</span></div><div class="s">montée en gamme</div></div>'
            '</div><div class="mu-callout" style="margin-top:16px;border-left:2px solid #2A432E;background:color-mix(in srgb,#2A432E 4%,transparent)">'
            f'<b>{int(seg.get("Élevé",0))} adhérents à risque élevé</b> + <b>{ch["inactifs"]} inactifs</b> : cibles prioritaires de rétention. '
            f'Seulement {ch["coaching"]:.0f} % utilisent le coaching → fort potentiel d\'upsell.</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="mu-card"><div class="mu-h2">Base adhérents.</div>'
                '<div class="mu-sub2">Filtrer par niveau de risque pour cibler les actions de rétention.</div>', unsafe_allow_html=True)
    seg_sel = st.selectbox("Risque", ["Tous", "Élevé", "Moyen", "Faible"], label_visibility="collapsed")
    a = d["adherents"]
    if seg_sel != "Tous":
        a = a[a.segment_risque == seg_sel]
    cols = ["membre_id", "prenom", "nom", "commune", "formule", "montant_mensuel",
            "anciennete_mois", "frequence_hebdo", "utilisation_coaching", "score_risque_churn", "segment_risque"]
    st.caption(f"{len(a)} adhérent(s)")
    st.dataframe(a[cols].sort_values("score_risque_churn", ascending=False),
                 hide_index=True, use_container_width=True, height=300)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div style="text-align:center;color:{MUTE};font-size:11px;margin-top:24px">'
            'MoveUp · Projet SalesOps Epitech · prototype Streamlit — données fictives.</div>', unsafe_allow_html=True)
