# Accessibility & Design System Discipline

Baseline (non-negotiable, applies to every interactive component):
1. **Semantic HTML first** — `<button>` not `<div onClick>`, `<nav>`/`<main>`/`<header>` over
   generic `<div>`. Semantic elements give keyboard/focus/screen-reader behavior for free.
2. **Keyboard navigation** — every interactive element reachable and operable via Tab/Enter/
   Space/Arrow keys, with a visible focus ring. If a click handler exists, a keyboard path must
   exist too.
3. **ARIA only when semantic HTML can't express the state** (`aria-expanded`, `aria-live` for
   dynamic regions, `aria-label` for icon-only buttons). ARIA on top of already-semantic
   elements is noise, not safety.
4. **Color contrast** — 4.5:1 for body text, 3:1 for large text/UI components (WCAG AA). Never
   convey state (error, disabled, required) through color alone.
5. **Focus management on route/modal change** — moving focus to the new content on
   navigation or dialog open is what makes an SPA usable with a screen reader.

Design-system consistency (see `daisyui.md` for the token/theme specifics in this workspace):
use theme tokens for color/spacing/radius, never hardcode hex values or pixel magic numbers in
component code — it's how a rebrand becomes a one-line token change instead of a grep-and-replace
across hundreds of files.
