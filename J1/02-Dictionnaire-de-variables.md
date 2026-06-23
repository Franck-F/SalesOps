# Dictionnaire de variables — MoveUp (SalesOps) · v2 — 🎯 CIBLE (idéal / TO-BE)

> 🟢 **Ceci est le modèle de données CIBLE (idéal)** — ce que MoveUp **devrait** avoir avec un CRM structuré.
> 🔴 Pour la réalité d'aujourd'hui (un simple Excel), voir → [02b-Dictionnaire-de-donnees-ACTUEL.md](02b-Dictionnaire-de-donnees-ACTUEL.md).
>
> Référentiel data du projet. Définit chaque entité, chaque variable et chaque indicateur calculé.
> **But** : garantir une donnée cohérente, alimenter le dashboard prototype et calculer les KPI du plan SalesOps.
> Contexte : **salle indépendante mono-site (Versailles), 1 200 adhérents, équipe de 7**.

---

## 1. Principes & conventions

| Règle | Convention |
|---|---|
| **Nommage** | `snake_case`, français sans accent (ex. `date_adhesion`) |
| **Clé primaire** 🔑 | `*_id` unique (ex. `lead_id`) |
| **Clé étrangère** 🔗 | même nom que la PK d'origine |
| **Dates / heures** | ISO 8601 `AAAA-MM-JJ` ou `AAAA-MM-JJThh:mm` |
| **Montants** | euros (€), décimal |
| **Booléens** | `vrai` / `faux` |
| **Valeur manquante** | `NULL` (jamais 0 ni "") |
| **Données personnelles** 🔒 | pseudonymisées dans le jeu de démo (RGPD) |

**Types** : `ID`, `Texte`, `Entier`, `Décimal`, `Booléen`, `Date`, `Datetime`, `Énum` (liste fermée → §3).

---

## 2. Modèle de données (entités & relations)

```
dim_utilisateur (équipe)
       │ (propriétaire)
       ▼
fact_lead ──(devient)──> dim_membre ──< fact_abonnement ──< fact_paiement
   │                          │
   ├──< fact_interaction      └──< fact_checkin (fréquentation)
   └──< fact_rdv (visite / essai)
```

- `dim_*` = dimensions (référentiels : équipe, membres) · `fact_*` = faits datés (leads, interactions, RDV, paiements, check-ins).
- **Mono-site** : pas de dimension multi-club. Identifiant interne du site = `MOV-VSL` (constante).
- Un **lead** gagné devient un **membre** (`lead_id` conservé comme origine).
- Le **lead porte aussi l'opportunité** : `mrr_estime` + `probabilite_close` (offre visée).
- **Couche acquisition (amont)** : `fact_acquisition` (canal × jour) et `fact_newsletter` (mensuel) se relient au reste par **`canal`/`source` + `date`** → funnel complet **dépense → clic → lead → adhésion → MRR**.

---

## 3. Référentiels (énumérations)

### `source` (canal d'acquisition)
`instagram` · `google_ads` · `site_web` · `recommandation` · `newsletter`
> Le `canal` de la couche acquisition (`fact_acquisition`) reprend ces mêmes valeurs.

### `statut_lead` (funnel MoveUp)
`nouveau` · `contacte` · `visite` · `essai` · `gagne` · `perdu`

### `raison_perte`
`prix` · `horaires` · `distance` · `concurrent` · `pas_pret` · `injoignable` · `sans_reponse_post_essai`

### `objectif_sportif`
`perte_poids` · `prise_de_masse` · `remise_en_forme` · `bien_etre` · `performance`

### `type_abonnement` / `montant`
`essentiel` (49 €) · `premium` (69 €) · `coaching_seance` (50 €) · `coaching_pack5` (225 €) · `coaching_pack10` (400 €)

### `statut_abonnement`
`actif` · `en_pause` · `resilie` · `suspendu_impaye`

### `motif_resiliation` (churn)
`prix` · `demenagement` · `manque_temps` · `horaires` · `insatisfaction` · `blessure_sante` · `inconnu`

