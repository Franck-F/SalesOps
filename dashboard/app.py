# -*- coding: utf-8 -*-
"""Dashboard de pilotage SalesOps — MoveUp (prototype Jour 4).
Lancer :  streamlit run app.py   (ou  streamlit run dashboard/app.py  depuis la racine)."""
import sys
from pathlib import Path

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).resolve().parent))
import data as D  # noqa: E402

# ---------- Style ----------
NAVY, ORANGE, GREEN, RED, BLUE, AMBER = "#16324F", "#E86A17", "#2E7D52", "#C0392B", "#2E5E8C", "#E8A317"
SEG_COLORS = {"Faible": GREEN, "Moyen": AMBER, "Élevé": RED}

st.set_page_config(page_title="MoveUp — Pilotage SalesOps", page_icon="📊", layout="wide")
st.markdown(f"""
<style>
.block-container {{padding-top: 1.6rem;}}
h1, h2, h3 {{color: {NAVY};}}
[data-testid="stMetricValue"] {{color: {NAVY}; font-weight: 700;}}
</style>
""", unsafe_allow_html=True)


def eur(x):
    return f"{x:,.0f} €".replace(",", " ")


def pct(x):
    return f"{x:.1f} %".replace(".", ",")


@st.cache_data
def get_data():
    return D.load_all()


d = get_data()
k = D.kpis(d)
q = D.qualite_commerciale(d)
roi = D.roi_canal(d)
ch = D.churn_view(d)

# ---------- En-tête ----------
st.markdown(f"<h1 style='margin-bottom:0'>📊 MoveUp — Pilotage commercial (SalesOps)</h1>"
            f"<p style='color:{ORANGE};font-weight:600;margin-top:2px'>Prototype de dashboard · "
            f"salle de sport indépendante, Versailles · données fictives</p>", unsafe_allow_html=True)
st.caption("« No pain, no change » — ce que MoveUp ne pouvait pas voir avec un Excel, on le pilote ici.")

# ---------- KPI cards ----------
c = st.columns(6)
c[0].metric("MRR (revenu mensuel)", eur(k["mrr"]))
c[1].metric("ARPM (panier moyen)", f"{k['arpm']:.1f} €".replace(".", ","))
c[2].metric("Adhérents actifs", f"{k['n_actifs']:,}".replace(",", " "))
c[3].metric("Conversion lead → adhérent", pct(k["conv"] * 100))
c[4].metric("Adhérents à risque churn", k["risque_eleve"], delta="élevé", delta_color="inverse")
c[5].metric("Résiliations (30 j)", k["churn30"], delta_color="inverse")

st.divider()
t1, t2, t3, t4 = st.tabs(["📉 Funnel & commercial", "📣 Acquisition / ROI",
                          "🔁 Rétention / churn", "🗂️ Données"])

# ===================== TAB 1 : Funnel & commercial =====================
with t1:
    col_a, col_b = st.columns([1.1, 1])
    with col_a:
        f = D.funnel(d)
        fig = go.Figure(go.Funnel(y=f["etape"], x=f["volume"],
                                  marker={"color": [BLUE, BLUE, ORANGE, ORANGE, GREEN]},
                                  textinfo="value+percent initial"))
        fig.update_layout(title="Funnel de vente (mensuel)", height=380,
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.subheader("Qualité commerciale")
        m = st.columns(2)
        m[0].metric("Speed-to-lead (1er contact)", f"{q['speed_to_lead']:.0f} h")
        m[1].metric("No-show sur essais", pct(q["no_show"]))
        m2 = st.columns(2)
        m2[0].metric("Relance des essais non convertis", pct(q["relance"]))
        m2[1].metric("Durée moyenne du cycle", f"{q['cycle']:.0f} j")
        st.error(f"⏱️ **Speed-to-lead {q['speed_to_lead']:.0f} h** — beaucoup trop lent, la joignabilité chute.")
        st.error(f"🚫 **No-show {q['no_show']:.0f} %** sur les essais — aucune relance/confirmation automatisée.")
        st.warning(f"📞 **Seulement {q['relance']:.0f} %** des essais non convertis sont rappelés "
                   f"→ ~3 prospects chauds sur 4 sont perdus.")

    st.subheader("Volume hebdomadaire : leads vs adhésions")
    lh = D.leads_hebdo(d)
    figl = px.line(lh, x="semaine", y=["Leads", "Adhésions"], markers=True,
                   color_discrete_map={"Leads": BLUE, "Adhésions": GREEN})
    figl.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10),
                       legend_title="", yaxis_title="", xaxis_title="")
    st.plotly_chart(figl, use_container_width=True)

