"""
02_patterns/07_human_in_the_loop.py
======================================
PATTERN: Human-in-the-Loop

Any tool with side effects should NOT execute purely on the agent's own
confidence. approval_mode="always_require" pauses execution and waits
for an explicit human decision before the tool actually runs -- the same
mechanism used for every write action across this course's enterprise
projects (code-change-orchestrator, incident-triage-copilot).

This demo is deliberately minimal: one read tool (no approval needed)
and one write tool (approval always required), so the gate itself is
the thing on display, not a complex scenario around it.
"""
import asyncio
from typing import Annotated

from pydantic import Field

from agent_framework import tool
from common.client import make_agent


@tool(approval_mode="never_require")
def check_inbox_count(
    folder: Annotated[str, Field(description="Folder name, e.g. 'inbox'.")],
) -> str:
    """Read-only: count messages in a folder (stubbed). No approval needed --
    reading has no side effect to approve."""
    return f"{folder}: 42 unread messages."


@tool(approval_mode="always_require")
def send_email(
    to: Annotated[str, Field(description="Recipient email address.")],
    subject: Annotated[str, Field(description="Email subject.")],
    body: Annotated[str, Field(description="Email body.")],
) -> str:
    """Send an email. NOTE: approval_mode='always_require' means this
    line only runs after an explicit human confirms it -- no matter how
    confident the agent is that the email should be sent."""
    return f"Email sent to {to}: '{subject}'"


HITL_INSTRUCTIONS = """\
You are an inbox assistant. You can check inbox counts freely. If asked
to send an email, draft it and use send_email -- but you understand that
action will pause for human approval before it actually sends.
"""


async def main():
    agent = make_agent("InboxAgent", HITL_INSTRUCTIONS, tools=[check_inbox_count, send_email])

    print("=== Read action (no approval gate) ===")
    result = await agent.run("How many unread messages are in my inbox?")
    print(result, "\n")

    print("=== Write action (approval gate) ===")
    print("The next call will pause at send_email until a human approves it.")
    print("In a real deployment this surfaces through your approval channel")
    print("(Teams/email/a CLI prompt) -- exactly like Deploy-Approval-Agent")
    print("\n")
    result = await agent.run(
        "Send an email to team@example.com with subject 'Status' and a short "
        "one-line body saying the demo is working."
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
