"""
common/client.py
==================
Same shared connection pattern used throughout the course. Kept short
here since students have already seen this in earlier modules.
"""
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_CHAT_DEPLOYMENT"]


def _check_env():
    missing = [v for v in REQUIRED_VARS if not os.environ.get(v)]
    if missing:
        raise RuntimeError(
            "Missing required environment variable(s): " + ", ".join(missing)
            + "\nCopy .env.example to .env and fill in your Foundry project details."
        )


def get_client() -> FoundryChatClient:
    _check_env()
    return FoundryChatClient(
        project_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        credential=AzureCliCredential(),
    )


def make_agent(name: str, instructions: str, tools: list | None = None) -> Agent:
    """Convenience wrapper so every demo script stays focused on the
    pattern it's teaching, not on client boilerplate."""
    return Agent(
        client=get_client(),
        name=name,
        instructions=instructions,
        tools=tools or [],
    )
