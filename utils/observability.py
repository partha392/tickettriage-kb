import logging
from logging.handlers import RotatingFileHandler
import json
import os
import re
import time
from datetime import datetime, timezone
from colorama import Fore, Style, init
from functools import wraps
from pathlib import Path

# Initialize colorama
init(autoreset=True)

# API key patterns to redact
_API_KEY_PATTERNS = [
    # Google-like keys (AIza followed by 30+ chars)
    re.compile(r"AIza[0-9A-Za-z\-_]{30,}"),
    # Generic-looking keys (bearer tokens / hex)
    re.compile(r"(?:api_key|api-key|apikey|secret|token)[=:]\s*([A-Za-z0-9\-_\.]{16,})", re.IGNORECASE),
    # AWS-like
    re.compile(r"AKIA[0-9A-Z]{16}"),
]

def sanitize_value(v, max_len=300):
    """Redact API-like patterns and truncate long strings."""
    if v is None:
        return v
    if isinstance(v, str):
        s = v
        # redact API-like patterns
        for pat in _API_KEY_PATTERNS:
            s = pat.sub("<REDACTED_API_KEY>", s)
        # redact bare-looking long tokens (replace long sequences of base64/hex)
        s = re.sub(r"[A-Za-z0-9\-_]{64,}", "<REDACTED_TOKEN>", s)
        # truncate
        if len(s) > max_len:
            return s[:max_len] + "...<TRUNCATED>"
        return s
    if isinstance(v, dict):
        return {k: sanitize_value(val, max_len) for k, val in v.items()}
    if isinstance(v, (list, tuple)):
        t = [sanitize_value(x, max_len) for x in v]
        return type(v)(t)
    # other primitives
    return v

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"  # repo/kaggle_Ai_agent/logs
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "events.log"

class EventLogger:
    def __init__(self, log_file: str | Path = LOG_FILE, max_bytes: int = 5_000_000, backup_count: int = 3):
        self.log_file = str(log_file)

        self.logger = logging.getLogger("TicketTriage")
        self.logger.setLevel(logging.INFO)

        # Only add handlers if they don't already exist
        if not self.logger.handlers:
            # File handler for JSON logs (using RotatingFileHandler as before)
            fh = RotatingFileHandler(self.log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
            fh.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(fh)
            
            # Console handler for pretty printing
            ch = logging.StreamHandler()
            ch.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(ch)

    def _now_iso(self):
        return datetime.now(timezone.utc).isoformat()

    def _sanitize_details(self, details: dict) -> dict:
        """Remove sensitive data from log details."""
        sanitized = {}
        sensitive_keys = {'api_key', 'password', 'token', 'secret', 'authorization'}
        
        for key, value in details.items():
            key_lower = key.lower()
            if any(sensitive in key_lower for sensitive in sensitive_keys):
                sanitized[key] = "***REDACTED***"
            elif isinstance(value, str) and len(value) > 500:
                sanitized[key] = value[:500] + "...[truncated]"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_details(value)
    def log_event(self, event_type: str, details: dict, level: str = "INFO"):
        timestamp = self._now_iso()
        # Sanitize all details before logging
        sanitized_details = sanitize_value(details)
        
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "level": level,
            "details": sanitized_details
        }

        # Write JSON to file (one JSON object per line)
        try:
            self.logger.info(json.dumps(log_entry))
        except Exception:
            self.logger.info(json.dumps({"timestamp": timestamp, "event_type": "logging.error", "details": "failed to serialize"}))

        # Pretty console print
        self._print_pretty(timestamp, event_type, sanitized_details, level)

    def _print_pretty(self, timestamp, event_type, details, level):
        color = Fore.WHITE
        if "start" in event_type:
            color = Fore.CYAN
        elif "finish" in event_type:
            color = Fore.GREEN
        elif "error" in event_type or "escalat" in event_type:
            color = Fore.RED
        elif "tool" in event_type:
            color = Fore.YELLOW

        print(f"{Fore.BLACK}{Style.BRIGHT}[{timestamp}] {color}{Style.BRIGHT}{event_type} {Style.RESET_ALL}| {details}")

logger = EventLogger()

def _truncate_arg(x, n=200):
    # If x is a JSON string, parse it first, then sanitize
    if isinstance(x, str):
        try:
            parsed = json.loads(x)
            x = parsed
        except:
            pass  # Not JSON, treat as regular string
    
    # Sanitize FIRST, then truncate
    x_sanitized = sanitize_value(x)
    try:
        s = json.dumps(x_sanitized, default=str)
    except Exception:
        s = str(x_sanitized)
    return s if len(s) <= n else s[:n-1] + "…"

def log_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        try:
            # Sanitize happens inside _truncate_arg now
            safe_args = {"args": [_truncate_arg(a) for a in args], "kwargs": {k: _truncate_arg(v) for k, v in kwargs.items()}}
            logger.log_event(f"{func_name}.start", {"args": safe_args})
        except Exception:
            logger.log_event(f"{func_name}.start", {"args": "unserializable"})
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.log_event(f"{func_name}.finish", {"duration_s": round(duration, 4)})
            return result
        except Exception as e:
            logger.log_event(f"{func_name}.error", {"error": str(e)})
            raise
    return wrapper
