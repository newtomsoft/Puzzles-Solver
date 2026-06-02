# Marutaringu

## Règles du jeu


Règle du puzzle Marutaringu

1. La règle du réseau : Les cellules noires doivent former un réseau continu où chaque cellule noire est associée à exactement deux cellules noires orthogonalement adjacentes. Cela signifie que les cellules noires forment une ou plusieurs boucles fermées (comme une boucle de Slitherlink), mais avec des différences cruciales (voir la règle 5).

2. L'interdiction des carrés 2x2 : Aucun carré 2x2 de la grille ne peut être entièrement noir. Ceci évite les « taches » et impose des boucles fines et sinueuses.

3. La contrainte de région : La grille est divisée en régions de polyominos.

Si une région contient un nombre , ce nombre indique le nombre exact de cellules noires dans cette région.

Si une région ne contient aucun nombre , le nombre de cellules noires est ≥ 1 (et il n'y a pas de contrainte dans les autres cas).

4. La règle du rectangle unique (la révélation fondamentale) : Dans chaque région, toutes les cellules noires doivent être connectées pour former un seul rectangle. Ce rectangle peut être de dimension 1xN (une ligne), 2x2 (ce qui contredit la règle 2, voir l'implication), ou toute autre forme de dimension MxN, mais il doit s'agir d'un rectangle parfait.

Implication cruciale : Le réseau noir (règle 1) n'est pas une simple boucle ; Il s'agit d'une boucle composée de rectangles connectés et alignés sur leurs axes, un par région .
