# Exercise: Risk Scoring with a New Signal Tool (Workshop)

## Scenario
Extend the Globe PH risk scoring agent with a new signal. If a user requests a high‑risk action, the agent should call an additional tool you design to fetch a new signal, then incorporate it into the decision.

## Constraints
- Follow the Agent Tooling principles from the root `README.md`.
- Keep logic simple; tools can be plain Python.
- Use Strands + OpenAI for the agent.
- The agent must use tools for scoring and escalation.

## Task
1. Add a new tool you design, such as:
   - `get_network_risk(msisdn) -> {"network_risk": "low|medium|high"}`
   - OR `get_geolocation_risk(msisdn) -> {"geo_risk": "low|medium|high"}`
2. Update the agent prompt so it **must call your new tool** before scoring.
3. Modify the scoring so your new signal can raise or lower the band.

## Required Tools
- `get_account_profile(msisdn: str) -> dict` (file-based)
- `get_recent_events(msisdn: str) -> dict` (file-based)
- `score_risk(profile: dict, events: dict, extra: dict) -> dict`
- `escalate_to_human(reason: str) -> str`
- **Your new tool** (design it; file-based or in-memory is fine)

## Example Run
```
$ python main.py
Tool #1: get_account_profile
Tool #2: get_recent_events
Tool #3: get_network_risk
Tool #4: score_risk
Escalated to human support: High risk (score 90) for SIM swap.
```

## Acceptance Checklist
- Tools are explicit and used as contracts.
- The agent decides which tools to call.
- No hidden state; any state is in a visible object or variable.
- The plan includes the new signal.
- The agent handles missing data safely.
- Tool usage is visible to humans.

---

Place your solution in `example5/solution/`.
