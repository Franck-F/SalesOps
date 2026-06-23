# -*- coding: utf-8 -*-
"""Couche données du dashboard MoveUp SalesOps — pandas pur (aucune dépendance Streamlit).
Lit les CSV CIBLE (../data-cible) et calcule les vues/KPI. Importable et testable seul."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
TODAY = pd.Timestamp("2026-06-23")


def _find_data_dir():
    """Localise le dossier des CSV CIBLE, robuste aux réorganisations du repo."""
    for c in [ROOT / "data-cible", ROOT / "Data base" / "data-cible"]:
        if (c / "fact_lead.csv").exists():
            return c
    for p in ROOT.rglob("fact_lead.csv"):
        return p.parent
    raise FileNotFoundError("Dossier data-cible introuvable (fact_lead.csv manquant)")


DATA_DIR = _find_data_dir()


def load_all():
    """Charge tous les CSV CIBLE et type les dates. Retourne un dict de DataFrames."""
    def read(name):
        return pd.read_csv(DATA_DIR / name)

    d = {
        "lead": read("fact_lead.csv"),
        "membre": read("dim_membre.csv"),
        "abo": read("fact_abonnement.csv"),
        "interaction": read("fact_interaction.csv"),
        "rdv": read("fact_rdv.csv"),
        "checkin": read("fact_checkin.csv"),
        "paiement": read("fact_paiement.csv"),
        "acquisition": read("fact_acquisition.csv"),
        "newsletter": read("fact_newsletter.csv"),
        "user": read("dim_utilisateur.csv"),
        "adherents": read("base_adherents.csv"),
    }
    for c in ["date_creation", "date_premier_contact", "date_cloture"]:
        d["lead"][c] = pd.to_datetime(d["lead"][c], errors="coerce")
    d["membre"]["date_adhesion"] = pd.to_datetime(d["membre"]["date_adhesion"], errors="coerce")
    d["membre"]["date_dernier_passage"] = pd.to_datetime(d["membre"]["date_dernier_passage"], errors="coerce")
    d["abo"]["date_resiliation"] = pd.to_datetime(d["abo"]["date_resiliation"], errors="coerce")
    d["acquisition"]["date"] = pd.to_datetime(d["acquisition"]["date"], errors="coerce")
    d["adherents"]["date_dernier_passage"] = pd.to_datetime(d["adherents"]["date_dernier_passage"], errors="coerce")
    return d


def kpis(d):
    lead, membre, abo = d["lead"], d["membre"], d["abo"]
    n_actifs = int((membre.statut_membre == "actif").sum())
    mrr = float(abo[abo.statut_abonnement.isin(["actif", "suspendu_impaye"])]["montant_mensuel"].sum())
    n_leads = len(lead)
    n_adh = int((lead.statut_lead == "gagne").sum())
    churn30 = int(abo[abo.date_resiliation.notna() & ((TODAY - abo.date_resiliation).dt.days <= 30)].shape[0])
    risque = int((d["adherents"].segment_risque == "Élevé").sum())
    return {
        "mrr": mrr,
        "arpm": mrr / n_actifs if n_actifs else 0.0,
        "n_actifs": n_actifs,
        "n_leads": n_leads,
        "n_adh": n_adh,
        "conv": n_adh / n_leads if n_leads else 0.0,
        "churn30": churn30,
        "risque_eleve": risque,
    }


def funnel(d):
    lead, rdv = d["lead"], d["rdv"]
    visite = rdv[(rdv.type_rdv == "visite") & (rdv.statut_rdv == "realise")].lead_id.nunique()
    essai = rdv[(rdv.type_rdv == "essai") & (rdv.statut_rdv == "realise")].lead_id.nunique()
    return pd.DataFrame({
        "etape": ["Lead", "Contacté", "Visite", "Essai réalisé", "Adhésion"],
        "volume": [
            len(lead),
            int(lead.date_premier_contact.notna().sum()),
            int(visite),
            int(essai),
            int((lead.statut_lead == "gagne").sum()),
        ],
    })


def qualite_commerciale(d):
    lead, rdv = d["lead"], d["rdv"]
    c = lead[lead.date_premier_contact.notna()]
    stl = ((c.date_premier_contact - c.date_creation).dt.total_seconds() / 3600).mean()
    essai = rdv[rdv.type_rdv == "essai"]
    no_show = (essai.statut_rdv == "no_show").mean() * 100 if len(essai) else 0
    won = set(lead.loc[lead.statut_lead == "gagne", "lead_id"])
    essai_real = essai[essai.statut_rdv == "realise"]
    nonconv = essai_real[~essai_real.lead_id.isin(won)]
    relance = (nonconv.relance_post_essai == "vrai").mean() * 100 if len(nonconv) else 0
    gagne = lead[lead.statut_lead == "gagne"]
    cycle = ((gagne.date_cloture - gagne.date_creation).dt.days).mean()
    return {"speed_to_lead": float(stl), "no_show": float(no_show),
            "relance": float(relance), "cycle": float(cycle)}


def roi_canal(d):
    acq, lead = d["acquisition"], d["lead"]
    g = acq.groupby("canal").agg(depense=("depense", "sum"), leads=("leads_generes", "sum")).reset_index()
    adh = (lead[lead.statut_lead == "gagne"].groupby("source").size()
           .rename("adhesions").reset_index().rename(columns={"source": "canal"}))
    g = g.merge(adh, on="canal", how="left")
    g["adhesions"] = g["adhesions"].fillna(0).astype(int)
    g["cpl"] = (g.depense / g.leads).where(g.depense > 0)
    g["cac"] = (g.depense / g.adhesions).where((g.depense > 0) & (g.adhesions > 0))
    g["conv_pct"] = (g.adhesions / g.leads * 100).round(1)
    return g.sort_values("depense", ascending=False).reset_index(drop=True)


def churn_view(d):
    a = d["adherents"]
    seg = a.segment_risque.value_counts().reindex(["Faible", "Moyen", "Élevé"]).fillna(0).astype(int)
    inactifs = int((((TODAY - a.date_dernier_passage).dt.days) > 30).sum())
    return {"seg": seg, "inactifs": inactifs,
            "coaching": float((a.utilisation_coaching == "oui").mean() * 100),
            "premium": float((a.formule == "Premium").mean() * 100), "total": len(a)}


def leads_hebdo(d):
    lead = d["lead"].copy()
    lead["semaine"] = lead.date_creation.dt.to_period("W").dt.start_time
    gagne = lead[lead.statut_lead == "gagne"]
    s = lead.groupby("semaine").size().rename("Leads")
    a = gagne.groupby("semaine").size().rename("Adhésions")
    return pd.concat([s, a], axis=1).fillna(0).astype(int).reset_index()


def filter_period(d, label):
    """Filtre les FLUX (leads/rdv/acquisition/audience/pages) sur la période choisie.
    Les STOCKS (membres/abonnements/adhérents) restent inchangés (instantanés).
    label : '12 semaines' (= tout) · '8 semaines' · '4 semaines' · 'Juin 2026'."""
    lead = d["lead"]
    if not label or label.startswith("12") or label.lower().startswith("tout"):
        return d
    end = lead["date_creation"].max()
    if label.startswith("Juin"):
        def in_p(s):
            return (s.dt.year == 2026) & (s.dt.month == 6)
    else:
        wk = 8 if label.startswith("8") else 4
        start = end - pd.Timedelta(weeks=wk)

        def in_p(s):
            return s >= start
    fd = dict(d)
    fd["lead"] = lead[in_p(lead["date_creation"])]
    ids = set(fd["lead"]["lead_id"])
    if "rdv" in d:
        fd["rdv"] = d["rdv"][d["rdv"]["lead_id"].isin(ids)]
    for key in ("acquisition", "audience", "pages"):
        if key in d and "date" in d[key].columns:
            s = pd.to_datetime(d[key]["date"], errors="coerce")
            fd[key] = d[key][in_p(s)]
    return fd


if __name__ == "__main__":
    d = load_all()
    print("Tables:", {k: len(v) for k, v in d.items()})
    print("KPIs:", {k: round(v, 2) if isinstance(v, float) else v for k, v in kpis(d).items()})
    print("Funnel:\n", funnel(d).to_string(index=False))
    print("Qualité:", {k: round(v, 1) for k, v in qualite_commerciale(d).items()})
    print("ROI canal:\n", roi_canal(d).to_string(index=False))
    print("Churn:", {k: (v.to_dict() if hasattr(v, "to_dict") else v) for k, v in churn_view(d).items()})
