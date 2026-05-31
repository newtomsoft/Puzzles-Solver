# Shirokuro

## Règles du jeu

Règles et astuces du Shirokuro

Shirokuro est un puzzle logique inventé par Nikoli.Il contient des cercles blancs et noirs.La tâche consiste à relier chaque cercle blanc à un cercle noir par une ligne horizontale ou verticale.Les lignes ne sont pas autorisées à en croiser d’autres.La ligne entre deux cercles ne peut pas passer par d’autres cercles.

Puzzle Shirokuro

Solution du casse-tête Shirokuro :

## 🧩 Techniques de résolution de puzzles Shirokuro

### 1. Concentrez-vous sur les indices de coin et de bord

Paires isolées : Les cercles situés dans les coins ou le long des bords de la grille ont souvent moins de chemins de connexion potentiels.Commencez par rechercher des paires qui n'ont qu'un un seul chemin possible pour relier un cercle blanc à un cercle noir.

Blocage : Lorsqu'un cercle est proche d'un coin ou d'un bord, son seul chemin de sortie peut être bloqué par un autre cercle ou par le bord lui-même, forçant la connexion à aller dans la direction opposée.

### 2. Analyser la proximité et la distance

Paires fermées : Si un cercle blanc et un cercle noir sont adjacents (horizontalement ou verticalement), ils forment souvent une paire , car toute tentative de les connecter à d'autres cercles plus éloignés nécessiterait probablement que leur chemin bloque immédiatement la connexion courte de la paire adjacente.

Paires éloignées : Si une paire est éloignée l'une de l'autre, leur ligne devra probablement traverser des zones ouvertes.Ces lignes peuvent être utiles pour segmenter le tableau et créer des chemins forcés pour d'autres paires.

### 3. La règle « Interdiction de traverser » est la clé

Virages forcés : Si un chemin est droit et qu'un autre cercle se trouve sur un chemin qui le forcerait à se croiser, l'un des chemins doit tourner.Ceci est crucial pour déduire les tours .

Couloirs : Recherchez les passages étroits ou « couloirs » créés par les lignes que vous avez déjà tracées.Si une paire doit se connecter et que le seul moyen de le faire est de passer par un espace étroit et ouvert, cet espace est le chemin forcé pour cette paire.

### 4. Vérifiez les cercles « piégés »

Impasses : Si vous dessinez un segment de chemin qui laisse un cercle (blanc ou noir) avec seulement une direction ouverte restante pour vous connecter à n'importe quel partenaire approprié, cette direction est un mouvement forcé pour ce cercle.

Encerclement : Si vous commencez à tracer des lignes et remarquez qu'un cercle est entouré par des lignes tracées ou d'autres cercles, vérifiez immédiatement s'il a toujours un chemin valide et non croisé vers un partenaire.Sinon, le dernier chemin que vous avez tracé doit être erroné.

### 5. Essais et erreurs/hypothèses de tests (en dernier recours)

Hypothéser et vérifier : Si vous êtes coincé entre deux connexions possibles pour une seule paire, choisissez-en une et dessinez-la à la légère ou mentalement.Ensuite, voyez si ce choix conduit à une contradiction (par exemple, laisser un cercle non apparié piégé ou forcer deux lignes à se croiser).Si cela conduit à une contradiction, l’ autre choix doit être le bon.
