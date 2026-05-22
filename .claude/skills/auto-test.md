# Skill: /auto-test

Génère et lance des tests unitaires, d'intégration et E2E pour le projet actuel.

## Comportement par défaut

Quand l'utilisateur tape `/auto-test` sans argument :
1. Détecter le framework de test installé (`jest`, `vitest`, `mocha`, `cypress`, `playwright`)
2. Si aucun framework détecté, recommander Jest pour JS/TS et l'installer si l'utilisateur accepte
3. Analyser les fichiers sans tests associés (`src/utils/format.ts` → existe-t-il `format.test.ts` ?)
4. Générer les tests manquants pour les fonctions exportées
5. Lancer les tests et afficher les résultats

## Étapes d'exécution

### 1. Détecter le framework
```bash
cat package.json | grep -E '"jest"|"vitest"|"mocha"|"cypress"|"playwright"'
ls *.config.{js,ts} 2>/dev/null | grep -E 'jest|vitest|playwright'
```

### 2. Analyser les fichiers sans couverture
Pour chaque fichier source, vérifier s'il a un fichier de test correspondant.
Lister les fonctions/méthodes exportées non testées.

### 3. Générer les tests

#### Tests unitaires (Jest/Vitest)
Couvrir systématiquement :
- **Happy path** : entrées valides → résultat attendu
- **Edge cases** : tableau vide, string vide, 0, null, undefined
- **Erreurs** : entrées invalides → exception attendue
- **Boundary** : valeurs limites (max int, string très longue)

```typescript
// Exemple généré pour: export function formatPrice(amount: number, currency: string): string
describe('formatPrice', () => {
  it('formats EUR price correctly', () => {
    expect(formatPrice(10.5, 'EUR')).toBe('10,50 €')
  })
  it('handles zero', () => {
    expect(formatPrice(0, 'EUR')).toBe('0,00 €')
  })
  it('throws for negative amount', () => {
    expect(() => formatPrice(-1, 'EUR')).toThrow('Amount must be positive')
  })
  it('handles large numbers', () => {
    expect(formatPrice(1000000, 'EUR')).toBe('1 000 000,00 €')
  })
})
```

#### Tests API/intégration (Supertest)
```typescript
describe('POST /api/users', () => {
  it('creates user with valid data', async () => {
    const res = await request(app).post('/api/users').send({ email: 'test@test.com' })
    expect(res.status).toBe(201)
    expect(res.body).toHaveProperty('id')
  })
  it('returns 400 for missing email', async () => {
    const res = await request(app).post('/api/users').send({})
    expect(res.status).toBe(400)
  })
})
```

#### Tests E2E (Playwright)
```typescript
test('user completes signup flow', async ({ page }) => {
  await page.goto('/signup')
  await page.fill('[name="email"]', 'user@test.com')
  await page.fill('[name="password"]', 'SecurePass123!')
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL('/dashboard')
  await expect(page.locator('h1')).toContainText('Bienvenue')
})
```

### 4. Lancer les tests
```bash
npx jest --coverage --passWithNoTests
# ou
npx vitest run --coverage
```

### 5. Afficher les résultats
```
╔══════════════════════════════════════════════╗
║            RÉSULTATS DES TESTS               ║
╚══════════════════════════════════════════════╝
✅  12 tests passés
❌   2 tests échoués
⏭️   1 test ignoré

COUVERTURE:
  Statements : 87% ████████░░
  Branches   : 74% ███████░░░
  Functions  : 92% █████████░
  Lines      : 88% ████████░░

Tests en échec:
  ❌ formatPrice › handles large numbers
     Expected: "1 000 000,00 €"
     Received: "1000000.00 €"
```

## Arguments

- `/auto-test [fichier]` → génère des tests pour un fichier spécifique
- `/auto-test --e2e` → génère uniquement des tests Playwright/Selenium
- `/auto-test --coverage` → lance avec rapport de couverture détaillé
- `/auto-test --watch` → lance en mode watch (re-run sur chaque changement)
- `/auto-test --fix` → analyse les tests qui échouent et propose/applique des corrections
- `/auto-test --missing` → liste tous les fichiers sans tests associés
