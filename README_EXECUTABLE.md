# PuzzleSolver - Guide d'Utilisation

## Installation

### Option 1 : Utiliser l'Exécutable (Recommandé)

1. **Télécharger** le dossier `PuzzleSolver` complet
2. **Installer les navigateurs Playwright** (requis une seule fois) :
   ```bash
   playwright install chromium
   ```
3. **Lancer** l'application : Double-cliquer sur `PuzzleSolver.exe`

### Option 2 : Depuis le Code Source

1. Installer Python 3.12+
2. Installer les dépendances : `pip install -r requirements.txt`
3. Lancer : `python Run/PuzzleGUI.py`

## Utilisation

### Interface Principale

1. **Entrer l'URL** du puzzle ou utiliser les boutons rapides (Queens, Zip, Tango)
2. **Cocher/décocher** "Enregistrer vidéo" selon vos besoins
3. **Cliquer** sur "Start Solver"
4. **Attendre** que le solver trouve la solution
5. **Observer** la solution jouée automatiquement dans le navigateur

### Options

- **Enregistrer vidéo** : Active/désactive l'enregistrement vidéo de la résolution
  - Cochée : Vidéo sauvegardée dans `videos/`
  - Décochée : Pas de vidéo, performances optimales

### Puzzles Supportés

- LinkedIn Queens
- LinkedIn Zip  
- LinkedIn Tango
- Et bien d'autres puzzles de logique...

## Configuration

### Navigateur

Par défaut, Chromium est utilisé. Pour changer :

1. Ouvrir `GridProviders/ScrapingGridProvider.ini`
2. Modifier `browser_type = chromium` vers `firefox` ou `webkit`

### Mode Headless

Pour exécuter sans afficher le navigateur :

1. Ouvrir `GridProviders/ScrapingGridProvider.ini`
2. Modifier `headless = False` vers `headless = True`

## Dépannage

### L'exécutable ne démarre pas
- Vérifier que tous les fichiers du dossier `PuzzleSolver` sont présents
- Vérifier les logs dans la console

### "Navigateur non trouvé"
- Installer les navigateurs Playwright : `playwright install chromium`

### Vidéos non créées
- Vérifier que la checkbox "Enregistrer vidéo" est cochée
- Vérifier que le dossier `videos/` existe et est accessible

### Performances lentes
- Décocher "Enregistrer vidéo" pour améliorer les performances
- Utiliser le mode headless

## Support

Pour signaler un bug ou demander de l'aide, créer une issue sur GitHub.

## Licences

Voir le fichier LICENSE dans le dépôt.

## Automatisation (GitHub Actions)

Ce projet inclut un workflow d'intégration continue `.github/workflows/build_release.yml` qui permet :

1.  **Build Automatique** : À chaque push de tag `v*` ou déclenchement manuel.
2.  **Création de Release** : Génère automatiquement une Release GitHub avec le fichier `PuzzleSolver.zip` attaché.

### Pour créer une nouvelle version :

1.  Pousser un tag sur GitHub :
    ```bash
    git tag v1.0.0
    git push origin v1.0.0
    ```
2.  GitHub Actions va lancer le build sur Windows.
3.  Une fois terminé, une nouvelle **Release** apparaîtra sur GitHub avec le fichier `.zip` prêt à télécharger.

### Pour lancer un build de test manuel :

1.  Aller dans l'onglet **Actions** du dépôt GitHub.
2.  Sélectionner le workflow **Build and Release Executable**.
3.  Cliquer sur **Run workflow**.
4.  L'exécutable sera disponible dans les **Artifacts** du run.
