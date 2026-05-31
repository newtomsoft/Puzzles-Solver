# KohiGyunyu

## Règles du jeu

Règles et astuces du Kohi Gyunyu

☕ Kohi Gyūnyū : règles et techniques de résolution

### 🧩 Comprendre les règles (le but)

L'objectif de Kohi Gyūnyū (littéralement « Café au lait ») est de diviser l'ensemble de la grille en zones distinctes connectées, ou groupes , en traçant des lignes entre les centres des cercles adjacents (horizontalement ou verticalement).

Chaque groupe doit remplir les trois conditions suivantes :

1. Cercle gris unique : Chaque groupe doit contenir exactement un cercle gris (le café).

2. Équilibre égal : Chaque groupe doit contenir un nombre égal de cercles blancs et de cercles noirs (le lait).

3. Pas de connexion directe : Un cercle blanc et un cercle noir ne peuvent pas être directement connectés (adjacents dans le même groupe).

4. Pas de croisement de lignes : Les lignes tracées (bordures) ne doivent pas traverser d'autres lignes tracées.

Puzzle Kohi Gyunyu

Solution de puzzle Kohi Gyunyu :

### 💡 Techniques de résolution essentielles

Les règles fournissent des contraintes fortes qui conduisent à des déductions logiques.Concentrez-vous d’abord sur les éléments les plus restrictifs.

#### 1. Taille et composition déduites

Puisque chaque groupe doit avoir 1 cercle gris, $N$ blanc et $N$ noir, la taille totale de tout groupe doit être $1 + 2N$ (un nombre impair, taille minimale 3 : 1 gris, 1 blanc, 1 noir).

Petits groupes (taille 3) : Si un groupe doit être de taille 3, il doit s'agir du cercle gris et de ses deux voisins adjacents, dont l'un est Blanc et l'autre Noir .C’est une déduction puissante.

#### 2. L'ancre du cercle gris

Vérification des limites : Le cercle gris doit être connecté à au moins un cercle blanc et à au moins un cercle noir pour former les paires $N$ requises.
