"""
02_patterns/08_agent_communication.py
========================================
HOW AGENTS COMMUNICATE: in-process message passing, made explicit

Every WorkflowBuilder demo so far has used ctx.send_message(...) without
calling attention to it as its own topic. This demo isolates that one
mechanism: two executors passing a STRUCTURED message (a dataclass, not
just a string) between them, so it's clear the graph can carry real
data, not only text.

See the Teaching Guide's Section 2 for how this compares to Group Chat
(agents sharing one transcript) and the A2A protocol (agents running as
separate services) -- this file demonstrates only the cheapest, fastest
mechanism: same-process message passing along a graph edge.
"""
import asyncio
from dataclasses import dataclass

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler
from common.client import make_agent


@dataclass
class TriageResult:
    """A structured message -- not a string. Executors can pass any
    Python object along a graph edge, as long as the receiving
    executor's handler declares a matching type."""
    category: str
    confidence: str
    original_question: str


CLASSIFIER_INSTRUCTIONS = """\
Classify the request as BILLING, TECHNICAL, or GENERAL, and rate your
confidence as HIGH or LOW. Output exactly two words: CATEGORY CONFIDENCE
(e.g. "BILLING HIGH").
"""

RESPONDER_INSTRUCTIONS = "You answer the user's question directly and helpfully."


class ClassifierStep(Executor):
    def __init__(self, id: str, agent):
        super().__init__(id=id)
        self.agent = agent

    @handler
    async def classify(self, question: str, ctx: WorkflowContext[TriageResult]) -> None:
        raw = str(await self.agent.run(question)).strip().upper()
        parts = raw.split()
        category = parts[0] if len(parts) > 0 else "GENERAL"
        confidence = parts[1] if len(parts) > 1 else "LOW"

        # This is the structured message being sent -- not just a string,
        # a typed object carrying three distinct pieces of information.
        await ctx.send_message(TriageResult(category=category, confidence=confidence, original_question=question))


class ResponderStep(Executor):
    def __init__(self, id: str, agent):
        super().__init__(id=id)
        self.agent = agent

    @handler
    async def respond(self, triage: TriageResult, ctx: WorkflowContext[str]) -> None:
        # This executor receives the STRUCTURED message from the previous
        # step and can use every field of it, not just raw text.
        prefix = ""
        if triage.confidence == "LOW":
            prefix = "[low-confidence classification -- consider human review] "
        answer = await self.agent.run(triage.original_question)
        await ctx.send_message(f"{prefix}[{triage.category}] {answer}")


async def main():
    classifier = ClassifierStep(id="classify", agent=make_agent("Classifier-Agent", CLASSIFIER_INSTRUCTIONS))
    responder = ResponderStep(id="respond", agent=make_agent("Responder-Agent", RESPONDER_INSTRUCTIONS))

    workflow = WorkflowBuilder(start_executor=classifier).add_edge(classifier, responder).build()

    for question in ["Why was I double-charged this month?", "What's the weather like today?"]:
        events = await workflow.run(question)
        print(f"Q: {question}")
        print(f"A: {events.get_outputs()}\n")


if __name__ == "__main__":
    asyncio.run(main())
