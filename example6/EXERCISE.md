# Exercise: Failure-First Risk Flow (Workshop)

## Scenario
Extend the failure-first risk agent so that it handles **missing files** and **partial data** with explicit fallback paths. Your goal is to make failure handling a first-class part of the agent’s plan.

## Constraints
- Follow the Agent Tooling principles from the root `README.md`.
- Keep logic simple; tools can be plain Python.
- Use Strands + OpenAI for the agent.
- The agent must not guess when data is invalid.

## Task
1. Add a new tool you design to **validate input** before scoring.
   - Example: `validate_msisdn(msisdn) -> {"ok": bool, "error": str}`
2. Update the agent so it calls the validator before any data lookup.
3. If validation fails, **escalate** with a clear reason.
4. If a data file is missing, **escalate** with a clear reason.

## Required Tools
- `get_account_profile(msisdn: str) -> {ok, data, error}`
- `get_recent_events(msisdn: str) -> {ok, data, error}`
- `score_risk(profile: dict, events: dict) -> dict`
- `escalate_to_human(reason: str) -> str`
- **Your new tool** (design it)

## Example Run
```
$ python main.py
Tool #1: validate_msisdn
Tool #2: get_account_profile
Tool #3: get_recent_events
Tool #4: escalate_to_human
Escalated to human support: recent events parse error
```

## Acceptance Checklist
- Failures are explicit and designed.
- No tool calls proceed when validation fails.
- Missing file paths produce a clear escalation.
- Tool usage is visible to humans.

---

Place your solution in `example6/solution/`.