# ===================== TAB 2 : Acquisition / ROI =====================
with t2:
    st.subheader("ROI par canal d'acquisition")
    paid = roi[roi["cac"].notna()].copy()
    col1, col2 = st.columns([1, 1])
    with col1:
        figc = px.bar(paid, x="canal", y="cac", text="cac", color="canal",
                      color_discrete_map={"instagram": GREEN, "google_ads": RED},
                      title="Coût d'Acquisition Client (CAC) par canal payant")
        figc.update_traces(texttemplate="%{text:.0f} €", textposition="outside")
        figc.update_layout(height=360, showlegend=False, yaxis_title="CAC (€)",
                           xaxis_title="", margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(figc, use_container_width=True)
    with col2:
        figl = px.bar(roi, x="canal", y="leads", text="leads", color="canal",
                      title="Leads générés par canal",
                      color_discrete_map={"instagram": GREEN, "google_ads": RED,
                                          "site_web": BLUE, "recommandation": AMBER})
        figl.update_layout(height=360, showlegend=False, yaxis_title="Leads",
                           xaxis_title="", margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(figl, use_container_width=True)

    show = roi.copy()
    show["depense"] = show["depense"].map(lambda x: eur(x) if x else "0 € (organique)")
    show["cpl"] = show["cpl"].map(lambda x: f"{x:.0f} €" if x == x else "—")
    show["cac"] = show["cac"].map(lambda x: f"{x:.0f} €" if x == x else "—")
    show["conv_pct"] = show["conv_pct"].map(lambda x: f"{x:.1f} %")
    show.columns = ["Canal", "Dépense", "Leads", "Adhésions", "CPL", "CAC", "Conv. %"]
    st.dataframe(show, hide_index=True, use_container_width=True)

    cac_ig = roi.loc[roi.canal == "instagram", "cac"].iloc[0]
    cac_gg = roi.loc[roi.canal == "google_ads", "cac"].iloc[0]
    st.success(f"✅ **Instagram** est le canal le plus rentable : CAC **{cac_ig:.0f} €**.")
    st.error(f"🔴 **Google Ads** coûte **{cac_gg:.0f} €** par adhérent (~{cac_gg/cac_ig:.1f}× Instagram) "
             f"→ réallouer le budget.")
    st.info("📨 **Recommandation & site web** : 0 € de dépense, "
            f"{int(roi.loc[roi.canal=='recommandation','adhesions'].iloc[0]) + int(roi.loc[roi.canal=='site_web','adhesions'].iloc[0])} "
            "adhésions → activer un programme de parrainage.")

# ===================== TAB 3 : Rétention / churn =====================
with t3:
    col1, col2 = st.columns([1, 1.2])
    with col1:
        seg = ch["seg"]
        figp = px.pie(names=seg.index, values=seg.values, hole=0.55,
                      color=seg.index, color_discrete_map=SEG_COLORS,
                      title="Adhérents par niveau de risque de churn")
        figp.update_layout(height=360, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(figp, use_container_width=True)
    with col2:
        st.subheader("Signaux de rétention")
        mm = st.columns(2)
        mm[0].metric("Inactifs (> 30 j sans visite)", ch["inactifs"])
        mm[1].metric("Risque élevé", int(ch["seg"].get("Élevé", 0)))
        mm2 = st.columns(2)
        mm2[0].metric("Utilisent le coaching", pct(ch["coaching"]))
        mm2[1].metric("Abonnés Premium", pct(ch["premium"]))
        st.warning(f"🔴 **{int(ch['seg'].get('Élevé', 0))} adhérents à risque élevé** + "
                   f"**{ch['inactifs']} inactifs** : cibles prioritaires de rétention.")
        st.info(f"💰 Seulement **{ch['coaching']:.0f} %** utilisent le coaching → "
                "fort potentiel d'upsell sur les ~86 % restants.")

    st.subheader("Base adhérents — exploration")
    fcol = st.columns([1, 3])
    seg_sel = fcol[0].selectbox("Filtrer par risque", ["Tous", "Élevé", "Moyen", "Faible"])
    a = d["adherents"]
    if seg_sel != "Tous":
        a = a[a.segment_risque == seg_sel]
    cols = ["membre_id", "prenom", "nom", "commune", "formule", "montant_mensuel",
            "anciennete_mois", "frequence_hebdo", "utilisation_coaching",
            "score_risque_churn", "segment_risque"]
    fcol[1].caption(f"{len(a)} adhérent(s) affiché(s)")
    st.dataframe(a[cols].sort_values("score_risque_churn", ascending=False),
                 hide_index=True, use_container_width=True, height=300)

# ===================== TAB 4 : Données =====================
with t4:
    st.subheader("Explorateur des tables (modèle CIBLE)")
    names = {"lead": "fact_lead — Leads / opportunités", "membre": "dim_membre — Adhérents",
             "abo": "fact_abonnement — Abonnements", "paiement": "fact_paiement — Paiements",
             "interaction": "fact_interaction — Interactions", "rdv": "fact_rdv — Visites & essais",
             "checkin": "fact_checkin — Fréquentation", "acquisition": "fact_acquisition — Acquisition",
             "newsletter": "fact_newsletter — Newsletter", "user": "dim_utilisateur — Équipe",
             "adherents": "base_adherents — Base adhérents enrichie"}
    sel = st.selectbox("Table", list(names.keys()), format_func=lambda x: f"{x} — {names[x]}")
    st.caption(f"{len(d[sel])} lignes · {len(d[sel].columns)} colonnes")
    st.dataframe(d[sel].head(300), hide_index=True, use_container_width=True, height=420)

st.divider()
st.caption("MoveUp · Projet SalesOps Epitech · prototype Streamlit — données générées (fictives).")
