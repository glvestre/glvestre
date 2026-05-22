# Skill: /auto-docs

Génère et maintient la documentation du projet : README, commentaires de code, site de docs, CHANGELOG.

## Comportement par défaut

Quand l'utilisateur tape `/auto-docs` sans argument :
1. Analyser le projet (type, dépendances, fonctions exportées, API)
2. Vérifier ce qui est déjà documenté vs ce qui manque
3. Générer ou mettre à jour le README.md en priorité
4. Ajouter les commentaires JSDoc/docstrings manquants sur les fonctions publiques
5. Afficher un résumé de ce qui a été généré

## Étapes d'exécution

### 1. Analyser l'existant
```bash
cat README.md 2>/dev/null | wc -l  # README existe et a du contenu ?
grep -r "\/\*\*" src/ | wc -l      # Combien de commentaires JSDoc ?
git log --oneline -20               # Historique pour le CHANGELOG
cat package.json | grep -E '"name"|"version"|"description"|"scripts"'
```

### 2. Générer le README.md complet

Structure cible :
```markdown
# Nom du Projet

[![CI](https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg)](...)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](...)
[![npm version](https://badge.fury.io/js/PACKAGE.svg)](...)

> Description courte et percutante du projet (1-2 phrases)

## Aperçu
[Screenshot ou GIF si applicable]

## Fonctionnalités
- ✅ Fonctionnalité 1
- ✅ Fonctionnalité 2

## Installation
\`\`\`bash
npm install nom-du-package
# ou
git clone https://github.com/user/repo && cd repo && npm install
\`\`\`

## Démarrage rapide
\`\`\`typescript
import { Client } from 'nom-du-package'
const client = new Client({ apiKey: process.env.API_KEY })
const result = await client.doSomething()
\`\`\`

## Configuration
| Variable | Description | Requis | Défaut |
|----------|-------------|--------|--------|
| `API_KEY` | Clé d'API | ✅ | — |
| `PORT` | Port du serveur | ❌ | 3000 |

## API Reference
[Généré automatiquement depuis le code]

## Contribuer
1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/ma-feature`)
3. Commit (`git commit -m 'feat: ajoute ma feature'`)
4. Push (`git push origin feature/ma-feature`)
5. Ouvrir une Pull Request

## Licence
MIT — voir [LICENSE](LICENSE)
```

### 3. Générer les commentaires JSDoc

Pour chaque fonction exportée sans documentation :

```typescript
// AVANT (non documenté)
export function calculateDiscount(price, discountPercent, maxDiscount) {
  if (discountPercent > 100) throw new Error('Invalid')
  const discount = price * (discountPercent / 100)
  return Math.min(discount, maxDiscount)
}

// APRÈS (documenté par /auto-docs)
/**
 * Calcule la remise appliquée à un prix, plafonnée à un maximum.
 * @param price - Prix original en euros (doit être positif)
 * @param discountPercent - Taux de remise en pourcentage (0-100)
 * @param maxDiscount - Montant maximum de remise autorisé
 * @returns Montant de la remise en euros
 * @throws {Error} Si discountPercent dépasse 100
 * @example
 * calculateDiscount(200, 20, 30) // → 30 (plafonné)
 * calculateDiscount(100, 10, 50) // → 10
 */
export function calculateDiscount(price: number, discountPercent: number, maxDiscount: number): number {
```

### 4. Générer le CHANGELOG

Depuis `git log --oneline`, classer par type de commit :

```markdown
# Changelog

## [Unreleased]

## [1.2.0] — 2026-05-22
### Ajouté
- Authentification OAuth2 avec Google (#45)
- Pagination sur l'endpoint /api/articles (#43)

### Modifié
- Amélioration des performances de la recherche (2x plus rapide)

### Corrigé
- Crash lors d'un email invalide à l'inscription (#48)
- Fuite mémoire dans le worker de notifications (#47)

## [1.1.0] — 2026-04-10
...
```

### 5. Générer le site de documentation (MkDocs)

```yaml
# mkdocs.yml généré
site_name: Nom du Projet
site_description: Documentation complète
theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
    - search.suggest

nav:
  - Accueil: index.md
  - Guide de démarrage: getting-started.md
  - API Reference: api-reference.md
  - Tutoriels:
    - Tutoriel 1: tutorials/tutorial-1.md
  - Contribuer: contributing.md

plugins:
  - search
  - mkdocstrings
```

## Arguments

- `/auto-docs readme` → génère/met à jour uniquement le README.md
- `/auto-docs jsdoc` → ajoute les commentaires JSDoc manquants dans tout le code
- `/auto-docs jsdoc [fichier]` → documente un fichier spécifique
- `/auto-docs changelog` → génère le CHANGELOG depuis l'historique git
- `/auto-docs site --mkdocs` → initialise un site MkDocs complet
- `/auto-docs site --docusaurus` → initialise un site Docusaurus
- `/auto-docs api` → génère la référence API complète depuis le code
- `/auto-docs --lang fr` → génère en français
- `/auto-docs --lang en` → génère en anglais
- `/auto-docs update` → met à jour uniquement la doc des fichiers modifiés depuis le dernier commit
- `/auto-docs missing` → liste les fonctions publiques sans documentation
