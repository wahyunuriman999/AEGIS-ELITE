# AEGIS Cognitive Scheduler

The Scheduler is responsible for determining the execution order of sub-routines and agents within the Virtual Machine.

## Execution Tiers
1. **Tier 1 (Kernel Interrupts)**: User overrides and `PRECEDENCE.md` rules. These execute instantly and override all other cognition.
2. **Tier 2 (Cognitive Pipeline)**: Execution of the ISA sequence (`OBSERVE` -> `VALIDATE`).
3. **Tier 3 (Agent Threading)**: 
   - `security_agent.md` always runs FIRST during the `DEBATE` phase.
   - `architecture_agent.md` runs SECOND.
   - `performance_agent.md` runs LAST to optimize the secure and scalable foundation.
4. **Tier 4 (Background Reflection)**: Updates to `FAILURE_DB.json` and Genome Mutation happen AFTER the response is generated.
