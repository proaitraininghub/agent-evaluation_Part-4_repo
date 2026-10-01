"""
02_patterns/04_tool_use.py
=============================
PATTERN: Tool Use

The agent is given multiple tools with distinct purposes and must
decide, from the user's request alone, which one (or which combination)
is relevant -- rather than being told which tool to call. This is what
turns a chatbot into something that can act. (You saw @tool basics in
the Agent Framework learning guide, Section 2 -- this demo is the
"choosing between several tools" version.)
"""
import asyncio
from typing import Annotated

from pydantic import Field

from agent_framework import tool
from common.client import make_agent


@tool(approval_mode="never_require")
def get_weather(
    city: Annotated[str, Field(description="City name.")],
) -> str:
    """Get the current weather for a city (stubbed)."""
    return f"{city}: 24C, partly cloudy."


@tool(approval_mode="never_require")
def get_time(
    timezone: Annotated[str, Field(description="IANA timezone, e.g. 'Asia/Kolkata'.")],
) -> str:
    """Get the current time in a timezone (stubbed)."""
    return f"{timezone}: 14:32 (stub value, not live)."


@tool(approval_mode="never_require")
def calculate(
    expression: Annotated[str, Field(description="A simple arithmetic expression, e.g. '12 * 4'.")],
) -> str:
    """Evaluate a simple arithmetic expression."""
    try:
        # Restricted eval: digits/operators only, no names -- fine for a
        # teaching stub, not something to ship as-is for untrusted input.
        allowed = "0123456789+-*/(). "
        if not all(c in allowed for c in expression):
            return "Expression contains disallowed characters."
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Could not evaluate: {e}"


TOOL_USE_INSTRUCTIONS = """\
You are a general assistant with three tools: get_weather, get_time,
and calculate. Use whichever tool(s) the user's question actually
needs -- don't call a tool that isn't relevant, and don't guess an
answer a tool could give you exactly.
"""


async def main():
    agent = make_agent("ToolUseAgent", TOOL_USE_INSTRUCTIONS, tools=[get_weather, get_time, calculate])

    questions = [
        "What's the weather in Pune?",
        "What is 340 * 12?",
        "What's the weather in Pune, and also what's 340 * 12?",
    ]
    for q in questions:
        result = await agent.run(q)
        print(f"Q: {q}\nA: {result}\n")


if __name__ == "__main__":
    asyncio.run(main())
