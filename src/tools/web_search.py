from ddgs import DDGS
from ddgs.exceptions import DDGSException

from src.tools.base import Tool

DEFAULT_MAX_RESULTS = 5
MAX_RESULTS_CAP = 10
SNIPPET_MAX_LENGTH = 200


class WebSearchTool(Tool):
    name = "web_search"
    description = "Searches the web and returns a compact list of results (title, snippet, URL)."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query, e.g. 'Google Gemini API'"},
            "max_results": {"type": "integer", "description": "Maximum number of results (default 5)"},
        },
        "required": ["query"],
    }

    def run(self, args: dict) -> str:
        query = args["query"]
        max_results = min(args.get("max_results", DEFAULT_MAX_RESULTS), MAX_RESULTS_CAP)

        try:
            results = DDGS().text(query, max_results=max_results)
        except DDGSException as e:
            return f"Fehler bei der Websuche: {e}"
        except Exception as e:
            return f"Fehler bei der Websuche: {e}"

        if not results:
            return f"Keine Ergebnisse für '{query}' gefunden."

        lines = []
        for i, r in enumerate(results, start=1):
            snippet = r.get("body", "")[:SNIPPET_MAX_LENGTH]
            lines.append(f"{i}. {r.get('title', '')}\n   {snippet}\n   {r.get('href', '')}")
        return "\n".join(lines)


web_search = WebSearchTool()
