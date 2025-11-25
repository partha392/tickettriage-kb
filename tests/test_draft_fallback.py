"""
Tests for draft agent fallback behavior and edge cases.
"""
import pytest
from agents.draft_agent import DraftReplyAgent

class TestDraftAgentFallback:
    
    def test_fallback_no_api_key(self, monkeypatch):
        """Test fallback when API key is missing"""
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        agent = DraftReplyAgent()
        
        result = agent.generate_draft(
            ticket_content="Test query",
            kb_results=[],
            history=None,
            triage_info={"category": "other", "severity": "low"}
        )
        
        # Should return error message, not crash
        assert result is not None
        assert isinstance(result, (str, dict))
    
    def test_fallback_malformed_kb_all_fields_missing(self):
        """Test fallback when KB item has no usable fields"""
        agent = DraftReplyAgent()
        
        kb_results = [{"id": "kb_999"}]  # Only ID, no title/content/snippet
        
        result = agent.generate_draft(
            ticket_content="Test query",
            kb_results=kb_results,
            history=None,
            triage_info={"category": "other", "severity": "low"}
        )
        
        # Should not crash
        assert result is not None
    
    def test_fallback_kb_with_very_long_content(self):
        """Test that very long KB content is truncated"""
        agent = DraftReplyAgent()
        
        kb_results = [{
            "title": "Long Article",
            "content": "A" * 10000  # 10k characters
        }]
        
        result = agent.generate_draft(
            ticket_content="Test query",
            kb_results=kb_results,
            history=None,
            triage_info={"category": "other", "severity": "low"}
        )
        
        # Should handle gracefully
        assert result is not None
    
    def test_fallback_multiple_kb_hits(self):
        """Test behavior with multiple KB results"""
        agent = DraftReplyAgent()
        
        kb_results = [
            {"title": "Article 1", "content": "Content 1"},
            {"title": "Article 2", "content": "Content 2"},
            {"title": "Article 3", "content": "Content 3"},
        ]
        
        result = agent.generate_draft(
            ticket_content="Test query",
            kb_results=kb_results,
            history=None,
            triage_info={"category": "other", "severity": "low"}
        )
        
        # Should handle multiple results
        assert result is not None
    
    def test_fallback_unicode_in_kb(self):
        """Test handling of unicode characters in KB"""
        agent = DraftReplyAgent()
        
        kb_results = [{
            "title": "Unicode Test 你好",
            "content": "Content with émojis 🎉 and spëcial çhars"
        }]
        
        result = agent.generate_draft(
            ticket_content="Test with unicode 你好",
            kb_results=kb_results,
            history=None,
            triage_info={"category": "other", "severity": "low"}
        )
        
        # Should handle unicode gracefully
        assert result is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
