import os
import json
import google.generativeai as genai
from utils.observability import logger, log_trace
from agents.draft_agent import draft_agent
from agents.escalation_agent import escalation_agent
from tools.kb_tool import kb_tool
from core.memory import memory_bank, session_manager
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

class TriageAgent:
    def __init__(self, model_name=None):
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        self.model = genai.GenerativeModel(self.model_name)

    def process_ticket(self, ticket: dict) -> dict:
        """
        Main entry point for processing a ticket.
        """
        ticket_id = ticket.get("id")
        user_query = ticket.get("description")
        
        logger.log_event("triage.start", {"ticket_id": ticket_id})
        
        # 1. Analyze Ticket (Intent, Severity, Category)
        analysis = self._analyze_ticket(user_query)
        logger.log_event("triage.analysis", analysis)
        
        # Save to memory
        ticket_data = {**ticket, **analysis}
        memory_bank.add_ticket(ticket_data)
        
        response = {}
        
        # 2. Decision Logic
        if analysis.get("severity") == "high" or analysis.get("category") == "billing_dispute":
            # Escalate immediately
            reason = f"High severity or billing dispute detected: {analysis.get('reasoning')}"
            escalation_result = escalation_agent.handle_escalation(ticket_id, reason, ticket)
            response = {"status": "escalated", "reply": escalation_result}
            
        else:
            # Standard flow: KB Search -> Draft
            # Search KB
            kb_results = kb_tool.search(user_query)
            
            # Check history
            history = memory_bank.get_similar_tickets(analysis.get("category"))
            
            # Draft Reply
            draft = draft_agent.generate_draft(user_query, kb_results, history)
            response = {"status": "drafted", "reply": draft, "kb_hits": len(kb_results)}

        logger.log_event("triage.finish", {"ticket_id": ticket_id, "status": response["status"]})
        return response

    def _classify_ticket(self, description: str) -> dict:
        """Simple rule-based classification for offline mode."""
        desc_lower = description.lower()
        
        # Billing (high priority)
        if any(word in desc_lower for word in ['charge', 'billing', 'refund', 'payment', 'double']):
            return {"category": "billing", "severity": "high", "reasoning": "Billing issue detected"}
        
        # Account access (high priority)
        if any(word in desc_lower for word in ['login', 'password', 'account', 'access']):
            return {"category": "account_access", "severity": "high", "reasoning": "Account access issue"}
        
        # Technical issues (high priority) - expanded detection
        if any(word in desc_lower for word in ['crash', 'error', 'not working', 'broken', 'bug', 'player', 'video']):
            return {"category": "technical_issue", "severity": "high", "reasoning": "Technical issue detected"}
        
        # Feature requests (low priority)
        if any(word in desc_lower for word in ['dark mode', 'feature', 'enable', 'how do i', 'how to']):
            return {"category": "feature_request", "severity": "low", "reasoning": "Feature request or question"}
        
        return {"category": "other", "severity": "low", "reasoning": "General inquiry"}

# Global instance
triage_agent = TriageAgent()
