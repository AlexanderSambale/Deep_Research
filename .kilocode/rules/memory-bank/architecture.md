# System Architecture Overview

## Major Components
1. **Prompts (`src/prompts.py`)** – System‑level instructions for:
   - Scoping the research question.
   - Guiding the research agent loop.
   - Supervisory decision‑making.
2. **Utilities (`src/utils.py`)** – LangChain tools:
   - `tavily_search` (search + summarise)
   - `think_tool` (reflection)
   - `refine_draft_report` (final report synthesis)
3. **Research Agent (`src/research_agent.py`)**
   - LangGraph state machine: `llm_call → tool_node → compress_research`.
   - Handles iterative searching, reflection, and compression of findings.
4. **Supervisor (`src/multi_agent_supervisor.py`)**
   - Coordinates multiple `research_agent` instances.
   - Manages iteration limits, parallelism, and aggregation of notes.
5. **State Definitions**
   - `ResearcherState`, `SupervisorState`, `AgentState`, etc. (typed with `TypedDict`/`BaseModel`).
6. **Entry Point (`src/state_scope.py`)**
   - Top‑level graph that receives user messages and starts the supervisor.

## Data Flow
```
User Input → Supervisor (scoping) → Research Brief
          ↳ Parallel Research Agents (search → think → compress)
          ↳ Aggregated Notes → `refine_draft_report` → Draft Report → Final Report
```

## Execution Model
- **Async‑compatible**: Supervisor launches research agents concurrently using `asyncio.gather`.
- **Iteration Limits**: `max_researcher_iterations` (default 15) prevents infinite loops.
- **Tool Binding**: LLMs are bound to the custom tools for seamless invocation.