# Exercise: Two-Step Greeting (Workshop)

## Scenario
You are building a tiny agent that greets users. If the user doesn’t say *who* to greet, the agent must first call another tool to get a name, then pass that name to the greeter tool.

## Constraints
- Follow the Agent Tooling principles from the root `README.md`.
- Keep it simple and library-free in the logic (tool functions can be plain Python).
- Use Strands for the agent interface and tools, and OpenAI as the model.
- The agent must use tools to complete the task, not greet directly.

## Task
Implement an agent that does the following:
1. If the user says: `Say hello to Raphael`
   - Call `greet(name)` once with `name="Raphael"`.
2. If the user says: `Say hello`
   - Call `get_name()` first to obtain a name.
   - Then call `greet(name)` with the name returned by `get_name()`.

## Files to Create or Update
- `agent.py`
- `tools.py`
- `main.py`

## Required Tools
- `greet(name: str) -> str`
- `get_name() -> str`

## Example Run
```
$ python main.py
Tool #1: get_name
Tool #2: greet
Hello, Raphael!
```

## Acceptance Checklist
- Tools are explicit and used as contracts.
- The agent decides which tools to call.
- No hidden state; any state is in a visible object or variable.
- The plan (get name → greet) is clear in behavior.
- The agent can choose not to use a tool if it has a name already.
- The agent can respond safely if it still cannot get a name.
- Tool failure is handled (e.g., missing name).
- The program output is easy for a human to audit.

---

Place your solution in `example1/solution/`.
