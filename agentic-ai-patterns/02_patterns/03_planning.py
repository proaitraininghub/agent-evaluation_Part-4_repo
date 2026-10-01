"""
02_patterns/03_planning.py
=============================
PATTERN: Planning

Before doing any work, the agent produces an explicit, numbered plan --
then each step is executed against that plan, one at a time, rather
than the agent figuring out the next move reactively (that's ReAct).
Planning matters once a task has enough steps that "just react to what
you see" risks getting lost, forgetting an earlier requirement, or
doing steps in a bad order.

This demo uses a Planner-Agent to produce a structured plan, then a
simple Python loop (deliberately NOT another agent -- see the Teaching
Doc's "agent vs. code" note) to execute each step against an
Executor-Agent in order, carrying forward prior results.
"""
import asyncio
import re

from common.client import make_agent

PLANNER_INSTRUCTIONS = """\
You break a task into a short numbered plan (3-5 steps max). Output
ONLY the numbered list, one short step per line. Do not execute
anything yourself.
"""

EXECUTOR_INSTRUCTIONS = """\
You execute exactly one step of a larger plan. You're given the overall
goal, the full plan for context, and the specific step to execute now,
plus any results from earlier steps. Do only this one step. Be concise.
"""


def parse_plan(plan_text: str) -> list[str]:
    """Pull numbered lines out of the planner's output. Deliberately
    plain code -- parsing a fixed 'N. text' format has one right answer."""
    steps = re.findall(r"^\s*\d+\.\s*(.+)$", plan_text, re.MULTILINE)
    return steps if steps else [plan_text.strip()]


async def main():
    planner = make_agent("Planner-Agent", PLANNER_INSTRUCTIONS)
    executor = make_agent("Executor-Agent", EXECUTOR_INSTRUCTIONS)

    goal = "Plan how to explain the difference between short-term and long-term agent memory to a beginner, using one analogy."

    plan_text = await planner.run(goal)
    steps = parse_plan(str(plan_text))
    print("=== Plan ===")
    for i, s in enumerate(steps, 1):
        print(f"{i}. {s}")

    results = []
    for i, step_text in enumerate(steps, 1):
        prompt = (
            f"Overall goal: {goal}\n"
            f"Full plan: {plan_text}\n"
            f"Step {i} to execute now: {step_text}\n"
            f"Results so far: {results}"
        )
        result = await executor.run(prompt)
        print(f"\n=== Step {i} result ===")
        print(result)
        results.append(str(result))

    print("\n=== Final combined output ===")
    print("\n".join(results))


if __name__ == "__main__":
    asyncio.run(main())
