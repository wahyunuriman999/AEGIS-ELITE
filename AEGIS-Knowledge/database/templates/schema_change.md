# Schema Change Template

**Change:** what's being added/modified/removed.

**Migration Plan:** additive-first steps (nullable → backfill → constrain), or explicit reason it's a single-step breaking change.

**Rollback Plan:** the reverse migration, or why one isn't possible.

**Query Impact:** which existing queries/indexes are affected.

**Risk:** Low / Medium / High, per `foundation/Risk.md` signals.
