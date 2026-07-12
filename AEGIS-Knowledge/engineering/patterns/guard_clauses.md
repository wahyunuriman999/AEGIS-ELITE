# Guard Clauses

Reduce nesting by returning/throwing early on invalid or edge conditions, instead of wrapping the "normal" path in nested `if`.

```
// instead of:
if (user) { if (user.active) { if (order) { ...deeply nested... } } }

// prefer:
if (!user) return error("no user");
if (!user.active) return error("inactive");
if (!order) return error("no order");
...flat happy path...
```
