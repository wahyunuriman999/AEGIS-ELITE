# Learning Engine (Evolution & Memory)

## The Reflection & Evolution Loop
After the task is completed and the user has provided feedback (or a bug is discovered), the Learning Engine is activated.

1. **Log Failure**: If the solution failed or caused a regression, append the incident to `FAILURE_DB.json`.
2. **Extract Lesson**: Convert the failure into a new architectural Rule.
3. **Update Genome**: Adjust the `score` and `success_rate` of the responsible node in `knowledge.graph.json`. Decrease the score for failures.
4. **Persistent Memory**: Ensure that future instances of the Planner read this new memory.
