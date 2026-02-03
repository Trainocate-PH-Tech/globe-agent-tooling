from agent import TripAgent

if __name__ == "__main__":
    agent = TripAgent()
    result = agent.run("Plan a short visit in Kyoto")
    print(result)
