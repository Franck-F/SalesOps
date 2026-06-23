# Jour 3 — Stratégie & conception : ce qu'on doit faire

> **Objectif du J3 (consignes)** : définir les **KPI**, concevoir le **nouveau funnel (TO-BE)**,
> proposer les **outils** à déployer, poser le **schéma de pilotage & gouvernance**, et démarrer
> le **prototype + la maquette**.
> Logique : on a montré le **pain** (AS-IS) au J2 → ici on conçoit le **remède** (TO-BE).

## ✅ Checklist des 5 livrables du J3

- [ ] **1. KPI clés** de pilotage commercial
- [ ] **2. Funnel TO-BE** + règles de passage entre étapes
- [ ] **3. Proposition d'outils** (CRM, automatisation, dashboard)
- [ ] **4. Schéma de pilotage & gouvernance** (cadence, rituels, ownership)
- [ ] **5. Maquette / prototype** (notre dashboard Streamlit)

---

## 1. KPI clés de pilotage

On pilote 3 familles (définitions complètes → `J1/02-Dictionnaire-de-variables.md`) :

| Famille | KPI |
|---|---|
| **Acquisition & vente** | Conversion globale & par étape · **Speed-to-lead** · No-show · Relance post-essai · Durée de cycle |
| **ROI marketing** | CPL · **CAC par canal** · CTR · ROAS · part des adhésions par canal |
| **Revenus & rétention** | MRR · ARPM · **Taux de churn** · LTV · ratio LTV/CAC · taux d'upsell · % inactifs |

**Cibles à 6 mois (proposées)** : conversion 13 % → **18 %** · speed-to-lead 26 h → **< 1 h** ·
no-show 40 % → **< 20 %** · churn mensuel 3 % → **< 2,5 %**.

---

## 2. Funnel TO-BE + règles de passage

```
Lead → Contacté → Qualifié → Visite/Essai → Proposition → Adhésion
                                   │                 │
                              (no-show ?)       (relance auto)
```

| Étape | Règle d'entrée (stage-gate) | SLA / cadence |
|---|---|---|
| **Lead** | Coordonnées capturées + canal tracé | — |
| **Contacté** | 1er contact effectué | **< 1 h** après le lead (SLA speed-to-lead) |
| **Qualifié** | Joignable + intérêt confirmé + `score ≥ 50` | Sinon : 5 tentatives sur 7 j → **Perdu (injoignable)** |
| **Visite / Essai** | RDV calé (réservation en ligne) | Confirmation **SMS auto J-1** (anti no-show) |
| **Proposition** | Essai réalisé → offre présentée | **Relance auto J+1 et J+3** post-essai |
| **Adhésion** | Contrat signé + 1er paiement | — |
| **Perdu** | Pas de réponse après **3 relances** OU refus explicite | Motif obligatoire (`raison_perte`) |

> Chaque lead a un **`proprietaire_id`** → fini le « prospect orphelin » quand le commercial est absent.

---

## 3. Proposition d'outils

| Besoin | Outil proposé | Ce que ça règle (irritant AS-IS) |
|---|---|---|
| **CRM unifié** | Pipedrive / HubSpot (Starter) | Fin de l'Excel : 1 fiche/lead, statuts, ownership, historique |
| **Messagerie centralisée** | WhatsApp Business API / Aircall | Fin du **tél. perso** du gérant → échanges visibles par l'équipe |
| **Réservation en ligne** | Calendly / module club | Plus de RDV pris « au téléphone » |
| **Automatisation** | Make / Zapier (ou natif CRM) | Séquences : J+1 demande, confirmation J-1, relance post-essai, **win-back inactifs** |
| **Dashboard de pilotage** | **Streamlit** (notre prototype) | Reporting **temps réel** : funnel, ROI canal, churn |

**Scénarios d'automatisation prioritaires** : (a) accusé + 1er contact J0, (b) confirmation RDV J-1,
(c) relance post-essai J+1/J+3, (d) alerte churn (adhérent inactif > 30 j → relance coaching).

---

## 4. Schéma de pilotage & gouvernance

| Rituel | Fréquence | Contenu | Qui |
|---|---|---|---|
| **Daily** (10 min) | quotidien | Leads chauds du jour, no-shows à relancer | Commercial + gérant |
| **Pipeline review** | hebdo | Conversion par étape, speed-to-lead, relances en retard | Équipe commerciale |
| **Revue performance** | mensuel | MRR, churn, **ROI par canal**, upsell, atteinte des quotas | Direction |

- **Ownership** : chaque étape a un responsable (commercial = leads ; gérant = arbitrage ; accueil/coachs = signal terrain).
- **Objectifs** : quota mensuel d'adhésions par conseiller + cible de conversion.
- **Une seule source de vérité** : le CRM (plus d'Excel parallèles).

---

## 5. Maquette / prototype

Le prototype final est le **dashboard Streamlit** (dossier [`dashboard/`](dashboard/)) :
funnel, speed-to-lead, no-show, **ROI par canal (CAC Instagram 84 € vs Google Ads 364 €)**,
segments de churn, base adhérents. Lancement : `streamlit run dashboard/app.py`.

> La maquette = préfiguration visuelle de ce dashboard (déjà fonctionnel sur les données CIBLE).

---

## 🗓️ Répartition & planning du J3

| Rôle | Tâche J3 |
|---|---|
| Lead conseil | Funnel TO-BE + règles de passage + cohérence du récit |
| Analyste | KPI cibles + chiffrage de l'impact (business case) |
| Architecte data | Brancher le dashboard, vérifier les KPI |
| Builder | Finaliser le dashboard + préparer la démo |

**Sortie attendue J3** : ce plan validé + le dashboard prêt à démontrer → on enchaîne le **J4** (pitch + répétition).
