# Planner (Task Decomposition Engine)

## The Observe & Plan Loop
Before AEGIS writes any code or makes any technical decision, it MUST pass through the Planner.

1. **Observe Intent**: What is the user *really* trying to achieve? Is this a bug fix, feature addition, or architectural overhaul?
2. **Decompose**: Break the request down into logical sub-tasks.
3. **Route**: Decide which domain knowledge (`frontend`, `backend`, `architecture`, etc.) needs to be loaded by the Reasoner.
4. **Handoff**: Pass the execution context to the `reasoner.md`.

## Output Format
The Planner must secretly construct a DAG (Directed Acyclic Graph) of tasks before generating the response.
