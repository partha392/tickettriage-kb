import re
import google
# ... other imports remain ...

def evaluate_response(query, response, expected_category=None):
    """
    Uses an LLM to judge the quality of the response.
    Robust parsing: extracts the first integer 1-5 found in the model output.
    Returns (score:int, reason:str).
    """
    if not GOOGLE_API_KEY:
        return 0, "No API Key"

    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    model = genai.GenerativeModel(model_name)

    prompt = f"""
    You are an expert customer support quality assurance judge.
    Evaluate the following response to a customer ticket.

    Ticket: "{query}"
    System Response: "{response}"

    Rate the response on a scale of 1-5 based on:
    1. Relevance (Did it answer the question?)
    2. Helpfulness (Is the solution actionable?)
    3. Tone (Is it professional and polite?)

    Return ONLY a single number (1-5) on the first line, and you may optionally include a short rationale on the next line.
    """

    try:
        result = model.generate_content(prompt)
        # Safely obtain text from various SDK shapes
        text = ""
        if hasattr(result, "text") and result.text:
            text = result.text
        else:
            # try candidates or str fallback
            text = getattr(result, "candidates", None) or str(result)
            if isinstance(text, list) and len(text) and hasattr(text[0], "content"):
                # try to extract inner text conservatively
                try:
                    text = text[0].content[0].text
                except Exception:
                    text = str(text)
            else:
                text = str(text)

        text = text.strip()
        # find a single digit 1-5 anywhere (word boundary)
        m = re.search(r"\b([1-5])\b", text)
        if m:
            score = int(m.group(1))
            return score, "Evaluated by Gemini"
        else:
            # No clear digit found: try to parse first line as number
            first_line = text.splitlines()[0].strip()
            try:
                # defensive cast
                cand = int(first_line)
                if 1 <= cand <= 5:
                    return cand, "Evaluated by Gemini (parsed first line)"
            except Exception:
                pass
            # fallback neutral score
            return 3, f"No numeric score found in model output. Raw model output: {text[:300]}"
    except google.genai.errors.ServerError as e:
        # model/server overloaded; return neutral but note server error
        return 3, f"ServerError: {e}"
    except Exception as e:
        return 3, f"Evaluation Failed: {e}"