### `type_interaction` (canal)
`appel` · `sms` · `whatsapp` · `email` · `instagram_dm`
> ⚠️ Aujourd'hui, `whatsapp`/`sms`/`instagram_dm` transitent par le **tél. perso du gérant** → **non centralisés** (champ `centralise = faux`). C'est un irritant clé à matérialiser dans la donnée.

### `type_rdv` / `statut_rdv`
`visite` · `essai` — `planifie` · `realise` · `no_show` · `annule`

### `role` (équipe)
`gerant` · `commercial` · `accueil` · `coach` · `alternant_comm`

### `mode_paiement` / `statut_paiement`
`prelevement_sepa` · `cb` · `especes` — `paye` · `en_attente` · `echoue` · `rembourse`

### `genre`
`H` · `F` · `NC`

---

## 4. Dictionnaire par entité

### 4.1 `dim_utilisateur` — Équipe (propriétaires de leads/actions)
| Variable | Type | Description | Exemple |
|---|---|---|---|
| `utilisateur_id` 🔑 | ID | Identifiant membre de l'équipe | `USR-02` |
| `nom` 🔒 | Texte | Nom | `Dubois` |
| `role` | Énum | Rôle | `commercial` |
| `actif` | Booléen | En poste / disponible | `vrai` |
| `objectif_mensuel` | Entier | Quota d'abonnements/mois (si commercial) | `25` |

> Reflète la réalité : 1 `gerant` (fait aussi du commercial), 1 `commercial`, 1 `accueil`, 3 `coach`, 1 `alternant_comm`.

### 4.2 `fact_lead` — Leads / Prospects (= opportunité)
| Variable | Type | Description | Exemple |
|---|---|---|---|
| `lead_id` 🔑 | ID | Identifiant du lead | `LEAD-2026-0412` |
| `date_creation` | Datetime | Arrivée du lead | `2026-06-01T09:14` |
| `nom_complet` 🔒 | Texte | Nom + prénom (personnalisation) | `Sarah Martin` |
| `email` 🔒 | Texte | Email | `s.martin@…` |
| `telephone` 🔒 | Texte | Téléphone | `+33…` |
| `age` | Entier | Âge | `31` |
| `genre` | Énum | Genre | `F` |
| `commune` | Texte | Ville (zone de chalandise) | `Viroflay` |
| `source` | Énum | Canal d'acquisition | `instagram` |
| `campagne` | Texte | Campagne / `utm_campaign` | `insta_rentree` |
| `objectif_sportif` | Énum | Motif (ciblage offres/relances) | `perte_poids` |
| `statut_lead` | Énum | Étape du funnel | `essai` |
| `score` | Entier | Score 0–100 (priorisation prospects chauds) | `78` |
| `mrr_estime` | Décimal | MRR de l'offre visée (prévisionnel) | `69.00` |
| `probabilite_close` | Décimal | Proba de signature selon l'étape (0–1) | `0.45` |
| `proprietaire_id` 🔗 | FK | Qui suit le lead (`dim_utilisateur`) | `USR-02` |
| `date_premier_contact` | Datetime | 1er contact réel → speed-to-lead | `2026-06-03T17:20` |
| `date_cloture` | Datetime | Gagné/perdu | `2026-06-08T18:00` |
| `raison_perte` | Énum | Si perdu | `sans_reponse_post_essai` |
| `consentement_rgpd` | Booléen | Opt-in marketing | `vrai` |

