# Dependency Thinking

Before adding a dependency, check:
- **Necessity** — can this be done in ~20 lines without it?
- **Maintenance health** — is it actively maintained, reasonably popular, permissively licensed?
- **Blast radius** — what does it pull in transitively? Does it need network/filesystem access it shouldn't have?
- **Removal cost** — how hard would this be to rip out later if it turns out to be wrong?

Before removing a dependency, grep for every usage first — "unused" is a hypothesis, not a fact, until verified.
