# 🏠 LOCAL.md - Running TicketTriage on Your Machine

**Your personal guide to running this multi-agent system on your local laptop.**

---

## ✅ Current Status

You already have the project set up! Here's what's ready:

- ✅ Project location: `~/projects/Ai/kaggle_Ai_agent`
- ✅ Dependencies installed
- ✅ API key configured
- ✅ System tested and working

---

## 🚀 Quick Start (Every Time You Use It)

### Step 1: Open Terminal and Navigate to Project

```bash
cd ~/projects/Ai/kaggle_Ai_agent
```

### Step 2: Activate Your Environment (if using conda)

```bash
conda activate test
```

### Step 3: Set Your API Key (if not using .env.local)

```bash
export GOOGLE_API_KEY="AIzaSyC2ahvKko4SR06wwGAvRXLBBizeLlIU-Mg"
export GEMINI_MODEL="gemini-2.0-flash-lite-preview-02-05"
```

### Step 4: Run the Agent!

**Interactive Mode (Recommended):**
```bash
python3 main.py --interactive
```

**Single Ticket Mode:**
```bash
python3 main.py --ticket "Your question here"
```

---

## 📋 Complete Workflow (Copy-Paste Ready)

```bash
# 1. Navigate to project
cd ~/projects/Ai/kaggle_Ai_agent

# 2. Activate environment
conda activate test

# 3. Set API key
export GOOGLE_API_KEY="AIzaSyC2ahvKko4SR06wwGAvRXLBBizeLlIU-Mg"
export GEMINI_MODEL="gemini-2.0-flash-lite-preview-02-05"

# 4. Run interactive mode
python3 main.py --interactive
```

---

## 🎮 What You Can Do

### Try These Prompts in Interactive Mode:

1. **Test KB Search:**
   ```
   How do I enable dark mode?
   ```
   *Should search the knowledge base*

2. **Test Escalation:**
   ```
   I was double charged for my subscription!
   ```
   *Should escalate to Tier 2 support*

3. **Test General Support:**
   ```
   My app crashes on Android
   ```
   *Should find KB article about Android crashes*

4. **Exit:**
   ```
   exit
   ```

---

## 🧠 Watch the Agent Think

Open a **second terminal** and run:

```bash
cd ~/projects/Ai/kaggle_Ai_agent
tail -f logs/events.log
```

This shows you the agent's internal reasoning in real-time!

---

## 📊 Run the Evaluation Suite

Test the system against 20 different tickets:

```bash
cd ~/projects/Ai/kaggle_Ai_agent
conda activate test
export GOOGLE_API_KEY="AIzaSyC2ahvKko4SR06wwGAvRXLBBizeLlIU-Mg"
export GEMINI_MODEL="gemini-2.0-flash-lite-preview-02-05"
python3 evaluation/evaluate.py
```

Results will be saved to `docs/evaluation.csv`.

---

## 🔧 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "GOOGLE_API_KEY not found"
Make sure you ran the export command in Step 3.

### "429 Quota exceeded"
Wait 1 minute, or the API rate limit will reset.

---

## 💡 Pro Tips

1. **Save your API key permanently:**
   ```bash
   echo 'export GOOGLE_API_KEY="AIzaSyC2ahvKko4SR06wwGAvRXLBBizeLlIU-Mg"' >> ~/.bashrc
   echo 'export GEMINI_MODEL="gemini-2.0-flash-lite-preview-02-05"' >> ~/.bashrc
   source ~/.bashrc
   ```
   Now you won't need to export it every time!

2. **Create an alias for quick access:**
   ```bash
   echo 'alias triage="cd ~/projects/Ai/kaggle_Ai_agent && conda activate test && python3 main.py --interactive"' >> ~/.bashrc
   source ~/.bashrc
   ```
   Now just type `triage` to start the agent!

---

## 📁 Your Project Structure

```
~/projects/Ai/kaggle_Ai_agent/
├── agents/           # The AI agents
├── tools/            # KB search tool
├── core/             # Memory & sessions
├── logs/             # Event logs (auto-created)
├── main.py           # Start here!
└── .env.local        # Your API key (if created)
```

---

**That's it! You're ready to use your multi-agent system anytime.** 🎉