### 4.3 `dim_membre` — Adhérents (1 200)
| Variable | Type | Description | Exemple |
|---|---|---|---|
| `membre_id` 🔑 | ID | Identifiant adhérent | `MEM-00873` |
| `lead_id` 🔗 | FK | Lead d'origine | `LEAD-2026-0412` |
| `date_adhesion` | Date | 1re adhésion | `2026-06-08` |
| `proprietaire_origine` 🔗 | FK | Qui a closé | `USR-02` |
| `age` / `genre` / `commune` | — | Données socio | `31 / F / Viroflay` |
| `source_acquisition` | Énum | Canal d'origine | `instagram` |
| `statut_membre` | Énum | `actif`/`en_pause`/`resilie` | `actif` |
| **`date_dernier_passage`** | Date | Dernier check-in (signal churn) | `2026-06-18` |
| **`frequence_hebdo`** | Décimal | Visites moyennes / semaine | `2.4` |
| **`utilisation_coaching`** | Booléen | Utilise les services coaching ? (upsell) | `faux` |
| **`score_risque_churn`** | Entier | Risque de résiliation 0–100 | `64` |

### 4.4 `fact_abonnement` — Abonnements / Contrats
| Variable | Type | Description | Exemple |
|---|---|---|---|
| `abonnement_id` 🔑 | ID | Identifiant | `ABO-01290` |
| `membre_id` 🔗 | FK | Adhérent | `MEM-00873` |
| `type_abonnement` | Énum | Offre | `premium` |
| `date_debut` / `date_fin` | Date | Période | `2026-06-08` / `NULL` |
| `montant_mensuel` | Décimal | € / mois | `69.00` |
| `mode_paiement` | Énum | Moyen | `prelevement_sepa` |
| `statut_abonnement` | Énum | État | `actif` |
| `date_resiliation` | Date | Si résilié | `NULL` |
| `motif_resiliation` | Énum | Cause du churn | `NULL` |

### 4.5 `fact_interaction` — Interactions commerciales
| Variable | Type | Description | Exemple |
|---|---|---|---|
| `interaction_id` 🔑 | ID | Identifiant | `INT-44120` |
| `lead_id` 🔗 | FK | Lead concerné | `LEAD-2026-0412` |
| `proprietaire_id` 🔗 | FK | Auteur | `USR-01` |
| `type_interaction` | Énum | Canal (appel/sms/whatsapp/email/dm) | `whatsapp` |
| `date_heure` | Datetime | Horodatage (prouve le manque de suivi) | `2026-06-03T17:20` |
| `resultat` | Énum | `joint`/`non_joint`/`rdv_pris`/`refus` | `rdv_pris` |
| `centralise` | Booléen | Visible par l'équipe (sinon = tél. perso) | `faux` |
| `notes` | Texte | Compte-rendu (souvent vide/incohérent) | `NULL` |

### 4.6 `fact_rdv` — Visites & séances d'essai
| Variable | Type | Description | Exemple |
|---|---|---|---|
| `rdv_id` 🔑 | ID | Identifiant | `RDV-0771` |
| `lead_id` 🔗 | FK | Lead | `LEAD-2026-0412` |
| `type_rdv` | Énum | `visite` / `essai` | `essai` |
| `proprietaire_id` 🔗 | FK | Accompagnateur (commercial/coach) | `USR-04` |
| `date_planifiee` | Datetime | Prévu | `2026-06-05T18:00` |
| `date_realisee` | Datetime | Réalisé (si présent) | `2026-06-05T18:03` |
| `statut_rdv` | Énum | État | `realise` |
| `relance_post_essai` | Booléen | A-t-on rappelé après l'essai ? | `faux` |

### 4.7 `fact_checkin` — Fréquentation (portique)
| Variable | Type | Description | Exemple |
|---|---|---|---|
| `checkin_id` 🔑 | ID | Identifiant passage | `CHK-552310` |
| `membre_id` 🔗 | FK | Adhérent | `MEM-00873` |
| `date_heure_entree` | Datetime | Entrée | `2026-06-18T19:12` |
| `type_acces` | Énum | `badge` / `qr_code` | `qr_code` |

### 4.8 `fact_paiement` — Paiements
| Variable | Type | Description | Exemple |
|---|---|---|---|
| `paiement_id` 🔑 | ID | Identifiant | `PAY-118402` |
| `abonnement_id` 🔗 | FK | Contrat | `ABO-01290` |
| `membre_id` 🔗 | FK | Adhérent | `MEM-00873` |
| `date_paiement` | Date | Date | `2026-07-08` |
| `montant` | Décimal | € | `69.00` |
| `statut_paiement` | Énum | État | `paye` |

