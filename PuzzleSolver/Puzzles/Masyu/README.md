# Masyu

## Règles du jeu

Règles et astuces du Masyu

Masyu se joue sur une grille rectangulaire de carrés, dont certains contiennent des cercles ; chaque cercle est soit « blanc » (vide), soit « noir » (rempli). Le but est de tracer une seule boucle continue sans intersection qui traverse correctement toutes les cellules encerclées. La boucle doit « entrer » dans chaque cellule qu'elle traverse par le centre d'un de ses quatre côtés et « sortir » par un côté différent ; tous les virages sont donc à 90 degrés.

Les deux variétés de cercles ont des exigences différentes quant à la façon dont la boucle doit les traverser :

Les cercles blancs doivent être parcourus tout droit, mais la boucle doit tourner dans la cellule précédente et/ou suivante sur son chemin.

Les cercles noirs doivent être activés, mais la boucle doit traverser directement les cellules suivantes et précédentes sur son chemin.

Méthodes de résolution

Comprendre les nuances des cercles et la manière dont ils interagissent les uns avec les autres est la clé pour résoudre un casse-tête Masyu. D’une manière générale, il est plus facile de commencer le long de la bordure extérieure de la grille et de travailler vers l’intérieur. Voici quelques scénarios de base dans lesquels des parties de la boucle peuvent être déterminées :

Tout segment partant d'un cercle noir doit parcourir deux cellules dans cette direction sans croiser une autre partie de la boucle ou la bordure extérieure ; chaque cellule noire doit avoir deux de ces segments à angle droit. La combinaison logique de ces deux affirmations est que si un segment d’une cellule noire ne peut pas être dessiné dans une direction orthogonale, un segment dans la direction opposée doit être dessiné. Par exemple, si l’on ne peut pas légalement remonter de deux cellules à partir d’un cercle noir, alors la boucle doit descendre de ce cercle noir sur deux cellules. Cela a deux résultats communs :

Tout cercle noir le long de la bordure extérieure ou une cellule de la bordure extérieure doit avoir un segment s'éloignant de la bordure (et ceux suffisamment proches d'un coin doivent partir des deux murs, définissant le le chemin de la boucle à travers le cercle );

Les cercles noirs orthogonalement adjacents doivent avoir des segments qui s'éloignent les uns des autres.

Les cercles noirs qui sont orthogonalement à côté de l'extrémité de la boucle qui ne se déplace pas vers lui, la boucle doit s'éloigner de l'autre segment de boucle.

Les cercles blancs le long de la bordure extérieure ont évidemment besoin que la boucle les traverse parallèlement à la bordure ; si deux cercles blancs le long d'une bordure sont adjacents ou sont séparés par une cellule, alors la boucle devra s'éloigner de la bordure juste au-delà des cercles.

Si trois cercles blancs ou plus sont orthogonalement contigus et colinéaires, alors la boucle devra passer par chacun de ces cercles perpendiculairement à la ligne des cercles.

Si deux cercles blancs sont orthogonalement contigus et qu'une cellule à chaque extrémité a un segment de boucle entrant parallèlement à la ligne du cercles, alors la boucle devra passer par chacun de ces cercles perpendiculairement à leur ligne. (Sinon, la ligne qui les traverse se connecterait au segment adjacent et l'une des cellules blanches ne serait pas à côté d'un tour dans la boucle.)

Un cercle noir avec deux cercles blancs adjacents en diagonale sur le même côté doit avoir la boucle s’éloignant de ce côté. Si ce n'était pas le cas, et qu'il passait plutôt entre les cercles blancs, alors les cercles blancs seraient parallèles à cette section de la boucle et rendraient impossible la réalisation du cercle noir.

Cercles noirs avec trois cercles blancs adjacents en diagonale. peut être entièrement complété par cette règle.

Si le diagramme est coupé virtuellement en deux morceaux, la boucle doit traverser la ligne de coupe un nombre pair de fois. Cela est dû au théorème de la courbe de Jordan.

Comme dans d'autres puzzles de construction de boucles, les "courts-circuits" doivent également être évités : comme la solution doit consister en une seule boucle, tout segment qui fermerait une boucle est interdit à moins qu'il ne donne immédiatement la solution à l'ensemble du puzzle. .

Comme beaucoup d’autres énigmes combinatoires et logiques, Masyu peut être très difficile à résoudre ; résoudre Masyu sur des grilles arbitrairement grandes est un problème NP-complet. Cependant, les cas publiés d'énigmes ont généralement été construits de manière à pouvoir être résolus dans un délai raisonnable.
