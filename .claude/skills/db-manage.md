# Skill: /db-manage

Conçoit, optimise et gère les bases de données : schémas, migrations, requêtes, seeders.
Supporte PostgreSQL, MongoDB et Redis.

## Comportement par défaut

Quand l'utilisateur tape `/db-manage` sans argument :
1. Détecter la base de données utilisée dans le projet
2. Analyser le schéma existant (fichiers de migration, modèles ORM)
3. Afficher un résumé du schéma actuel
4. Proposer des optimisations si des problèmes sont détectés

## Étapes d'exécution

### 1. Détecter la base de données
```bash
cat package.json | grep -E '"prisma"|"typeorm"|"sequelize"|"mongoose"|"pg"|"mysql2"'
ls prisma/ 2>/dev/null && cat prisma/schema.prisma
ls migrations/ 2>/dev/null | head -5
cat .env | grep -E 'DATABASE_URL|MONGO_URI|REDIS_URL' | sed 's/=.*/=***/'
```

### 2. Analyser et afficher le schéma actuel
Lire les fichiers de migration/schema existants et afficher un résumé ERD :

```
SCHÉMA ACTUEL
─────────────
users (6 colonnes)
  id         UUID, PK
  email      VARCHAR(255), UNIQUE, NOT NULL
  password   VARCHAR(255), NOT NULL
  role       ENUM(admin, user), DEFAULT 'user'
  created_at TIMESTAMPTZ, DEFAULT NOW()

products (8 colonnes)
  id          UUID, PK
  name        VARCHAR(255), NOT NULL
  price       DECIMAL(10,2), NOT NULL
  stock       INTEGER, DEFAULT 0
  user_id     UUID, FK → users.id, CASCADE DELETE

INDEX
  idx_users_email (users.email)
  idx_products_price (products.price)
```

### 3. Générer un schéma depuis une description

```
/db-manage "Application e-commerce: utilisateurs, produits avec variants, commandes, avis"
```

#### PostgreSQL — Migration SQL
```sql
-- Migration: 001_create_ecommerce_schema.sql
-- Généré le 2026-05-22 par /db-manage

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE user_role AS ENUM ('admin', 'customer');
CREATE TYPE order_status AS ENUM ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled');

CREATE TABLE users (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email       VARCHAR(255) UNIQUE NOT NULL,
  password    VARCHAR(255) NOT NULL,
  role        user_role DEFAULT 'customer',
  first_name  VARCHAR(100),
  last_name   VARCHAR(100),
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE products (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        VARCHAR(255) NOT NULL,
  description TEXT,
  base_price  DECIMAL(10,2) NOT NULL CHECK (base_price >= 0),
  category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
  is_active   BOOLEAN DEFAULT true,
  metadata    JSONB DEFAULT '{}',
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE product_variants (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  sku        VARCHAR(100) UNIQUE NOT NULL,
  price      DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  stock      INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
  attributes JSONB NOT NULL DEFAULT '{}'  -- { "color": "red", "size": "L" }
);

CREATE TABLE orders (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES users(id),
  status      order_status DEFAULT 'pending',
  total       DECIMAL(10,2) NOT NULL CHECK (total >= 0),
  metadata    JSONB DEFAULT '{}',
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE order_items (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id    UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  variant_id  UUID NOT NULL REFERENCES product_variants(id),
  quantity    INTEGER NOT NULL CHECK (quantity > 0),
  unit_price  DECIMAL(10,2) NOT NULL
);

-- Index pour les performances
CREATE INDEX idx_products_category ON products(category_id) WHERE is_active = true;
CREATE INDEX idx_products_metadata ON products USING gin(metadata);
CREATE INDEX idx_orders_user ON orders(user_id, created_at DESC);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_variants_product ON product_variants(product_id);
CREATE INDEX idx_variants_sku ON product_variants(sku);

-- Trigger: updated_at automatique
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$ LANGUAGE plpgsql;
CREATE TRIGGER users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Schéma Prisma
```prisma
// schema.prisma généré par /db-manage
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  password  String
  role      UserRole @default(CUSTOMER)
  orders    Order[]
  createdAt DateTime @default(now()) @map("created_at")

  @@map("users")
}

