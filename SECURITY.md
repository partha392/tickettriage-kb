# Security Policy

## Reporting Security Issues

Report security vulnerabilities to the project maintainer.

## Secrets Policy

- **Never commit API keys, tokens, or credentials** to version control
- Use `.env` files for local development only (excluded from git)
- Use CI secrets or environment variables for production
- Pre-commit hooks are configured to block key patterns

## Kaggle Submission Policy

- For Kaggle submissions, the repository runs in **offline mode** by default (`--kaggle` or `--offline` flag)
- No network calls are attempted in offline mode
- All functionality works without external API keys

## API Key Management

### Local Development
1. Copy `.env.template` to `.env`
2. Add your API key to `.env`
3. Never commit `.env` to git

### Key Rotation
If a key is exposed:
1. Immediately revoke it in Google Cloud Console
2. Generate a new key with restricted permissions
3. Update local `.env` file
4. Check git history: `git log -S "AIza"`

## Logging Security

The system automatically sanitizes logs to prevent key leakage:
- API keys matching patterns like `AIza...` or `AKIA...` are redacted as `<REDACTED_API_KEY>`
- Long strings are truncated
- Sensitive fields are never written to log files

## Pre-commit Hooks

Install pre-commit hooks to prevent accidents:
```bash
pip install pre-commit
pre-commit install
```

Hooks will:
- Block commits containing API key patterns
- Block commits of `.env` files
- Run tests before commit
- Check for trailing whitespace

## Incident Response

If you suspect a security breach:
1. Rotate all API keys immediately
2. Review `logs/events.log` for suspicious activity
3. Check for unusual API usage in cloud console
4. Report the incident to the maintainer

## Contact

For security issues, contact the project maintainer directly.