### 4.9 `fact_acquisition` — Performance acquisition (canal × jour)
| Variable | Type | Description | Exemple |
|---|---|---|---|
| `acquisition_id` 🔑 | ID | Identifiant de ligne | `ACQ-00142` |
| `date` | Date | Jour | `2026-06-15` |
| `canal` | Énum | Canal d'acquisition | `instagram` |
| `campagne` | Texte | Campagne | `insta_rentree` |
| `depense` | Décimal | € dépensés (0 si organique) | `120.50` |
| `impressions` | Entier | Affichages pub (`NULL` si organique) | `8200` |
| `clics` | Entier | Clics pub (`NULL` si organique) | `98` |
| `ctr` | Décimal | Taux de clic = `clics / impressions` | `0.0120` |
| `sessions_site` | Entier | Sessions web attribuées au canal | `92` |
| `temps_moyen_site_sec` | Entier | Temps moyen sur le site (s) | `74` |
| `taux_rebond` | Décimal | Part de sessions sans interaction | `0.61` |
| `leads_generes` | Entier | Leads issus du canal ce jour | `3` |
| `cpl` | Décimal | Coût par lead = `depense / leads_generes` | `18.30` |

> Relié au reste par **`canal` (= `source`) + `date`** → permet le ROI par canal et le funnel complet dépense→MRR.

### 4.10 `fact_newsletter` — Emailing / nurturing (mensuel)
| Variable | Type | Description | Exemple |
|---|---|---|---|
| `date` 🔑 | Texte | Mois (`AAAA-MM`) | `2026-06` |
| `abonnes` | Entier | Base d'abonnés en fin de mois | `3403` |
| `nouveaux_abonnes` | Entier | Inscrits du mois | `104` |
| `desabonnements` | Entier | Désinscrits du mois | `41` |
| `taux_ouverture` | Décimal | Taux d'ouverture moyen | `0.34` |
| `taux_clic_email` | Décimal | Taux de clic email | `0.04` |

### 4.11 `fact_audience` — Audience web (date × appareil)
| Variable | Type | Description | Exemple |
|---|---|---|---|
| `date` | Date | Jour | `2026-06-15` |
| `device` | Énum | `mobile` · `desktop` · `tablette` | `mobile` |
| `sessions` | Entier | Sessions | `186` |
| `utilisateurs` | Entier | Visiteurs uniques | `148` |
| `duree_moy_session_sec` | Entier | Durée moyenne de session (s) | `78` |
| `pages_par_session` | Décimal | Pages vues par session | `2.2` |
| `taux_rebond` | Décimal | Part de sessions à 1 page | `0.60` |

### 4.12 `fact_pages` — Pages vues (date × page)
| Variable | Type | Description | Exemple |
|---|---|---|---|
| `date` | Date | Jour | `2026-06-15` |
| `page` | Texte | Page du site | `Essai gratuit` |
| `pages_vues` | Entier | Vues | `112` |
| `duree_moy_page_sec` | Entier | Temps moyen sur la page (s) | `55` |
| `taux_sortie` | Décimal | Part de sorties depuis la page | `0.31` |

> Source : Google Analytics. Reliées par `date` (+ `device` / `page`). Sessions cohérentes avec `fact_acquisition.sessions_site`.

---

## 5. Indicateurs calculés (KPI)

### 5.1 Acquisition & vente
| Indicateur | Formule | Unité |
|---|---|---|
| **Taux de conversion global** | `adhésions / leads` | % |
| **Conversion par étape** | `passés étape N+1 / étape N` (contact, visite, essai, close) | % |
| **Taux de no-show** | `rdv no_show / rdv planifiés` | % |
| **Speed-to-lead** | `moy(date_premier_contact − date_creation)` | heures |
| **Durée du cycle de vente** | `moy(date_adhesion − date_creation)` | jours |
| **Taux de relance post-essai** | `essais avec relance / essais non convertis` | % |
| **Atteinte d'objectif** | `adhésions / objectif_mensuel` | % |

