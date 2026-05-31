# Miti

## Règles du jeu

Règles et astuces du Miti

Miti (du japonais, littéralement « route ») est un puzzle logique créé par Nishiyama Yukari (Japon).Une grille contient des points à certaines intersections des lignes de la grille.Le but est de noircir certaines bordures entre cellules.

- Dans chaque point de grille donné, exactement trois lignes noires doivent se rencontrer.

- Dans tous les autres points de la grille, au maximum deux lignes noires peuvent se croiser.

- Toutes les cellules de la grille forment une seule boucle fermée sans impasse, d'une largeur d'exactement une cellule.

Puzzle Miti

Solution de puzzle Miti :

### 💡 Techniques de résolution Miti

La clé pour résoudre Miti est d’utiliser les quelques « certaines » règles pour créer des réactions en chaîne.Vous recherchez des lignes que vous pouvez définitivement noircir ou définitivement laisser vides (qui peuvent être marquées d'un 'X').

### 1. Commencez avec des mouvements garantis (coins et bords)

Ce sont souvent les meilleurs points de départ.

Cellules de coin : La boucle doit visiter chaque cellule, y compris les quatre cellules de coin.Une cellule de coin n’a que deux voisins.Pour faire partie de la boucle, il doit se connecter aux deux.

> Règle : Les deux bordures d'une cellule de coin qui font face à l' intérieur de la grille sont toujours noircies .

Points sur le bord : Un point sur le bord de la grille (mais pas dans un coin) n'a que trois bordures disponibles.La règle dit qu'un point doit avoir exactement trois lignes.

> Règle : Pour tout point situé sur le bord extérieur de la grille, les trois bordures disponibles doivent être noircies .

### 2. La règle des points (la règle des 3 lignes)

Il s’agit de votre outil de déduction le plus puissant.

Une bordure doit être vide : Un point au milieu de la grille a quatre bordures.Puisque trois exactement doivent être noircis, un doit rester vide .

Trouver la bordure vide : Recherchez les points où d'autres règles (comme la règle sans point à proximité) forcent l'une de ses bordures à être vide (marquée « X »).Une fois que vous savez qu'une bordure est vide, vous savez que les trois autres doivent être noircies .

Trouvez les bordures noircies : À l'inverse, si vous pouvez prouver que trois bordures doivent être noircies, vous pouvez en toute confiance marquer la quatrième comme vide (« X »).

### 3. La règle sans points (la règle « sans branchement »)

Cette règle détermine le chemin de la boucle.

Empêcher les jonctions « T » ou « + » : Une intersection sans points peut avoir au plus deux lignes.Cela signifie que la boucle peut passer tout droit ou faire un virage à 90 degrés, mais elle ne peut jamais bifurquer dans trois ou quatre directions.

La déduction « deux lignes » : Si vous avez noirci deux lignes qui se rejoignent à une intersection sans points, les deux autres bordures à cette même intersection doivent être laissées vides (« X ») .Ceci est crucial pour forcer la boucle à tourner et éviter qu’elle ne se referme prématurément.

### 4. Logique de boucle globale (vue d'ensemble)

Gardez toujours ces trois règles globales à l’esprit avec chaque ligne que vous tracez.

1.Évitez les petites boucles : Le noircissement d'une ligne ne doit jamais créer une petite boucle fermée qui n'inclut pas toutes les cellules.Le chemin doit être une seule boucle.

2.Connectez chaque cellule (pas d'orphelins) : La boucle doit visiter toutes les cellules.Recherchez toute cellule qui risque d’être coupée du chemin principal.Si une cellule n'a qu'une seule bordure « ouverte » restante pour se connecter à la boucle, cette bordure doit être noircie pour la « sauvegarder ».

3.Aucune impasse : La boucle ne peut pas s'arrêter.Un segment de chemin entrant dans une cellule doit également en sortir.Cela signifie que chaque cellule doit avoir exactement deux bordures noircies (une « entrée » et une « sortie »).(Les cellules situées sur le bord extérieur de la grille constituent un cas particulier, mais le principe est le même).Si une cellule possède déjà deux bordures noircies, ses autres bordures doivent rester vides.