model Product {
  id          String           @id @default(uuid())
  name        String
  basePrice   Decimal          @db.Decimal(10, 2) @map("base_price")
  isActive    Boolean          @default(true) @map("is_active")
  variants    ProductVariant[]
  createdAt   DateTime         @default(now()) @map("created_at")

  @@index([isActive])
  @@map("products")
}

enum UserRole { ADMIN CUSTOMER }
enum OrderStatus { PENDING CONFIRMED SHIPPED DELIVERED CANCELLED }
```

#### Schéma MongoDB (Mongoose)
```typescript
// models/Product.ts
import { Schema, model } from 'mongoose'

const variantSchema = new Schema({
  sku:        { type: String, required: true, unique: true },
  price:      { type: Number, required: true, min: 0 },
  stock:      { type: Number, required: true, default: 0, min: 0 },
  attributes: { type: Map, of: String },  // { color: 'red', size: 'L' }
})

const productSchema = new Schema({
  name:       { type: String, required: true, trim: true, maxlength: 255 },
  price:      { type: Number, required: true, min: 0 },
  category:   { type: Schema.Types.ObjectId, ref: 'Category' },
  variants:   [variantSchema],
  isActive:   { type: Boolean, default: true },
  metadata:   { type: Map, of: Schema.Types.Mixed },
}, { timestamps: true })

productSchema.index({ category: 1, isActive: 1 })
productSchema.index({ 'variants.sku': 1 }, { unique: true, sparse: true })

export const Product = model('Product', productSchema)
```

#### Architecture Redis
```
# Sessions utilisateur
session:{userId}          → Hash { token, userAgent, ip, createdAt }
                             TTL: 7 jours

# Panier (rapide, volatile)
cart:{userId}             → Hash { variantId: quantity }
                             TTL: 30 jours

# Cache produits (lecture fréquente)
product:{productId}       → String (JSON sérialisé)
                             TTL: 1 heure

# Rate limiting
rate:{endpoint}:{ip}      → String (compteur)
                             TTL: 1 minute (fenêtre glissante)

# File d'attente emails
queue:emails              → List (LPUSH pour ajouter, BRPOP pour consommer)

# Classement produits populaires
leaderboard:products      → Sorted Set { productId: score }
```

### 4. Optimiser les requêtes lentes
Analyser les requêtes dans le code et détecter :
- Requêtes N+1 (boucle avec requête à chaque itération → utiliser `include`/`JOIN`)
- Absence d'index sur les colonnes filtrées/triées fréquemment
- `SELECT *` au lieu de sélectionner les colonnes nécessaires
- Requêtes sans `LIMIT` sur de grandes tables

### 5. Générer les seeders
```typescript
// seeds/development.ts — données de test réalistes
import { faker } from '@faker-js/faker'

export async function seed(db: PrismaClient) {
  const users = await Promise.all(
    Array.from({ length: 10 }, () =>
      db.user.create({ data: {
        email: faker.internet.email(),
        password: await bcrypt.hash('password123', 10),
        firstName: faker.person.firstName(),
      }})
    )
  )
  console.log(`✅ ${users.length} utilisateurs créés`)
}
```

## Arguments

- `/db-manage "[description]"` → génère un schéma complet depuis une description
- `/db-manage --postgres` → cible PostgreSQL (SQL + migrations)
- `/db-manage --mongo` → cible MongoDB (schémas Mongoose)
- `/db-manage --redis` → propose l'architecture Redis
- `/db-manage --prisma` → génère/met à jour le schéma Prisma
- `/db-manage optimize` → analyse et optimise les requêtes et index existants
- `/db-manage seed` → génère des données de test réalistes avec faker
- `/db-manage erd` → affiche le diagramme ERD ASCII du schéma actuel
- `/db-manage migrate "[changement]"` → génère une migration pour un changement de schéma
- `/db-manage add [table]` → ajoute une nouvelle table au schéma existant
