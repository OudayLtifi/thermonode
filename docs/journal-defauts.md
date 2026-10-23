# Journal des défauts révélés — TP 3

| ID | Étape | Exigence | Test révélateur | Symptôme observé (message Unity/pytest) | Hypothèse de cause | Technique qui l'a révélé |
|---|---|---|---|---|---|---|
| DEF-01 | 1 | EF-05 | test_EF05_range_check_bounds | range_check(12500) : Expected TRUE Was FALSE | La comparaison exclut probablement la borne haute inclusive | Valeurs limites (BVA) |
| DEF-02 | 2 | EF-03 | test_EF03_transient_partial_window ; test_EF03_invalid_sample_is_excluded | Expected 100 Was 2600 ; Expected 2500 Was 2650 ; AddressSanitizer signale index 5 hors limites | Le filtre lit hors du tableau de 5 éléments et traite mal la fenêtre partielle | Séquences, partitions et AddressSanitizer |
| DEF-03 | 4 | EF-04 | test_EF04_counter_resets_below_threshold | Après 7000, 7000, 2500, 7000, 7000 : Expected THR_NONE (0) Was THR_RAISE (1) | Une mesure sous le seuil ne remet probablement pas le compteur à zéro | Table de décision et test de séquence |
| DEF-04 | TP0, corrigé avant TP3 | EI-02 | test_EI02_crc_check_value_123456789_is_29B1 ; test_EI02_crc_of_empty_is_FFFF | Les 11 tests de trame passent ; correctif apporté au TP0 | L’initialisation à 0xFFFF rétablit CCITT-FALSE et l’accord avec la passerelle | Oracle CRC normalisé |
| DEF-05 | 7 | ENF-05 | test_ENF05_push_61_keeps_60_and_drops_oldest | Après 61 ajouts : Expected 60 Was 61 ; aucun débordement ASan signalé dans ringbuf.c | Le test de capacité utilise `count > RINGBUF_CAP`, donc détecte le trop-plein trop tard | Valeurs limites 59 / 60 / 61 |
| DEF-06 | 5 | EF-05 | test_EF05_recovers_to_normal_after_5_valid_samples | Après cinq mesures valides : Expected NORMAL (1) Was FAULT (3) | La transition de reprise après défaut semble absente ou incomplète | Test de transition d’états avec séquence simulée |
