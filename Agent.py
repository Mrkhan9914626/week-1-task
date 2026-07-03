from agents import Agent, Runner, RunResult, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from config import GEMINI_API_KEY
from tools import calculate, get_weather, search_web

api_key = GEMINI_API_KEY

external_client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key
)

model = OpenAIChatCompletionsModel(
    model="gemini-3.1-flash-lite-preview",
    openai_client=external_client  
)



SYSTEM_INSTRUCTION = (
    "You are a helpful AI assistant with access to three tools:\n"
    "1. **Calculator** — evaluate mathematical expressions (e.g., '2 + 2', 'math.sqrt(144)').\n"
    "2. **Weather** — get the current weather for any city using OpenWeatherMap.\n"
    "3. **Web Search** — search the web using Tavily for up-to-date information.\n\n"
    "When a user asks a question, decide which tool(s) to use. "
    "If you need the answer to a tool call to respond to the user, call the tool. "
    "Be concise, clear, and helpful."
)


def create_agent() -> Agent:
    return Agent(
        name="AgenticAssistant",
        instructions=SYSTEM_INSTRUCTION,
        tools=[calculate, get_weather, search_web],
        model=model
    )


async def run_agent(query: str, history: list[dict] | None = None) -> RunResult:
    """Run the agent with the given query and optional conversation history.

    Args:
        query: The user's message.
        history: Previous conversation turns as a list of input items
            (from RunResult.to_input_list()).

    Returns:
        A RunResult with the agent's final response.
    """
    agent = create_agent()

    if history:
        input_items = history + [{"role": "user", "content": query}]
    else:
        input_items = query

    return await Runner.run(agent, input=input_items)
