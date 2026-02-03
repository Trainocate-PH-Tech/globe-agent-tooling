# Example 8: Mock API Call + Record Update (Failure-First)

## Narrative
This example simulates a realistic **API call** that can fail (timeout, 500). The agent must handle failures explicitly and only update records when the API call succeeds. This shows **Failures are Designed, Not Avoided** while still taking a real action (updating a case record file).

## Goal

```
Check fraud risk for 09171234567 and update the case record
```

## Outline

1) Tools are contracts, not functions
- API tool returns `{ok, data, error}`.

2) Agents decide, tools execute
- Agent decides whether to update a record based on API success.

3) State is explicit and inspectable
- Keep `state["last_msisdn"]` and `state["plan"]`.

4) Plans are first-class objects
- Plan: call API → validate → update record or escalate.

5) Tools are chosen, not forced
- No update tool call if API fails.

6) Uncertainty is a valid option
- Missing data routes to escalation.

7) Failures are designed, not avoided
- Tool returns explicit failure reasons.

8) Humans stay in the loop
- On failure, the agent escalates with a clear reason.

---

## Simple Example

Files:
- `agent.py`
- `tools.py`
- `main.py`
- `api.py`
- `data/mock_api.txt`
- `data/case_records.txt`

Run:
```
python main.py
```

Optional: run the mock API backend
```
python api.py
```

Expected output (example):
```
Tool #1: call_fraud_api
Tool #2: update_case_record
Case updated: FRAUD_REVIEW
```
