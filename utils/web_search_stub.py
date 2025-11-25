# utils/web_search_stub.py
"""
Local web-search fallback for offline / test runs.

Returns a normalized dict:
{
  "source": "kb_fallback",
  "query": "<original query>",
  "results": [
    {"title": "...", "snippet": "...", "url": "...", "source": "kb"},
    ...
  ]
}
"""
from typing import Dict, Any, List
from tools.kb_tool import kb_tool  # uses the global KBSearchTool instance
from utils.observability import logger, log_trace

MAX_SNIPPET_LEN = 300

@log_trace
def web_search_stub(query: str, max_results: int = 3) -> Dict[str, Any]:
    """
    Query the local KB as a fallback "web search".
    Returns a normalized structure that other parts of the code expect.
    """
    if not isinstance(query, str) or not query.strip():
        logger.log_event("web_search_stub.error", {"query": query, "error": "Empty or invalid query"})
        return {"source": "kb_fallback", "query": query, "results": []}

    # Use the project's KB search tool (which returns a list of KB entries)
    try:
        kb_results = kb_tool.search(query)
    except Exception as e:
        logger.log_event("web_search_stub.error", {"query": query, "error": str(e)})
        kb_results = []

    normalized: List[Dict[str, Any]] = []
    for item in (kb_results or [])[:max_results]:
        title = item.get("title", "") if isinstance(item, dict) else ""
        content = item.get("content", "") if isinstance(item, dict) else ""
        url = item.get("url", "") if isinstance(item, dict) else ""
        snippet = content.strip().replace("\n", " ")
        if len(snippet) > MAX_SNIPPET_LEN:
            snippet = snippet[:MAX_SNIPPET_LEN].rsplit(" ", 1)[0] + "..."

        normalized.append({
            "title": title,
            "snippet": snippet,
            "url": url,
            "source": "kb"
        })

    result = {"source": "kb_fallback", "query": query, "results": normalized}
    logger.log_event("web_search_stub.result", {"query": query, "hits": len(normalized)})
    return result


if __name__ == "__main__":
    # quick local smoke check
    q = "dark mode"
    print("Running local web_search_stub smoke test for query:", q)
    print(web_search_stub(q, max_results=3))