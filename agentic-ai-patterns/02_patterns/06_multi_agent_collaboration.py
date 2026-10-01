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

EDITOR_INSTRUCTIONS = """
You take a drafted report (outline + supporting sentences) and tighten
it into a single flowing paragraph, removing bullet formatting.
"""


def _preview(text: str, limit: int = 160) -> str:
    """Trim long handoff text for a readable log line."""
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + "..."


class AgentStep(Executor):
    def __init__(self, id: str, agent, is_final: bool = False):
        super().__init__(id=id)
        self.agent = agent
        self.is_final = is_final

    @handler
    async def run_agent(self, input_text: str, ctx: WorkflowContext[str, str]) -> None:
        # --- Log what this agent received, before it does anything ---
        print(f"  [{self.agent.name}] received input:")
        print(f"    {_preview(input_text)}")

        result = await self.agent.run(input_text)
        output_text = result.text

        # --- Log what this agent produced, i.e. its "thinking made visible" ---
        print(f"  [{self.agent.name}] produced output:")
        print(f"    {_preview(output_text)}\n")

        if self.is_final:
            await ctx.yield_output(output_text)
        else:
            await ctx.send_message(output_text)


async def main():
    outline_step = AgentStep(id="outline", agent=make_agent("Outline-Agent", OUTLINE_INSTRUCTIONS))
    details_step = AgentStep(id="details", agent=make_agent("Details-Agent", DETAILS_INSTRUCTIONS))
    editor_step = AgentStep(id="edit", agent=make_agent("Editor-Agent", EDITOR_INSTRUCTIONS), is_final=True)

    workflow = (
        WorkflowBuilder(start_executor=outline_step)
        .add_edge(outline_step, details_step)
        .add_edge(details_step, editor_step)
        .build()
    )

    print("=== Collaborative report (Outline-Agent -> Details-Agent -> Editor-Agent) ===\n")
    events = await workflow.run("The tradeoffs between single-agent and multi-agent system design.")

    print("=== Final merged report ===")
    for output in events.get_outputs():
        print(output)


if __name__ == "__main__":
    asyncio.run(main())