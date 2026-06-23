# MoveUp — Projet SalesOps (Epitech, promotion 2026)

Mission de conseil **SalesOps** : structurer la performance commerciale d'une entreprise B2C
en croissance dont l'exécution stagne par **manque de structure**. Cas fictif réaliste : **MoveUp**.

> Logique du projet : **« No pain, no change »** — on rend visibles les irritants (AS-IS),
> puis on conçoit la cible (TO-BE) et un **prototype** démontrable.

---

## 🏢 L'entreprise (cas fictif)

**MoveUp** — salle de sport **indépendante** à **Versailles** · 1 000 m² · **1 200 adhérents** ·
équipe de 7 · offres Essentiel (49 €) / Premium (69 €) / coaching.
Bonne offre, bonne réputation, du trafic… mais **perd de l'argent faute de structure** :
pas de CRM (Excel + tél. perso), funnel non défini, zéro automatisation, aucun KPI fiable.

---

## 🗂️ Arborescence

| Dossier / fichier | Contenu |
|---|---|
| [`J1/`](J1/) | Dossier d'entreprise, dictionnaires, process AS-IS, modèle de données |
| [`Data base/`](Data%20base/) | Jeux de données Excel + CSV (`Data base/data-cible/`) |
| [`dashboard/`](dashboard/) | **Prototype dashboard Streamlit** (J4) |
| [`J3-Strategie-conception.md`](J3-Strategie-conception.md) | Plan & stratégie du Jour 3 (TO-BE) |

---

## 📦 Livrables par jour

### Jour 1 — Cadrage & définition du cas
| Livrable | Fichier |
|---|---|
| Dossier d'entreprise | [J1/01-Dossier-entreprise.md](J1/01-Dossier-entreprise.md) |
| Dictionnaire de données — **CIBLE** (idéal) | [J1/02-Dictionnaire-de-variables.md](J1/02-Dictionnaire-de-variables.md) · [.docx](J1/02-Dictionnaire-de-variables.docx) |
| Dictionnaire de données — **ACTUEL** (Excel) | [J1/02b-Dictionnaire-de-donnees-ACTUEL.md](J1/02b-Dictionnaire-de-donnees-ACTUEL.md) |

### Jour 2 — Diagnostic & analyse
| Livrable | Fichier |
|---|---|
| Processus de vente **AS-IS** (+ irritants) | [J1/03-Processus-vente-AS-IS.md](J1/03-Processus-vente-AS-IS.md) · [PNG](J1/03-Processus-vente-AS-IS.png) |
| Modèle de données (ERD, 10 entités) | [J1/04-Modele-de-donnees.excalidraw](J1/04-Modele-de-donnees.excalidraw) |

### Données (pour le prototype)
| Jeu de données | Fichier |
|---|---|
| **ACTUEL** — Excel « suivi prospects » brouillon | [Data base/05-…xlsx](Data%20base/05-Donnees-ACTUELLES-suivi-prospects.xlsx) |
| **CIBLE** — 10 entités structurées (+ KPI) | [Data base/06-…xlsx](Data%20base/06-Donnees-CIBLE.xlsx) · [README](J1/06-Donnees-CIBLE-README.md) · [CSV](Data%20base/data-cible/) |
| **Base adhérents** — 1 200 actifs enrichis | [Data base/07-…xlsx](Data%20base/07-Base-adherents.xlsx) |

### Jour 3 — Stratégie & conception
- [J3-Strategie-conception.md](J3-Strategie-conception.md) : KPI cibles, **funnel TO-BE + règles de passage**, outils, gouvernance.

### Jour 4 — Prototype & pitch
- ✅ **Dashboard Streamlit fonctionnel** → [`dashboard/`](dashboard/) (funnel, ROI canal, churn, base adhérents).

---

## ▶️ Lancer le dashboard

```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

---

## 🗂️ Modèle de données (10 entités)

**CRM (8)** : `dim_utilisateur` · `fact_lead` (pivot) · `dim_membre` · `fact_abonnement` ·
`fact_paiement` · `fact_interaction` · `fact_rdv` · `fact_checkin`
**Acquisition / marketing (2)** : `fact_acquisition` · `fact_newsletter`

Détail des variables, types et KPI → [J1/02-Dictionnaire-de-variables.md](J1/02-Dictionnaire-de-variables.md).

---

## 📈 Chiffres clés du cas

| | Valeur |
|---|---|
| Conversion globale lead → adhérent | **13,7 %** |
| Speed-to-lead moyen | ~26 h |
| No-show sur essais | 40 % |
| MRR / ARPM | ~67 k€ / ~56 € |
| Adhérents à risque de churn élevé | 333 |
| ROI : CAC Instagram vs Google Ads | **84 € vs 364 €** |
