# TP0 — Réponses aux questions

## Question 1

`firmware/src/hal.h` définit l’interface entre le code du nœud et le matériel : il déclare les fonctions dont le firmware a besoin sans imposer leur implémentation. Les trois implémentations permettent d’utiliser le même code applicatif sur la carte réelle, dans le simulateur ou avec des doublures pendant les tests.

## Question 2

Non. Deux tests réussis montrent seulement que le code a passé ces deux cas précis. Ils ne prouvent pas que toutes les exigences et tous les cas limites sont corrects. Il faut aussi des tests adaptés et suffisamment nombreux, ainsi que d’autres vérifications.

## Question 3

La passerelle vérifie les trames entrantes. Une trame invalide est rejetée et comptabilisée au lieu d’être stockée ; son traitement ne fait pas planter la passerelle. Cela vérifie la robustesse de l’entrée et le rejet des données invalides.

## Question 4

`ADC:4095` indique une valeur ADC saturée au maximum, correspondant ici à un capteur débranché selon le scénario. Le nœud doit passer à l’état `FAULT` pendant le défaut, puis revenir à `NORMAL` lorsque les mesures normales reprennent.
