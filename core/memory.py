import json
import os
from typing import List, Dict, Any
from utils.observability import logger

MEMORY_FILE = "core/memory_bank.json"

class MemoryBank:
    def __init__(self, filepath=MEMORY_FILE):
        self.filepath = filepath
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = {"tickets": [], "escalations": []}
        else:
            self.data = {"tickets": [], "escalations": []}
            self._save_memory()

    def _save_memory(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_ticket(self, ticket_data: Dict[str, Any]):
        """Saves a processed ticket to history."""
        self.data["tickets"].append(ticket_data)
        self._save_memory()
        logger.log_event("memory.add_ticket", {" ticket_id": ticket_data.get("id")})
    
    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Retrieves a ticket from memory by ID. Returns None if not found."""
        for ticket in self.data["tickets"]:
            if ticket.get("id") == ticket_id:
                return ticket
        return None

    def get_similar_tickets(self, category: str) -> List[Dict]:
        """Simple retrieval of tickets by category."""
        return [t for t in self.data["tickets"] if t.get("category") == category][-3:] # Return last 3

    def log_escalation(self, ticket_id: str, reason: str):
        self.data["escalations"].append({"ticket_id": ticket_id, "reason": reason, "timestamp": str(datetime.now())})
        self._save_memory()

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def get_session(self, session_id: str) -> Dict:
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "history": [],
                "context": {},
                "last_interaction": None
            }
        return self.sessions[session_id]

    def update_session(self, session_id: str, key: str, value: Any):
        session = self.get_session(session_id)
        session["context"][key] = value
        
    def add_turn(self, session_id: str, role: str, content: str):
        session = self.get_session(session_id)
        session["history"].append({"role": role, "content": content})

# Global instances
memory_bank = MemoryBank()
session_manager = SessionManager()

from datetime import datetime
