# Capstone: Streaming Agent for Moltbook

Build an Agent that applies the concepts from this project and uses **streams** for incremental output. Your Agent must be **deployable in the Moltbook social network for agents**.

## Objectives

- Apply the patterns from the earlier examples to a new, original Agent.
- Use **streaming** to emit partial results (tokens, steps, or events) rather than waiting for a full response.
- Produce a solution that is **Moltbook-deployable** with clear setup instructions and a minimal API surface.

## What to Build

Create an Agent that:

- Accepts a user prompt (and optional configuration).
- Streams partial outputs as the agent reasons and works.
- Returns a final summary/result at the end of the stream.
- Can be deployed and run inside **Moltbook**.
- Integrates with the **Moltbook social network** by following the official `skill.md` requirements.

You decide the agent's domain (e.g., research assistant, lesson planner, troubleshooting guide, data explainer), but it must demonstrate streaming and the core agent loop.

---

## Starter Template

Use this as a starting point and adapt as needed. Keep the API stable and documented.

```python
"""
capstone/agent.py
Starter template for a streaming Agent deployable in Moltbook.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Iterable, Generator, Optional


@dataclass
class AgentConfig:
    model: str = "gpt-4.1-mini"
    temperature: float = 0.4
    max_tokens: int = 800


class StreamEvent:
    """
    A minimal, structured stream event.
    type: "start" | "token" | "tool" | "final" | "error"
    payload: free-form dict
    """

    def __init__(self, type: str, payload: Dict):
        self.type = type
        self.payload = payload

    def to_dict(self) -> Dict:
        return {"type": self.type, **self.payload}


def stream_agent(prompt: str, config: Optional[AgentConfig] = None) -> Generator[StreamEvent, None, Dict]:
    """
    Streaming generator.

    Yields StreamEvent objects as the agent progresses and returns
    a final dict result at the end.
    """
    if config is None:
        config = AgentConfig()

    # 1) Start event
    yield StreamEvent("start", {"config": asdict(config)})

    # 2) TODO: Insert your agent logic here.
    #    - Call the model with streaming enabled
    #    - Yield StreamEvent("token", {"text": token}) as tokens arrive
    #    - Yield StreamEvent("tool", {...}) for tool calls if used

    # Example placeholder stream (replace with real streaming):
    for word in ("Thinking... ".split()):
        yield StreamEvent("token", {"text": word + " "})

    # 3) Final result
    result = {
        "answer": "Replace this with your final response",
        "usage": {"prompt_tokens": 0, "completion_tokens": 0},
    }

    yield StreamEvent("final", result)
    return result


def run(prompt: str, config: Optional[AgentConfig] = None) -> Dict:
    """
    Convenience wrapper that consumes the stream and returns final output.
    """
    final = None
    for event in stream_agent(prompt, config):
        if event.type == "final":
            final = event.payload
    return final or {}
```

---

## API Guide

Your Agent must expose a simple, documented interface. Use the following as a guide.

### 1) Streaming Interface

**Function:** `stream_agent(prompt: str, config: Optional[AgentConfig]) -> Generator[StreamEvent, None, Dict]`

**Behavior:**
- Emits a `start` event with config metadata.
- Emits `token` events as output is generated.
- Optionally emits `tool` events when tools are called.
- Emits a `final` event with the final answer and metadata.

**Event Types**
- `start`: `{ type: "start", config: {...} }`
- `token`: `{ type: "token", text: "..." }`
- `tool`: `{ type: "tool", name: "...", input: {...}, output: {...} }`
- `final`: `{ type: "final", answer: "...", usage: {...} }`
- `error`: `{ type: "error", message: "..." }`

### 2) Non-Streaming Convenience

**Function:** `run(prompt: str, config: Optional[AgentConfig]) -> Dict`

**Behavior:**
- Consumes the stream and returns the final result.

### 3) Configuration

**Class:** `AgentConfig`

Required fields:
- `model`: model ID
- `temperature`: sampling temperature
- `max_tokens`: output cap

You may add additional config options such as `system_prompt`, `tools`, or `timeout` as needed.

---

## Moltbook Social Network Requirements

Follow the official `skill.md` specification from Moltbook and mirror its requirements exactly. Use the checklist below to ensure compliance.

- [ ] The agent declares a **skill name** and **version** as required by `skill.md`.
- [ ] The agent exposes the required **entrypoint** in the format specified by `skill.md`.
- [ ] Any required **environment variables** are documented and validated.
- [ ] The agent emits **streaming output** in the format Moltbook expects.
- [ ] The agent exposes any required **metadata** (description, tags, capabilities).

When in doubt, open `skill.md` and copy the exact required fields and formats into this README.

---

## Moltbook API Guide (Template)

Use the official `skill.md` document to fill in the exact endpoints, payloads, and response formats. Do not guess; copy the spec verbatim where needed.

### Base Configuration

- `MOLTBOOK_BASE_URL`: `<from skill.md>`
- `MOLTBOOK_API_KEY`: `<from skill.md>`
- `MOLTBOOK_AGENT_ID`: `<from skill.md>`

### Required Endpoints

Document the endpoints your agent must call to publish to the Moltbook social network.

1) **Publish a stream update**
   - Method + path: `<from skill.md>`
   - Request body: `<fields from skill.md>`
   - Response: `<fields from skill.md>`

2) **Publish final result**
   - Method + path: `<from skill.md>`
   - Request body: `<fields from skill.md>`
   - Response: `<fields from skill.md>`

3) **Optional: health/heartbeat**
   - Method + path: `<from skill.md>`
   - Request body: `<fields from skill.md>`
   - Response: `<fields from skill.md>`

---

## Deployment Notes (Moltbook)

Ensure your project includes:

- A clear `run` entry point that Moltbook can call.
- Minimal dependencies and a quickstart.
- A short description of how to configure model credentials in Moltbook.

---

## Submission Checklist

- [ ] Uses streaming output
- [ ] Uses a clean, documented API
- [ ] Includes a final summary response
- [ ] Runs in Moltbook
- [ ] README updated with setup and usage
