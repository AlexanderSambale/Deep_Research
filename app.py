import os
import sys
import asyncio

import streamlit as st
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Import the builder from the project source
from src.research_agent_full import deep_researcher_builder
from src.utils import (
    MODEL_CONFIG,
    MODEL,
    BASE_URL,
    API_KEY,
    MODEL_CLASS,
    TAVILY_CLIENT,
    MAX_CONCURRENT_RESEARCHERS,
    MAX_RESEARCHER_ITERATIONS,
    CONFIGURABLE,
)

from tavily import TavilyClient
import langchain

langchain.debug = True

# Ensure the `src` package is on the import path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
load_dotenv()

# ----------------------------------------------------------------------
# UI layout
# ----------------------------------------------------------------------
st.set_page_config(page_title="Deep Research Demo", layout="wide")
st.title("🧠 Deep Research – Multi‑Agent Report Generator")

with st.sidebar:
    prompt = st.text_area(
        "Research Prompt",
        height=300,
        value=(
            "Write a paper to discuss the influence of AI interaction on interpersonal "
            "relations, considering AI's potential to fundamentally change how and why "
            "individuals relate to each other."
        ),
    )
    
    run_button = st.button("Run Research")

    st.header("Configuration")
    # Language model configuration (defaults from .env)
    model = st.text_input(
        "Model",
        value=os.getenv("MODEL", "qwen3-235b-a22b"),
        help="Name of the language model to use."
    )
    base_url = st.text_input(
        "Base URL",
        value=os.getenv("BASE_URL", "https://api.openai.com/v1/"),
        help="Base URL for the model API. OpenAI compatible Endpoint."
    )
    api_key = st.text_input(
        "API Key",
        type="password",
        value=os.getenv("API_KEY", ""),
        help="API key for the model service."
    )

    tavily_api_key = st.text_input(
        "Tavily API Key",
        type="password",
        value=os.getenv("TAVILY_KEY", ""),
        help="Tavily API key for the search service."
    )

# System constants (configurable via UI)
# Maximum number of tool call iterations for individual researcher agents
max_researcher_iterations = st.sidebar.number_input(
    "Max Researcher Iterations",
    min_value=1,
    max_value=100,
    value=15,
    step=1,
    help="Controls the depth of research per agent (prevents infinite loops).",
)

# Maximum number of concurrent research agents the supervisor can launch
max_concurrent_researchers = st.sidebar.number_input(
    "Max Concurrent Researchers",
    min_value=1,
    max_value=20,
    value=3,
    step=1,
    help="Limits how many agents run in parallel.",
)


# ----------------------------------------------------------------------
# Cached resources
# ----------------------------------------------------------------------
@st.cache_resource
def get_agent():
    """Create and compile the research agent (cached for the session)."""
    checkpointer = InMemorySaver()
    agent = deep_researcher_builder.compile(checkpointer=checkpointer)
    return agent


# ----------------------------------------------------------------------
# Main execution
# ----------------------------------------------------------------------
if run_button:
    agent = get_agent()
    model_class = ChatOpenAI
    tavily_client = TavilyClient(api_key=tavily_api_key)
    config = {
        "configurable": {"thread_id": "1", "recursion_limit": 50},
        MODEL_CONFIG: {
            MODEL: model,
            BASE_URL: base_url,
            API_KEY: api_key,
        },
        MODEL_CLASS: model_class,
        TAVILY_CLIENT: tavily_client,
        MAX_RESEARCHER_ITERATIONS: max_researcher_iterations,
        MAX_CONCURRENT_RESEARCHERS: max_concurrent_researchers,
    }

    async def invoke_agent():
        """Run the agent and return the result dict."""
        result = await agent.ainvoke(
            {"messages": [HumanMessage(content=prompt)]},
            config=config,
        )
        return result

    with st.spinner(
        "Running the research agent (this may take several minutes)…",
    ):
        try:
            result = asyncio.run(invoke_agent())
        except Exception as exc:
            st.error(f"Agent execution failed: {exc}")
            st.stop()
    # ------------------------------------------------------------------
    # Render the final report
    # ------------------------------------------------------------------
    st.subheader("📄 Final Report")
    final_report = result.get("final_report", "")
    if final_report:
        # The notebook used `rich.Markdown`; Streamlit can render Markdown directly.
        st.markdown(final_report)
    else:
        st.info("No report was returned by the agent.")
