# Journal des défauts révélés — TP 3

| ID | Étape | Exigence | Test révélateur | Symptôme observé (message Unity/pytest) | Hypothèse de cause | Technique qui l'a révélé |
|---|---|---|---|---|---|---|
| DEF-01 | 1 | EF-05 | test_EF05_range_check_bounds | range_check(12500) : Expected TRUE Was FALSE | La comparaison exclut probablement la borne haute inclusive | Valeurs limites (BVA) |
| DEF-02 | 2 | EF-03 | test_EF03_transient_partial_window ; test_EF03_invalid_sample_is_excluded | Expected 100 Was 2600 ; Expected 2500 Was 2650 ; AddressSanitizer signale index 5 hors limites | Le filtre lit hors du tableau de 5 éléments et traite mal la fenêtre partielle | Séquences, partitions et AddressSanitizer |
| DEF-03 | 4 | EF-04 | test_EF04_counter_resets_below_threshold | Après 7000, 7000, 2500, 7000, 7000 : Expected THR_NONE (0) Was THR_RAISE (1) | Une mesure sous le seuil ne remet probablement pas le compteur à zéro | Table de décision et test de séquence |
