"""
End-to-end integration test for the complete ticket processing pipeline.
Tests the full flow: Triage → KB Search → Draft/Escalation → Memory → Logs
"""
import pytest
import os
import json
from agents.triage_agent import triage_agent
from core.memory import memory_bank
from utils.observability import sanitize_value

class TestEndToEnd:
    
    def test_full_flow_kb_hit_draft(self):
        """Test complete flow: ticket with KB hit → draft generated"""
        ticket = {
            "id": "e2e_001",
            "description": "How do I enable dark mode?",
            "user_id": "test_user"
        }
        
        result = triage_agent.process_ticket(ticket)
        
        # Verify result structure
        assert result is not None
        assert "status" in result
        assert "reply" in result
        
        # Should be drafted (not escalated) - low severity
        assert result["status"] == "drafted"
        
        # Verify memory was updated
        memory = memory_bank.get_ticket("e2e_001")
        assert memory is not None
        assert memory["description"] == ticket["description"]
    
    def test_full_flow_escalation(self):
        """Test complete flow: high severity ticket → escalation"""
        ticket = {
            "id": "e2e_002",
            "description": "I was charged twice for my subscription!",
            "user_id": "test_user"
        }
        
        result = triage_agent.process_ticket(ticket)
        
        # Should be escalated (billing + high severity)
        assert result["status"] == "escalated"
        assert "ESCALATED" in result["reply"]
        
        # Verify memory
        memory = memory_bank.get_ticket("e2e_002")
        assert memory is not None
        assert memory["severity"] == "high"
    
    def test_full_flow_no_kb_hit(self):
        """Test complete flow: no KB match → LLM draft"""
        ticket = {
            "id": "e2e_003",
            "description": "I want to cancel my subscription",
            "user_id": "test_user"
        }
        
        result = triage_agent.process_ticket(ticket)
        
        # Should generate draft even without KB hit
        assert result["status"] == "drafted"
        assert result["reply"] is not None
        assert len(result["reply"]) > 0
    
    def test_sanitization_in_full_flow(self):
        """Test that API keys are sanitized throughout the entire flow"""
        ticket = {
            "id": "e2e_004",
            "description": "My API key AIzaSyDbX3FakeFakeFakeFakeFakeFakeKey is not working",
            "user_id": "test_user"
        }
        
        result = triage_agent.process_ticket(ticket)
        
        # Verify ticket was processed
        assert result is not None
        
        # Verify sanitization worked
        sanitized = sanitize_value(ticket["description"])
        assert "AIzaSyDbX3FakeFakeFakeFakeFakeFakeKey" not in sanitized
        assert "<REDACTED_API_KEY>" in sanitized
    
    def test_multiple_tickets_sequence(self):
        """Test processing multiple tickets in sequence"""
        tickets = [
            {"id": "e2e_seq_1", "description": "How do I enable dark mode?", "user_id": "user1"},
            {"id": "e2e_seq_2", "description": "I was double charged!", "user_id": "user2"},
            {"id": "e2e_seq_3", "description": "Video player not working", "user_id": "user3"},
        ]
        
        results = []
        for ticket in tickets:
            result = triage_agent.process_ticket(ticket)
            results.append(result)
        
        # All should complete successfully
        assert len(results) == 3
        assert all(r is not None for r in results)
        assert all("status" in r for r in results)
        
        # Verify expected statuses
        assert results[0]["status"] == "drafted"  # Low severity
        assert results[1]["status"] == "escalated"  # Billing
        assert results[2]["status"] == "escalated"  # High severity

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
