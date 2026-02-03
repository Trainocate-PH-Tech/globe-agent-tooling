import os
import re
from typing import Any

from strands import Agent
from strands.models.openai import OpenAIModel
from tools import escalate_to_human, get_account_profile, get_recent_events, score_risk


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


class RiskAgent:
    def __init__(self):
        self.model = OpenAIModel(model_id="gpt-4o-mini")
        if os.getenv("OPENAI_API_KEY"):
            self.model = OpenAIModel(
                client_args={"api_key": os.getenv("OPENAI_API_KEY")},
                model_id="gpt-4o-mini",
            )

        self.agent = Agent(
            model=self.model,
            tools=[get_account_profile, get_recent_events, score_risk, escalate_to_human],
            system_prompt=(
                "You are a simple risk scoring agent for Globe PH.\n"
                "If the user provides an MSISDN, call get_account_profile and get_recent_events.\n"
                "Then call score_risk(profile, events).\n"
                "If band is high, call escalate_to_human with a reason.\n"
                "If band is medium or low, approve with a brief explanation.\n"
                "If MSISDN is missing, ask for it.\n"
                "Do not invent MSISDNs or signals."
            ),
            callback_handler=ToolLogCallbackHandler(),
            state={"last_msisdn": None, "plan": []},
        )

    def run(self, user_input: str):
        msisdn_match = re.search(r"\b09\d{9}\b", user_input)
        if msisdn_match:
            self.agent.state["last_msisdn"] = msisdn_match.group(0)
            self.agent.state["plan"] = [
                "fetch profile",
                "fetch events",
                "score risk",
                "decide",
            ]
        return self.agent(user_input)
