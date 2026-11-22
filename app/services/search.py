from tavily import TavilyClient
from app.config import TAVILY_API_KEY
import json

client = TavilyClient(api_key=TAVILY_API_KEY)

def search_web(query: str, max_results: int = 5) -> list[dict]:

    try:
        response = client.search(
            query,
            max_results=max_results
        )

        sources = []

        for result in response["results"]:
            sources.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("content", "")
            })

        return sources

    except Exception as e:
        raise RuntimeError(f"Web search failed for: {query}") from e


if __name__ == "__main__":
    query = "The impact of climate change on global agriculture"
    results = search_web(query, max_results=5)
    print(json.dumps(results, indent=4))
