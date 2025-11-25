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
                results = list(self.ddgs.text(query, max_results=max_results, backend="html"))
            except Exception:
                # Fallback to default backend if html fails
                try:
                    results = list(self.ddgs.text(query, max_results=max_results))
                except Exception as e:
                    print(f"Search failed: {e}")
                    logger.log_event("web_search.error", {"query": query, "error": str(e), "backend_fallback_failed": True})
                    return []
            logger.log_event("web_search.success", {"query": query, "hits": len(results)})
            
            # Normalize keys to match KB format (title, url, snippet)
            normalized = []
            for r in results:
                normalized.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "snippet": r.get("body"),
                    "source": "web"
                })
            return normalized
        except Exception as e:
            logger.log_event("web_search.error", {"query": query, "error": str(e)})
            return []

# Global instance
web_search_tool = WebSearchTool()
