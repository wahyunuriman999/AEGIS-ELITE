# Design Tokens & Concrete Values

Load this reference when implementing design systems, choosing colors, typography, spacing, motion values, or checking accessibility compliance.

---

## Color System

### Default Foundation: Cinematic Concrete Digital

```css
/* Foundation */
--color-black: #0a0a0a;
--color-charcoal: #1a1a1a;
--color-graphite: #2a2a2a;
--color-surface: #1e1e1e;
--color-surface-elevated: #2a2a2a;

/* Text */
--color-text: #f0f0f0;
--color-text-muted: #888888;
--color-text-subtle: #666666;

/* Accent — Primary */
--color-teal: #2dd4bf;
--color-cyan: #22d3ee;

/* Accent — Secondary */
--color-copper: #f59e0b;
--color-warm-gold: #fbbf24;

/* Semantic */
--color-success: #10b981;
--color-warning: #f59e0b;
--color-error: #ef4444;
```

### When NOT to Use Dark Foundation

| Context | Use Instead | Reason |
|---|---|---|
| Healthcare / Medical | Light neutral (white, soft gray) | Trustworthiness, readability for elderly users |
| Children / Education | Light with vibrant accents | Approachability, safety perception |
| Government / Civic | Light with high contrast | WCAG AAA compliance, universal access |
| Print-heavy / Reading | Light background, dark text | Extended reading comfort |
| Accessibility-critical | Light with 7:1+ contrast | WCAG AAA requirements |

Adapt the accent palette to the brand. The foundation darkness is a preference, not a mandate.

---

## Typography Scale

```css
/* Font Families */
--font-display: 'Inter', 'Helvetica Neue', sans-serif;
--font-body: 'Inter', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;

/* Scale (Desktop) */
--text-hero: clamp(3rem, 6vw, 5rem);    /* 48-80px */
--text-h1: clamp(2rem, 4vw, 3rem);       /* 32-48px */
--text-h2: clamp(1.5rem, 3vw, 2.25rem);  /* 24-36px */
--text-h3: 1.25rem;                       /* 20px */
--text-body: 1rem;                        /* 16px */
--text-small: 0.875rem;                   /* 14px */
--text-micro: 0.75rem;                    /* 12px */
--text-label: 0.6875rem;                  /* 11px, uppercase, tracked */

/* Line Heights */
--leading-tight: 1.1;
--leading-normal: 1.5;
--leading-relaxed: 1.7;

/* Letter Spacing */
--tracking-tight: -0.02em;
--tracking-normal: 0;
--tracking-wide: 0.05em;
--tracking-label: 0.1em;
```

---

## Spacing Scale

```css
--space-2xs: 0.25rem;   /* 4px */
--space-xs: 0.5rem;     /* 8px */
--space-sm: 0.75rem;    /* 12px */
--space-md: 1rem;       /* 16px */
--space-lg: 1.5rem;     /* 24px */
--space-xl: 2rem;       /* 32px */
--space-2xl: 3rem;      /* 48px */
--space-3xl: 4rem;      /* 64px */
--space-4xl: 6rem;      /* 96px */
--space-section: 8rem;  /* 128px */
```

---

## Motion Tokens

```css
/* Duration */
--duration-instant: 100ms;
--duration-fast: 150ms;       /* micro-interactions, hover */
--duration-normal: 300ms;     /* state transitions, reveals */
--duration-slow: 500ms;       /* section transitions */
--duration-cinematic: 800ms;  /* hero animations, page transitions */

/* Easing */
--ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
--ease-emphasis: cubic-bezier(0.0, 0, 0.2, 1);
--ease-decelerate: cubic-bezier(0.0, 0, 0.2, 1);
--ease-accelerate: cubic-bezier(0.4, 0, 1, 1);
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
```

---

## Border & Radius

```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
--radius-full: 9999px;

--border-subtle: 1px solid rgba(255, 255, 255, 0.06);
--border-default: 1px solid rgba(255, 255, 255, 0.1);
--border-strong: 1px solid rgba(255, 255, 255, 0.2);
```

---

## Accessibility Minimums

| Element | Minimum Contrast | Standard |
|---|---|---|
| Body text | 4.5:1 | WCAG AA |
| Large text (18px+ bold, 24px+ regular) | 3:1 | WCAG AA |
| UI components & icons | 3:1 | WCAG AA |
| Focus indicators | 3:1 | WCAG 2.2 |
| Touch targets | 44×44px minimum | WCAG 2.2 |

Always support: keyboard navigation, focus-visible states, reduced-motion media query, semantic HTML, screen reader labels.

---

## Shadow System

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
--shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
--shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.5);
--shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.6);
--shadow-glow-teal: 0 0 20px rgba(45, 212, 191, 0.15);
--shadow-glow-copper: 0 0 20px rgba(245, 158, 11, 0.15);
```
