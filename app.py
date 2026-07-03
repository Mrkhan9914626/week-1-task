import asyncio
from pathlib import Path

import streamlit as st

# Ensure the src package is importable
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from Agent import create_agent, run_agent

st.set_page_config(
    page_title="Agentic Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Agentic Assistant")
st.markdown(
    "I have access to **calculator**, **weather**, and **web search** tools. "
    "Ask me anything!"
)


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.input_history = []
    if "agent_initialized" not in st.session_state:
        # Validate API keys by attempting to create the agent
        try:
            create_agent()
            st.session_state.agent_initialized = True
        except ValueError as e:
            st.session_state.agent_initialized = False
            st.session_state.init_error = str(e)


def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


async def handle_query(user_input: str):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = await run_agent(
                    query=user_input,
                    history=st.session_state.input_history or None,
                )
                response = result.final_output
                st.markdown(response)
            except Exception as e:
                response = f"Sorry, an error occurred: {e}"
                st.error(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    init_session_state()

    if not st.session_state.agent_initialized:
        st.error(
            f"⚠️ Configuration error: {st.session_state.get('init_error', 'Unknown error')}"
        )
        st.info(
            "Make sure your `.env` file contains OPENAI_API_KEY, "
            "WEATHER_API_KEY, and TAVILY_API_KEY."
        )
        return

    display_chat_history()

    if prompt := st.chat_input("Ask me anything..."):
        asyncio.run(handle_query(prompt))


if __name__ == "__main__":
    main()
