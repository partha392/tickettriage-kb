# 🎯 How to Run This Notebook

## Option 1: One-Click Demo (Recommended)

**Just click "Run All" at the top!**

The notebook runs in **OFFLINE mode** by default - no API key needed. You'll see:
- ✅ System initialization
- ✅ 4 test cases demonstrating the multi-agent flow
- ✅ Memory bank summary
- ✅ Security sanitization demo

## Option 2: Online Mode (Optional - Gemini-Powered)

For AI-generated responses instead of templates:

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. In Kaggle: **Add-ons** → **Secrets** → Add secret named `GOOGLE_API_KEY`
3. Enable secrets for this notebook
4. Run all cells

The notebook will automatically detect the API key and use Gemini for intelligent classification and draft generation.

## 📊 What You'll See

### Test Case 1: KB Hit (Dark Mode)
```
Input: "How do I enable dark mode?"
Output: Drafted reply with KB article about dark mode beta feature
```

### Test Case 2: Escalation (Billing)
```
Input: "I was double charged!"
Output: Ticket escalated to Tier 2 Support (high severity)
```

### Test Case 3: Technical Issue
```
Input: "The video player is not working"
Output: Escalated (technical issue)
```

### Test Case 4: General Support
```
Input: "I want to cancel my subscription"
Output: Drafted reply with cancellation process
```

## ⚠️ Important Notes

- **Offline mode** = Template responses (no API calls)
- **Online mode** = Gemini-powered responses (requires API key)
- **Security**: Never paste API keys directly in cells
- **Quota**: Online mode uses Gemini API quota

## 🔧 Troubleshooting

**"No module named 'google.generativeai'"**
- This is normal in offline mode - the notebook handles it gracefully
- Only needed for online mode

**"Quota exceeded"**
- You've hit Gemini API limits
- Switch to offline mode or wait for quota reset

**Outputs look different**
- Offline mode uses templates (consistent)
- Online mode uses AI (varies each run)

---

**Ready? Click "Run All" now!** 🚀
