# Architecture Review

Checklist mindset when reviewing a structural proposal:
- Does it match a pattern the team already understands, or does it require new shared knowledge?
- Where are the boundaries, and what crosses them (data, calls, events)? Fewer, well-defined crossings beat many implicit ones.
- What's the cost to change this decision later? If high, get more signoff/evidence before committing.
- Does it solve a problem that exists today, or one anticipated for the future ("YAGNI" check)?
