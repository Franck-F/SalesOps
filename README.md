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

## 📦 Livrables par jour

### Jour 1 — Cadrage & définition du cas
| Livrable | Fichier |
|---|---|
| Dossier d'entreprise | [01-Dossier-entreprise.md](01-Dossier-entreprise.md) |
| Dictionnaire de données — **CIBLE** (idéal) | [02-Dictionnaire-de-variables.md](02-Dictionnaire-de-variables.md) · [.docx](02-Dictionnaire-de-variables.docx) |
| Dictionnaire de données — **ACTUEL** (Excel) | [02b-Dictionnaire-de-donnees-ACTUEL.md](02b-Dictionnaire-de-donnees-ACTUEL.md) |

### Jour 2 — Diagnostic & analyse
| Livrable | Fichier |
|---|---|
| Processus de vente **AS-IS** (+ irritants) | [03-Processus-vente-AS-IS.md](03-Processus-vente-AS-IS.md) · [PNG](03-Processus-vente-AS-IS.png) |
| Modèle de données (ERD, 10 entités) | [04-Modele-de-donnees.excalidraw](04-Modele-de-donnees.excalidraw) |

### Données (pour le prototype)
| Jeu de données | Fichier |
|---|---|
| **ACTUEL** — Excel « suivi prospects » brouillon | [Data base/05-Donnees-ACTUELLES-suivi-prospects.xlsx](Data%20base/05-Donnees-ACTUELLES-suivi-prospects.xlsx) |
| **CIBLE** — 10 entités structurées (+ KPI) | [Data base/06-Donnees-CIBLE.xlsx](Data%20base/06-Donnees-CIBLE.xlsx) · [README](06-Donnees-CIBLE-README.md) · [CSV](data-cible/) |
| **Base adhérents** — 1 200 actifs enrichis | [Data base/07-Base-adherents.xlsx](Data%20base/07-Base-adherents.xlsx) |

### Jours 3 & 4 — Stratégie, prototype & pitch *(en cours)*
- Funnel **TO-BE** + règles de passage · outils · KPI · gouvernance
- **Prototype : dashboard de pilotage** (funnel, conversion, ROI canal, churn)
- Support de soutenance

---

## 🗂️ Modèle de données (10 entités)

**CRM (8)** : `dim_utilisateur` · `fact_lead` (pivot) · `dim_membre` · `fact_abonnement` ·
`fact_paiement` · `fact_interaction` · `fact_rdv` · `fact_checkin`
**Acquisition / marketing (2)** : `fact_acquisition` · `fact_newsletter`

Détail des variables, types et KPI → [02-Dictionnaire-de-variables.md](02-Dictionnaire-de-variables.md).

---

## 📈 Chiffres clés du cas (estimés)

| | Valeur |
|---|---|
| Conversion globale lead → adhérent | **13 %** (200 → 26 / mois) |
| Speed-to-lead moyen | ~26 h |
| No-show sur essais | 40 % |
| MRR / ARPM | ~67 k€ / ~56 € |
| Adhérents à risque de churn élevé | 333 |
| ROI : CAC Instagram vs Google Ads | 84 € vs 364 € |
