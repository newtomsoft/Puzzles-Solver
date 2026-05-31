# KinKonKan

## Règles du jeu

Règles et astuces du Kin-Kon-Kan

Règles du puzzle Kin-Kon-Kan

Kin-Kon-Kan est un puzzle logique joué sur une grille divisée en régions polyomino (blocs).

Objectif :

Placez exactement une ligne diagonale (un « miroir », soit / ou ) dans chaque région de la grille.

Règles clés :

1. Miroirs : Chaque région doit contenir exactement un miroir.Aucune cellule ne peut contenir plus d'un miroir.

2. Faisceaux laser : À l'extérieur de la grille, il y a des indices composés d'une lettre ( A , B , C , etc.) et d'un chiffre (par exemple, A3 , B1 ).Ceux-ci représentent les points d’entrée/sortie du laser.

La lettre indique une « ligne laser » spécifique.Deux indices partageant la même lettre sont le début et la fin du même faisceau laser.

Le nombre indique sur combien de miroirs le faisceau laser se reflétera (c'est-à-dire rebondira) tout au long de son trajet du début à la fin.

3. Chemin du faisceau : Les faisceaux laser se déplacent en lignes droites dans les cellules de la grille jusqu'à ce qu'ils touchent un miroir.Lorsqu'il heurte un miroir, le faisceau se reflète à un angle de 90 degrés.Les faisceaux ne s'arrêtent pas aux intersections à moins qu'ils ne heurtent un miroir.

4. Nombre de réflexions : Le faisceau doit réfléchir exactement le nombre de miroirs spécifié par le numéro d'indice.

5. Utilisation du miroir : Chaque miroir placé dans la grille doit être frappé (réfléchi) par au moins un faisceau laser.Un miroir peut être utilisé par plusieurs faisceaux.

Contraintes :

Les faisceaux ne peuvent pas entrer ou sortir de la grille sauf aux points d'indice désignés.

Les faisceaux ne peuvent pas traverser une cellule dotée d'un miroir sans s'y refléter.

Les faisceaux voyagent cellule par cellule, à travers le centre des cellules.Ils ne se déplacent pas le long des bords des cellules.

Puzzle Kin-Kon-Kan :

Solution du casse-tête Kin-Kon-Kan :

Conseils et techniques de résolution de casse-tête Kin-Kon-Kan :

1. Commencez par les extrêmes : Recherchez les indices avec "0" ou les nombres les plus élevés.Un "0" signifie que les deux points de la même lettre se voient sur une ligne droite sans pas de miroirs entre les deux : toutes les cellules de cette ligne directe doivent être vides de miroirs.Des nombres élevés obligent souvent à des chemins plus longs et sinueux.

2. Logique de coin et de bord : Un faisceau entrant dans une cellule de coin depuis l'extérieur doit immédiatement se refléter si un miroir est présent.Cela peut définir rapidement l'orientation du miroir dans cette région.

3. Déduction de région : Puisque chaque région a exactement un miroir, si vous pouvez en déduire qu'une certaine cellule ne peut pas avoir de miroir, cela restreint les possibilités pour d'autres cellules de la même région.

4. Traçage de faisceaux : Tracez mentalement les chemins possibles pour les faisceaux, en particulier ceux avec de faibles nombres (1, 2).Recherchez des moyens uniques pour obtenir les réflexions requises compte tenu de la position des autres miroirs/cellules vides.

5. Nécessité du miroir : Si les seules positions de miroir possibles d'une région se trouvent toutes dans des cellules qu'aucun faisceau laser ne pourrait atteindre, votre hypothèse est fausse.Chaque miroir doit être frappé par un faisceau.

6. Intersection et exclusion : Les poutres peuvent se croiser sans interagir.Utilisez des cellules vides confirmées (à partir d'indices « 0 » ou de tentatives de chemin ayant échoué) pour limiter les chemins possibles pour d'autres faisceaux.

7. Vérifiez à nouveau le nombre de miroirs : Vérifiez périodiquement que le nombre de réflexions de chaque faisceau actif correspond à son indice.Placer un miroir affecte souvent plusieurs faisceaux.
