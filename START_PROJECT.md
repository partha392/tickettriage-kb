# 🚀 How to Start This Project

Welcome! If you have just opened this project in your IDE (VS Code, PyCharm, etc.), follow these steps to get running.

## 1. Open the Terminal
Open your IDE's built-in terminal.
- **VS Code:** `Ctrl + ~` (or `Terminal > New Terminal`)

## 2. Activate Your Python Environment
You likely have a virtual environment folder (like `env`, `venv`, or a Conda env).

**If you are using Conda:**
```bash
conda activate test
# (Replace 'test' with your actual environment name)
```

**If you are using standard Python venv:**
```bash
# Mac/Linux:
source venv/bin/activate
# OR
source env/bin/activate

# Windows:
.\venv\Scripts\activate
```
*You should see `(env)` or `(test)` appear at the start of your command line.*

## 3. Install Dependencies
Ensure you have all the required libraries installed:
```bash
pip install -r requirements.txt
```

## 4. Set Up Your API Key (Optional for Offline Mode)
To use the AI features (Gemini), you need an API key.

1.  **Create the .env file:**
    ```bash
    cp .env.template .env
    ```
2.  **Edit the file:**
    Open `.env` and paste your Google API Key:
    ```ini
    GOOGLE_API_KEY=AIzaSy...
    ```

## 5. Run the Project

### Option A: Quick Demo (Recommended)
Runs 3 automatic test cases.
```bash
./run_demo.sh
```

### Option B: Manual Test (Offline Mode)
Test without an API key (uses templates).
```bash
python3 main.py --ticket "How do I enable dark mode?" --offline
```

### Option C: Manual Test (Online Mode)
Test with real AI (requires Step 4).
```bash
python3 main.py --ticket "My video player is broken"
```

---
**Happy Coding!** 🤖
