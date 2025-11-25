# Setup Instructions

## Install Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# Test the hooks (optional)
pre-commit run --all-files
```

## What the Hooks Do

1. **Prevent API Key Commits**
   - Scans diffs for patterns like `AIza...` or `AKIA...`
   - Blocks commit if keys detected

2. **Prevent .env Commits**
   - Blocks commits containing `.env` or `.env.local`

3. **Run Tests**
   - Runs sanitizer and KB parsing tests before commit
   - Ensures no regressions

4. **Code Quality**
   - Removes trailing whitespace
   - Ensures files end with newline
   - Detects private keys

## Manual Testing

```bash
# Run all tests
export PYTHONPATH="$PWD:$PYTHONPATH"
pytest -v

# Run specific test suites
pytest tests/test_sanitizer.py -v
pytest tests/test_kb_parsing.py -v

# Check for API keys in logs
grep -R "AIza" logs/ || echo "✅ No keys found"
```

## CI/CD Integration

Add to `.github/workflows/test.yml`:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements-dev.txt
      - run: export PYTHONPATH="$PWD:$PYTHONPATH" && pytest -v
      - run: grep -R "AIza" logs/ && exit 1 || echo "✅ No keys in logs"
```
