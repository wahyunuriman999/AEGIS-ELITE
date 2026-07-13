# Backup & Restore

- Automated, regular backups are non-negotiable for anything holding real data — "we'll add it later" is how data loss happens.
- Test restores periodically — an untested backup is a hypothesis, not a guarantee.
- Point-in-time recovery (via WAL/binlog) matters more than snapshot frequency for minimizing data loss window.
- Know your RPO (acceptable data loss) and RTO (acceptable downtime) targets before an incident, not during one.
