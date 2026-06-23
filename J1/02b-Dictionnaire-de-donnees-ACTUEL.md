# Dictionnaire de données — ACTUEL (AS-IS) · MoveUp

> 🔴 **La réalité d'aujourd'hui** : MoveUp n'a **pas de CRM ni de modèle de données**. Tout tient dans **un seul fichier Excel partagé**, en saisie libre.
> À opposer au dictionnaire **CIBLE / idéal** → [02-Dictionnaire-de-variables.md](02-Dictionnaire-de-variables.md).
> Logique consultant : montrer **l'écart** entre ce qui existe et ce qu'il faudrait (« no pain, no change »).

---

## 1. Ce qui existe vraiment

- **1 fichier Excel** « Suivi prospects » partagé sur un drive, **1 seul onglet plat**.
- **Saisie libre**, sans règles, sans listes déroulantes, sans validation.
- Édité par **plusieurs personnes** (commercial + gérant) → écrasements, doublons.
- **Aucune table reliée** : interactions, paiements, fréquentation **n'y figurent pas**.
- D'autres données existent mais **ailleurs et non reliées** (tél. perso, logiciel de caisse, portique).

---

## 2. L'onglet « Suivi prospects » (le seul "modèle de données" actuel)

| Colonne Excel | Type réel | Censé contenir | Problèmes constatés |
|---|---|---|---|
| **Nom** | Texte libre | Nom du prospect | Parfois juste un prénom, parfois vide |
| **Téléphone** | Texte libre | Numéro | Formats hétérogènes (`06 12…`, `+33…`, `0612…`), **doublons** |
| **Email** | Texte libre | Email | **Souvent vide** |
| **Source** | Texte libre | Canal d'origine | Valeurs incohérentes : `insta` / `Instagram` / `IG` / `ami` / `pub` |
| **Date** | Date ou texte | *(ambigu : arrivée ? contact ?)* | Formats variables (`12/06`, `2026-06-12`, `lundi`), **souvent vide** |
| **Statut** | Texte libre | Étape du funnel | Vocabulaire libre : `à rappeler`, `venu`, `pas chaud`, `RDV` → **non normalisé** |
| **Essai** | Texte libre | A fait un essai ? | `oui` / `non` / `?` / vide |
| **Abonnement** | Texte libre | A signé ? | `oui` / `Premium` / vide (incohérent) |
| **Commentaire** | Texte libre | Notes diverses | Fourre-tout, **souvent vide** ou cryptique |
| **Responsable** | Texte libre | Qui suit le prospect | **Colonne souvent absente ou vide** |

> 👉 Conséquence directe : impossible de **dédoublonner**, de **prioriser**, de **mesurer** quoi que ce soit de fiable.

---

## 3. Données qui existent… mais hors de l'Excel (les 4 silos)

| Donnée | Où elle se trouve | État |
|---|---|---|
| Échanges **WhatsApp / SMS** | **Tél. personnel** du gérant | Non centralisé, invisible pour l'équipe, perdu |
| **Abonnements & paiements** | Logiciel de caisse | Séparé, **non relié** au prospect Excel |
| **Fréquentation** (badges/portique) | Système de contrôle d'accès | **Jamais exploitée** (≠ relié au membre) |
| **Données marketing** (clics, CTR, temps sur site, newsletter) | Google Analytics · Meta/Google Ads · outil d'emailing | **Jamais reliées** aux leads → **ROI par canal inconnu** |

---

## 4. Problèmes structurels (synthèse)

1. **Aucun identifiant unique** → doublons, pas de liaison possible.
2. **Un seul onglet plat** → pas de relations (1 prospect = 1 ligne, le reste se perd).
3. **Saisie libre** → pas de référentiels, pas de types, pas de contrôle qualité.
4. **Une seule date ambiguë** → impossible de calculer le *speed-to-lead* ou la durée de cycle.
5. **Pas de score / MRR / probabilité** → aucune priorisation.
6. **Pas de propriétaire** → prospect « orphelin » dès que le commercial est absent.
7. **4 silos non reliés** → aucune vision du cycle de vie (acquisition → adhésion → fréquentation → churn).

---

## 5. Analyse d'écart (gap) : ACTUEL → CIBLE

| Aujourd'hui (Excel) | Cible (modèle structuré) | Ce que ça débloque |
|---|---|---|
| Colonne « Nom » fourre-tout | `nom_complet` + champs séparés | Dédoublonnage, personnalisation |
| **Aucun ID** | `lead_id` (PK) | Traçabilité, fin des doublons |
| « Source » en texte libre | Référentiel `source` | **ROI par canal** |
| 1 date ambiguë | `date_creation` · `date_premier_contact` · `date_cloture` | **Speed-to-lead**, durée de cycle |
| « Statut » libre | Référentiel `statut_lead` | **Funnel mesurable** |
| Pas de responsable | `proprietaire_id` | Fini les prospects orphelins |
| Pas de priorisation | `score` · `mrr_estime` · `probabilite_close` | **Prospects chauds traités d'abord** |
| WhatsApp/SMS éparpillés | `fact_interaction` (+ `centralise`) | Historique centralisé & repris en cas d'absence |
| Abonnements/paiements séparés | `fact_abonnement` + `fact_paiement` | Vision **cycle de vie** & impayés |
| Fréquentation ignorée | `fact_checkin` + `score_risque_churn` | **Anticipation du churn** + upsell |
| Marketing en silo (GA, Ads, newsletter) | `fact_acquisition` + `fact_newsletter` | Funnel complet dépense→MRR, **ROI par canal** |

---

## 6. Conclusion (le « saut » à réaliser)

> **AS-IS : 1 onglet Excel plat, ~10 colonnes floues, 4 silos déconnectés.**
> **CIBLE : 10 entités reliées, référentiels normalisés, scoring & KPI temps réel.**

C'est précisément ce **passage de l'Excel au modèle structuré** que le plan SalesOps doit porter — et que le prototype (CRM + dashboard) doit rendre tangible à la soutenance.
