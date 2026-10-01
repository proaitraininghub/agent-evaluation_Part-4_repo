"""
02_patterns/02_reflection.py
===============================
PATTERN: Reflection
 
An agent produces a first draft, then a second pass -- either the same
agent re-prompted, or (cleaner, as here) a dedicated Critic-Agent --
reviews it and points out concrete problems, and a final pass revises
based on that critique. Unlike Multi-agent Collaboration (pattern 6),
the point here isn't specialization of *tools*, it's specialization of
*perspective*: the same task looked at twice, generation and critique
kept deliberately separate so the critique isn't biased by having just
written the thing.
 
For teaching: the three print blocks below (Draft / Critique / Revised)
ARE the visible "trace" of this pattern -- there's no tool-calling loop
to peel back like in ReAct, so showing each stage's own output, as its
own clearly-labeled block, is already the right level of transparency.
"""
import asyncio
 
from common.client import make_agent
 
DRAFTER_INSTRUCTIONS = """\
You write a short explanation of a technical concept for a beginner.
Write ONLY the explanation, 3-4 sentences, no preamble.
"""
 
CRITIC_INSTRUCTIONS = """\
You review a beginner-level technical explanation. List up to 3 concrete
problems with it (jargon left unexplained, missing an example, too long,
factually questionable) as a short bulleted list. If it's genuinely
good, say so briefly. Do not rewrite it yourself.
"""
 
REVISER_INSTRUCTIONS = """\
You receive an original explanation and a critique of it. Rewrite the
explanation to address every point in the critique. Output ONLY the
revised explanation.
"""
 
 
async def main():
    drafter = make_agent("Drafter-Agent", DRAFTER_INSTRUCTIONS)
    critic = make_agent("Critic-Agent", CRITIC_INSTRUCTIONS)
    reviser = make_agent("Reviser-Agent", REVISER_INSTRUCTIONS)
 
    topic = "Explain what a WorkflowBuilder does in Microsoft Agent Framework."
 
    # agent.run(...) (non-streaming) returns a response object. Printing
    # that object directly prints its raw repr, not clean text -- use
    # `.text` to get the aggregated, human-readable result, same as the
    # streaming `update.text` used in the ReAct demo.
    draft = await drafter.run(topic)
    print("=== Draft ===")
    print(draft.text, "\n")
 
    critique = await critic.run(f"Explanation to review:\n{draft.text}")
    print("=== Critique ===")
    print(critique.text, "\n")
 
    revised = await reviser.run(f"Original:\n{draft.text}\n\nCritique:\n{critique.text}")
    print("=== Revised ===")
    print(revised.text)
 
 
if __name__ == "__main__":
    asyncio.run(main())
 
