from agent import FraudAgent

if __name__ == "__main__":
    agent = FraudAgent()
    result = agent.run("Check fraud risk for 09171234567 and update the case record")
    print(result)
