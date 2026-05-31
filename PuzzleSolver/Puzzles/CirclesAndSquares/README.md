# CirclesAndSquares

## Règles du jeu

Règles et astuces du Cercles et Carrés

1.Règle des cercles et des carrés

1. Contraintes de cercle :

- Cercle noir → La cellule doit être noircie.

- Cercle blanc → La cellule doit rester blanche .

2. Règle de la région blanche :

- Après avoir noirci les cellules, toutes les cellules blanches restantes doivent être regroupées dans des zones de carrés blancs distincts (carrés au sens géométrique : 1×1, 2×2, 3×3, etc.).

3. Pas de bloc noir 2×2 :

- Aucun groupe 2×2 de cellules n'importe où dans la grille ne peut être entièrement noir.

4. Connectivité noire :

- Toutes les cellules noires doivent être connectées orthogonalement (touchant les côtés, pas seulement les coins).

Puzzle de cercles et de carrés

Solution de puzzle de cercles et de carrés :

## 2.Cercles et carrés Déductions et techniques logiques

### A) Implications du cercle blanc

- Un cercle blanc doit faire partie d'un carré blanc d'une certaine taille (n x n).

- Si un cercle blanc se trouve dans un coin de la grille → ce carré blanc doit s'étendre vers l'intérieur à partir de ce coin.

- Les cercles blancs donnent le carré blanc minimum possible les contenant.

Si un cercle blanc est seul sans cercles blancs adjacents, il doit s'agir d'un carré blanc 1 × 1, donc les quatre cellules orthogonalement adjacentes doivent être noires (sauf si d'autres règles l'empêchent).

### B) Implications du cercle noir

- Un cercle noir doit être noir, vérifiez donc la connectivité et aucune violation du noir 2×2.

- Parfois, des cellules noires forcées autour des carrés blancs peuvent provoquer une violation du noir 2×2 → une détection précoce des contradictions est possible.

- Un cercle noir peut forcer les voisins à être blancs sinon cela créerait un bloc noir 2×2.

### C) Construction carrée blanche

- Lorsque vous avez deux cercles blancs dans des cellules orthogonales adjacentes, ils appartiennent probablement au même carré blanc.

- Pour déterminer la taille possible d'un carré blanc contenant un cercle blanc, recherchez le plus grand carré de cellules blanches possible sans enfreindre les règles du cercle.

- Marquer mentalement les limites provisoires des carrés blancs ;les bords des carrés blancs sont des cellules noires .

### D) Pas de bloc noir 2×2 + connectivité

- Si vous avez trois cellules d'un 2×2 déjà noires, la quatrième doit être blanche .

- Cette règle force souvent les cellules blanches qui influencent la taille des carrés blancs.

- La connectivité des cellules noires signifie que les régions noires ne peuvent pas être isolées ;toutes les cellules noires doivent se toucher orthogonalement.

### E) Flux de déduction du réseau

1. Commencez par les cercles blancs – forcez les bordures minimales de leurs carrés blancs (les cellules adjacentes sont noires).

2. Utilisez des cercles noirs pour forcer les cellules noires.

3. Appliquer pas de blocs noirs 2×2 – transforme souvent les triplets noirs forcés en une cellule blanche dans le 4ème coin.

4. Assurez-vous que les carrés blancs sont des carrés complets – en les agrandissant parfois pour éviter de rompre la connectivité des noirs.

5. Utilisez la connectivité noire pour forcer des cellules noires supplémentaires entre les régions noires séparées.

6. Faites une boucle entre les règles jusqu'à ce que toutes les cellules soient déterminées.
