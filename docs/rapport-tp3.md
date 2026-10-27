# TP 3 — Tests automatisés et analyse de ThermoNode

**Étudiant :** Ouday Ltifi
**Projet :** ThermoNode
**Branche de travail :** `tp3-corrections`

## 1. Objectif et environnement

Ce TP avait pour objectif de tester le firmware ThermoNode et sa passerelle, de révéler des défauts par des techniques de test ciblées, puis de vérifier les corrections avec des tests automatisés.

Le firmware a été testé sous Ubuntu dans la machine virtuelle Vagrant, avec Unity pour les tests C. La passerelle Python a été vérifiée avec pytest. Le HAL simulé permet de contrôler les lectures ADC, l’horloge et les échanges réseau sans matériel physique.

## 2. Techniques de test et traçabilité

Les tests ont utilisé des partitions d’équivalence, des valeurs limites (BVA), des séquences, des tables de décision, des tests d’intégration et des contrôles de mémoire avec AddressSanitizer.

| Exigences | Technique principale | Fichiers ou preuves | Tests réussis |
|---|---|---|---:|
| EF-01 | Test temporel avec horloge simulée | `firmware/test/test_node.c` | 1 |
| EF-02 | Conversion et valeurs limites ADC | `firmware/test/test_convert.c` | 6 |
| EF-03 | Séquences de filtrage, fenêtre partielle et mesures invalides | `firmware/test/test_filter.c` | 6 |
| EF-04 | Table de décision et séquences de seuil | `firmware/test/test_threshold.c`, `test_node.c` | 13 |
| EF-05 | Partitions invalides, défaut figé et reprise | `firmware/test/test_fault.c`, `test_node.c` | 17 |
| EF-06 à EF-08 | Périodicité, trames et commandes | `firmware/test/test_node.c` | 7 |
| EI-01 à EI-03 | Interface ADC, CRC, trames et commandes | Tests firmware et `gateway/tests/unit` | 40 |
| ENF-01 et ENF-05 | Latence simulée, tampon circulaire, déconnexion et dédoublonnage | Tests firmware, passerelle et intégration | 13 |

La matrice complète est dans `reports/traceability.md`. Elle compte 19 exigences couvertes sur 20 : 13 sont rattachées à des tests automatisés et 6 à des preuves d’analyse ou de mesure.

## 3. Défauts révélés et corrections

| Défaut | Exigence | Symptôme et cause | Correction | Commit |
|---|---|---|---|---|
| DEF-01 | EF-05 | La borne haute inclusive était rejetée par `range_check`. | Inclusion de la borne haute. | `366749e` |
| DEF-02 | EF-03 | Le filtre lisait un élément hors de la fenêtre active ; AddressSanitizer signalait un dépassement. | Correction de la limite de boucle. | `abc4f52` |
| DEF-03 | EF-04 | Une mesure sous le seuil ne réinitialisait pas le compteur de mesures consécutives. | Réinitialisation du compteur lorsque la mesure n’est pas au-dessus du seuil. | `52b4eba` |
| DEF-04 | EI-02 | Le CRC avait été corrigé durant le TP0 ; le vecteur de référence CCITT-FALSE vérifie le résultat. | Initialisation CRC conforme à CCITT-FALSE, avec `0xFFFF`. | Corrigé au TP0 |
| DEF-05 | ENF-05 | Après 61 ajouts, le compteur dépassait la capacité de 60 et l’ancienne trame n’était pas écrasée correctement. | Détection du tampon plein avant l’ajout suivant. | `7f7777c` |
| DEF-06 | EF-05 | Après cinq mesures valides, le nœud restait en défaut. La reprise n’était pas reliée à la condition de récupération. | Transition vers l’état normal quand `fault_recover_ready()` est vrai. | `ea74b40` |
| DEF-07 | EI-02 | Une température texte et une séquence négative étaient acceptées. | Validation stricte des types et rejet des séquences négatives. | `41250e1` |
| DEF-08 | ENF-05 | Les trames dupliquées ou anciennes pouvaient être stockées à nouveau. | Réactivation du contrôle du numéro de séquence persisté. | `26d39e9` |

## 4. Résultats de couverture et qualité

Au début du TP0, la couverture firmware était faible : 2,5 % des lignes, 5,3 % des fonctions et 2,9 % des branches. Après l’ajout des tests mais avant les corrections, elle atteignait environ 92,0 % des lignes, 89,5 % des fonctions et 89,0 % des branches. Après les corrections, elle est de 93,6 % des lignes, 92,1 % des fonctions et 89,9 % des branches.

