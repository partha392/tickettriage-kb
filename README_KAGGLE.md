# TicketTriage+KB Multi-Agent System

**A lightweight, offline-capable multi-agent ticket triage system for Kaggle submission.**

## 🚀 Quick Start (Offline Mode - No API Key Needed)

```python
# Simply run all cells in the notebook!
# The system defaults to OFFLINE mode and uses template responses.
```

## 📋 What This Does

Multi-agent ticket triage system that:
- **Classifies** support tickets (billing, technical, feature requests)
- **Searches** knowledge base for relevant articles
- **Drafts** professional replies (template-based offline or Gemini-powered online)
- **Escalates** high-severity issues automatically
- **Tracks** ticket history in memory

## 🎯 How It Works

```
User Ticket → TriageAgent (classify) → KB Search → DraftAgent (reply) → Memory
                    ↓
              High Severity? → EscalationAgent → Tier 2
```

## 💻 Running on Kaggle

### Offline Mode (Default - Recommended for Submission)
- No setup required
- Uses template-based responses
- Fully functional demo
- **Just click "Run All"**

### Online Mode (Optional - Requires API Key)
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to Kaggle Secrets as `GOOGLE_API_KEY`
3. Notebook auto-detects and uses Gemini for intelligent responses

## 📊 Expected Output

**Test Case 1 (Dark Mode):**
```
Status: drafted
Reply: Dark mode is currently in beta. Users can enable it...
```

**Test Case 2 (Billing):**
```
Status: escalated
Reply: Ticket has been ESCALATED to Tier 2 Support...
```

## 🔧 Technical Components

- **TriageAgent**: Coordinator (rule-based classification)
- **KBSearchTool**: 8 KB articles with query normalization
- **DraftReplyAgent**: Template or Gemini-powered responses
- **EscalationAgent**: High-severity routing
- **MemoryBank**: Ticket history tracking
- **SimpleLogger**: Observability with API key sanitization

## 🔒 Security

- ✅ API key sanitization (AIza*, AKIA* patterns)
- ✅ No hardcoded secrets
- ✅ Offline mode by default
- ✅ Sanitized logging

## 📦 What's Included

- Complete multi-agent system (self-contained)
- 8 knowledge base articles
- 4 demo test cases
- Security sanitization
- Memory management

## ⚙️ Requirements

- Python 3.10+
- No external dependencies for offline mode
- `google-generativeai` only if running online mode

## 📝 License

MIT License - See LICENSE file

## 🎓 Use Cases

- Enterprise support automation demo
- Multi-agent system architecture example
- Kaggle capstone project
- Learning resource for agent coordination

---

**Ready to run!** Just open the notebook and click "Run All" 🚀
