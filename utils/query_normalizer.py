import re

def normalize_query(q: str) -> str:
    """
    Normalize query for better KB matching.
    - Lowercase
    - Remove punctuation
    - Apply synonyms
    - Collapse whitespace
    """
    q = q.lower().strip()
    q = re.sub(r"[^\w\s]", " ", q)  # drop punctuation
    q = re.sub(r"\s+", " ", q)       # collapse whitespace
    
    # Synonyms
    q = q.replace("theme", "mode")
    q = q.replace("how do i enable", "enable")
    q = q.replace("how to enable", "enable")
    q = q.replace("how can i", "")
    
    return q.strip()
