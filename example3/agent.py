import os
import re
from typing import Any

from strands import Agent
from strands.models.openai import OpenAIModel
from tools import get_hours, list_attractions


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


class TripAgent:
    def __init__(self):
        self.model = OpenAIModel(model_id="gpt-4o-mini")
        if os.getenv("OPENAI_API_KEY"):
            self.model = OpenAIModel(
                client_args={"api_key": os.getenv("OPENAI_API_KEY")},
                model_id="gpt-4o-mini",
            )

        self.agent = Agent(
            model=self.model,
            tools=[list_attractions, get_hours],
            system_prompt=(
                "You are a simple trip planner.\n"
                "If the user provides a city, call list_attractions(city).\n"
                "Pick two attractions and call get_hours(place) for each.\n"
                "Return a JSON-like dict with city and stops.\n"
                "If no city is provided, ask for it.\n"
                "Do not invent places or hours."
            ),
            callback_handler=ToolLogCallbackHandler(),
            state={"last_city": None, "plan": []},
        )

    def run(self, user_input: str):
        city_match = re.search(r"\b(Kyoto|Osaka)\b", user_input)
        if city_match:
            self.agent.state.set("last_city", city_match.group(0))
            self.agent.state.set("plan", [
                "list attractions",
                "pick top 2",
                "get hours",
                "respond",
            ])
        return self.agent(user_input)
