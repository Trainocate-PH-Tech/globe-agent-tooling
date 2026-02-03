# Example 7: Human-in-the-Loop Review Queue

## Narrative
This example focuses on **Humans Stay in the Loop**. The agent gathers evidence, computes a risk signal, and then **routes the decision to a human review queue**. The agent does not finalize high‑risk actions. It prepares a review packet, logs the action, and waits for a human decision.

## Goal

```
Approve a SIM swap for 09171234567
```

## Outline

1) Tools are contracts, not functions
- Evidence tools return structured data.
- Review tools return a `ticket_id` and acknowledgement.

2) Agents decide, tools execute
- The agent decides whether to escalate and which queue to use.

3) State is explicit and inspectable
- Keep `state["last_msisdn"]`, `state["plan"]`, and `state["ticket_id"]`.

4) Plans are first-class objects
- Plan includes gather → summarize → create ticket → route.

5) Tools are chosen, not forced
- If risk is low, the agent can approve without a ticket.

6) Uncertainty is a valid option
- If signals are missing, the agent escalates to human.

7) Failures are designed, not avoided
- Missing data triggers safe escalation with reason.

8) Humans stay in the loop
- The final decision is made by a human reviewer.

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
Tool #3: score_risk
Tool #4: build_review_summary
Tool #5: create_review_ticket
Tool #6: route_to_queue
Review ticket created: R-1001
```
