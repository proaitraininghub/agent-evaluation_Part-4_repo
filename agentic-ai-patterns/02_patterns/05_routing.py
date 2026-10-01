"""
02_patterns/05_routing.py
============================
PATTERN: Routing

A lightweight Router-Agent classifies an incoming request and dispatches
it to ONE of several specialized agents -- rather than one agent trying
to handle every kind of request with one enormous instruction block.
Unlike Planning (which breaks one task into ordered steps), routing
picks exactly one path and doesn't chain further steps afterward.

This demo keeps the routing decision as plain Python (an if/elif on the
router's classification) rather than a WorkflowBuilder graph, because
the specialist needs the ORIGINAL user question, not the router's
one-word output -- see the note in main() for when a graph-based
conditional edge (as used in the code-change-orchestrator pipelines) is
the better fit instead.
"""
import asyncio

from common.client import make_agent

ROUTER_INSTRUCTIONS = """\
Classify the user's request into exactly one category: BILLING,
TECHNICAL, or GENERAL. Output ONLY that one word.
"""

BILLING_INSTRUCTIONS = "You handle billing questions: invoices, refunds, payment methods. Be concise and precise about policy."
TECHNICAL_INSTRUCTIONS = "You handle technical support questions: errors, setup, troubleshooting. Ask a clarifying question if the issue is underspecified."
GENERAL_INSTRUCTIONS = "You handle general questions that aren't billing or technical. Be friendly and brief."


async def route_one(question: str):
    router = make_agent("Router-Agent", ROUTER_INSTRUCTIONS)
    category = str(await router.run(question)).strip().upper()

    if "BILLING" in category:
        specialist = make_agent("Billing-Agent", BILLING_INSTRUCTIONS)
    elif "TECHNICAL" in category:
        specialist = make_agent("Technical-Agent", TECHNICAL_INSTRUCTIONS)
    else:
        specialist = make_agent("General-Agent", GENERAL_INSTRUCTIONS)

    answer = await specialist.run(question)
    return category, specialist.name, answer


async def main():
    # NOTE: when the routing decision needs to feed into further chained
    # steps (not just "answer and stop"), a WorkflowBuilder graph with a
    # conditional add_edge(condition=...) -- the same mechanism used in
    # the code-change-orchestrator pipelines -- is the better fit than
    # this plain if/elif. Use a graph once routing is one step of a
    # longer pipeline rather than the whole pipeline.
    questions = [
        "Why was I charged twice this month?",
        "My agent keeps throwing a 404 error when I call the API.",
        "What time zone are you running in?",
    ]
    for q in questions:
        category, agent_name, answer = await route_one(q)
        print(f"Q: {q}\n  -> routed to: {agent_name} (classified as {category})\n  -> A: {answer}\n")


if __name__ == "__main__":
    asyncio.run(main())
