# Architecture Thinking

Before proposing any structural change, ask:
- What pattern does this codebase already follow? (Don't introduce a second one — see `architecture/`.)
- Is this a *local* problem (fits inside one module) or a *structural* one (needs a boundary to move)? Most requests are local; treat structural change as the expensive option it is.
- What's the blast radius if this abstraction is wrong? Prefer deferring an abstraction until the second or third use case makes the right shape obvious ("rule of three").
