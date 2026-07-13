# AEGIS Cognitive BIOS (Pre-Boot Sequence)

Before AEGIS can execute any command, the Cognitive BIOS MUST run to ensure system integrity.

## Boot Checks
1. **Integrity Check**: Verify that `AEGIS-Kernel`, `AEGIS-Compiler`, `AEGIS-Runtime`, `AEGIS-Knowledge`, and `AEGIS-SDK` packages exist.
2. **Knowledge Graph Check**: Verify that `AEGIS-Knowledge/knowledge.graph.json` is healthy.
3. **Memory Load**: Mount L0, L1, L2, L3, L4 memory modules into the Runtime Image.
4. **Runtime Ready**: Emit `EVENT_BOOT_SUCCESS` and transition state to `IDLE`.

*If any check fails, the system PANICS and reverts to the last known good compilation.*
