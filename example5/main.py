from agent import RiskAgent

if __name__ == "__main__":
    agent = RiskAgent()
    result = agent.run("Please approve a SIM swap for 09171234567")
    print(result)
