import os
import re
from typing import Any

from strands import Agent
from strands.models.openai import OpenAIModel
from tools import call_fraud_api, escalate_to_human, update_case_record


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


class FraudAgent:
    def __init__(self):
        self.model = OpenAIModel(model_id="gpt-4o-mini")
        if os.getenv("OPENAI_API_KEY"):
            self.model = OpenAIModel(
                client_args={"api_key": os.getenv("OPENAI_API_KEY")},
                model_id="gpt-4o-mini",
            )

        self.agent = Agent(
            model=self.model,
            tools=[call_fraud_api, update_case_record, escalate_to_human],
            system_prompt=(
                "You are a failure-first fraud check agent.\n"
                "Always call call_fraud_api(msisdn).\n"
                "If ok=false, call escalate_to_human with the error.\n"
                "If ok=true and risk_band is high, update_case_record with status 'FRAUD_REVIEW'.\n"
                "If ok=true and risk_band is low, update_case_record with status 'APPROVED'.\n"
                "If MSISDN is missing, ask for it.\n"
                "Do not invent data."
            ),
            callback_handler=ToolLogCallbackHandler(),
            state={"last_msisdn": None, "plan": []},
        )

    def run(self, user_input: str):
        msisdn_match = re.search(r"\b09\d{9}\b", user_input)
        if msisdn_match:
            self.agent.state["last_msisdn"] = msisdn_match.group(0)
            self.agent.state["plan"] = [
                "call api",
                "validate",
                "update record or escalate",
            ]
        return self.agent(user_input)
