import httpx
from agents import function_tool
from config import TAVILY_API_KEY

TAVILY_URL = "https://api.tavily.com/search"


@function_tool
def search_web(query: str) -> str:
    """Search the web for information using Tavily search API.

    Use this tool when the user asks about current events, general knowledge,
    or information that may be beyond the LLM's training data.

    Args:
        query: The search query string (e.g., "latest AI news 2026").
    """
    try:
        response = httpx.post(
            TAVILY_URL,
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": 5,
                "search_depth": "basic",
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            return f"No results found for '{query}'."

        formatted = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "Untitled")
            url = r.get("url", "")
            content = r.get("content", "No preview available.")
            formatted.append(f"{i}. {title}\n   URL: {url}\n   {content}")

        answer = data.get("answer")
        if answer:
            formatted.insert(0, f"Summary: {answer}")

        return "\n\n".join(formatted)

    except httpx.HTTPStatusError as e:
        return f"Error: Search API returned status {e.response.status_code}."
    except httpx.RequestError:
        return "Error: Could not connect to the search service. Please check your internet connection."
    except (KeyError, IndexError) as e:
        return f"Error: Unexpected response format from search API: {e}"
