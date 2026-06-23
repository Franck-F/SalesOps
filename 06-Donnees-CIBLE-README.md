# Jeu de données CIBLE — MoveUp (README)

> Données **propres et structurées** (modèle à 8 entités du dictionnaire CIBLE), reliées par identifiants.
> Les **valeurs reflètent la performance réelle (problématique)** de MoveUp → le dashboard révèle les fuites.
> Période des leads : **avril → juin 2026**. Photo prise le **2026-06-22**.

## Fichiers
- Excel multi-onglets : `06-Donnees-CIBLE.xlsx`
- CSV (un par entité) : dossier `data-cible/`

## Volumétrie
| Entité | Lignes |
|---|---|
| dim_utilisateur | 7 |
| fact_lead | 600 |
| dim_membre | 1380 |
| fact_abonnement | 1380 |
| fact_interaction | 980 |
| fact_rdv | 470 |
| fact_paiement | 3600 |
| fact_checkin | 7254 |
| fact_acquisition | 332 |
| fact_newsletter | 3 |

## KPI de contrôle (ce que le dashboard montrera)
| Indicateur | Valeur |
|---|---|
| Leads (avr–juin) | 600 |
| Contactés | 381 (64 %) |
| Visites réalisées | 244 |
| Essais planifiés / réalisés | 226 / 135 |
| Adhésions (gagné) | 82 (13.7 %) |
| Speed-to-lead moyen | 26.3 h |
| No-show sur essais | 40 % |
| Relance post-essai (essais NON convertis) | 25 % |
| Membres actifs | 1200 |
| MRR | 67,120 € |
| ARPM (panier moyen) | 55.9 € |
| Membres inactifs (>30 j sans visite) | 187 (16 %) |
| Résiliations (30 derniers jours) | 36 |

## Acquisition / marketing (couche amont)
| Indicateur | Valeur |
|---|---|
| Dépense pub (avr–juin) | 11 818 € |
| Impressions / clics | 668,268 / 12,995 |
| CTR moyen (payant) | 1.94 % |
| Leads générés (toutes sources) | 586 |
| Abonnés newsletter (juin) | 3,403 |
| Taux d'ouverture newsletter | 34 % · clic 4 % |

### ROI par canal (la réponse à « quel canal rapporte ? »)
| Canal | Dépense | Leads | CPL | Adhésions | CAC |
|---|---|---|---|---|---|
| instagram | 3 449 € | 226 | 15 € | 41 | 84 € |
| google_ads | 8 370 € | 163 | 51 € | 23 | 364 € |
| site_web | 0 € (organique) | 88 | — | 13 | — |
| recommandation | 0 € (organique) | 109 | — | 5 | — |

> Conventions, types et définitions des variables : voir `02-Dictionnaire-de-variables.md` (CIBLE).
