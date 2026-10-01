"""
02_patterns/06_multi_agent_collaboration.py
==============================================
PATTERN: Multi-Agent Collaboration

Two or more agents work on DIFFERENT PARTS of the same deliverable and
their outputs are combined -- distinct from Routing (which sends a
request down exactly ONE path) and from Reflection (which is the same
task looked at twice, generation vs. critique). Here, an Outline-Agent
and a Details-Agent each own a genuinely different piece of the final
report, and a third step merges them.
"""
import asyncio

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler
from common.client import make_agent

OUTLINE_INSTRUCTIONS = """\
You produce a 3-bullet outline for a short report on the given topic.
Output ONLY the outline.
"""

DETAILS_INSTRUCTIONS = """\
You take a report outline and, for EACH bullet, write one supporting
sentence with a concrete fact or example. Output the outline with each
bullet followed by its supporting sentence.
"""

EDITOR_INSTRUCTIONS = """\
You take a drafted report (outline + supporting sentences) and tighten
it into a single flowing paragraph, removing bullet formatting.
"""


class AgentStep(Executor):
    def __init__(self, id: str, agent):
        super().__init__(id=id)
        self.agent = agent

    @handler
    async def run_agent(self, input_text: str, ctx: WorkflowContext[str]) -> None:
        result = await self.agent.run(input_text)
        await ctx.send_message(str(result))


async def main():
    outline_step = AgentStep(id="outline", agent=make_agent("Outline-Agent", OUTLINE_INSTRUCTIONS))
    details_step = AgentStep(id="details", agent=make_agent("Details-Agent", DETAILS_INSTRUCTIONS))
    editor_step = AgentStep(id="edit", agent=make_agent("Editor-Agent", EDITOR_INSTRUCTIONS))

    workflow = (
        WorkflowBuilder(start_executor=outline_step)
        .add_edge(outline_step, details_step)
        .add_edge(details_step, editor_step)
        .build()
    )

    events = await workflow.run("The tradeoffs between single-agent and multi-agent system design.")
    print("=== Collaborative report (Outline-Agent -> Details-Agent -> Editor-Agent) ===")
    print(events.get_outputs())


if __name__ == "__main__":
    asyncio.run(main())
