# Skill: /deploy

Prépare et déploie l'application avec Docker, GitHub Actions et les plateformes cloud (Heroku, AWS, Vercel, etc.).

## Ce que fait ce skill

1. **Crée le Dockerfile** optimisé pour le type de projet détecté
2. **Génère le docker-compose.yml** pour l'environnement local et production
3. **Configure le pipeline CI/CD** GitHub Actions (build, test, deploy)
4. **Déploie sur la plateforme cible** (Heroku, Vercel, Netlify, AWS, GCP)
5. **Configure les variables d'environnement** de manière sécurisée
6. **Génère les scripts de déploiement** (build, migration DB, health check)

## Instructions

Quand l'utilisateur invoque `/deploy` :

- Détecter le type de projet (Node.js, Python, Go, PHP, etc.)
- Créer un Dockerfile multi-stage optimisé (build léger, image de production minimale)
- Générer le workflow GitHub Actions adapté
- Demander la plateforme cible si non précisée
- Ne jamais écrire de secrets en dur — utiliser des variables d'environnement / GitHub Secrets

## Fichiers générés

### Dockerfile (multi-stage)
```dockerfile
# Stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage production
FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### GitHub Actions (.github/workflows/deploy.yml)
```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: ./scripts/deploy.sh
```

### docker-compose.yml
```yaml
version: '3.9'
services:
  app:
    build: .
    ports: ["3000:3000"]
    env_file: .env
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
```

## Arguments optionnels

- `/deploy --platform vercel` → configure le déploiement Vercel
- `/deploy --platform heroku` → configure Heroku avec Procfile
- `/deploy --platform aws` → génère les configs ECS/EC2
- `/deploy --platform gcp` → génère les configs Cloud Run
- `/deploy --docker` → crée uniquement le Dockerfile et docker-compose
- `/deploy --ci` → génère uniquement le pipeline CI/CD GitHub Actions
- `/deploy --rollback` → crée un script de rollback en cas de problème
- `/deploy check` → vérifie que tout est prêt pour un déploiement (tests, build, env vars)
