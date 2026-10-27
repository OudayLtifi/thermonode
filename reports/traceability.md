| Exigence | Prio | Titre | Tests | Réussis | Échoués | Statut |
|---|---|---|---|---|---|---|
| C-01 | P1 | Cible | 0 | 0 | 0 | couvert par Configuration cible et mesure mémoire |
| C-02 | P1 | Testabilité | 0 | 0 | 0 | couvert par Tests hors cible avec HAL simulée |
| C-03 | P2 | Passerelle | 0 | 0 | 0 | couvert par Tests unitaires et revue de la passerelle |
| EF-01 | P1 | Période d'acquisition | 1 | 1 | 0 | validé |
| EF-02 | P1 | Conversion ADC | 6 | 6 | 0 | validé |
| EF-03 | P2 | Filtrage | 6 | 6 | 0 | validé |
| EF-04 | P1 | Alerte seuil haut | 13 | 13 | 0 | validé |
| EF-05 | P1 | Mesure invalide | 17 | 17 | 0 | validé |
| EF-06 | P2 | Trame périodique | 1 | 1 | 0 | validé |
| EF-07 | P2 | Commande de seuil | 4 | 4 | 0 | validé |
| EF-08 | P3 | Commande de période | 2 | 2 | 0 | validé |
| EI-01 | P1 | Interface capteur | 2 | 2 | 0 | validé |
| EI-02 | P1 | Format des trames | 33 | 33 | 0 | validé |
| EI-03 | P2 | Commandes | 5 | 5 | 0 | validé |
| ENF-01 | P1 | Latence d'alerte | 1 | 1 | 0 | validé |
| ENF-02 | P2 | Consommation | 0 | 0 | 0 | ORPHELIN |
| ENF-03 | P1 | Empreinte mémoire | 0 | 0 | 0 | couvert par Mesure de l’empreinte mémoire |
| ENF-04 | P1 | Règles de codage | 0 | 0 | 0 | couvert par Revue C99 et analyse statique |
| ENF-05 | P2 | Perte de liaison | 12 | 12 | 0 | validé |
| ENF-06 | P2 | Robustesse réseau | 0 | 0 | 0 | couvert par Essai de reprise après coupure réseau, utilisé comme scénario proxy |

Exigences : 20 ; couvertes : 19 (95 %) ; orphelines : ENF-02
