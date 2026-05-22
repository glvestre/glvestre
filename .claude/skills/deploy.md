# Skill: /deploy

Prépare et déploie l'application avec Docker, GitHub Actions et les plateformes cloud.

## Comportement par défaut

Quand l'utilisateur tape `/deploy` sans argument :
1. Détecter le type de projet (Node.js, Python, Go, PHP, static)
2. Vérifier les prérequis : tests passants, build OK, variables d'env définies
3. Créer le Dockerfile s'il n'existe pas
4. Créer le pipeline GitHub Actions s'il n'existe pas
5. Demander la plateforme cible si non précisée

## Étapes d'exécution

### 1. Détecter le projet et vérifier les prérequis
```bash
# Type de projet
[ -f package.json ] && node -e "const p=require('./package.json'); console.log(p.scripts)"
[ -f requirements.txt ] && echo "python"
[ -f go.mod ] && echo "go"
[ -f Dockerfile ] && echo "dockerfile:exists"

# Prérequis
git status --porcelain  # fichiers non commités ?
npm test 2>&1 | tail -5  # tests passants ?
npm run build 2>&1 | tail -5  # build OK ?
```

### 2. Générer le Dockerfile (multi-stage optimisé)

#### Node.js
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder /app/package.json ./
USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

#### Python/FastAPI
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.12-slim AS runner
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
RUN useradd -m appuser && chown -R appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Générer docker-compose.yml
```yaml
version: '3.9'
services:
  app:
    build:
      context: .
      target: runner
    ports:
      - "${PORT:-3000}:3000"
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME:-myapp}
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:?DB_PASSWORD required}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 4. Générer le pipeline GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    name: Tests & Qualité
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  build:
    name: Build Docker
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build & Push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    name: Déploiement Production
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - name: Deploy
        run: |
          # Adapté selon la plateforme (voir /deploy --platform)
          echo "Déploiement en cours..."
```

### 5. Scripts utilitaires générés

```bash
# scripts/deploy.sh
#!/bin/bash
set -euo pipefail

echo "🔍 Vérification des prérequis..."
[ -z "$(git status --porcelain)" ] || { echo "❌ Fichiers non commités"; exit 1; }
npm test || { echo "❌ Tests en échec"; exit 1; }
npm run build || { echo "❌ Build en échec"; exit 1; }

echo "🐳 Build Docker..."
docker build -t myapp:latest .
docker tag myapp:latest myapp:$(git rev-parse --short HEAD)

echo "✅ Prêt pour le déploiement"
echo "   Image: myapp:$(git rev-parse --short HEAD)"
```

## Arguments

- `/deploy --platform vercel` → génère `vercel.json` + config Next.js optimale
- `/deploy --platform netlify` → génère `netlify.toml` + build config
- `/deploy --platform heroku` → génère `Procfile` + `app.json`
- `/deploy --platform aws` → génère config ECS Task Definition + ALB
- `/deploy --platform gcp` → génère `cloudbuild.yaml` + Cloud Run config
- `/deploy --docker` → crée uniquement Dockerfile + docker-compose.yml
- `/deploy --ci` → génère uniquement le pipeline GitHub Actions
- `/deploy check` → vérifie que tout est prêt (tests, build, env vars, secrets)
- `/deploy rollback` → génère un script de rollback vers la version précédente
