# Skill: /security-scan

Analyse les vulnérabilités de sécurité du projet en appliquant les règles OWASP Top 10, Snyk et Checkmarx.

## Ce que fait ce skill

1. **Scanne les dépendances** pour des CVE connues (équivalent Snyk/Dependabot)
2. **Analyse le code** pour détecter les OWASP Top 10 :
   - Injection SQL / NoSQL / Command
   - XSS (Cross-Site Scripting)
   - CSRF, SSRF
   - Authentification/session mal configurée
   - Exposition de données sensibles (tokens, mots de passe en clair)
   - Mauvaise configuration de sécurité
3. **Vérifie les variables d'environnement** et fichiers de config (pas de secrets exposés)
4. **Priorise les vulnérabilités** par sévérité : CRITICAL / HIGH / MEDIUM / LOW
5. **Propose des corrections** avec du code concret pour chaque vulnérabilité

## Instructions

Quand l'utilisateur invoque `/security-scan` :

- Scanner d'abord le `package.json` / `requirements.txt` / `go.mod` pour les dépendances vulnérables
- Analyser le code source pour les patterns dangereux
- Vérifier les fichiers `.env`, configs, et tout secret potentiel
- Ne jamais afficher de secrets réels dans le rapport — les masquer avec `***`
- Classer les résultats par sévérité décroissante

## Format du rapport

```
RAPPORT DE SÉCURITÉ — 2026-05-22
================================
CRITICAL (1)
  [DEP] lodash@4.17.20 — CVE-2021-23337: Prototype Pollution
  → Mettre à jour vers lodash@4.17.21

HIGH (2)
  [CODE] src/api/users.js:45 — Injection SQL possible
  → Utiliser des requêtes paramétrées : db.query('SELECT * FROM users WHERE id = ?', [id])

  [CODE] src/auth/login.js:23 — Mot de passe comparé sans bcrypt
  → Utiliser bcrypt.compare() au lieu de ===

MEDIUM (1)
  [CONFIG] .env.example expose une clé API réelle
  → Remplacer par un placeholder : API_KEY=your_api_key_here
```

## Arguments optionnels

- `/security-scan --deps` → analyse uniquement les dépendances
- `/security-scan --code` → analyse uniquement le code source
- `/security-scan --owasp` → rapport orienté OWASP Top 10
- `/security-scan --fix` → applique les corrections automatiques disponibles
- `/security-scan --ci` → mode CI/CD, retourne un code d'erreur si CRITICAL trouvé
