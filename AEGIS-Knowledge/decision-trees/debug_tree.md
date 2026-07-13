# Decision Tree — Debugging

```
Bug reported
  ├─ Reproducible? 
  │    ├─ No  → get better repro steps / add logging, stop here until yes
  │    └─ Yes → gather evidence (stack trace, logs, recent commits)
  ├─ Root cause found?
  │    ├─ No  → bisect (time or call-stack) → repeat
  │    └─ Yes → does it explain ALL symptoms?
  │              ├─ No  → keep investigating, likely more than one bug
  │              └─ Yes → write regression test → implement fix → confirm green
```
