# Skill: /auto-test

Génère, organise et lance automatiquement des tests en utilisant Jest, Mocha ou Selenium selon le contexte.

## Ce que fait ce skill

1. **Détecte le framework de test** déjà en place (Jest, Mocha, Vitest, Cypress)
2. **Génère des tests unitaires** pour les fonctions/composants sélectionnés
3. **Génère des tests d'intégration** pour les APIs et modules
4. **Génère des tests E2E** (end-to-end) avec Selenium/Playwright pour les interfaces web
5. **Lance les tests** et affiche les résultats avec couverture de code
6. **Identifie les zones non couvertes** et propose des tests supplémentaires

## Instructions

Quand l'utilisateur invoque `/auto-test` :

- Analyser le fichier ou module ciblé pour comprendre les fonctions exportées
- Générer des cas de test couvrant : happy path, edge cases, erreurs attendues
- Placer les fichiers de test dans le dossier conventionnel (`__tests__/`, `*.test.ts`, `*.spec.ts`)
- Si un framework n'est pas installé, proposer d'en installer un adapté au projet
- Lancer les tests après génération et afficher la couverture

## Types de tests générés

### Tests unitaires (Jest/Mocha)
```typescript
describe('functionName', () => {
  it('should return expected value for valid input', () => { ... })
  it('should throw error for invalid input', () => { ... })
  it('should handle edge case: empty array', () => { ... })
})
```

### Tests E2E (Selenium/Playwright)
```typescript
test('user can complete checkout flow', async ({ page }) => {
  await page.goto('/checkout')
  await page.fill('#email', 'test@example.com')
  await page.click('#submit')
  await expect(page.locator('.success')).toBeVisible()
})
```

## Arguments optionnels

- `/auto-test src/utils/format.ts` → génère des tests pour un fichier spécifique
- `/auto-test --e2e` → génère uniquement des tests end-to-end
- `/auto-test --coverage` → lance les tests avec rapport de couverture détaillé
- `/auto-test --watch` → lance les tests en mode watch (re-run sur chaque changement)
- `/auto-test --fix-failing` → analyse les tests qui échouent et propose des corrections
