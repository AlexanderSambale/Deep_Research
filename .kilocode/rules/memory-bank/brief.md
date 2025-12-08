# Project Brief

## Overview
Deep Research is a programmable multi‑agent research assistant that automates the process of gathering, synthesizing, and reporting information based on user queries. It leverages LangChain and LangGraph to orchestrate multiple research agents that perform web searches via Tavily, reflect on findings, and compress results into a polished report.

## Objectives
- Automate research workflow to minimize manual prompting.
- Scale to multiple parallel agents with configurable iteration limits.
- Provide extensibility for adding new tools, prompts, or agent types.
- Ensure transparency by retaining raw notes and tool observations.

## Scope
The system includes:
- Prompt templates (`src/prompts.py`) for scoping and reporting.
- Utility tools (`src/utils.py`) for searching, reflection, and report refinement.
- A research agent graph (`src/research_agent.py`) handling LLM calls and tool execution.
- A supervisor (`src/multi_agent_supervisor.py`) coordinating parallel agents and aggregating results.