### 5.2 ROI marketing (par canal)
| Indicateur | Formule | Unité |
|---|---|---|
| **CPL** (coût par lead) | `dépense canal / leads du canal` | € |
| **CAC** (coût par adhérent) | `dépense canal / adhésions du canal` | € |
| **Taux de conversion par canal** | `adhésions canal / leads canal` | % |
| **Part des adhérents par canal** | `adhésions canal / total adhésions` | % |
| **CTR** (taux de clic) | `clics / impressions` | % |
| **CPC** (coût par clic) | `dépense / clics` | € |
| **Taux de rebond** | `sessions sans interaction / sessions` | % |
| **ROAS** (Return On Ad Spend — retour sur dépense pub) | `MRR généré / dépense pub` | ratio |
| **Taux d'ouverture / clic newsletter** | `ouvertures (clics) / emails envoyés` | % |
| **Croissance abonnés newsletter** | `nouveaux_abonnes − desabonnements` | abonnés |

### 5.3 Revenus, rétention & upsell
| Indicateur | Formule | Unité |
|---|---|---|
| **MRR** | `Σ montant_mensuel des abonnements actifs` | € |
| **ARPM** (panier moyen) | `MRR / membres actifs` | € |
| **Taux de churn mensuel** | `résiliations / membres actifs début de mois` | % |
| **Durée de vie moyenne** | `1 / churn` | mois |
| **LTV** | `ARPM × durée de vie moyenne` | € |
| **Ratio LTV / CAC** | `LTV / CAC` | ratio |
| **Taux d'upsell coaching** | `membres avec coaching / membres actifs` | % |
| **Taux Premium** | `abonnements premium / abonnements actifs` | % |

### 5.4 Engagement (signaux avancés de churn)
| Indicateur | Formule | Unité |
|---|---|---|
| **Fréquence de visite** | `check-ins / membre / mois` | visites |
| **Taux de membres inactifs** | `membres 0 visite sur 30 j / membres actifs` | % |

> 🔑 **Insight clé** : croiser `fact_checkin` × `dim_membre` (`frequence_hebdo`, `date_dernier_passage`) alimente `score_risque_churn` → on **anticipe** la résiliation et on déclenche une relance. Donnée aujourd'hui inexploitée chez MoveUp.

---

## 6. Gouvernance, sources & astuce démo

| Domaine | Source actuelle | Cible (plan SalesOps) |
|---|---|---|
| Leads, interactions, RDV | **Excel partagé + tél. perso** | **CRM unifié** |
| Abonnements, paiements | Logiciel de caisse / Excel | CRM + connecteur |
| Check-ins | Portique (badge/QR) | Flux vers le CRM/reporting |
| Acquisition (coûts) | Instagram / Google Ads | Connecteur reporting (ROI) |
| Web analytics & newsletter | Google Analytics / outil d'emailing | `fact_acquisition` + `fact_newsletter` (reliés par canal + date) |

**Règles de gouvernance**
- **Granularité** : 1 ligne = 1 événement (`fact_*`) ou 1 entité (`dim_*`).
- **Ownership** : chaque lead a un `proprietaire_id` → fini le « prospect orphelin » quand le commercial est absent.
- **Complétude** : champs obligatoires non `NULL` à chaque changement d'étape (règle CRM).
- **RGPD** : champs 🔒 pseudonymisés dans la démo ; consentement tracé.

> 💡 **Astuce démo (avant/après)** : on génère volontairement de la **donnée « sale »** (champs `notes` vides, `date_premier_contact` à plusieurs jours, `centralise = faux`, doublons, `relance_post_essai = faux`) pour illustrer **le problème**, puis la version structurée pour illustrer **la solution**.
