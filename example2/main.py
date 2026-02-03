from agent import OrderAgent

if __name__ == "__main__":
    agent = OrderAgent()
    result = agent.run("Where is my order A123?")
    print(result)
