# Example 3: Mini Trip Planner (In-Memory)

## Goal

```
Plan a short visit in Kyoto
```

## Outline

1) Tools are contracts, not functions
- `list_attractions(city)` and `get_hours(place)` return specific data shapes.

2) Agents decide, tools execute
- Agent selects which tool to call and in what order.

3) State is explicit and inspectable
- Keep `state["last_city"]` and `state["plan"]`.

4) Plans are first-class objects
- The plan is a visible list of steps.

5) Tools are chosen, not forced
- If the user already names a place, skip `list_attractions`.

6) Uncertainty is a valid option
- Ask for the city if missing.

7) Failures are designed, not avoided
- If the city is unknown, return a safe message.

8) Humans stay in the loop
- Tool usage is printed for auditability.

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
Tool #1: list_attractions
Tool #2: get_hours
Tool #3: get_hours
{"city": "Kyoto", "stops": [{"name": "Fushimi Inari", "hours": "Always open"}, {"name": "Kiyomizu-dera", "hours": "6:00-18:00"}]}
```
