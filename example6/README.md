# Example 6: Failure-First Risk Checks (File-Based)

## Narrative
This example follows Example 5 but centers on **Failures are Designed, Not Avoided**. The agent expects messy data, missing files, or parsing errors and responds with safe, explicit outcomes instead of guessing.

## Goal

```
Please approve a SIM swap for 09189999999
```

## Outline

1) Tools are contracts, not functions
- Tools return a **success flag** and **error message** when they fail.

2) Agents decide, tools execute
- Agent chooses whether to continue or stop based on tool results.

3) State is explicit and inspectable
- Keep `state["last_msisdn"]` and `state["plan"]`.

4) Plans are first-class objects
- Plan includes validation and fallback handling.

5) Tools are chosen, not forced
- If a tool fails, the agent does not continue blindly.

6) Uncertainty is a valid option
- The agent can request manual verification when data is incomplete.

7) Failures are designed, not avoided
- Bad rows, missing files, and parse errors are handled intentionally.

8) Humans stay in the loop
- Escalation occurs with a clear reason.

---

## Simple Example

Files:
- `agent.py`
- `tools.py`
- `main.py`
- `data/account_profiles.txt`
- `data/recent_events.txt`

Run:
```
python main.py
```

Expected output (example):
```
Tool #1: get_account_profile
Tool #2: get_recent_events
Tool #3: escalate_to_human
Escalated to human support: Risk data invalid or incomplete for MSISDN 09189999999.
```
