# Skill: /web-design

Crée des composants UI, maquettes et systèmes de design pour le web.
Utilise le MCP Figma quand disponible, sinon génère du code HTML/CSS/React directement.

## Comportement par défaut

Quand l'utilisateur tape `/web-design` sans argument :
- Demander : "Que souhaitez-vous créer ? (composant, page, système de design)"
- Détecter le framework du projet (React, Vue, HTML pur, Next.js)
- Détecter si Tailwind, styled-components, ou CSS modules est utilisé
- Générer le composant dans le style du projet existant

## Étapes d'exécution

### 1. Détecter le contexte du projet
```bash
cat package.json | grep -E '"react"|"vue"|"tailwind"|"styled-components"|"next"'
ls src/components/ 2>/dev/null | head -5  # analyser les composants existants pour le style
```

### 2. Si une URL Figma est fournie
Utiliser le MCP Figma (`get_design_context`, `get_screenshot`) pour :
- Lire les dimensions, couleurs, typographie, espacements exacts
- Extraire les tokens de design (variables CSS ou Tailwind config)
- Générer le code pixel-perfect

### 3. Si une description est fournie
Générer le composant complet :
- HTML sémantique (balises correctes : `<nav>`, `<main>`, `<article>`, etc.)
- CSS responsive (mobile-first, breakpoints : 375px, 768px, 1024px, 1280px)
- Accessibilité : attributs ARIA, contraste WCAG AA (ratio 4.5:1 minimum), focus visible
- États interactifs : hover, focus, active, disabled, loading

### 4. Proposer des variantes
Toujours proposer 2-3 options de style :
- Minimaliste (blanc, gris, beaucoup d'espace)
- Moderne (couleurs vives, gradients, ombres prononcées)
- Corporate (sobre, professionnel, couleurs neutres)

## Composants disponibles

### Composants de base
- `Button` — variantes: primary, secondary, ghost, danger + tailles sm/md/lg
- `Input` — text, email, password, textarea + états: error, success, disabled
- `Card` — product card, article card, stats card, pricing card
- `Modal` — avec overlay, animation d'entrée, focus trap
- `Dropdown` — menu déroulant accessible au clavier
- `Toast` — notifications success/error/warning/info

### Sections de page
- `Navbar` — responsive avec menu hamburger mobile
- `Hero` — avec CTA, image, gradient background
- `Features` — grille de features avec icônes
- `Pricing` — tableau comparatif de prix
- `Testimonials` — carrousel d'avis
- `Footer` — avec liens, réseaux sociaux, newsletter
- `Dashboard` — layout avec sidebar, header, main content

### Pages complètes
- Landing page SaaS
- Page de connexion / inscription
- Page de profil utilisateur
- Page 404
- Page de checkout e-commerce

## Exemple de sortie (React + Tailwind)

```tsx
// Button.tsx — généré par /web-design
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  disabled?: boolean
  children: React.ReactNode
  onClick?: () => void
}

const variants = {
  primary: 'bg-indigo-600 hover:bg-indigo-700 text-white',
  secondary: 'bg-white hover:bg-gray-50 text-gray-900 border border-gray-300',
  ghost: 'hover:bg-gray-100 text-gray-700',
  danger: 'bg-red-600 hover:bg-red-700 text-white',
}
const sizes = { sm: 'px-3 py-1.5 text-sm', md: 'px-4 py-2 text-base', lg: 'px-6 py-3 text-lg' }

export function Button({ variant = 'primary', size = 'md', loading, disabled, children, onClick }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      aria-busy={loading}
      className={`inline-flex items-center gap-2 rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed ${variants[variant]} ${sizes[size]}`}
    >
      {loading && <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" aria-hidden />}
      {children}
    </button>
  )
}
```

## Arguments

- `/web-design [description]` → génère un composant depuis une description
- `/web-design figma [url]` → convertit un design Figma en code
- `/web-design page [nom]` → génère une page complète (landing, login, dashboard…)
- `/web-design --framework react` → force React + Tailwind
- `/web-design --framework vue` → génère en Vue 3 + CSS Modules
- `/web-design --framework html` → génère en HTML/CSS pur sans framework
- `/web-design --dark-mode` → ajoute le support dark mode complet
- `/web-design audit` → audite les composants existants (accessibilité, cohérence, responsive)
- `/web-design tokens` → génère/met à jour le système de tokens de design du projet
