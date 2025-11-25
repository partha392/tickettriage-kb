import pytest
from agents.draft_agent import DraftReplyAgent

def test_kb_parse_missing_snippet():
    """Test that draft agent handles KB items without 'snippet' field."""
    agent = DraftReplyAgent()
    
    # KB item with only 'content' (no 'snippet')
    kb_results = [{
        "id": "kb_004",
        "title": "Feature Request - Dark Mode",
        "content": "Dark mode is currently in beta. Users can enable it by going to Settings > Display > Theme (Beta)."
    }]
    
    # Should not crash, should use 'content' as fallback
    draft = agent.generate_draft(
        ticket_content="How do I enable dark mode?",
        kb_results=kb_results,
        history=None,
        triage_info={"category": "feature_request", "severity": "low"}
    )
    
    # Verify draft was generated (not an error message)
    assert draft is not None
    assert "error" not in draft.lower() or "Error" not in draft
    assert len(draft) > 0

def test_kb_parse_with_snippet():
    """Test that draft agent handles KB items with 'snippet' field."""
    agent = DraftReplyAgent()
    
    # KB item with 'snippet' field (from web_search_stub)
    kb_results = [{
        "title": "Feature Request - Dark Mode",
        "snippet": "Dark mode is currently in beta.",
        "url": "",
        "source": "kb"
    }]
    
    draft = agent.generate_draft(
        ticket_content="How do I enable dark mode?",
        kb_results=kb_results,
        history=None,
        triage_info={"category": "feature_request", "severity": "low"}
    )
    
    assert draft is not None
    assert len(draft) > 0

def test_kb_parse_empty_results():
    """Test that draft agent handles empty KB results gracefully."""
    agent = DraftReplyAgent()
    
    draft = agent.generate_draft(
        ticket_content="How do I enable dark mode?",
        kb_results=[],
        history=None,
        triage_info={"category": "feature_request", "severity": "low"}
    )
    
    assert draft is not None
    assert len(draft) > 0

def test_kb_parse_malformed_item():
    """Test that draft agent handles malformed KB items."""
    agent = DraftReplyAgent()
    
    # KB item missing both 'snippet' and 'content'
    kb_results = [{
        "title": "Incomplete KB Item"
        # No snippet, content, summary, or description
    }]
    
    # Should not crash, should use title as fallback
    draft = agent.generate_draft(
        ticket_content="Test query",
        kb_results=kb_results,
        history=None,
        triage_info={"category": "other", "severity": "low"}
    )
    
    assert draft is not None
    assert len(draft) > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
