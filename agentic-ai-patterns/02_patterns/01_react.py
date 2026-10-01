"""
02_patterns/01_react.py
=========================
PATTERN: ReAct (Reasoning + Acting)
 
The agent alternates between reasoning about what to do next and taking
an action (a tool call), observing the result, and reasoning again --
until it has enough to answer. This is the DEFAULT behavior of any
Agent Framework agent that has tools: you don't implement a separate
ReAct loop yourself, the framework's tool-calling loop already does it.
 
This demo makes that loop visible by giving the agent two tools it must
use in sequence -- it cannot answer correctly without reasoning about
which tool to call, observing the result, then reasoning about the next
one.
"""
import asyncio
from typing import Annotated
 
from pydantic import Field
 
from agent_framework import tool
from common.client import make_agent
 
 
@tool(approval_mode="never_require")
def get_stock_price(
    ticker: Annotated[str, Field(description="Stock ticker symbol.")],
) -> str:
    """Look up a (stubbed) stock price."""
    prices = {"MSFT": 480.25, "AAPL": 232.10}
    return f"{ticker}: ${prices.get(ticker.upper(), 'unknown')}"
 
 
@tool(approval_mode="never_require")
def convert_currency(
    amount: Annotated[float, Field(description="Amount to convert.")],
    to_currency: Annotated[str, Field(description="Target currency code, e.g. 'INR'.")],
) -> str:
    """Convert a USD amount to another currency (stubbed rate)."""
    rates = {"INR": 83.2, "EUR": 0.92}
    rate = rates.get(to_currency.upper())
    if rate is None:
        return f"No rate available for {to_currency}."
    return f"${amount} = {amount * rate:.2f} {to_currency.upper()}"
 
 
REACT_INSTRUCTIONS = """\
You answer questions that require looking up a stock price AND then
converting it to another currency. You must call get_stock_price first,
read the result, THEN decide the right input to convert_currency based
on what you observed. Do not guess the price yourself.
"""
 
 
async def main():
    agent = make_agent("ReActAgent", REACT_INSTRUCTIONS, tools=[get_stock_price, convert_currency])
 
    # Streaming makes the Thought -> Action -> Observation -> Thought loop
    # visible as it happens, rather than only seeing the final answer.
    #
    # Each streamed `update` carries a list of Content items, distinguished
    # by `.type`:
    #   - "function_call"   -> the model deciding to call a tool (THOUGHT + ACTION)
    #   - "function_result" -> the tool's raw return value          (OBSERVATION)
    #   - "text"            -> the model's natural-language output  (final answer,
    #                          or reasoning text, depending on the model)
    #
    # Printing .text alone (as earlier versions of this demo did) silently
    # drops the function_call / function_result content, so students only
    # ever see the final sentence and never the steps that produced it.
    print("=== ReAct trace (streaming) ===\n")
 
    async for update in agent.run(
        "What is MSFT's stock price, in Indian Rupees?", stream=True
    ):
        for content in update.contents:
            if content.type == "function_call":
                print(f"\n🔧 ACTION   -> {content.name}({content.arguments})")
            elif content.type == "function_result":
                print(f"   OBSERVE  <- {content.result}")
            elif content.type == "text" and content.text:
                print(content.text, end="", flush=True)
 
    print("\n")
 
 
if __name__ == "__main__":
    asyncio.run(main())