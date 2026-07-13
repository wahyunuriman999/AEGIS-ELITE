# Unit of Work Pattern

Coordinate multiple repository operations as a single atomic transaction, tracking changes and committing/rolling back them together. Prevents the situation where one repository's write succeeds and a related one silently fails, leaving inconsistent state.
