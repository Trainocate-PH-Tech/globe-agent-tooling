import os
import re
from typing import Any

from strands import Agent
from strands.models.openai import OpenAIModel
from tools import check_system_status, classify_issue, escalate_to_human, lookup_invoice


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


class HelpDeskAgent:
    def __init__(self):
        self.model = OpenAIModel(model_id="gpt-4o-mini")
        if os.getenv("OPENAI_API_KEY"):
            self.model = OpenAIModel(
                client_args={"api_key": os.getenv("OPENAI_API_KEY")},
                model_id="gpt-4o-mini",
            )

        self.agent = Agent(
            model=self.model,
            tools=[classify_issue, lookup_invoice, check_system_status, escalate_to_human],
            system_prompt=(
                "You are a simple help desk router.\n"
                "First call classify_issue(text).\n"
                "If billing, call lookup_invoice(account_id).\n"
                "If technical, call check_system_status(service).\n"
                "If unknown, call escalate_to_human(reason).\n"
                "Do not invent account IDs or services."
            ),
            callback_handler=ToolLogCallbackHandler(),
            state={"issue_type": None, "last_account_id": None, "plan": []},
        )

    def run(self, user_input: str):
        account_match = re.search(r"\bACC-\d{3}\b", user_input)
        if account_match:
            self.agent.state["last_account_id"] = account_match.group(0)
        self.agent.state["plan"] = [
            "classify issue",
            "route to tool",
            "respond or escalate",
        ]
        return self.agent(user_input)
