# Agentic AI Patterns — Part 1: Single vs Multi-Agent, and the 7 Patterns

Companion repo to `Agentic_AI_Part1_Teaching_Guide.docx`. Every script
runs standalone and prints its own trace so a concept can be demoed live
without scrolling through unrelated code.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
az login
cp .env.example .env   # fill in your Foundry project endpoint + deployment
```

## Run order (matches the Teaching Guide's sequence)

```bash
# Module 1: Single vs Multi-Agent
python 01_single_vs_multi_agent/single_agent_demo.py
python 01_single_vs_multi_agent/multi_agent_demo.py

# Module 2: The 7 Patterns
python 02_patterns/01_react.py
python 02_patterns/02_reflection.py
python 02_patterns/03_planning.py
python 02_patterns/04_tool_use.py
python 02_patterns/05_routing.py
python 02_patterns/06_multi_agent_collaboration.py
python 02_patterns/07_human_in_the_loop.py
python 02_patterns/08_agent_communication.py
```

## Layout

```
agentic-ai-patterns/
├── common/
│   └── client.py                       # shared Foundry connection helper
├── 01_single_vs_multi_agent/
│   ├── single_agent_demo.py
│   ├── multi_agent_demo.py
│   └── README.md                       # what to compare between the two runs
├── 02_patterns/
│   ├── 01_react.py
│   ├── 02_reflection.py
│   ├── 03_planning.py
│   ├── 04_tool_use.py
│   ├── 05_routing.py
│   ├── 06_multi_agent_collaboration.py
│   ├── 07_human_in_the_loop.py
│   └── 08_agent_communication.py
├── requirements.txt / pyproject.toml
├── .env.example
└── README.md
```

## A note on the stub tools

Every tool in this repo (search, stock price, weather, email) returns
fixed stub data so the demos run with zero external dependencies and
zero cost beyond the model calls themselves. Swap any `_stub` function
for a real API call once you're comfortable with the pattern — the
`@tool` decorator and the agent's behavior around it don't change.
