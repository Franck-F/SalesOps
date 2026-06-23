import pandas as pd
from data import load_all

d = load_all()
# Mock the data
d["audience"] = pd.read_csv("Data base/data-cible/fact_audience.csv")
d["pages"] = pd.read_csv("Data base/data-cible/fact_pages.csv")

def audience_kpis(d):
    if "audience" not in d or d["audience"].empty:
        return {"sessions":0, "users":0, "views":0, "duration_s":0, "pages_session":0, "bounce_rate":0}
    a = d["audience"]
    sess = a["sessions"].sum()
    users = a["utilisateurs"].sum()
    dur = (a["duree_moy_session_sec"] * a["sessions"]).sum() / sess if sess > 0 else 0
    pps = (a["pages_par_session"] * a["sessions"]).sum() / sess if sess > 0 else 0
    bounce = (a["taux_rebond"] * a["sessions"]).sum() / sess if sess > 0 else 0
    views = (a["pages_par_session"] * a["sessions"]).sum()
    return {
        "sessions": sess, "users": users, "views": views, 
        "duration_s": dur, "pages_session": pps, "bounce_rate": bounce
    }

def audience_device(d):
    if "audience" not in d or d["audience"].empty:
        return pd.DataFrame()
    a = d["audience"]
    g = a.groupby("device").apply(lambda x: pd.Series({
        "sessions": x["sessions"].sum(),
        "duree_s": (x["duree_moy_session_sec"] * x["sessions"]).sum() / x["sessions"].sum() if x["sessions"].sum() > 0 else 0,
        "rebond": (x["taux_rebond"] * x["sessions"]).sum() / x["sessions"].sum() if x["sessions"].sum() > 0 else 0
    })).reset_index()
    tot = g["sessions"].sum()
    g["pct_sessions"] = (g["sessions"] / tot) * 100 if tot > 0 else 0
    return g.sort_values("sessions", ascending=False)

def pages_top(d):
    if "pages" not in d or d["pages"].empty:
        return pd.DataFrame()
    p = d["pages"]
    g = p.groupby("page").apply(lambda x: pd.Series({
        "vues": x["pages_vues"].sum(),
        "duree_s": (x["duree_moy_page_sec"] * x["pages_vues"]).sum() / x["pages_vues"].sum() if x["pages_vues"].sum() > 0 else 0,
        "sortie": (x["taux_sortie"] * x["pages_vues"]).sum() / x["pages_vues"].sum() if x["pages_vues"].sum() > 0 else 0
    })).reset_index()
    return g.sort_values("vues", ascending=False)

print("KPIs:", audience_kpis(d))
print("Device:\n", audience_device(d))
print("Pages:\n", pages_top(d).head())
