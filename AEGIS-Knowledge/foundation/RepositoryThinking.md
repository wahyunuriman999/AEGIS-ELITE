# Repository Thinking

How to read an unfamiliar codebase fast, without reading every file:

1. **Entry points first** — `main`, `index`, route/handler registration, or the test suite's setup — these tell you what the system actually does, faster than any README.
2. **Follow one request/data flow end to end** before making changes anywhere.
3. **Find the seams** — where domain logic, infrastructure, and presentation are separated (or aren't — that's useful information too).
4. **Trust the tests, not the docs.** Docs go stale; a passing test suite describes current guaranteed behavior.
5. **Note the local dialect** — naming conventions, error-handling style, how they do dependency injection — and match it.
