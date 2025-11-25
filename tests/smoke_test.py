import json
from tools.kb_tool import kb_tool
from utils.web_search_stub import web_search_stub
from evaluation.evaluate import _parse_score_from_text

def test_kb():
    r = kb_tool.search("dark mode")
    print("KB hits:", len(r))
    if len(r):
        print("Sample KB item:", json.dumps(r[0], indent=2)[:400])

def test_stub():
    r = web_search_stub("dark mode")
    print("Stub result (normalized):", json.dumps(r, indent=2)[:800])

def test_parse():
    samples = ["5 - Excellent", "4 good", "three", "no number here"]
    for s in samples:
        print(f"parse('{s}') ->", _parse_score_from_text(s))

if __name__ == "__main__":
    print("Running smoke tests...")
    test_kb()
    test_stub()
    test_parse()
    print("\nSmoke tests complete. Do NOT run evaluate_response here unless you set GOOGLE_API_KEY.")
