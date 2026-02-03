# Example 2: Order Status (In-Memory)

## Goal

```
Where is my order A123?
```

## Outline

1) Tools are contracts, not functions
- `get_order_status(order_id)` returns a string status.

2) Agents decide, tools execute
- Agent chooses when to call `get_order_status`.

3) State is explicit and inspectable
- Keep `state["last_order_id"]` so the user can say “that one.”

4) Plans are first-class objects
- Plan: extract id → check status → respond.

5) Tools are chosen, not forced
- If no order ID, ask for it instead of calling tools.

6) Uncertainty is a valid option
- “I need an order ID to check the status.”

7) Failures are designed, not avoided
- Unknown order IDs return “Order not found.”

8) Humans stay in the loop
- Print tool usage for auditability.

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
Tool #1: get_order_status
Packed
```
