# Skill: /db-manage

Génère et optimise les schémas de base de données, migrations, requêtes et seeders pour PostgreSQL, MongoDB et Redis.

## Ce que fait ce skill

1. **Conçoit le schéma de base de données** depuis une description métier
2. **Génère les migrations** (SQL pour PostgreSQL, Mongoose schemas pour MongoDB)
3. **Optimise les requêtes** lentes et propose des index
4. **Génère les seeders** (données de test réalistes)
5. **Crée les modèles ORM** (Prisma, TypeORM, Sequelize, Mongoose)
6. **Documente le schéma** avec un diagramme ERD textuel

## Instructions

Quand l'utilisateur invoque `/db-manage` :

- Si une description est fournie → concevoir le schéma optimal
- Si un schéma existe → l'analyser et proposer des optimisations
- Toujours inclure : clés primaires/étrangères, index, contraintes d'intégrité
- Pour PostgreSQL : utiliser des types appropriés (UUID, JSONB, ENUM, etc.)
- Pour MongoDB : définir les schémas Mongoose avec validation
- Pour Redis : proposer les structures de données adaptées (String, Hash, List, Set, Sorted Set)

## Exemples de ce que ce skill génère

### Description → Schéma PostgreSQL
```
/db-manage "Application e-commerce: utilisateurs, produits, commandes"
```

```sql
-- Migration générée
CREATE TABLE users (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email       VARCHAR(255) UNIQUE NOT NULL,
  password    VARCHAR(255) NOT NULL,
  role        user_role DEFAULT 'customer',
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE products (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        VARCHAR(255) NOT NULL,
  price       DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  stock       INTEGER DEFAULT 0,
  metadata    JSONB,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_metadata ON products USING gin(metadata);
```

### Modèle Prisma
```prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  orders    Order[]
  createdAt DateTime @default(now())
}
```

### Schéma Redis pour sessions
```
session:{userId}  → Hash { token, expiresAt, ip }
cart:{userId}     → Hash { productId: quantity }
rate_limit:{ip}   → String (counter avec TTL)
```

## Arguments optionnels

- `/db-manage "description"` → génère un schéma depuis une description
- `/db-manage --postgres` → cible PostgreSQL (SQL + migrations)
- `/db-manage --mongo` → cible MongoDB (schémas Mongoose)
- `/db-manage --redis` → propose l'architecture Redis
- `/db-manage --prisma` → génère le schéma Prisma
- `/db-manage optimize` → analyse les requêtes lentes et propose des index
- `/db-manage seed` → génère des données de test réalistes
- `/db-manage erd` → affiche le diagramme ERD du schéma actuel
- `/db-manage migrate` → crée une nouvelle migration depuis les changements de schéma
