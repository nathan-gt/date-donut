# 🍩 Date-Donut Generator 🍩

Bienvenue au générateur à date donuts, un programme python permettant de générer des dates donuts avec une liste de noms donnés.

## Comment générer des dates ✔📆🍩
1. clonez le projet avec `git clone https://github.com/nathan-gt/date-donut.git`
2. Remplacez les noms dans `saves/save_clear.csv` par les noms de votre groupe (le nombre total de ligne peut changer, tant que la ligne 1 `name,donuts` soit gardée et que chaque nom soit suivi d'une virgule et un retour de ligne)
3. Éxecuter le fichier main.py avec `python 3.11+` à la source du projet
```bash
python main.py
```
4. Et voilà! les groupes sont renvoyé en console, il suffit simplement de copier coller l'output dans slack et <ins>*normalement*</ins> ça devrait tag les personnes associées, tant que les noms match encore.

## Explications des saves 💾
Les noms pour les dates sont pris des fichiers `saves/save-*.csv`, où * est le epoch time de la save. Chaque nom a une liste des IDs des autres personnes rencontré à d'autres date donuts sous le format `id-id-id-...`.

Le programme prendra initialement ses données du fichier `save_clear.csv`, puis prendra la dernière sauvegarde enregistrée dans `saves/`. Si vous voulez regénerer des dates avec une sauvegarde spécifique, vous n'avez qu'à enlever les autres saves du dossier `saves/`

## BUGS 🐛
- Plus vous faites de générations, plus les chances qu'il n'y ai plus de formations de date donuts possibles augmentent, le programme reste pris alors dans une boucle infinie, cela arrive lorsqu'il ne reste plus de candidats valides pour une personne. Simplement arrêter et réexecuter le script règle le problème, à moins qu'il ne reste vraiment plus ou presque plus de combinaisons dates possibles.

## Pour changer la taille des groupes de donut🍩
Par défaut, les dates sont en groupes de 3, si votre nombre de noms total ne forme pas un multiple de 3, alors les dernières personnes se feront mettre automatiquement à d'autres groupes pour former des groupes ***JUMBO***. Pour changer la taille des groupes, vous pouvez aller modifier la variable `GROUP_SIZE` dans `main.py`.

## Pour apporter des changements au code 👩‍💻👨‍💻
Si vous êtes intéressé à apporter des modifictions au code, vous pouvez fork le projet et envoyer un merge request au repository, ou bien pour des petits changements ouvrir une github issue.

©Nathan Gueissaz-Teufel, 2023