"""
01_single_vs_multi_agent/single_agent_demo.py
================================================
Task: "Research a topic, then write a short summary of it."

Solved here with ONE agent that has both a research tool and the
instruction to write the summary itself. Run this next to
multi_agent_demo.py, which solves the exact same task with two
specialized agents -- compare the transcripts, not just the code.
"""
import asyncio
from typing import Annotated

from pydantic import Field

from agent_framework import tool
from common.client import make_agent


@tool(approval_mode="never_require")
def web_search_stub(
    query: Annotated[str, Field(description="Search query.")],
) -> str:
    """Stubbed search tool so this demo runs with no external dependency.
    Swap for a real search/RAG tool in your own environment."""
    return (
        f"[stub search results for '{query}']\n"
        "- Microsoft Agent Framework unifies Semantic Kernel and AutoGen.\n"
        "- It supports agents, workflows, and durable hosting.\n"
        "- Released in 2025, positioned as the successor to both prior frameworks."
    )


INSTRUCTIONS = """\
You are a research-and-write assistant. When asked about a topic:
1. Use web_search_stub to gather a few facts.
2. Write a 3-sentence summary directly from those facts.
Do both steps yourself, in one response.
"""


async def main():
    agent = make_agent("ResearchAndWriteAgent", INSTRUCTIONS, tools=[web_search_stub])
    result = await agent.run("Research Microsoft Agent Framework and summarize it.")
    print("=== Single-Agent Result ===")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
