# Marutaringu

## Règles du jeu

Règles et astuces du Marutaringu

Règle du puzzle Marutaringu

Les règles que vous avez fournies sont complètes. Pour une résolution plus claire, elles peuvent être structurées selon une hiérarchie logique :

1. La règle du réseau : Les cellules noires doivent former un réseau continu où chaque cellule noire est associée à exactement deux cellules noires orthogonalement adjacentes. Cela signifie que les cellules noires forment une ou plusieurs boucles fermées (comme une boucle de Slitherlink), mais avec des différences cruciales (voir la règle 5).

2. L'interdiction des carrés 2x2 : Aucun carré 2x2 de la grille ne peut être entièrement noir. Ceci évite les « taches » et impose des boucles fines et sinueuses.

3. La contrainte de région : La grille est divisée en régions de polyominos.

Si une région contient un nombre , ce nombre indique le nombre exact de cellules noires dans cette région.

Si une région ne contient aucun nombre , le nombre de cellules noires est ≥ 1 (et il n'y a pas de contrainte dans les autres cas).

4. La règle du rectangle unique (la révélation fondamentale) : Dans chaque région, toutes les cellules noires doivent être connectées pour former un seul rectangle. Ce rectangle peut être de dimension 1xN (une ligne), 2x2 (ce qui contredit la règle 2, voir l'implication), ou toute autre forme de dimension MxN, mais il doit s'agir d'un rectangle parfait.

Implication cruciale : Le réseau noir (règle 1) n'est pas une simple boucle ; Il s'agit d'une boucle composée de rectangles connectés et alignés sur leurs axes, un par région .

Casse-tête Marutaringu

Solution du casse-tête Marutaringu :

Implications logiques et techniques de résolution du Marutaringu

La logique du casse-tête découle de l'interaction entre les règles globales de la boucle (1 et 2) et la règle locale du rectangle par région (4).

A. Déductions de la règle du rectangle dans la région

Déduction d'angle : Si une case noire se trouve dans un angle d'une région, le rectangle entier doit être poussé dans cet angle. On peut souvent « agrandir » le rectangle à partir d'un indice numéroté ou d'un angle.

Logique des régions numérotées :

Un nombre correspond à l’ aire du rectangle noir dans cette région.

Factorisez le nombre pour trouver les dimensions possibles du rectangle (par exemple, « 6 » peut correspondre à 1 × 6, 2 × 3, 3 × 2 ou 6 × 1).

Utilisez les bords de la grille, les bordures des régions et la règle du 2 × 2 pour éliminer les possibilités.

Logique des régions « sans numéro » : Ces régions sont flexibles mais restrictives en raison de leur forme rectangulaire. Elles doivent contenir au moins une cellule noire de 1 × 1 (un seul point), ce qui constitue un rectangle valide.

Interaction bord/bordure : Si la bordure d’une région coupe l’endroit où le côté d’un rectangle devrait logiquement s’étendre, le rectangle doit s’arrêter ou être orienté différemment.

B. Déductions des règles de boucle et de 2x2

La règle de sortie à 2 cellules : Puisque chaque cellule noire possède exactement deux voisines, le chemin noir doit traverser le rectangle d'une région via des points d'entrée/sortie spécifiques.

Une boucle ne peut traverser un rectangle que de quelques manières :

D'un coin à un coin adjacent (chemin en L) : Utilise 2 cellules.

Par un côté entier : Entrée et sortie sur les côtés opposés (par exemple, gauche-droite, haut-bas). Ce chemin utilise une ligne ou une colonne entière du rectangle.

D'un coin à un coin opposé (chemin en diagonale) : Impossible, car cela nécessiterait une connexion diagonale (et non orthogonale).

Les points de jonction sont essentiels : La boucle doit entrer et sortir de chaque rectangle. Par conséquent :

Un rectangle 1x1 (une seule cellule) est presque toujours impossible à traverser car il ne peut pas avoir deux voisines noires distinctes à l'intérieur de sa propre région . La seule exception est si la boucle effectue un virage à 180 degrés, ce qui correspond fonctionnellement à une ligne de deux cellules. Par conséquent, une cellule noire 1x1 isolée est impossible.

Un rectangle 1xN aura ses deux extrémités comme points d'entrée/sortie de la boucle.

Pour les rectangles plus grands (MxN où M, N > 1), la boucle entrera d'un côté et sortira d'un côté adjacent (formant ainsi un chemin en L à l'intérieur du rectangle), ou la traversera directement.

Éviter les carrés noirs 2x2 : Ceci limite fortement l'alignement des rectangles dans les régions adjacentes. Deux rectangles dans des régions adjacentes ne peuvent pas former un bloc 2x2 de part et d'autre de la frontière.

Approche de résolution étape par étape

Commencer par les régions numérotées : Pour chaque région numérotée, listez toutes les dimensions possibles de rectangles compatibles avec sa surface. Utilisez la forme de la région pour éliminer les options incompatibles. 2. Analyser les régions voisines : Observez comment un rectangle potentiel dans une région s'aligne avec les rectangles possibles dans ses régions voisines. Utilisez la règle d'interdiction 2x2 et la règle de sortie à 2 cellules pour créer des frontières « amies » ou « hostiles ».

Exploiter les régions « sans numéro » : N'oubliez pas qu'elles doivent contenir un rectangle. Parfois, la seule façon pour la boucle globale de se connecter est qu'une telle région utilise une forme rectangulaire spécifique pour relier deux chemins.

Penser en termes de boucle : Changez constamment de perspective. Du « placement local des rectangles » à la « connectivité de la boucle globale ». Demandez-vous : « Si je place ce rectangle ici, comment… »
