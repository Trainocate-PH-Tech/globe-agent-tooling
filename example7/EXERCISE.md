# Exercise: Human-in-the-Loop Review Packet (Workshop)

## Scenario
Extend the review agent so it always produces a structured review packet **and** logs it for audit, even if the action is approved. The human reviewer can later inspect the packet if needed.

## Constraints
- Follow the Agent Tooling principles from the root `README.md`.
- Keep logic simple; tools can be plain Python.
- Use Strands + OpenAI for the agent.
- The agent must not finalize high‑risk actions without a review ticket.

## Task
1. Add a new tool you design:
   - `append_audit_log(packet: dict) -> str`
2. Update the agent to always call `build_review_summary` and `append_audit_log`.
3. If risk is high or unknown, create and route a ticket.
4. If risk is low or medium, approve but still log the review packet.

## Required Tools
- `get_account_profile(msisdn: str) -> dict`
- `get_recent_events(msisdn: str) -> dict`
- `score_risk(profile: dict, events: dict) -> dict`
- `build_review_summary(msisdn: str, profile: dict, events: dict, risk: dict) -> dict`
- `create_review_ticket(payload: dict) -> str`
- `route_to_queue(queue_name: str, ticket_id: str) -> str`
- **Your new tool** `append_audit_log(packet: dict) -> str`

## Example Run
```
$ python main.py
Tool #1: get_account_profile
Tool #2: get_recent_events
Tool #3: score_risk
Tool #4: build_review_summary
Tool #5: append_audit_log
Tool #6: create_review_ticket
Tool #7: route_to_queue
Review ticket created: R-1001
```

## Acceptance Checklist
- Humans stay in the loop by default.
- Audit logs are always written.
- High/unknown risk creates a review ticket.
- Tool usage is visible to humans.

---

Place your solution in `example7/solution/`.
