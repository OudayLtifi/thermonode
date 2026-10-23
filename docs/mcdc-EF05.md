# MC/DC — décision de défaut EF-05

Décision : D = A OU B OU C

- A : centi < -4000
- B : centi > 12500
- C : frozen_count >= 5

| Test | A | B | C | D | Influence démontrée |
|---|---|---|---|---|---|
| T1 | F | F | F | F | Référence |
| T2 | V | F | F | V | A, comparé à T1 |
| T3 | F | V | F | V | B, comparé à T1 |
| T4 | F | F | V | V | C, comparé à T1 |

A et B vrais simultanément est irréalisable : une même température ne peut être à la fois
inférieure à -4000 et supérieure à 12500 centièmes.

Vecteurs choisis :
- T1 : ADC 931, température nominale valide
- T2 : ADC 124, température -4001
- T3 : ADC 2173, température 12507
- T4 : cinq mesures identiques à ADC 931
