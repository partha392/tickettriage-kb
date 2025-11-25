import os
import csv
import time
import re
import google.generativeai as genai
from agents.triage_agent import triage_agent
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

EVAL_PROMPTS_FILE = "docs/evaluation_prompts.txt"
EVAL_RESULTS_FILE = "docs/evaluation.csv"

def _parse_score_from_text(text: str) -> int:
    """
    Robustly parse an integer score 1-5 from an LLM response.
    Returns -1 if no clear score found.
    
    Examples it supports:
      - "5"
      - "5 - Excellent"
      - "Score: 4"
      - "I give this a 3/5"
      - "four" -> 4
    """
    if not text:
        return -1
    
    s = text.strip().lower()
    
    # Direct digits 1-5
    m = re.search(r'\b([1-5])\b', s)
    if m:
        return int(m.group(1))
    
    # Digits with slash e.g. 4/5
    m = re.search(r'\b([1-5])\s*/\s*5\b', s)
    if m:
        return int(m.group(1))
    
    # Spelled-out words
    words_map = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "1": 1, "2": 2, "3": 3, "4": 4, "5": 5
    }
    for word, val in words_map.items():
        if re.search(r'\b' + re.escape(word) + r'\b', s):
            return val
    
    return -1

def evaluate_response(query, response, expected_category=None, max_retries=2, backoff=1.0):
    """
    Uses an LLM to judge the quality of the response.
    Returns: (score:int 1..5, reason:str)
    """
    if not GOOGLE_API_KEY:
        return 0, "No API Key"

    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite-preview-02-05")
    model = genai.GenerativeModel(model_name)

    prompt = f"""
You are an expert customer support quality assurance judge.
Evaluate the following response to a customer ticket.

Ticket: "{query}"
System Response: "{response}"

Rate the response on a scale of 1-5 (1 = very poor, 5 = excellent) based on:
1. Relevance (Did it answer the question?)
2. Helpfulness (Is the solution actionable?)
3. Tone (Is it professional and polite?)

Return a short reply that starts with the numeric score (1-5) followed by a brief explanation.
Return ONLY the score and a one-line rationale.
"""

    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            result = model.generate_content(prompt)
            raw = (result.text or "").strip()
            score = _parse_score_from_text(raw)
            
            if score == -1:
                # Fallback: try heuristic keyword matching
                txt = raw.lower()
                if re.search(r'\b(excellent|very good|5)\b', txt):
                    score = 5
                elif re.search(r'\b(good|helpful|4)\b', txt):
                    score = 4
                elif re.search(r'\b(average|ok|3)\b', txt):
                    score = 3
                elif re.search(r'\b(poor|2)\b', txt):
                    score = 2
                else:
                    score = 3  # neutral fallback
            
            score = max(1, min(5, int(score)))
            return score, f"Evaluated by Gemini (raw: {raw[:200]})"
            
        except Exception as e:
            last_exc = e
            time.sleep(backoff * (2 ** attempt))
            continue

    # Fallback after all retries
    fallback_score = 3
    reason = f"Fallback scoring used after errors: {str(last_exc)}"
    return fallback_score, reason

def run_evaluation():
    print("Starting Evaluation...")

    if not os.path.exists(EVAL_PROMPTS_FILE):
        print(f"Error: {EVAL_PROMPTS_FILE} not found.")
        return

    results = []

    with open(EVAL_PROMPTS_FILE, 'r') as f:
        prompts = [line.strip() for line in f if line.strip()]

    for i, query in enumerate(prompts):
        print(f"Evaluating [{i+1}/{len(prompts)}]: {query}")

        start_time = time.time()
        try:
            agent_result = triage_agent.process_ticket({
                "id": f"eval_{i}", 
                "description": query, 
                "user_id": "eval_user"
            })
            response_text = agent_result.get("reply", "") if isinstance(agent_result, dict) else ""
            status = agent_result.get("status", "") if isinstance(agent_result, dict) else "error"
        except Exception as e:
            response_text = f"Error: {str(e)}"
            status = "error"

        duration = time.time() - start_time

        # LLM-as-Judge
        score, reason = evaluate_response(query, response_text)

        results.append({
            "ticket_id": f"eval_{i}",
            "query": query,
            "response": response_text[:500],  # Truncate for CSV readability
            "status": status,
            "score": score,
            "duration": round(duration, 2)
        })

    if not results:
        print("No prompts evaluated.")
        return

    # Save to CSV
    keys = results[0].keys()
    os.makedirs(os.path.dirname(EVAL_RESULTS_FILE), exist_ok=True)
    with open(EVAL_RESULTS_FILE, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

    print(f"\nEvaluation Complete. Results saved to {EVAL_RESULTS_FILE}")

    avg_score = sum(r["score"] for r in results) / len(results)
    print(f"Average Score: {avg_score:.2f}/5.0")

if __name__ == "__main__":
    run_evaluation()
