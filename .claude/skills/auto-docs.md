# Skill: /auto-docs

Génère automatiquement la documentation du projet (README, API docs, guides) avec MkDocs, JSDoc ou Sphinx.

## Ce que fait ce skill

1. **Génère le README.md** complet avec badges, installation, usage, exemples
2. **Documente le code** (JSDoc pour JS/TS, docstrings Python, GoDoc)
3. **Crée un site de documentation** (MkDocs, Sphinx, Docusaurus)
4. **Génère le CHANGELOG** depuis l'historique git
5. **Crée les guides utilisateur** (Getting Started, Tutorials, API Reference)
6. **Maintient la doc à jour** en synchronisant avec le code modifié

## Instructions

Quand l'utilisateur invoque `/auto-docs` :

- Analyser le code source pour extraire : fonctions exportées, types, classes, routes API
- Générer des commentaires JSDoc/docstrings sur les fonctions sans documentation
- Créer ou mettre à jour le README avec les infos du projet
- Si MkDocs/Sphinx est configuré, régénérer la documentation
- Adapter le style et la langue (FR/EN) selon la préférence de l'utilisateur

## Exemples de ce que ce skill génère

### README.md complet
```markdown
# Nom du Projet

[![CI](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

## Description
Brève description du projet.

## Installation
\`\`\`bash
npm install && npm run dev
\`\`\`

## Usage
\`\`\`typescript
import { myFunction } from './lib'
myFunction({ option: 'value' })
\`\`\`

## API Reference
| Endpoint | Méthode | Description |
|----------|---------|-------------|
| /api/users | GET | Liste des utilisateurs |
```

### JSDoc généré
```typescript
/**
 * Calcule le prix total avec taxes
 * @param price - Prix hors taxes en euros
 * @param taxRate - Taux de TVA (ex: 0.20 pour 20%)
 * @returns Prix TTC arrondi à 2 décimales
 * @throws {Error} Si le prix est négatif
 * @example
 * calculateTotal(100, 0.20) // → 120.00
 */
export function calculateTotal(price: number, taxRate: number): number
```

## Arguments optionnels

- `/auto-docs readme` → génère uniquement le README
- `/auto-docs jsdoc` → ajoute les commentaires JSDoc manquants dans le code
- `/auto-docs changelog` → génère le CHANGELOG depuis git log
- `/auto-docs site --mkdocs` → crée un site de doc MkDocs complet
- `/auto-docs site --docusaurus` → crée un site Docusaurus
- `/auto-docs --lang fr` → génère la documentation en français
- `/auto-docs update` → met à jour la doc pour les fichiers modifiés récemment
- `/auto-docs api` → génère la référence API complète
