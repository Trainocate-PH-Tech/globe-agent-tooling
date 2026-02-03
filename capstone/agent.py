"""
Streaming Agent stub for the capstone.
"""

from dataclasses import dataclass
from typing import Dict, Generator, Optional


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


class Agent:
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()

    def stream(self, prompt: str) -> Generator[StreamEvent, None, Dict]:
        # 1) Start event
        yield StreamEvent("start", {"config": vars(self.config)})

        # 2) TODO: Insert your agent logic here.
        #    - Call the model with streaming enabled
        #    - Yield StreamEvent("token", {"text": token}) as tokens arrive
        #    - Yield StreamEvent("tool", {...}) for tool calls if used

        # Example placeholder stream (replace with real streaming):
        yield StreamEvent("token", {"text": "Thinking... "})

        # 3) Final result
        result = {
            "answer": "Replace this with your final response",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0},
        }

        yield StreamEvent("final", result)
        return result

    def run(self, prompt: str) -> Dict:
        """
        Convenience wrapper that consumes the stream and returns final output.
        """
        final = None
        for event in self.stream(prompt):
            if event.type == "final":
                final = event.payload
        return final or {}


def stream_agent(prompt: str, config: Optional[AgentConfig] = None) -> Generator[StreamEvent, None, Dict]:
    """
    Backwards-compatible functional interface.
    """
    return Agent(config=config).stream(prompt)


def run(prompt: str, config: Optional[AgentConfig] = None) -> Dict:
    """
    Backwards-compatible functional interface.
    """
    return Agent(config=config).run(prompt)
