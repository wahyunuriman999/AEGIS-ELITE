# Frontend Performance

Fix in this order — each earlier item dwarfs the impact of the ones below it:

1. **Bundle size** — code-split by route, lazy-load anything below the fold or behind an
   interaction. A 2MB bundle costs more on a mid-range phone than any render optimization
   below can claw back.
2. **Render count** — a component re-rendering because a parent re-rendered (not because its
   own props changed) is the default failure mode in prop/context-heavy trees. Memoize the
   expensive subtree, not everything.
3. **Main-thread blocking** — long synchronous work (large list rendering, heavy computation)
   blocks input. Virtualize long lists; move heavy computation off the main thread (worker) or
   defer it.
4. **Image weight** — serve responsive/compressed images with explicit width/height (prevents
   layout shift) before reaching for JS-level fixes.
5. **Network waterfall** — parallelize independent requests, prefetch on hover/intent for
   likely next navigations.

Measure before optimizing: a profiler flame graph or Lighthouse trace, not intuition — this is
`engineering/Performance.md`'s "evidence before action" invariant applied to the browser.
