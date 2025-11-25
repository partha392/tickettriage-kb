from duckduckgo_search import DDGS
from utils.observability import logger, log_trace

class WebSearchTool:
    def __init__(self):
        self.ddgs = DDGS()

    @log_trace
    def search(self, query: str, max_results: int = 5) -> list:
        """
        Search the web using DuckDuckGo.
        Returns a list of dicts: {"title": str, "href": str, "body": str}
        """
        try:
            try:
                # Try 'api' backend first (smarter, better ranking)
                results = list(self.ddgs.text(query, max_results=max_results, backend="api", region="us-en"))
                if not results:
                    raise ValueError("No results from API backend")
            except Exception as e:
                # Fallback to 'html' backend if api fails or returns nothing
                print(f"API backend failed ({e}), falling back to HTML...")
                results = list(self.ddgs.text(query, max_results=max_results, backend="html", region="us-en"))
        except Exception as e:
            print(f"Search failed: {e}")
            logger.log_event("web_search.error", {"query": query, "error": str(e), "backend_fallback_failed": True})
            return []

        logger.log_event("web_search.success", {"query": query, "hits": len(results)})
        
        # Normalize keys to match KB format (title, url, snippet)
        normalized_results = []
        print(f"\n--- Web Search Results ({len(results)}) ---")
        for r in results:
            snippet = r.get("body", "")
            print(f"- {r.get('title', 'No Title')}: {snippet[:100]}...")
            normalized_results.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": snippet,
                "source": "web"
            })
        print("-----------------------------------\n")
        return normalized_results

# Global instance
web_search_tool = WebSearchTool()
