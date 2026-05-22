# Skill: /code-quality

Analyse la qualité du code du projet en combinant ESLint, Stylelint et les règles SonarQube.

## Ce que fait ce skill

1. **Détecte le type de projet** (JS/TS, CSS/SCSS, React, Vue, etc.)
2. **Analyse le code** selon les règles de qualité :
   - JavaScript/TypeScript → règles ESLint (no-unused-vars, no-console, complexity, etc.)
   - CSS/SCSS → règles Stylelint (order, naming, specificity)
   - Logique métier → règles SonarQube (code smells, duplications, complexity cyclomatique)
3. **Reporte les problèmes** classés par sévérité : ERROR / WARNING / INFO
4. **Corrige automatiquement** les problèmes auto-fixables
5. **Propose des refactorisations** pour les problèmes complexes

## Instructions

Quand l'utilisateur invoque `/code-quality` :

- Si aucun fichier n'est précisé, analyser tous les fichiers modifiés (`git diff --name-only`)
- Si un fichier/dossier est précisé, analyser uniquement celui-ci
- Afficher un rapport groupé par fichier avec numéros de ligne
- Appliquer les corrections auto-fixables directement
- Pour chaque problème non auto-fixable, proposer une solution concrète avec exemple de code

## Format du rapport

```
[FICHIER] src/components/Button.tsx
  L12 ERROR   no-unused-vars: 'props' est déclaré mais jamais utilisé
  L34 WARNING complexity: fonction trop complexe (score: 15, max: 10)
  L67 INFO    prefer-const: utiliser 'const' au lieu de 'let'

Résumé: 3 problèmes (1 ERROR, 1 WARNING, 1 INFO) — 1 auto-fixable
```

## Arguments optionnels

- `/code-quality --fix` → applique toutes les corrections automatiques
- `/code-quality --strict` → active toutes les règles, zéro tolérance
- `/code-quality src/components` → analyse un dossier spécifique
- `/code-quality --report` → génère un rapport HTML exportable
