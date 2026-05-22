# Skill: /web-design

Crée des composants UI, maquettes et systèmes de design pour le web, avec intégration Figma et génération de code CSS/HTML/React.

## Ce que fait ce skill

1. **Génère des composants UI** (boutons, cards, formulaires, nav, hero sections, etc.)
2. **Crée des mises en page** responsive (mobile-first, grid, flexbox)
3. **Synchronise avec Figma** via le MCP Figma pour lire ou pousser des designs
4. **Génère des tokens de design** (couleurs, typographie, espacements, ombres)
5. **Propose des variantes de design** (dark mode, thèmes, états hover/focus/disabled)
6. **Exporte le code** en HTML/CSS, React/Tailwind, Vue, ou CSS pur

## Instructions

Quand l'utilisateur invoque `/web-design` :

- Si une URL Figma est fournie → lire le design et le convertir en code
- Si une description est fournie → générer le composant depuis zéro
- Si un composant existant est fourni → l'analyser et proposer des améliorations visuelles
- Toujours générer du code accessible (ARIA, contraste WCAG AA minimum)
- Proposer 2-3 variantes de style quand possible

## Exemples de ce que ce skill peut créer

### Composants
- Hero section avec CTA
- Navbar responsive avec menu hamburger
- Cards produits / articles
- Formulaires de contact / login
- Tableaux de données avec filtres
- Dashboards avec graphiques
- Landing pages complètes

### Systèmes de design
```css
:root {
  --color-primary: #6366f1;
  --color-secondary: #8b5cf6;
  --font-heading: 'Inter', sans-serif;
  --spacing-unit: 8px;
  --radius-md: 8px;
  --shadow-card: 0 4px 24px rgba(0,0,0,0.08);
}
```

## Arguments optionnels

- `/web-design hero "SaaS landing page moderne"` → génère une hero section
- `/web-design figma https://figma.com/...` → convertit un design Figma en code
- `/web-design component Button --variants` → génère un composant avec toutes ses variantes
- `/web-design --framework react` → génère en React + Tailwind
- `/web-design --framework vue` → génère en Vue + CSS Modules
- `/web-design --dark-mode` → ajoute le support dark mode
- `/web-design audit` → audite l'UI existante (accessibilité, contraste, cohérence)
