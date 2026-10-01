"""
01_single_vs_multi_agent/multi_agent_demo.py
===============================================
Same task as single_agent_demo.py: "Research a topic, then write a short
summary of it." Solved here with TWO specialized agents wired through
WorkflowBuilder -- a Researcher (only has the search tool, no writing
instructions) and a Writer (only has writing instructions, no tools).

Compare this transcript to single_agent_demo.py's. For a task this
small, notice single-agent wins on latency (one call vs. two) and
simplicity. Multi-agent starts winning once either role needs a
distinct model, a distinct tool set that would bloat one agent's
instructions, or independent testing/versioning -- see the comparison
table in the Teaching Doc for the full decision framework.
"""
import asyncio
from typing import Annotated

from pydantic import Field

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler, tool
from common.client import make_agent


@tool(approval_mode="never_require")
def web_search_stub(
    query: Annotated[str, Field(description="Search query.")],
) -> str:
    """Same stub as the single-agent version, for a fair comparison."""
    return (
        f"[stub search results for '{query}']\n"
        "- Microsoft Agent Framework unifies Semantic Kernel and AutoGen.\n"
        "- It supports agents, workflows, and durable hosting.\n"
        "- Released in 2025, positioned as the successor to both prior frameworks."
    )


RESEARCHER_INSTRUCTIONS = """\
You are Researcher-Agent. Use web_search_stub to gather facts about the
requested topic. Output ONLY the raw facts you found -- do not summarize
or write prose. That is not your job.
"""

WRITER_INSTRUCTIONS = """\
You are Writer-Agent. You receive raw research facts and must write a
3-sentence summary from them. You have no tools and cannot search
yourself -- work only from what you're given.
"""

class AgentStep(Executor):
    def __init__(self, id: str, agent, is_final: bool = False):
        super().__init__(id=id)
        self.agent = agent
        self.is_final = is_final

    @handler
    async def run_agent(self, input_text: str, ctx: WorkflowContext[str, str]) -> None:
        result = await self.agent.run(input_text)
        if self.is_final:
            await ctx.yield_output(str(result))
        else:
            await ctx.send_message(str(result))


async def main():
    researcher = AgentStep(id="research", agent=make_agent("Researcher-Agent", RESEARCHER_INSTRUCTIONS, tools=[web_search_stub]))
    writer = AgentStep(id="write", agent=make_agent("Writer-Agent", WRITER_INSTRUCTIONS, tools=[]), is_final=True)

    workflow = WorkflowBuilder(start_executor=researcher).add_edge(researcher, writer).build()

    events = await workflow.run("Research Microsoft Agent Framework and summarize it.")
    print("=== Multi-Agent Result ===")
    print(events.get_outputs())


if __name__ == "__main__":
    asyncio.run(main())
