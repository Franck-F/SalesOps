# Jour 4 — Réalisation & pitch : ce qu'on doit faire

> **Objectif du J4 (consignes)** : **finaliser le prototype** et **structurer le pitch + le support**.
> Sortie attendue : **support final + prototype testé**. (Le J5 = soutenance de 20 min.)

## ✅ Checklist du J4

- [ ] **Finaliser** le dashboard (données, libellés, lisibilité)
- [ ] **Tester** le prototype de bout en bout (zéro bug en démo)
- [ ] **Structurer le pitch** (fil narratif, 20 min)
- [ ] **Construire le support** (slides)
- [ ] **Répétition générale** + chronométrage + Plan B

---

## 1. Finalisation & test du prototype

- Lancer : `streamlit run dashboard/app.py` → parcourir les **4 onglets**.
- Vérifier que les chiffres correspondent au README / dictionnaire (conversion 13,7 %, MRR 67 k€, CAC…).
- **Mode démo** : plein écran, zoom suffisant, données déjà chargées (cache chaud).
- **Plan B (indispensable)** : exporter des **captures / un PDF** du dashboard au cas où (pas de réseau, souci d'install le jour J).

---

## 2. Trame du pitch (20 min) — structure imposée par les consignes

| # | Section | Durée | Contenu clé | Qui |
|---|---|---|---|---|
| 1 | **Entreprise & contexte** | 2–3 min | MoveUp : bonne offre, du trafic… mais perd de l'argent | — |
| 2 | **Diagnostic** | 4 min | AS-IS : Excel aveugle, funnel qui fuit, **le chiffre qui claque** (13 % de conversion) | — |
| 3 | **Recommandations** | 4 min | Funnel TO-BE + règles, outils (CRM/auto), gouvernance, KPI | — |
| 4 | **Démonstration du prototype** | 5–6 min | Le **dashboard live** (voir script ci-dessous) | — |
| 5 | **Impact & conditions de réussite** | 3 min | Business case (**+100–150 k€/an**), conditions (adoption CRM, rituels) | — |
| — | Questions / réponses | reste | — | tous |

> ⚠️ **Tous les membres doivent présenter** — un étudiant absent du pitch est en échec.

---

## 3. Script de démo du dashboard (ordre conseillé)

1. **KPI cards** → « voilà ce que MoveUp ne voyait pas » : MRR 67 k€, **conversion 13,7 %**, **333 adhérents à risque**.
2. **Onglet Funnel & commercial** → montrer les **fuites** : speed-to-lead **26 h**, no-show **40 %**, relance **25 %**.
3. **Onglet Acquisition / ROI** → l'insight choc : **CAC Instagram 84 € vs Google Ads 364 €** → réallouer le budget.
4. **Onglet Rétention / churn** → **333 à risque + 187 inactifs**, et seulement **14 % de coaching** → levier d'upsell.
5. **Conclure** : « donnée structurée = pilotage = argent récupéré ».

---

## 4. Le fil rouge (à marteler)

**AS-IS** (Excel aveugle, on ne mesure rien) → **TO-BE** (data structurée + dashboard, on pilote) → **impact chiffré**.
C'est la démonstration vivante du **« No pain, no change »**.

---

## 5. Répartition & planning du J4

| Rôle | Tâche J4 |
|---|---|
| Lead conseil | Fil narratif du pitch + slides 1–3 |
| Analyste | Slides diagnostic + impact (business case) |
| Architecte data | Finalisation dashboard + vérif des chiffres |
| Builder | Démo dashboard + Plan B (captures/PDF) |

**Sortie J4** : support final + prototype testé + pitch répété/chronométré → **prêt pour la soutenance (J5)**.
