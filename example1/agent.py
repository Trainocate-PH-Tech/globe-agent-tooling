from strands import Agent
from strands.models.openai import OpenAIModel
import os
from tools import greet

class ToolLogCallbackHandler:
    def __init__(self):
        self.tool_count = 0

    def __call__(self, **kwargs):
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

class HelloAgent:
    def __init__(self):
        self.model = OpenAIModel(model_id="gpt-4o-mini")
        if os.getenv("OPENAI_API_KEY"):
            self.model = OpenAIModel(
                client_args={"api_key": os.getenv("OPENAI_API_KEY")},
                model_id="gpt-4o-mini"
            )

        self.agent = Agent(
            model=self.model,
            tools=[greet],
            system_prompt=(
                "You are a simple agent",
                "If the user wants to greet someone, use greet tool",
                "Do not greet directly"
            ),
            callback_handler=ToolLogCallbackHandler()
        )

    def run(self, user_input: str):
        return self.agent(user_input)
