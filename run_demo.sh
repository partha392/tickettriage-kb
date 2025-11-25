#!/bin/bash
# Demo script for TicketTriage+KB system
# Runs 3 test cases in offline mode

set -euo pipefail

echo "=== TicketTriage+KB Demo ==="
echo ""

# Set PYTHONPATH to include current directory
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)"

echo "Test 1: KB Hit (Dark Mode)"
python3 main.py --ticket "How do I enable dark mode?" --offline
echo ""

echo "Test 2: Escalation (Billing)"
python3 main.py --ticket "I was double charged!" --offline
echo ""

echo "Test 3: General Support"
python3 main.py --ticket "I want to cancel my subscription" --offline
echo ""

echo "=== Demo Complete ==="
