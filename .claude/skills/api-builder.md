# Skill: /api-builder

Conçoit, génère et documente des APIs REST ou GraphQL.
Génère automatiquement : code des routes, validation, schéma OpenAPI, collection Postman.

## Comportement par défaut

Quand l'utilisateur tape `/api-builder` sans argument :
- Détecter si une API existe déjà dans le projet (routes, controllers)
- Si oui : générer le schéma OpenAPI depuis le code existant
- Si non : demander une description pour générer l'API depuis zéro

## Étapes d'exécution

### 1. Détecter le framework backend
```bash
cat package.json | grep -E '"express"|"fastify"|"nestjs"|"hono"|"koa"'
# Python
cat requirements.txt | grep -E 'fastapi|flask|django'
```

### 2. Analyser l'API existante (si présente)
Lire les fichiers de routes et extraire :
- Méthode HTTP + chemin
- Paramètres (path, query, body)
- Réponses possibles
- Middlewares d'authentification

### 3. Générer l'API depuis une description

Format de génération :
```
/api-builder "API blog: articles, catégories, commentaires, authentification JWT"
```

Génère automatiquement pour chaque ressource :
- Routes CRUD complètes
- Validation des entrées (zod / joi / pydantic)
- Gestion d'erreurs standardisée
- Pagination pour les listes
- Authentification JWT sur les routes protégées

#### Exemple Express + TypeScript généré

```typescript
// routes/articles.ts
import { Router } from 'express'
import { z } from 'zod'
import { authenticate } from '../middleware/auth'
import { ArticleController } from '../controllers/ArticleController'

const router = Router()
const ctrl = new ArticleController()

const CreateArticleSchema = z.object({
  title: z.string().min(3).max(200),
  content: z.string().min(10),
  categoryId: z.string().uuid(),
  published: z.boolean().default(false),
})

/**
 * @openapi
 * /api/articles:
 *   get:
 *     summary: Liste des articles
 *     parameters:
 *       - name: page
 *         in: query
 *         schema: { type: integer, default: 1 }
 *       - name: category
 *         in: query
 *         schema: { type: string }
 */
router.get('/', ctrl.list)

/**
 * @openapi
 * /api/articles:
 *   post:
 *     summary: Créer un article
 *     security: [{ bearerAuth: [] }]
 */
router.post('/', authenticate, async (req, res, next) => {
  try {
    const data = CreateArticleSchema.parse(req.body)
    const article = await ctrl.create(data, req.user.id)
    res.status(201).json({ success: true, data: article })
  } catch (err) {
    next(err)
  }
})

router.get('/:id', ctrl.getById)
router.put('/:id', authenticate, ctrl.update)
router.delete('/:id', authenticate, ctrl.delete)

export default router
```

#### Réponses d'erreur standardisées
```typescript
// Toujours utiliser ce format
{ "success": false, "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }
{ "success": false, "error": { "code": "NOT_FOUND", "message": "Article introuvable" } }
{ "success": false, "error": { "code": "UNAUTHORIZED", "message": "Token invalide ou expiré" } }
```

### 4. Générer le schéma OpenAPI

```yaml
# swagger.yaml généré automatiquement
openapi: 3.0.3
info:
  title: Blog API
  version: 1.0.0
  description: API RESTful pour la gestion d'un blog

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    Article:
      type: object
      properties:
        id: { type: string, format: uuid }
        title: { type: string, maxLength: 200 }
        content: { type: string }
        published: { type: boolean }
        createdAt: { type: string, format: date-time }
      required: [id, title, content]

paths:
  /api/articles:
    get:
      summary: Liste des articles
      parameters:
        - name: page
          in: query
          schema: { type: integer, default: 1, minimum: 1 }
        - name: limit
          in: query
          schema: { type: integer, default: 20, maximum: 100 }
      responses:
        '200':
          description: Liste paginée
          content:
            application/json:
              schema:
                type: object
                properties:
                  data: { type: array, items: { $ref: '#/components/schemas/Article' } }
                  pagination: { type: object, properties: { page: { type: integer }, total: { type: integer } } }
```

### 5. Générer la collection Postman
```json
{
  "info": { "name": "Blog API", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json" },
  "variable": [{ "key": "baseUrl", "value": "http://localhost:3000" }, { "key": "token", "value": "" }],
  "item": [
    {
      "name": "Articles",
      "item": [
        { "name": "GET /api/articles", "request": { "method": "GET", "url": "{{baseUrl}}/api/articles?page=1&limit=20" } },
        { "name": "POST /api/articles", "request": { "method": "POST", "url": "{{baseUrl}}/api/articles", "header": [{ "key": "Authorization", "value": "Bearer {{token}}" }], "body": { "mode": "raw", "raw": "{ \"title\": \"Mon article\", \"content\": \"Contenu...\", \"categoryId\": \"uuid\" }" } } }
      ]
    }
  ]
}
```

## Arguments

- `/api-builder "[description]"` → génère une API complète depuis une description
- `/api-builder --graphql` → génère une API GraphQL (schema + resolvers)
- `/api-builder --framework nestjs` → utilise NestJS avec decorators et modules
- `/api-builder --framework fastapi` → génère en Python/FastAPI avec Pydantic
- `/api-builder export-swagger` → génère `swagger.yaml` depuis le code existant
- `/api-builder export-postman` → génère `collection.postman.json`
- `/api-builder mock` → crée un serveur mock JSON pour tester sans backend
- `/api-builder validate` → valide les routes existantes (cohérence, sécurité, docs)
- `/api-builder add [ressource]` → ajoute une nouvelle ressource CRUD à l'API existante
