# 🚀 TicketTriage+KB Quick Start Guide

**Complete step-by-step guide for running this multi-agent system from scratch.**

---

## 📋 Prerequisites

- **Python 3.10+** installed
- **Git** (to clone the project)
- **Google Gemini API Key** ([Get one free here](https://ai.google.dev/))

---

## 🛠️ Step 1: Clone or Download the Project

```bash
# If you have the project as a zip, extract it
# If it's on GitHub, clone it:
git clone <repository-url>
cd kaggle_Ai_agent
```

---

## 📦 Step 2: Install Dependencies

```bash
# Install all required Python packages
pip install -r requirements.txt
```

**What this installs:**
- `google-generativeai` (Gemini SDK)
- `python-dotenv` (Environment variables)
- `colorama` (Pretty terminal colors)
- `streamlit` (Web UI, optional)

---

## 🔑 Step 3: Set Your API Key

You have **two options**:

### Option A: Environment Variable (Temporary)
```bash
export GOOGLE_API_KEY="your_api_key_here"
export GEMINI_MODEL="gemini-2.0-flash-lite-preview-02-05"
```
*Note: You'll need to run this every time you open a new terminal.*

### Option B: Create a `.env.local` File (Permanent)
```bash
# Create the file
echo 'GOOGLE_API_KEY="your_api_key_here"' > .env.local
echo 'GEMINI_MODEL="gemini-2.0-flash-lite-preview-02-05"' >> .env.local
```
*This saves your key permanently (but don't commit this file to Git!).*

---

## ✅ Step 4: Verify Installation

Run a quick test:

```bash
python3 main.py --ticket "Test ticket"
```

**Expected output:**
```
=== TicketTriage+KB System Initialized ===
Processing Ticket [ticket_001]: Test ticket
...
=== Result ===
Status: drafted (or escalated)
Reply/Action: [Generated response]
```

If you see this, **you're ready!** 🎉

---

## 🎮 Step 5: Run the System

### **Mode 1: Single Ticket Test**
Process one ticket at a time:
```bash
python3 main.py --ticket "I cannot login to my account"
```

### **Mode 2: Interactive Chat** (Recommended)
Chat with the agent in real-time:
```bash
python3 main.py --interactive
```

Try these prompts:
- `How do I enable dark mode?`
- `I was double charged for my subscription!` (Should escalate)
- `My app crashes on Android` (Should find KB article)

Type `exit` to quit.

### **Mode 3: Full Evaluation**
Run 20 test cases and get a quality score:
```bash
python3 evaluation/evaluate.py
```

Results saved to `docs/evaluation.csv`.

---

## 🧠 Step 6: See the Agent's "Brain"

Watch the logs in real-time to see how the agent thinks:

```bash
tail -f logs/events.log
```

You'll see:
- `triage.analysis` - How it categorized the ticket
- `kb_tool.search` - What it searched for
- `draft_agent.success` - When it generated a reply
- `escalation_agent.triggered` - When it escalated

---

## 🌐 Step 7: (Optional) Web UI

If you want a visual dashboard:

```bash
python3 adk.py web --port 8501
```

Open your browser to `http://localhost:8501`.

*Note: If you get errors, the terminal mode works perfectly fine!*

---

## 📂 Project Structure

```
kaggle_Ai_agent/
├── agents/           # AI agents (Triage, Draft, Escalation)
├── tools/            # KB Search tool + mock data
├── core/             # Memory Bank + Session Manager
├── utils/            # Observability (logging)
├── logs/             # Event logs (auto-generated)
├── main.py           # CLI entry point
├── evaluation/       # LLM-as-a-judge scripts
└── README.md         # Full documentation
```

---

## 🆘 Troubleshooting

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'google'` | Run `pip install -r requirements.txt` |
| `GOOGLE_API_KEY not found` | Set your API key (Step 3) |
| `KB hits: 0` | Normal! The mock KB is small. The agent still generates a reply. |
| `429 Quota exceeded` | Wait 1 minute or switch to `gemini-2.0-flash-lite-preview-02-05` |

---

## 🎯 What Makes This a Multi-Agent System?

1. **Triage Agent** - Analyzes tickets and decides what to do
2. **KB Search Tool** - Retrieves relevant documentation
3. **Draft Agent** - Generates professional responses
4. **Escalation Agent** - Handles high-severity cases
5. **Memory Bank** - Remembers past interactions
6. **Observability** - Logs every decision for transparency

---

## 📊 For Kaggle Judges

To demonstrate the system:

1. Run `python3 main.py --interactive`
2. Open a second terminal: `tail -f logs/events.log`
3. Ask: "I was double charged!" → Watch it escalate
4. Ask: "How do I enable dark mode?" → Watch it search KB
5. Run `python3 evaluation/evaluate.py` → Show the scores

---

**You're all set! Happy triaging! 🤖✨**
