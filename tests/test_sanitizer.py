import pytest
from utils.observability import sanitize_value

def test_redacts_google_key():
    """Test that Google API keys are redacted."""
    text = "My key: AIzaSyDbX3FakeFakeFakeFakeFakeFakeKey"
    out = sanitize_value(text)
    assert "<REDACTED_API_KEY>" in out
    assert "AIzaSyDbX3FakeFakeFakeFakeFakeFakeKey" not in out

def test_redacts_aws_key():
    """Test that AWS keys are redacted."""
    text = "AWS key: AKIAIOSFODNN7EXAMPLE"
    out = sanitize_value(text)
    assert "<REDACTED_API_KEY>" in out
    assert "AKIAIOSFODNN7EXAMPLE" not in out

def test_redacts_generic_tokens():
    """Test that generic API tokens are redacted."""
    text = "api_key=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567890abcdef"
    out = sanitize_value(text)
    assert "<REDACTED" in out
    assert "abc123def456" not in out

def test_truncates_long_strings():
    """Test that long strings are truncated."""
    text = "This is a very long support ticket description. " * 20  # Mixed chars, won't trigger token pattern
    out = sanitize_value(text, max_len=100)
    assert len(out) < 120  # 100 + truncation marker
    assert "TRUNCATED" in out

def test_sanitizes_nested_dicts():
    """Test that nested dictionaries are sanitized."""
    data = {
        "user": "test",
        "credentials": {
            "api_key": "AIzaSyDbX3FakeFakeFakeFakeFakeFakeKey"
        }
    }
    out = sanitize_value(data)
    assert "<REDACTED_API_KEY>" in str(out)
    assert "AIzaSyDbX3FakeFakeFakeFakeFakeFakeKey" not in str(out)

def test_preserves_safe_content():
    """Test that safe content is preserved."""
    text = "This is a normal support ticket about dark mode"
    out = sanitize_value(text)
    assert out == text

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
