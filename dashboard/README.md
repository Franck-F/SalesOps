# Dashboard MoveUp — Prototype SalesOps (Jour 4)

Prototype de **dashboard de pilotage commercial** (Streamlit + Plotly) branché sur le jeu de
données **CIBLE** de MoveUp. Il rend visible ce qu'un simple Excel ne permettait pas de voir.

## ▶️ Lancer le dashboard

```bash
# 1. installer les dépendances (idéalement dans un venv)
pip install -r dashboard/requirements.txt

# 2. lancer (depuis la racine du repo)
streamlit run dashboard/app.py
```

Le navigateur s'ouvre sur `http://localhost:8501`.

## 🧩 Structure

| Fichier | Rôle |
|---|---|
| `data.py` | Couche données **pandas pure** : charge les CSV CIBLE et calcule funnel, KPI, ROI, churn. Testable seule (`python dashboard/data.py`). |
| `app.py` | Interface **Streamlit** : KPI, graphiques Plotly, onglets, callouts de diagnostic. |
| `requirements.txt` | Dépendances. |

> Le chemin des données est **auto-détecté** (`data-cible/` ou `Data base/data-cible/`),
> robuste aux réorganisations du repo.

## 📊 Ce que montre le dashboard

- **KPI** : MRR, ARPM, adhérents actifs, conversion, churn, adhérents à risque.
- **Funnel & commercial** : entonnoir Lead→Adhésion, speed-to-lead, no-show, relance post-essai, volume hebdo.
- **Acquisition / ROI** : CAC & CPL par canal (l'insight Instagram vs Google Ads), parrainage.
- **Rétention / churn** : segments de risque, inactifs, potentiel d'upsell coaching, base adhérents filtrable.
- **Données** : explorateur des 11 tables du modèle CIBLE.
