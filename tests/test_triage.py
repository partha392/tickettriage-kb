"""
Unit tests for Triage Agent
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set offline mode for tests
os.environ["OFFLINE_MODE"] = "1"

from agents.triage_agent import triage_agent

def test_process_ticket_structure():
    """Test that process_ticket returns correct structure"""
    ticket = {
        "id": "test_001",
        "description": "Test ticket",
        "user_id": "test_user"
    }
    
    result = triage_agent.process_ticket(ticket)
    
    assert "status" in result
    assert "reply" in result
    assert result["status"] in ["drafted", "escalated"]

def test_billing_escalation():
    """Test that billing issues are escalated"""
    ticket = {
        "id": "test_002",
        "description": "I was double charged for my subscription",
        "user_id": "test_user"
    }
    
    result = triage_agent.process_ticket(ticket)
    assert result["status"] == "escalated"

def test_feature_request_drafted():
    """Test that feature requests are drafted"""
    ticket = {
        "id": "test_003",
        "description": "How do I enable dark mode?",
        "user_id": "test_user"
    }
    
    result = triage_agent.process_ticket(ticket)
    assert result["status"] == "drafted"
