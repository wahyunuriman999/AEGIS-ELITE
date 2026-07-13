# AEGIS Elite — Quick Start Guide
**Get value in 10 minutes. No setup required.**

---

## 1. Install

```bash
# Clone the repository
git clone https://github.com/wahyunuriman999/AEGIS-ELITE.git
cd AEGIS-ELITE

# Install dependencies
pip install -r requirements.txt   # or: pip install pyyaml
```

---

## 2. Check Your Environment

```bash
python aegis.py doctor
```

This shows the health of all Platform components: Kernel, Registry, Dispatcher, Compiler, etc.

---

## 3. Start a New Project

```bash
python aegis.py new my-api-project
```

AEGIS scaffolds a clean workspace with `.aegis/config.yaml`, `src/`, `tests/`, `docs/`, and a `README.md`.

---

## 4. Generate an Engineering Plan

```bash
python aegis.py plan "Build a production REST API with JWT authentication and rate limiting"
```

AEGIS will:
- **Classify** the task domain (code_generation, security, architecture…)
- **Score** complexity (trivial / moderate / complex / critical)
- **Route** to the optimal model (Claude 3.7 Sonnet for complex code, GPT-4o for architecture)
- **Dispatch** via the Runtime Dispatcher with full Capability Graph resolution
- **Print** a step-by-step Engineering Plan

---

## 5. Run a Task via Event Bus

```bash
python aegis.py run "Implement the authentication middleware"
```

Watch the AEGIS Event Bus fire in real-time:
```
⚡ TASK_RECEIVED       → Ingesting intent
⚡ INTENT_ANALYZED     → AST mapped
⚡ RISK_CHECK          → Blast Radius: LOW
⚡ CAPABILITY_RESOLVED → Claude 3.7 Sonnet selected
⚡ CODE_GENERATED      → Implementation complete
⚡ AUDIT_PASSED        → Security score: 98
⚡ CONSENSUS_REACHED   → Council APPROVED
⚡ MEMORY_SAVED        → ADR-101 committed
```

---

## 6. Audit Your Codebase

```bash
python aegis.py review .
```

Runs a full AEGIS Governance Audit: security, architecture patterns, technical debt.

---

## 7. Platform Status Dashboard

```bash
python aegis.py status
```

Shows live status of the **Capability Graph** (all 10 capabilities), **Engine Registry** (lifecycle, health, metrics).

---

## 8. Full Command Reference

| Command | Description |
|---|---|
| `aegis new <name>` | Scaffold new AEGIS-managed project |
| `aegis plan "<task>"` | Generate engineering plan via Model Router |
| `aegis run "<task>"` | Execute task via Event Bus |
| `aegis review [path]` | Deep Governance Audit |
| `aegis scan [path]` | Quick vulnerability scan |
| `aegis status` | Live platform dashboard |
| `aegis doctor` | Environment health check |
| `aegis benchmark` | Run AI benchmark suite |
| `aegis quickstart` | 60-second interactive onboarding |
| `aegis studio` | Open Studio UI dashboard |
| `aegis marketplace` | Browse extension packs |
| `aegis install <pack>` | Install an extension pack |
| `aegis install-hooks` | Install as git pre-commit hook |

---

## Architecture at a Glance

```
User Task (CLI)
     ↓
Runtime Dispatcher
     ↓
Capability Graph ←→ Engine Registry (SSOT)
     ↓
Model Router (selects optimal LLM)
     ↓
Provider (Claude / GPT-4o / Gemini / Ollama)
     ↓
AEGIS Governance → AEGIS Consensus (if critical)
     ↓
AEGIS Memory (ADR committed)
     ↓
Event Bus (publishes completion event)
```

---

> **AEGIS Elite** is built by [Wahyu Nur Iman](https://github.com/wahyunuriman999).
> Copyright (c) 2024-2026. Proprietary and Confidential. All rights reserved.
