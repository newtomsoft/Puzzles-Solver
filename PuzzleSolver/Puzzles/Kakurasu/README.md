# Kakurasu

## Règles du jeu

Règles et astuces du Kakurasu

1. Comment jouer à Kakurasu

Kakurasu est un puzzle logique où vous devez colorier certaines cases d'une grille pour satisfaire des indices numériques.

Objectif : Décider quelles cases de la grille doivent être coloriées (noires) et lesquelles doivent rester vides (blanches).

Valeur des cases : Les nombres sur le côté droit et en bas de la grille indiquent la valeur de chaque case. Dans une ligne ou une colonne donnée, la première case vaut 1, la deuxième 2, la troisième 3, et ainsi de suite.

Indices : Les nombres sur le côté gauche et en haut sont les sommes cibles. La somme des valeurs des cases coloriées dans une ligne doit correspondre exactement à l'indice à sa gauche. De même, la somme des valeurs des cases coloriées dans une colonne doit correspondre à l'indice au-dessus.

2. Techniques de résolution

Résoudre Kakurasu implique logique et déduction. Il est rarement nécessaire de deviner. Voici les stratégies les plus efficaces, des plus basiques aux plus avancées.

Prenons une grille 5x5 comme exemple. La somme maximale possible pour une ligne ou une colonne est 1+2+3+4+5 = 15.

Stratégie 1 : Commencer par les certitudes

Cherchez les indices qui ne laissent aucun doute.

Indices Zéro : Si une ligne ou colonne a un indice de 0 , aucune case de cette ligne ne peut être coloriée. Il est utile de marquer toutes les cases de cette ligne avec un 'X' pour indiquer qu’elles doivent rester vides. C’est le premier mouvement le plus puissant.

Indices de valeur maximale : Si un indice est égal à la somme maximale possible, toutes les cases de cette ligne doivent être coloriées. Dans notre exemple 5x5, un indice de 15 signifie qu’il faut colorier les cinq cases de cette ligne ou colonne.

Stratégie 2 : Utiliser les éliminations

Concentrez-vous sur ce qui ne peut pas être colorié.

Indices supérieurs à la valeur d'une case : Si la valeur d'une case est supérieure à l'indice de sa ligne ou colonne, cette case ne peut pas être coloriée.

Exemple : Si une ligne a un indice de 3 , les cases de cette ligne ayant les valeurs 4 et 5 ne peuvent pas faire partie de la somme. Vous pouvez les marquer avec un 'X'.

Indices "presque maximum" : Astuce très utile. Si un indice est juste en dessous de la somme maximale, vous pouvez déterminer exactement quelle case doit rester vide.

Soit S_{max} la somme maximale (ex. 15 pour une grille 5x5).

Si l’indice C est S_{max} - k, cela signifie que vous devez colorier toutes les cases sauf celle de valeur k.

Exemple : Dans une grille 5x5 (S_{max}=15), un indice de 14 signifie qu’il faut laisser vide la case de valeur '1'. Donc, vous coloriez les cases 2, 3, 4 et 5, et mettez un 'X' dans la case 1. Un indice de 13 signifie qu’il faut laisser vide la case de valeur '2'.

Stratégie 3 : Recoupement

Kakurasu se résout en combinant les informations des lignes et des colonnes. Chaque fois que vous coloriez une case ou la marquez avec un 'X', considérez immédiatement les conséquences pour l’autre direction.

Colorier une case : Lorsqu’une case est coloriée, sa valeur est maintenant engagée à la fois pour la somme de sa ligne et de sa colonne. Mettez à jour votre compte mental pour les deux.

Exemple : Vous déterminez que dans la ligne 2, la case de valeur 4 doit être coloriée. Cette case se trouve dans la colonne 4. Consultez maintenant l’indice de la colonne 4. Vous savez que 4 fait déjà partie de sa somme, il ne reste plus qu’à trouver la valeur manquante.

Vider une case : Lorsque vous marquez une case avec un 'X', vous savez qu’elle contribue à 0 pour sa ligne et sa colonne. Cela peut être tout aussi utile.

Exemple : Grâce à la règle "Presque Maximum", vous déterminez que la ligne 1 avec un indice de 14 doit laisser vide la case '1'. Cette case est dans la colonne 1. Vous savez maintenant que pour la somme de la colonne 1, la case '1' ne peut pas être utilisée.

Stratégie 4 : Travailler avec les combinaisons

Certains indices n’ont qu’une seule combinaison possible de cases.

Petits indices :

Un indice de 1 ne peut être satisfait qu’en coloriant la case de valeur '1'.

Un indice de 2 ne peut être satisfait qu’en coloriant la case de valeur '2'.

Combinaisons uniques : Au fur et à mesure que la grille se remplit, certaines options pour un indice peuvent se réduire.

Exemple : Une ligne a un indice de 4 . Les possibilités sont de colorier la case '4', ou les cases '1' et '3'. Si vous avez déjà déterminé (grâce à la logique des colonnes) que la case '1' doit rester vide, la seule option restante est de colorier la case '4'.

Workflow étape par étape pour résoudre :

Cherchez les Zéros : Marquez toutes les cases des lignes/colonnes avec un indice '0' avec un 'X'.

Cherchez les Maximums : Coloriez toutes les cases des lignes/colonnes avec un indice maximum.

Utilisez les éliminations : Recherchez les indices "presque maximum" (comme 14 dans une grille 5x5) et marquez la case correspondante avec un 'X'. Marquez également toutes les cases dont la valeur est supérieure à l’indice de leur ligne.

Recoupez : Pour chaque case coloriée ou marquée 'X', vérifiez immédiatement l’impact sur la colonne/ligne correspondante et faites d’autres déductions.

Cherchez les coups forcés : Identifiez les indices qui n’ont maintenant qu’une seule combinaison possible de cases.

Répétez : Continuez ce cycle de déduction. Au fur et à mesure que la grille se remplit, de nouvelles certitudes et éliminations apparaissent.

Exemple de puzzle Kakurasu et solution

Voici un exemple de puzzle Kakurasu et de solution pour vous aider à comprendre l’objectif de ce puzzle logique.

Exemple de puzzle Kakurasu

Solution de l’exemple de puzzle Kakurasu
