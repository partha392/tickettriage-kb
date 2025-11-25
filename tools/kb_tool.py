import json
import os
import re
from typing import List, Dict
from utils.observability import logger, log_trace

KB_FILE = "tools/kb_data.json"

def normalize_query(q: str) -> str:
    """Normalize query for better KB matching."""
    q = q.lower().strip()
    q = re.sub(r"[^\w\s]", " ", q)  # drop punctuation
    q = re.sub(r"\s+", " ", q)       # collapse whitespace
    # Synonyms
    q = q.replace("theme", "mode")
    q = q.replace("how do i enable", "enable")
    q = q.replace("how to enable", "enable")
    return q.strip()

class KBSearchTool:
    def __init__(self, kb_path=KB_FILE):
        self.kb_path = kb_path
        self._load_kb()

    def _load_kb(self):
        if os.path.exists(self.kb_path):
            with open(self.kb_path, 'r') as f:
                self.kb = json.load(f)
        else:
            self.kb = []
            logger.log_event("kb_tool.error", {"error": "KB file not found", "path": self.kb_path})

    @log_trace
    def search(self, query: str) -> List[Dict]:
        """
        Searches the knowledge base for relevant articles.
        Token-based keyword matching with normalization for better recall.
        """
        # Normalize the query
        normalized_query = normalize_query(query)
        query_lower = normalized_query.lower()
        
        # Split query into meaningful tokens (filter out short words)
        tokens = [t for t in query_lower.split() if len(t) > 2]
        results = []
        
        for item in self.kb:
            # Combine title and content for searching, normalize them too
            combined = normalize_query(item["title"] + " " + item["content"]).lower()
            
            # Check if all tokens appear in the combined text
            if tokens and all(tok in combined for tok in tokens):
                results.append(item)
            # Fallback: original substring match
            elif query_lower in combined:
                if item not in results:
                    results.append(item)
        
        # Log the search results count
        logger.log_event("kb_tool.search", {"query": query, "hits": len(results)})
        
        return results[:3] # Return top 3

# Global instance
kb_tool = KBSearchTool()
