# Example 4: Multi-Path Help Desk (In-Memory)

## Narrative
This example simulates a tiny help desk that can route a user’s request to either billing or technical support, or escalate to a human when unsure. It is more complex than previous examples because the agent must choose between multiple tools and paths based on classification, while keeping state and plan explicit.

## Goal

```
I was charged twice on my last invoice
```

## Outline

1) Tools are contracts, not functions
- `classify_issue(text)` returns `billing`, `technical`, or `unknown`.
- `lookup_invoice(account_id)` returns a billing status.
- `check_system_status(service)` returns system health.
- `escalate_to_human(reason)` returns a handoff message.

2) Agents decide, tools execute
- The agent chooses the route based on classification.

3) State is explicit and inspectable
- Keep `state["issue_type"]`, `state["last_account_id"]`, and `state["plan"]`.

4) Plans are first-class objects
- Plan includes classify → route → resolve or escalate.

5) Tools are chosen, not forced
- Only call the tool that matches the route.

6) Uncertainty is a valid option
- `unknown` routes to `escalate_to_human`.

7) Failures are designed, not avoided
- Missing account IDs or unknown invoices return safe messages.

8) Humans stay in the loop
- Tool usage is logged for auditability.

---

## Simple Example

Files:
- `agent.py`
- `tools.py`
- `main.py`

Run:
```
python main.py
```

Expected output (example):
```
Tool #1: classify_issue
Tool #2: lookup_invoice
We found your invoice. Status: Duplicate charge flagged.
```
