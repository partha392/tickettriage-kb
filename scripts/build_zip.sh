#!/usr/bin/env bash
set -eo pipefail

echo "=== Building Kaggle Submission ZIP ==="

# Set PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH:-}"

# Run tests first
echo "Running tests..."
pytest -q || { echo "Tests failed! Fix before building."; exit 1; }

# Security check
echo "Running security checks..."
grep -R "AIza" . --exclude-dir=.git --exclude="*.md" --exclude-dir=logs --exclude=".env.local" && { echo "ERROR: API keys found!"; exit 1; } || echo "✅ No API keys found"

# Create temp directory
echo "Creating package..."
rm -rf /tmp/kaggle_pkg
mkdir -p /tmp/kaggle_pkg

# Copy required files
rsync -av --exclude '.git' --exclude '__pycache__' --exclude '*.pyc' --exclude '.env' --exclude '.env.local' --exclude 'logs/' \
  main.py README.md LICENSE SECURITY.md requirements.txt requirements-dev.txt run_demo.sh \
  agents/ tools/ core/ utils/ evaluation/ tests/ scripts/ \
  /tmp/kaggle_pkg/

# Create ZIP
cd /tmp/kaggle_pkg
zip -r kaggle_submission.zip ./*

# Move to project root
mv kaggle_submission.zip /home/helas/projects/Ai/kaggle_Ai_agent/

echo "✅ Created kaggle_submission.zip"
echo "Location: /home/helas/projects/Ai/kaggle_Ai_agent/kaggle_submission.zip"
echo ""
echo "Upload this file to Kaggle!"
