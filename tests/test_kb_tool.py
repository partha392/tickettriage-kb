"""
Unit tests for KB Search Tool
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.kb_tool import kb_tool, normalize_query

def test_normalize_query():
    """Test query normalization"""
    assert normalize_query("How do I enable dark mode?") == "enable dark mode"
    assert normalize_query("  DARK MODE  ") == "dark mode"

def test_kb_search_dark_mode():
    """Test KB search for dark mode"""
    results = kb_tool.search("dark mode")
    assert len(results) > 0
    assert any("dark mode" in r["title"].lower() or "dark mode" in r["content"].lower() for r in results)

def test_kb_search_billing():
    """Test KB search for billing"""
    results = kb_tool.search("billing duplicate charge")
    assert len(results) > 0

def test_kb_search_no_results():
    """Test KB search with no matches"""
    results = kb_tool.search("xyzabc123nonexistent")
    assert len(results) == 0

def test_kb_search_returns_max_3():
    """Test KB search returns max 3 results"""
    results = kb_tool.search("the")
    assert len(results) <= 3
