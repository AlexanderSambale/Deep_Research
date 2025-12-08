# Technical Stack

## Language
- Python ≥3.9

## Core Libraries
- **LangChain** – LLM orchestration, message handling.
- **LangGraph** – State‑graph construction (`StateGraph`, `Command`).
- **Pydantic** – Typed schemas for tool inputs/outputs.
- **Tavily** – Web‑search API client.
- **AsyncIO** – Concurrency for parallel research agents.
- **Nest‑asyncio** – Compatibility with Jupyter/IPython environments.

## Project Structure
- `src/` – All source code.
  - `prompts.py` – Prompt templates.
  - `utils.py` – Tool definitions.
  - `research_agent.py` – Single‑agent graph.
  - `multi_agent_supervisor.py` – Supervisor graph.
  - `state_*.py` – Typed state definitions.
- `.kilocode/rules/memory-bank/` – Documentation (brief, product, context, architecture, tech, tasks).

## Configuration
- Dependencies are listed in `pyproject.toml` (e.g., `langchain`, `langgraph`, `tavily`, `pydantic`, `typing‑extensions`).
- LLM models are instantiated via `init_chat_model(model="openai:gpt-5")`; can be swapped for other providers.

## Runtime Requirements
- Internet access for Tavily searches.
- Valid API key for the chosen LLM provider.
- Python environment with the above packages installed.