Pour la passerelle, la première mesure disponible était de 78 % de couverture globale et 30 branches couvertes sur 38. Après les tests complémentaires, les tests unitaires couvrent 100 % des lignes et 38 branches sur 38. La suite complète a réussi : **38 tests passés**.

Les tests firmware avec AddressSanitizer ont réussi après correction, sans diagnostic de dépassement mémoire. L’analyse cppcheck a terminé avec zéro constat. Le contrôle de taille indique **10 192 octets de flash sur 49 152** et **1 640 octets de RAM sur 8 192**, dans les limites définies.

## 5. Réponses aux questions du TP

1. **Valeur limite de température :** la conversion ADC est quantifiée. Aucun code ADC ne correspond nécessairement exactement à 125,00 °C. On teste donc les codes voisins et on teste directement `range_check()` pour vérifier la borne exacte.
2. **Défaut du filtre :** la boucle utilisait une limite inclusive et accédait au-delà des éléments valides. Les anciennes valeurs en mémoire faussaient la moyenne ; AddressSanitizer a révélé l’accès hors limites.
3. **Rôle du HAL simulé :** il fournit des valeurs ADC contrôlées, une horloge déterministe et des espions pour les émissions radio et les acquittements. Cela rend les tests répétables sans carte physique.
4. **Compteur du seuil :** seules trois mesures filtrées consécutives strictement supérieures au seuil déclenchent l’alerte. Une mesure égale ou inférieure doit remettre le compteur à zéro.
5. **Mesure hors plage :** une valeur ADC qui produit une température hors plage physique doit provoquer l’état défaut. Les tests de seuil doivent employer des valeurs valides pour ne pas confondre défaut capteur et alerte thermique.
6. **Reprise du nœud :** le défaut révélé venait de la transition d’état du nœud : la condition de cinq mesures valides existait, mais n’était pas utilisée pour quitter l’état défaut.
7. **Oracle CRC :** le vecteur standard `123456789` donne `0x29B1` en CRC-16/CCITT-FALSE. Un oracle indépendant est nécessaire, car deux composants utilisant le même algorithme erroné pourraient tout de même sembler compatibles.
8. **Tampon circulaire :** les cas 59, 60 et 61 vérifient la capacité et le débordement. À la 61e trame, le nombre doit rester à 60 et la plus ancienne trame doit être remplacée.
9. **Tests unitaires et intégration :** les tests unitaires isolent les modules ; le test du nœud vérifie les transitions à travers les composants et le HAL. Cette séparation aide à localiser le défaut.
10. **Validation des trames :** chaque test de champ invalide doit avoir un CRC correct. Sinon, le parseur rejette d’abord le CRC et le test ne vérifie jamais le champ visé.
11. **Limite du test de reconnexion :** l’essai d’intégration vérifie une coupure du broker et l’ordre des séquences après reprise. Il n’ajoute que 30 mesures, donc il ne vérifie pas le débordement à 61 trames ni exactement le scénario de pertes aléatoires demandé.

## 6. Vérifications CPS et limites

- **Temps :** les tests temporels utilisent l’horloge simulée ; ils ne mesurent pas une carte réelle.
- **Communication :** l’intégration vérifie l’arrêt du broker puis la reprise MQTT. Le test est un scénario proxy pour ENF-06 ; il ne reproduit pas exactement 30 % de pertes et ne démontre pas le délai maximal de 30 secondes.
- **Capteur :** les valeurs ADC permettent de tester la conversion, les valeurs hors plage et les séquences de mesures figées.
- **Ressources :** le contrôle `size-check` valide la flash et la RAM. La consommation moyenne de moins de 5 mA pendant une heure n’a pas été mesurée, faute de banc matériel.
- **MISRA :** la compilation C99, les avertissements traités en erreurs, cppcheck et les dérogations documentées apportent des contrôles statiques. Ils ne constituent pas à eux seuls une certification complète MISRA C:2012.

## 7. Conclusion

Les tests ont révélé huit défauts fonctionnels ou de validation, dont un défaut CRC corrigé pendant le TP0. Les corrections firmware et passerelle ont été vérifiées par les tests unitaires, les tests d’intégration, l’analyse statique et les contrôles de taille. La traçabilité couvre 19 exigences sur 20. ENF-02 reste à mesurer sur banc ; ENF-06 est vérifiée par un scénario de reconnexion proxy et nécessite un essai avec pertes réseau contrôlées pour confirmer strictement ses seuils.
