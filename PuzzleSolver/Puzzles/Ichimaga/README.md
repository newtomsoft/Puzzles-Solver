# Ichimaga

## Règles du jeu

Règles et astuces du Ichimaga

Règles du puzzle Ichimaga

1.L'objectif : une connectivité unique

Connectez tous les cercles (nœuds) pour former un réseau unique et continu.Aucun cercle ne peut rester isolé.

2.Contraintes de connexion (Valence)

Cercles numérotés : Le nombre à l'intérieur d'un cercle indique exactement combien de lignes doivent s'y connecter.

Cercles vides : Doivent être connectés à au moins une ligne ($n \ge 1$).Ils servent de conducteurs ou de hubs.

3.La mécanique du chemin (la règle du "L")

Horizontal/Vertical : Les lignes doivent suivre les lignes du quadrillage.

Limite d'un tour : Une ligne reliant deux cercles peut être une ligne droite ou elle peut tourner de 90 degrés exactement une fois .Cela signifie que chaque connexion forme soit une ligne droite (« I »), soit une forme de « L ».Les zigzags (deux tours ou plus) sont interdits.

4.Restrictions physiques

Pas de croisement : Les lignes ne peuvent pas se croiser.

Pas de branchement : Une ligne relie exactement deux cercles (elle ne peut pas se diviser ou fusionner dans un espace vide).

Pas de chevauchement : Les lignes ne peuvent pas traverser d'autres cercles pour atteindre une destination.

Puzzle Ichimaga

Solution de casse-tête Ichimaga :

Techniques de résolution de casse-tête Ichimaga

Maîtriser Ichimaga nécessite de passer de la « recherche de chemin » à la « géométrie ».Puisque les connexions sont limitées à un tour, vous recherchez essentiellement des rectangles valides définis par deux cercles.

I. Logique fondamentale (les bases)

1.Le contrôle « Portée »

Avant de tracer des lignes, vérifiez quels cercles peuvent réellement « se voir ».

Parce qu'une ligne ne peut tourner qu'une seule fois, le cercle A ne peut se connecter au cercle B que s'ils partagent une ligne, une colonne ou forment les deux coins d'un rectangle non obstrués par d'autres cercles.

Conseil : Si un cercle numéroté (par exemple, un « 3 ») n'a que 3 voisins valides qu'il peut éventuellement atteindre (compte tenu de la limite de virage et des obstacles), vous devez vous connecter à chacun d'eux.

2.Contraintes de coin et de bord

Les cercles situés dans les coins ou sur les bords de la grille ont naturellement moins d'options pour les formes en « L », car la limite de la grille coupe les chemins potentiels.

Un cercle dans le coin extrême a souvent un espace de rotation très limité.

3.Paires à somme nulle

Si deux cercles portant le chiffre « 1 » sont adjacents (ou ne peuvent s'atteindre que l'un l'autre et rien d'autre), leur connexion formerait une « boucle fermée » de seulement deux nœuds.S'il y a d'autres cercles dans le puzzle, cela n'est pas valide car cela viole la règle de Connectivité unique .Par conséquent, ces deux « 1 » ne peuvent généralement pas se connecter l’un à l’autre à moins qu’ils ne soient les deux seuls cercles restants.

II.Géométrie avancée (la logique "L")

4.Le bloc diagonal

C'est la saveur unique d'Ichimaga.

Imaginez deux paires de cercles essayant de traverser le même espace vide.

Si le cercle A se connecte au cercle B via une forme en « L », il occupe des cellules de grille spécifiques.

Si le cercle C doit se connecter au cercle D et que son chemin traverse A-B, il est bloqué.

Technique : Visualisez la "Bounding Box" entre deux cercles cibles.Si tracer une ligne entre A et B coupe le plateau en deux et isole les autres cercles, cette connexion n'est pas valide.

5.La ligne droite forcée

Parfois, utiliser le virage à 90 degrés est impossible car cela bloquerait un chemin critique pour un voisin.

Scénario : Vous avez un « 2 » qui doit quitter.L'utilisation d'une forme en "L" pourrait bloquer un "1" coincé dans un coin.Le '2' doit donc sortir par une ligne droite pour laisser la place au '1'.

6.Utilisation du cercle vide

N'ignorez pas les cercles vides.Bien qu’ils n’aient pas de numéro spécifique, ils sont essentiels pour « combler » les distances.

Si un cercle numéroté est trop éloigné des autres cercles numérotés pour les atteindre en un seul tour, il doit d'abord se connecter à un cercle vide intermédiaire.

III.Logique structurelle (contraintes globales)

7.Prévention de l'isolement

Recherchez constamment les « groupes bloqués ».

Si la connexion de A à B aboutit à un petit groupe de cercles n'ayant plus de sorties valides (les valences sont pleines), cette connexion est interdite.

Conseil : Ce problème est souvent résolu en travaillant à rebours.« Si je connecte ceci, le graphique restant a-t-il une solution mathématique ? »

8.Le rayon « un tour »

N'oubliez pas que la règle du « un tour » crée effectivement un rayon d'influence spécifique.Un cercle ne peut pas se connecter à un autre cercle qui est dans une relation de « mouvement de chevalier » (échecs) s'il y a un obstacle dans le « coude » du tour.

Liste de contrôle récapitulative pour les solveurs

Recherchez des nombres élevés : Un « 4 » nécessite généralement des lignes dans toutes les directions cardinales ou des formes complexes en « L ».

Recherchez les « 1 » : Ce sont les points de terminaison.Assurez-vous qu’ils ne ferment pas une boucle prématurément.

Visualisez les rectangles : Pour chaque connexion potentielle, imaginez le rectangle défini par les deux points.Le chemin est-il clair ?

Vérifiez la connectivité : Cette ligne isolera-t-elle une section du puzzle ?
