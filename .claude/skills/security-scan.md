# Skill: /security-scan

Analyse les vulnérabilités de sécurité du projet : dépendances, code source, configuration.

## Comportement par défaut

Quand l'utilisateur tape `/security-scan` sans argument :
1. Scanner les dépendances pour des CVE connues
2. Analyser le code source pour les patterns OWASP Top 10
3. Vérifier les fichiers de configuration et secrets exposés
4. Afficher le rapport classé par sévérité

## Étapes d'exécution

### 1. Scanner les dépendances
```bash
npm audit --json 2>/dev/null || pip-audit 2>/dev/null || bundle audit 2>/dev/null
cat package.json | grep -E '"dependencies"|"devDependencies"' -A 100
```

Comparer les versions avec les CVE connues majeures :
- `lodash < 4.17.21` → Prototype Pollution (CVE-2021-23337)
- `axios < 1.6.0` → SSRF (CVE-2023-45857)
- `express < 4.19.0` → Open Redirect (CVE-2024-29041)
- `jsonwebtoken < 9.0.0` → Algorithme "none" accepté (CVE-2022-23529)
- `multer < 1.4.5-lts.1` → Path Traversal (CVE-2022-24434)

### 2. Détecter les patterns OWASP Top 10 dans le code

#### A1 - Injection
```regex
# SQL Injection — rechercher les concaténations de requêtes
"SELECT.*\+.*req\." | "query\(.*\$\{" | "WHERE id = " + variable

# Command Injection
exec\(.*req\. | spawn\(.*req\. | eval\(.*req\.
```

#### A2 - Authentification cassée
```regex
# Tokens JWT sans expiration
jwt\.sign\([^,]+,[^,]+\)  # manque { expiresIn }
# Mots de passe comparés en clair
password === req.body.password | password == userInput
# Secrets en dur
(secret|password|key)\s*=\s*["'][^"']{8,}["']
```

#### A3 - Exposition de données sensibles
```regex
# Clés API / tokens exposés dans le code
(api_key|apikey|API_KEY|token|secret)\s*[:=]\s*["'][a-zA-Z0-9]{16,}["']
# Données sensibles dans les logs
console\.log.*password | console\.log.*token
# Chiffrement faible
crypto\.createHash\(['"]md5['"] | crypto\.createHash\(['"]sha1['"]
```

#### A5 - Mauvaise configuration de sécurité
```regex
# CORS ouvert
origin: ['"]?\*['"]? | Access-Control-Allow-Origin: *
# Headers de sécurité manquants (vérifier si helmet.js est utilisé)
# Debug mode en production
DEBUG=true | NODE_ENV !== 'production'
```

#### A7 - XSS
```regex
# Injection HTML non sanitisée
innerHTML\s*= | dangerouslySetInnerHTML | document\.write\(
res\.send\(.*req\. | res\.json\(.*req\.body
```

#### A8 - Désérialisation
```regex
JSON\.parse\(req\. | eval\(.*JSON | unserialize\(
```

### 3. Vérifier les secrets exposés
Rechercher dans TOUS les fichiers (y compris .env.example, configs) :
```
- Clés AWS : AKIA[0-9A-Z]{16}
- Tokens GitHub : ghp_[a-zA-Z0-9]{36}
- Clés Stripe : sk_live_[a-zA-Z0-9]{24}
- JWT secrets évidents : "secret", "password", "changeme", "1234"
- Mots de passe en dur dans les fichiers de config
```

### 4. Vérifier .gitignore
S'assurer que `.env`, `*.pem`, `*.key`, `credentials.json` sont bien ignorés.

## Format du rapport

```
╔══════════════════════════════════════════════════╗
║         RAPPORT SÉCURITÉ — 2026-05-22            ║
╚══════════════════════════════════════════════════╝

🔴 CRITICAL (1)
  [DEP] lodash@4.17.20
  CVE-2021-23337 — Prototype Pollution
  Fix: npm install lodash@^4.17.21

🟠 HIGH (2)
  [CODE] src/api/users.js:45
  Injection SQL — concaténation directe dans la requête
  Code:    db.query('SELECT * FROM users WHERE id = ' + req.params.id)
  Fix:     db.query('SELECT * FROM users WHERE id = ?', [req.params.id])

  [CODE] src/auth/login.js:23
  Comparaison de mot de passe en clair (pas de bcrypt)
  Fix:     await bcrypt.compare(password, user.hashedPassword)

🟡 MEDIUM (1)
  [CONFIG] .env.example
  Clé API réelle exposée (ligne 8)
  Fix:     Remplacer par: STRIPE_KEY=sk_live_VOTRE_CLE_ICI

ℹ️  INFO (2)
  [CODE] CORS ouvert sur toutes les origines (src/app.js:12)
  [CODE] 3 console.log avec données utilisateur (src/auth/)

────────────────────────────────────────────────────
Score sécurité: 6/10 | 1 CRITICAL · 2 HIGH · 1 MEDIUM · 2 INFO
```

## Arguments

- `/security-scan --deps` → analyse uniquement les dépendances
- `/security-scan --code` → analyse uniquement le code source
- `/security-scan --secrets` → recherche uniquement les secrets exposés
- `/security-scan --owasp` → rapport structuré par catégorie OWASP
- `/security-scan --fix` → applique les corrections automatiques disponibles
- `/security-scan --ci` → mode CI/CD, exit code 1 si CRITICAL ou HIGH trouvé
