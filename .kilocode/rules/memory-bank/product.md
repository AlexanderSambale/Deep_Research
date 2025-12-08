# Deep Research – Product Overview

## Purpose
A programmable, multi‑agent research assistant that can:
- Interpret a user’s research request.
- Decompose the request into sub‑topics.
- Dispatch parallel research agents to gather information via web search (Tavily) and summarisation.
- Aggregate, compress, and refine findings into a polished report.

## Core Goals
- **Automation** – minimise manual prompting by using LangGraph state machines.
- **Scalability** – support concurrent sub‑agents (configurable max_concurrent_researchers).
- **Extensibility** – easy to add new tools, prompts, or agent types.
- **Transparency** – retain raw notes and tool observations for auditability.