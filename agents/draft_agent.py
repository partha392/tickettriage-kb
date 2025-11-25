import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
from utils.observability import logger, log_trace
from tools.web_search_tool import web_search_tool

load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


# ---------- Helper Functions ---------- #

def extract_json(text):
    """
    Extracts the first JSON object from model text output.
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None
    return None


def sanitize(text):
    """
    Remove any hallucinated instructions or system prompts.
    """
    banned = ["As an AI", "I cannot", "model cannot", "ChatGPT", "Gemini"]
    for b in banned:
        text = text.replace(b, "")
    return text.strip()


# ---------- Agent Class ---------- #

class DraftReplyAgent:
    def __init__(self, model_name=None):
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite-preview-02-05")
        self.model = genai.GenerativeModel(self.model_name)

    def generate_draft(self, ticket_content: str, kb_results: list, history: list = None, triage_info: dict = None):
        """
        Generate a structured and professional customer support reply.
        """

        if not GOOGLE_API_KEY:
            return json.dumps({
                "subject": "Missing API Key",
                "body": "GOOGLE_API_KEY not found. Cannot generate draft.",
                "action": "error"
            })
        
        # Fallback to Web Search if KB is empty
        if not kb_results:
            logger.log_event("draft_agent.web_fallback", {"query": ticket_content})
            web_results = web_search_tool.search(ticket_content)
            if web_results:
                kb_results = web_results

        # Format KB results (handle missing fields gracefully)
        def get_kb_snippet(item):
            """Extract snippet from KB item, trying multiple fields."""
            for key in ('snippet', 'content', 'summary', 'description'):
                val = item.get(key)
                if val:
                    # Truncate if too long
                    return val if len(val) <= 500 else val[:500] + "...<TRUNCATED>"
            return item.get('title', 'KB Result')
        
        kb_text = "\n".join([f"- {item.get('title', 'KB Result')}: {get_kb_snippet(item)}" for item in kb_results]) if kb_results else "No KB matches."

        memory_text = history if history else "No previous conversations found."

        category = triage_info.get("category", "unknown") if triage_info else "unknown"
        severity = triage_info.get("severity", "low") if triage_info else "low"

        # --- MAIN PROMPT --- #
        prompt = f"""
You are an enterprise-grade Tier-1 Customer Support Agent.

You must ALWAYS reply in **STRICT JSON** with:
{{
  "subject": "...",
  "body": "...",
  "action": "reply | escalate | request_info",
  "explain": "explanation for logs only"
}}

Rules:
- Professional, concise, helpful.
- If KB hits exist → summarize and use them.
- If Web Search Results exist → EXTRACT the specific answer (e.g., price, weather, news) and state it clearly. Even if the info is partial, provide what you found.
- If NO info found → ask for missing info politely.
- If severity is HIGH → automatically escalate.
- NEVER output anything outside the JSON.

Context:
Ticket: "{ticket_content}"
Category: {category}
Severity: {severity}

Knowledge Base / Web Results:
{kb_text}

Customer History:
{memory_text}

Write the JSON ONLY.
"""

        try:
            response = self.model.generate_content(prompt)
            raw = response.text

            parsed = extract_json(raw)

            # fallback if JSON fails
            draft = getattr(response, "text", "") or str(response)
            logger.log_event("draft_agent.success", {"draft_length": len(draft)})
            return draft
        except Exception as e:
            logger.log_event("draft_agent.error", {"error": str(e)})
            return "Error generating draft reply. Please check logs."


# Global instance
draft_agent = DraftReplyAgent()
