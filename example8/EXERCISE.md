# Exercise: API Failure Handling + Failure Report (Workshop)

## Scenario
Extend the fraud agent so that when the API call fails, it writes a **failure report file** with the reason and MSISDN. This makes failures visible and auditable.

## Constraints
- Follow the Agent Tooling principles from the root `README.md`.
- Keep logic simple; tools can be plain Python.
- Use Strands + OpenAI for the agent.
- The agent must not update records if the API call fails.

## Task
1. Add a new tool you design:
   - `write_failure_report(msisdn: str, reason: str) -> str`
2. Update the agent prompt so it **must call** this tool on API failure.
3. Keep escalation to human as well.

## Required Tools
- `call_fraud_api(msisdn: str) -> {ok, data, error}`
- `update_case_record(msisdn: str, status: str) -> str`
- `escalate_to_human(reason: str) -> str`
- **Your new tool** `write_failure_report(msisdn: str, reason: str) -> str`

## Example Run
```
$ python main.py
Tool #1: call_fraud_api
Tool #2: write_failure_report
Tool #3: escalate_to_human
Escalated to human support: timeout
```

## Acceptance Checklist
- Failures create a report file.
- No record updates on API failure.
- Tool usage is visible to humans.

---

Place your solution in `example8/solution/`.
