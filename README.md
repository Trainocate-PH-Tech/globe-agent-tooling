# Agent Tooling

Below is a simple, end-to-end example that stays library-free for now. We'll later swap in **Strands** as the agent framework and **OpenAI** as the LLM backend. The overarching use case is a **small shop order-status assistant**: it answers "Where is my order?" by checking a local in-memory store.

```python
class Agent:
    def __init__(self, name, tools):
        self.name = name
        self.tools = {t.name: t for t in tools}
        self.state = {}

    def decide(self, user_input):
        # Simple rule-based decision for now.
        if "order" in user_input.lower():
            return {"tool": "get_order_status", "args": {"order_id": "A123"}}
        return {"tool": None, "args": {}}

    def act(self, decision):
        tool_name = decision["tool"]
        if tool_name is None:
            return "I can help with orders. Ask me about an order ID."
        return self.tools[tool_name].run(decision["args"])

    def handle(self, user_input):
        decision = self.decide(user_input)
        return self.act(decision)


class Tool:
    def __init__(self, name, fn, input_schema):
        self.name = name
        self.fn = fn
        self.input_schema = input_schema  # kept simple for now

    def run(self, args):
        return self.fn(args)


def get_order_status(args):
    store = {"A123": "Packed", "B456": "Shipped", "C789": "Delivered"}
    order_id = args.get("order_id", "")
    return store.get(order_id, "Order not found")
```

Example usage:

```python
agent = Agent(
    name="OrderBuddy",
    tools=[Tool("get_order_status", get_order_status, {"order_id": "string"})]
)

print(agent.handle("What is the status of my order A123?"))
# -> "Packed"
```

---

## ToolLogCallbackHandler (Logging Tool Usage)

**Purpose:** Provide a minimal, consistent way to log tool usage without streaming model text. This keeps outputs clean while still showing which tools were called.

**Where it’s used:** `example1/agent.py`, `example1/solution/agent.py`, `example2/agent.py`, `example2/solution/agent.py`.

**Arguments**
- `tool_count` (int, internal): incremented each time a tool is invoked.
- `**kwargs`: event payload from Strands. We only read:
  - `event.contentBlockStart.start.toolUse.name` (tool name)

**Minimal implementation**

```python
from typing import Any

class ToolLogCallbackHandler:
    def __init__(self) -> None:
        self.tool_count = 0

    def __call__(self, **kwargs: Any) -> None:
        tool_use = (
            kwargs.get("event", {})
            .get("contentBlockStart", {})
            .get("start", {})
            .get("toolUse")
        )
        if tool_use:
            self.tool_count += 1
            tool_name = tool_use.get("name", "unknown")
            print(f"Tool #{self.tool_count}: {tool_name}")
```

## 1 - Tools are Contracts Not Functions

**Simple explanation:** A tool is a *promise* about what it accepts and what it returns, not just a random function.

### Tools
- Explicit
- Typed
- Constrained
- Auditable

### Value
- Prevents hallucination
- Enables auditing
- Enables retries
- Enables substitution (local → cloud)

**Content:** Treat tools as small APIs. Even if they are just Python functions today, define their inputs clearly so the agent can't "guess" missing fields.

Example:

```python
get_order_status_tool = Tool(
    name="get_order_status",
    fn=get_order_status,
    input_schema={"order_id": "string"}  # simple contract
)
```

## 2 - Agents Decide, Tools Execute

**Simple explanation:** The agent *chooses* what to do; the tool *does* it. Keep reasoning separate from actions.

**Content:** The `decide` method picks a tool and arguments. The tool runs without extra reasoning.

Example:

```python
decision = agent.decide("Where is my order?")
# decision -> {"tool": "get_order_status", "args": {"order_id": "A123"}}

result = agent.act(decision)
# result -> "Packed"
```

## 3 - State is Explicit and Inspectable

**Simple explanation:** State should be stored in one place you can read and debug.

**Content:** The agent keeps a `state` dict to track conversation facts, like the last order ID.

Example:

```python
agent.state["last_order_id"] = "A123"
print(agent.state)
# -> {"last_order_id": "A123"}
```

## 4 - Plans are First-Class Objects

**Simple explanation:** A plan is not just a thought—it's a data structure you can log, test, and update.

**Content:** Even in simple cases, write down the steps the agent intends to take.

Example:

```python
plan = [
    "extract order id",
    "call get_order_status",
    "format response"
]
```

## 5 - Tools are Chosen Not Forced

**Simple explanation:** The agent should choose the right tool, not be forced to call one.

**Content:** If no tool fits, the agent should respond without tools.

Example:

```python
decision = agent.decide("Hello!")
# decision -> {"tool": None, "args": {}}

print(agent.act(decision))
# -> "I can help with orders. Ask me about an order ID."
```

## 6 - Uncertainty is a Valid Option

**Simple explanation:** It's okay for the agent to say "I don't know" instead of guessing.

**Content:** If the order ID is missing, the agent should ask for it.

Example:

```python
def decide(self, user_input):
    if "order" in user_input.lower() and "A123" not in user_input:
        return {"tool": None, "args": {}, "ask": "What is your order ID?"}
```

## 7 - Failures are Designed, Not Avoided

**Simple explanation:** Expect things to break, and design for it.

**Content:** When the tool fails (missing order), the agent gives a safe response.

Example:

```python
def get_order_status(args):
    store = {"A123": "Packed"}
    order_id = args.get("order_id", "")
    if order_id not in store:
        return "Order not found. Please check the ID."
    return store[order_id]
```

## 8 - Humans Stay in the Loop

**Simple explanation:** A human should always be able to correct or take over.

**Content:** Provide a clear escape hatch for users or operators.

Example:

```python
agent.state["escalate_to_human"] = True
# A real system could route to support at this point.
```
