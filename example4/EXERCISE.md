# Exercise: Help Desk Router with a Missing-ID Tool (Workshop)

## Scenario
Extend the help desk agent so that if a billing issue is detected but the user did not provide an account ID, the agent must call a helper tool to obtain one, then proceed with `lookup_invoice`.

## Constraints
- Follow the Agent Tooling principles from the root `README.md`.
- Keep logic simple; tools can be plain Python.
- Use Strands + OpenAI for the agent.
- The agent must use tools for classification and billing lookup.

## Task
1. If the user says: `I was charged twice on my last invoice` (no account ID)
   - Call `classify_issue(text)`.
   - Because it is billing, call a **new tool you design** to obtain an account ID.
   - Then call `lookup_invoice(account_id)`.
2. If the user says: `Login keeps failing`
   - Route to `check_system_status(service)`.
3. If the issue is unknown
   - Call `escalate_to_human(reason)`.

## Required Tools
- `classify_issue(text: str) -> str`
- `lookup_invoice(account_id: str) -> str`
- `check_system_status(service: str) -> str`
- `escalate_to_human(reason: str) -> str`

## Your Design Choice (Required)
Create **one additional tool** that helps resolve missing account IDs. Keep it simple (e.g., return a default ID or parse from a file).

## Example Run
```
$ python main.py
Tool #1: classify_issue
Tool #2: get_account_id
Tool #3: lookup_invoice
We found your invoice. Status: Duplicate charge flagged.
```

## Acceptance Checklist
- Tools are explicit and used as contracts.
- The agent decides which tools to call.
- No hidden state; any state is in a visible object or variable.
- The plan (classify → route → resolve/escalate) is clear in behavior.
- The agent handles missing IDs safely via your new tool.
- Tool usage is visible to humans.

---

Place your solution in `example4/solution/`.
