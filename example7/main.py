from agent import ReviewAgent

if __name__ == "__main__":
    agent = ReviewAgent()
    result = agent.run("Approve a SIM swap for 09171234567")
    print(result)
