# Exercise: Order Status with Fallback Name (Workshop)

## Scenario
Build a simple agent that can answer order-status questions using in-memory data. If the user doesn’t include an order ID, the agent must call a helper tool to fetch a default order ID, then use it to check status.

## Constraints
- Follow the Agent Tooling principles from the root `README.md`.
- Keep logic simple; tools can be plain Python.
- Use Strands + OpenAI for the agent.
- The agent must use tools for any order lookup.

## Task
1. If the user says: `Where is my order B456?`
   - Call `get_order_status(order_id)` once with `order_id="B456"`.
2. If the user says: `Where is my order?`
   - Call `get_default_order_id()` first.
   - Then call `get_order_status(order_id)` with the returned ID.

## Required Tools
- `get_order_status(order_id: str) -> str`
- `get_default_order_id() -> str`

## Example Run
```
$ python main.py
Tool #1: get_default_order_id
Tool #2: get_order_status
Shipped
```

## Acceptance Checklist
- Tools are explicit and used as contracts.
- The agent decides which tools to call.
- No hidden state; any state is in a visible object or variable.
- The plan (get ID → check status → respond) is clear in behavior.
- The agent can choose not to call tools if it already has an ID.
- The agent handles missing or unknown IDs safely.
- Tool usage is visible to humans.

---

Place your solution in `example2/solution/`.
