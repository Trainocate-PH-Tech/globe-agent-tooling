from strands import tool

@tool
def greet(name: str) -> str:
    print(f"Hello {name}")
