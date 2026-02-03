# Example 1: Hello World

## Goal

```
Say hello to Raphael
```

**Agent Behavior**
1. Decide it needs a tool
2. Call a tool to format a greeting
3. Return the result
4. Explain what it did (implicitly via logs/state)

## Agent Tooling Principles Used

1) Tools are contracts, not functions  
The `greet` tool has a clear input (`name`) and output (string greeting).

2) Agents decide, tools execute  
The agent decides to call `greet`, and the tool performs the greeting.

3) State is explicit and inspectable  
This example is stateless, which is still an explicit design choice.

4) Plans are first-class objects  
The plan is minimal: decide → tool → response.

5) Tools are chosen, not forced  
The agent only uses the tool when it detects a greeting request.

6) Uncertainty is a valid option  
If the prompt is not a greeting, the agent can respond without tools.

7) Failures are designed, not avoided  
A missing or unclear name can be handled with a follow-up question.

8) Humans stay in the loop  
The program prints the final response so a human can see and verify it.
