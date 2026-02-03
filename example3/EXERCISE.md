# Exercise: Trip Planner with File Reader (Workshop)

## Scenario
You are building a tiny trip-planning agent. If the user provides a city, the agent should read attraction data from a file using a tool, then call a second tool to fetch hours for each chosen place.

## Constraints
- Follow the Agent Tooling principles from the root `README.md`.
- Keep logic simple; tools can be plain Python.
- Use Strands + OpenAI for the agent.
- The agent must use tools to read data and fetch hours.

## Task
1. If the user says: `Plan a short visit in Kyoto`
   - Call `read_attractions_file(city)` to get a list of attractions.
   - Choose two places.
   - Call `get_hours(place)` for each.
   - Return a simple dict: `{ "city": "Kyoto", "stops": [...] }`.
2. If the user says: `Plan a short visit`
   - Ask for the city.

## Required Tools
- `read_attractions_file(city: str) -> list[str]`
- `get_hours(place: str) -> str`

## Dummy Data
Create a file `data/attractions.txt` with lines in this format:
```
Kyoto|Fushimi Inari,Kiyomizu-dera,Arashiyama
Osaka|Osaka Castle,Dotonbori
```

## Example Run
```
$ python main.py
Tool #1: read_attractions_file
Tool #2: get_hours
Tool #3: get_hours
{"city": "Kyoto", "stops": [{"name": "Fushimi Inari", "hours": "Always open"}, {"name": "Kiyomizu-dera", "hours": "6:00-18:00"}]}
```

## Acceptance Checklist
- Tools are explicit and used as contracts.
- The agent decides which tools to call.
- No hidden state; any state is in a visible object or variable.
- The plan (read file → pick 2 → get hours → respond) is clear in behavior.
- The agent handles unknown cities safely.
- Tool usage is visible to humans.

---

Place your solution in `example3/solution/`.

## Challenge Constraints
- Consider the user passing in a budget in terms of number of hours
- If there are no attractions that fit within the budget, do not respond with anything.
