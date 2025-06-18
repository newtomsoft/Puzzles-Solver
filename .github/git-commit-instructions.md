# 📘 Git Commit Guidelines — Conventional Commits

Ce projet suit la convention **[Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/)** pour garantir des messages de commit cohérents et lisibles par les humains et les outils.

---

## 📌 Format de base

```text
<type>(<scope>): <description>
```

- `type` : nature du changement (obligatoire)
- `scope` : module ou fonctionnalité concernée (optionnel mais recommandé)
- `description` : courte phrase à l’infinitif ou au présent de l’indicatif, sans majuscule ni point final

---

## ✅ Exemples valides

```text
feat(auth): add OAuth2 login support
fix(cart): correct total calculation on discount
docs(readme): update installation instructions
style(ui): improve button spacing
refactor(user): extract name parsing logic
test(api): add tests for order controller
chore(ci): migrate to GitHub Actions
```

---

## 🔤 Types autorisés

| Type       | Description |
|------------|-------------|
| `feat`     | Nouvelle fonctionnalité |
| `fix`      | Correction de bug |
| `docs`     | Documentation uniquement |
| `style`    | Changement de style (indentation, formatage, etc.) sans impact fonctionnel |
| `refactor` | Refactoring sans ajout de fonctionnalité ni correction de bug |
| `perf`     | Amélioration de performance |
| `test`     | Ajout ou modification de tests |
| `chore`    | Maintenance, configuration, tâches internes |
| `build`    | Changements impactant le système de build |
| `ci`       | Modifications liées à l’intégration continue |

---

## 🔥 Règles d’écriture

- ✅ Phrase courte, sans majuscule initiale, sans point final :
  ```text
  fix(ui): prevent crash on empty input
  ```
- ❌ À éviter :
  ```text
  Fix: Crash on empty input.
  ```

- ✅ Préférer les verbes d’action clairs : "add", "remove", "fix", "improve", "refactor", etc.

---

## 🧪 Exemples avancés

- Commit multiple :
  ```text
  feat(payment): add PayPal support
  fix(payment): resolve currency mismatch bug
  ```
- Commit technique :
  ```text
  chore(deps): update eslint to v8.4.1
  build(docker): add multi-arch support
  ```

---

## 🚀 Tips

- Utilise l’outil `commitizen` ou un hook Git pour être guidé automatiquement.
- Garde les commits petits et cohérents pour une meilleure relecture et un changelog clair.

---

📚 Pour plus d'infos : [conventionalcommits.org](https://www.conventionalcommits.org/fr/v1.0.0/)
