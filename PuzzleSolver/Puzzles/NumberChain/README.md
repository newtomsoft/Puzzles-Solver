# NumberChain

## Règles du jeu

Règles et astuces du Chaîne Numérique

Règles du Casse-tête de Chaîne de Nombres

La Chaîne de Nombres, parfois appelée Serpent de Nombres, a été inventée par un concepteur de casse-tête russe nommé Leonid Mochalov. Elle contient des nombres entre 1 et X, où X est généralement compris entre 10 et 40, selon la taille de la grille.

Votre objectif est de tracer un chemin unique de la cellule en haut à gauche à la cellule en bas à droite, en ne faisant que des mouvements orthogonaux (haut, bas, gauche ou droite). Le long de ce chemin, tous les nombres de 1 à X seront inclus, mais une seule fois – il ne peut y avoir de nombres en double le long du chemin, et les nombres peuvent apparaître dans n'importe quel ordre. Ce chemin ne peut visiter chaque cellule qu'une seule fois, il ne peut donc pas se croiser lui-même.

Casse-tête de Chaîne de Nombres

Solution du Casse-tête de Chaîne de Nombres

Une bonne première étape pour résoudre une Chaîne de Nombres consiste en deux parties :

- Recherchez les doublons des nombres de début et de fin dans le chemin. Comme nous savons que le chemin commence en haut à gauche et se termine en bas à droite, ces nombres ailleurs dans la grille ne peuvent pas faire partie du chemin.

- Recherchez tous les nombres qui n'apparaissent qu'une seule fois dans la grille, car ils feront certainement partie de la chaîne.
