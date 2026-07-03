# Week 1 — Agentic Assistant with Tool Use

## Live App

Deployed at: [https://week-1-task-2jym6t94xuygymxn8iawdf.streamlit.app/](https://week-1-task-2jym6t94xuygymxn8iawdf.streamlit.app/)

## Objective
Build a Streamlit-based AI assistant using the OpenAI Agents SDK that responds to user queries by invoking three tools: calculator, weather lookup (OpenWeatherMap), and web search (Tavily). The agent uses Gemini 3.1 Flash Lite via an OpenAI-compatible endpoint while leveraging the OpenAI Agents SDK for tool orchestration.

## Architecture

```
User Query (Streamlit Chat UI)
        │
        ▼
┌──────────────────────────────────────────┐
│            Agent Runner                  │
│   (OpenAI Agents SDK Runner.run())       │
│   │                                      │
│   ├── Model: gemini-3.1-flash-lite       │
│   │   (via OpenAI-compatible endpoint)   │
│   ├── Tools registered:                  │
│   │   ├── Calculator                     │
│   │   ├── Weather (OpenWeatherMap)       │
│   │   └── Web Search (Tavily)            │
│   └── Built-in agent loop                │
└──────────────────────────────────────────┘
        │
        ▼
    Response back to Streamlit
```

## Tools

### Calculator
- Function: `calculate(expression: str) → str`
- Implementation: A restricted `eval()` with `globals={}` and `locals={}` containing only `{"math": math}`.
  The expression is regex-validated to only contain digits, spaces, math operators (`+`, `-`, `*`, `/`, `**`, `//`, `%`), parentheses, and `math.` function calls.
- Returns: Evaluated result as string or an error message if the expression is invalid.

### Weather (OpenWeatherMap)
- Function: `get_weather(city: str) → str`
- Implementation: Calls `https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric`.
- Returns: Formatted string with temperature, feels-like, condition description, humidity, and wind speed.

### Web Search (Tavily)
- Function: `search_web(query: str) → str`
- Implementation: Calls Tavily Search API, returns top 5 results.
- Returns: Formatted string with numbered results (title, URL, content snippet each).

## Project Structure

```
internship/
├── .env                        # API keys (OPENAI_API_KEY, WEATHER_API_KEY, TAVILY_API_KEY)
├── .gitignore
├── .python-version             # Python version pinning
├── README.md                   # Setup instructions, usage, screenshots
├── pyproject.toml              # Project metadata and dependencies (uv)
├── uv.lock                     # Lockfile for uv
├── app.py                      # Streamlit entry point with chat UI
├── config.py                   # Load environment variables
├── Agent.py                    # Create agent with instructions, tools, and run function
└── tools/
    ├── __init__.py             # Re-exports calculate, get_weather, search_web
    ├── calculator.py           # Calculator tool (restricted eval)
    ├── weather.py              # OpenWeatherMap tool
    └── search.py               # Tavily search tool
```

## Data Flow

1. User types a query in the Streamlit chat input
2. Query is appended to `st.session_state.messages`
3. `Agent.py:run_agent()` is called with the full message history
4. OpenAI Agents SDK `Runner.run()` invokes the agent loop:
   - LLM decides whether to respond directly or call a tool
   - If tool call: SDK executes the tool function, feeds result back to LLM
   - Loop continues until LLM produces a final response
5. Final response is appended to session messages and displayed

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Agent SDK | OpenAI Agents SDK | Built-in agent loop, tool registration, minimal boilerplate |
| Model | gemini-3.1-flash-lite-preview | Fast, cost-effective, reliable function calling (via OpenAI-compatible endpoint) |
| LLM Client | `openai` SDK pointed at Gemini endpoint | Lets the OpenAI Agents SDK work with a Gemini model without extra adapters |
| Calculator safety | Restricted eval | Only numeric math ops, no builtins, no IO |
| UI | Streamlit | Required by internship spec, simple chat interface |
| Async bridge | `asyncio.run()` | Agents SDK is async; Streamlit runs synchronously |
| Package manager | uv | Fast, modern Python package management with lockfile |
| Dependencies | pyproject.toml | PEP 621 standard; replaces requirements.txt |

