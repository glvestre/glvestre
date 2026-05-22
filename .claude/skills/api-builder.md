# Skill: /api-builder

Conçoit, génère et documente des APIs REST ou GraphQL avec export Swagger/OpenAPI et collections Postman.

## Ce que fait ce skill

1. **Génère le code d'une API** (Express, FastAPI, NestJS, Go Fiber, etc.) depuis une description
2. **Crée la documentation OpenAPI/Swagger** automatiquement
3. **Exporte une collection Postman** prête à importer
4. **Génère les types TypeScript** depuis le schéma API
5. **Crée les tests d'API** (requêtes, assertions sur les réponses)
6. **Valide un schéma API existant** et détecte les incohérences

## Instructions

Quand l'utilisateur invoque `/api-builder` :

- Si une description est fournie → générer l'API complète (routes, contrôleurs, validation)
- Si un fichier de code existe → en extraire le schéma OpenAPI
- Toujours inclure : authentification JWT, validation des entrées, gestion d'erreurs standard
- Générer la doc Swagger inline (commentaires JSDoc ou decorators)
- Proposer des exemples de requêtes pour chaque endpoint

## Exemple de ce que ce skill génère

### Description → API complète
```
/api-builder "API e-commerce: produits, panier, commandes"
```

Génère :
```
GET    /api/products         → liste des produits avec filtres
GET    /api/products/:id     → détail d'un produit
POST   /api/products         → créer un produit (admin)
PUT    /api/products/:id     → modifier un produit (admin)
DELETE /api/products/:id     → supprimer (admin)
POST   /api/cart/add         → ajouter au panier
GET    /api/cart             → voir le panier
POST   /api/orders           → passer une commande
GET    /api/orders/:id       → statut d'une commande
```

### Schéma OpenAPI généré
```yaml
openapi: 3.0.0
info:
  title: E-Commerce API
  version: 1.0.0
paths:
  /api/products:
    get:
      summary: Liste des produits
      parameters:
        - name: category
          in: query
          schema:
            type: string
```

## Arguments optionnels

- `/api-builder "description"` → génère une API depuis une description
- `/api-builder --graphql` → génère une API GraphQL au lieu de REST
- `/api-builder --framework nestjs` → utilise NestJS avec decorators
- `/api-builder --framework fastapi` → génère en Python/FastAPI
- `/api-builder export-postman` → exporte la collection Postman du projet
- `/api-builder export-swagger` → génère le fichier swagger.yaml
- `/api-builder validate` → valide et corrige le schéma API existant
- `/api-builder mock` → génère un serveur mock pour tester sans backend
