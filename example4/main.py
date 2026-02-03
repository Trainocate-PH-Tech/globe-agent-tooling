from agent import HelpDeskAgent

if __name__ == "__main__":
    agent = HelpDeskAgent()
    result = agent.run("I was charged twice on my last invoice. My account is ACC-100")
    print(result)
