# Example 5: Globe PH Risk Scoring (In-Memory)

## Narrative
This example simulates a simple risk management flow for Globe PH account actions (e.g., SIM swap or high‑value load transfer). The agent reads account signals from files, computes a risk score, and decides whether to allow the action or escalate to a human reviewer.

## Goal

```
Please approve a SIM swap for 09171234567
```

## Outline

1) Tools are contracts, not functions
- `get_account_profile(msisdn)` returns `{region, tenure_months, kyc_level}`.
- `get_recent_events(msisdn)` returns `{last_sim_swap_days, device_change_days, failed_logins_24h}`.
- `score_risk(profile, events)` returns `{score, band}`.
- `escalate_to_human(reason)` returns a handoff string.

2) Agents decide, tools execute
- The agent chooses which tools to call and when to escalate.

3) State is explicit and inspectable
- Keep `state["last_msisdn"]` and `state["plan"]`.

4) Plans are first-class objects
- Plan: fetch profile → fetch events → score risk → decide.

5) Tools are chosen, not forced
- If MSISDN missing, ask for it before calling tools.

6) Uncertainty is a valid option
- If profile is missing, return a safe request for verification.

7) Failures are designed, not avoided
- Unknown MSISDN returns a safe message rather than guessing.

8) Humans stay in the loop
- High risk routes to human escalation and tool usage is logged.

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
Escalated to human support: High risk (score 85) for SIM swap.
```
