# Roma

## Règles du jeu

Roma est un puzzle logique publié par Nikoli. La grille est divisée en zones (régions) délimitées par des lignes épaisses.

- Placez une flèche dans chaque cellule vide. Certaines flèches sont données.
- Chaque zone délimitée contient des flèches toutes différentes (↑, ↓, ←, →).
- En suivant les flèches depuis n'importe quelle cellule, on doit toujours aboutir à l'une des cellules cerclées (objectifs).

## Encodage de la grille

- `'U'`, `'D'`, `'L'`, `'R'` : flèches données (haut, bas, gauche, droite)
- `'C'` : cellule cerclée (objectif)
- `None` : cellule vide à remplir

La grille de régions indique l'identifiant de la zone de chaque cellule.

## Exemple

Grille :
```
R _ L
D D _
_ _ C
```

Régions :
```
1 1 2
3 2 2
3 4 5
```

Solution :
```
R D L
D D U
R R C
```
