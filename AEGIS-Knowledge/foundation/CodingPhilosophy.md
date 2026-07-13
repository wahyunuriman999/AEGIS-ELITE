# Coding Philosophy

- **Readable over clever.** Code is read far more often than written; optimize for the reader.
- **Explicit over implicit.** Magic behavior (implicit type coercion, hidden side effects, "clever" metaprogramming) costs more than it saves.
- **Boring is a feature.** Reach for the well-understood solution before the novel one.
- **Small diffs compound.** A change that's easy to review is a change that's easy to trust; a 2000-line diff is a change nobody actually reviewed.
- **Delete more than you add, when you can.** Every line is a maintenance liability.
- **Match the codebase, don't fight it.** Local convention beats personal preference, even when personal preference is "more correct" in the abstract.
