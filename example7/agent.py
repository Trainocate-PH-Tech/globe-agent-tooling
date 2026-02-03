import os
import re
from typing import Any

from strands import Agent
from strands.models.openai import OpenAIModel
from tools import (
    build_review_summary,
    create_review_ticket,
    get_account_profile,
    get_recent_events,
    route_to_queue,
    score_risk,
)


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


class ReviewAgent:
    def __init__(self):
        self.model = OpenAIModel(model_id="gpt-4o-mini")
        if os.getenv("OPENAI_API_KEY"):
            self.model = OpenAIModel(
                client_args={"api_key": os.getenv("OPENAI_API_KEY")},
                model_id="gpt-4o-mini",
            )

        self.agent = Agent(
            model=self.model,
            tools=[
                get_account_profile,
                get_recent_events,
                score_risk,
                build_review_summary,
                create_review_ticket,
                route_to_queue,
            ],
            system_prompt=(
                "You are a human-in-the-loop review agent.\n"
                "If MSISDN is provided, gather profile and events, then score risk.\n"
                "If risk is high or unknown, build a review summary, create a ticket,\n"
                "and route it to the 'risk-review' queue.\n"
                "If risk is low or medium, respond with approval and reason.\n"
                "Do not invent data."
            ),
            callback_handler=ToolLogCallbackHandler(),
            state={"last_msisdn": None, "plan": [], "ticket_id": None},
        )

    def run(self, user_input: str):
        msisdn_match = re.search(r"\b09\d{9}\b", user_input)
        if msisdn_match:
            self.agent.state["last_msisdn"] = msisdn_match.group(0)
            self.agent.state["plan"] = [
                "fetch profile",
                "fetch events",
                "score risk",
                "summarize",
                "create ticket",
                "route to queue",
            ]
        return self.agent(user_input)
