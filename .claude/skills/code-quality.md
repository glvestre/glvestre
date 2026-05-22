# Skill: /code-quality

Analyse et corrige la qualité du code du projet actuel.

## Comportement par défaut

Quand l'utilisateur tape `/code-quality` sans argument :
1. Lancer `git diff --name-only HEAD` pour obtenir les fichiers modifiés
2. Si aucun fichier modifié, analyser tout le projet (`src/`, `app/`, `lib/`)
3. Détecter le langage (JS/TS/CSS/Python) et appliquer les règles correspondantes
4. Afficher le rapport puis proposer `--fix`

## Étapes d'exécution

### 1. Détecter les outils disponibles
```bash
# Vérifier si les outils sont installés localement
[ -f node_modules/.bin/eslint ] && echo "eslint:ok"
[ -f node_modules/.bin/stylelint ] && echo "stylelint:ok"
[ -f .eslintrc* ] || [ -f eslint.config* ] && echo "eslint-config:ok"
```

Si les outils ne sont PAS installés : analyser le code manuellement en appliquant les règles ci-dessous.

### 2. Règles ESLint à appliquer (JS/TS)
- `no-unused-vars` : variables déclarées jamais utilisées
- `no-console` : console.log laissés dans le code
- `eqeqeq` : utilisation de `==` au lieu de `===`
- `no-var` : utilisation de `var` au lieu de `const`/`let`
- `prefer-const` : `let` qui n'est jamais réassigné
- `complexity` : fonctions avec complexité cyclomatique > 10
- `max-lines-per-function` : fonctions dépassant 50 lignes
- `no-duplicate-imports` : imports dupliqués du même module
- `@typescript-eslint/no-explicit-any` : usage de `any` en TypeScript

### 3. Règles Stylelint à appliquer (CSS/SCSS)
- Propriétés dans l'ordre alphabétique ou logique
- Pas de `!important` sauf exception justifiée
- Unités cohérentes (px vs rem)
- Sélecteurs trop spécifiques (profondeur > 3)
- Variables CSS non utilisées

### 4. Règles SonarQube à appliquer (tous langages)
- Code dupliqué (même bloc > 10 lignes copié ailleurs)
- Fonctions trop longues (> 100 lignes)
- Fichiers trop longs (> 300 lignes)
- TODO/FIXME laissés dans le code
- Retours anticipés manquants (fonctions avec trop d'imbrications)

## Format du rapport

```
╔══════════════════════════════════════════════╗
║         RAPPORT QUALITÉ — src/Button.tsx     ║
╚══════════════════════════════════════════════╝

❌ ERROR   L12  no-unused-vars: 'theme' déclaré mais jamais utilisé
⚠️  WARNING L34  complexity: score 14/10 — décomposer en sous-fonctions
ℹ️  INFO    L67  prefer-const: remplacer 'let count' par 'const count'
ℹ️  INFO    L89  no-console: supprimer console.log de debug

────────────────────────────────────────────────
Résumé: 4 problèmes | 1 ERROR · 1 WARNING · 2 INFO
Auto-fixables: 2 (taper /code-quality --fix pour corriger)
```

## Arguments

- `/code-quality --fix` → corrige tous les problèmes auto-fixables directement dans les fichiers
- `/code-quality --strict` → active toutes les règles sans tolérance
- `/code-quality [chemin]` → analyse un fichier ou dossier spécifique
- `/code-quality --report` → génère un rapport markdown dans `quality-report.md`
- `/code-quality --ci` → mode silencieux, retourne erreur si ERROR trouvé (usage CI/CD)
