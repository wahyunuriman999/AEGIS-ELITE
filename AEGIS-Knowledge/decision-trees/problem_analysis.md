# Decision Tree — Problem Analysis

```
Problem reported
  ├─ Can you reproduce it? 
  │    ├─ No  → gather more evidence (logs, repro steps) before touching code
  │    └─ Yes → isolate root cause (Engine 3: Symptom → Evidence → Root Cause → Fix → Regression Check)
  ├─ Is it a symptom of a known anti-pattern? → fix the pattern, not just the instance
  ├─ Does the fix touch a shared/public contract? → escalate risk tier, check Compatibility (Engine 11)
  └─ Multiple valid fixes? → run Decision Engine, priority order applies
```
