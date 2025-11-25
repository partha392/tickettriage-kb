import streamlit as st
import time
import json
import os
from dotenv import load_dotenv

load_dotenv(".env.local")
load_dotenv() # Fallback to .env

from agents.triage_agent import triage_agent
from core.memory import memory_bank
from utils.observability import logger

# Page Config
st.set_page_config(
    page_title="TicketTriage Mission Control",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Premium" feel
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
    .st-emotion-cache-1y4p8pa {
        padding-top: 0rem;
    }
    h1 {
        color: #4A90E2;
    }
    .metric-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "logs" not in st.session_state:
    st.session_state.logs = []

def load_logs():
    """Reads the last N lines from the log file."""
    log_file = "logs/events.log"
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            lines = f.readlines()
            return [json.loads(line) for line in lines[-20:]] # Last 20 logs
    return []

# --- Sidebar (Controls) ---
with st.sidebar:
    st.title("🎛️ Controls")
    
    # Model Selector
    current_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    model_choice = st.selectbox(
        "Gemini Model", 
        ["gemini-2.0-flash-lite-preview-02-05", "gemini-2.0-flash-exp", "gemini-1.5-flash"],
        index=0
    )
    if model_choice != current_model:
        os.environ["GEMINI_MODEL"] = model_choice
        st.toast(f"Model switched to {model_choice}")

    st.divider()
    
    # System Status
    st.subheader("System Status")
    st.success("● Triage Agent: Online")
    st.success("● KB Service: Online")
    st.success("● Memory Bank: Active")
    
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# --- Main Layout ---
col1, col2 = st.columns([1.5, 1])

# --- Left Column: Chat Interface ---
with col1:
    st.title("💬 Support Agent")
    
    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Describe your issue..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Agent Processing
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            # Run the Agent
            start_time = time.time()
            ticket = {"id": f"web_{int(start_time)}", "description": prompt, "user_id": "web_user"}
            
            try:
                result = triage_agent.process_ticket(ticket)
                response_text = result.get("reply", "No response generated.")
                status = result.get("status", "unknown")
                
                # Format output based on status
                if status == "escalated":
                    final_response = f"🚨 **ESCALATED**: {response_text}"
                else:
                    final_response = response_text
                
                message_placeholder.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
                
            except Exception as e:
                message_placeholder.error(f"Error: {str(e)}")

# --- Right Column: Observability (The "Brain") ---
with col2:
    st.title("🧠 Agent Internals")
    
    # Live Logs Tab
    tab1, tab2, tab3 = st.tabs(["📡 Live Traces", "📚 Knowledge Base", "💾 Memory State"])
    
    with tab1:
        st.caption("Real-time stream of agent reasoning")
        logs = load_logs()
        for log in reversed(logs): # Show newest first
            with st.expander(f"{log['event_type']} @ {log['timestamp'].split('T')[1][:8]}"):
                st.json(log['details'])
                
    with tab2:
        st.caption("Relevant articles found for last query")
        # In a real app, we'd pull this from the agent's return value or a shared state
        # For now, we inspect the logs to find the last search result
        last_search = next((l for l in reversed(logs) if l['event_type'] == 'kb_tool.search'), None)
        if last_search:
            st.info(f"Query: '{last_search['details'].get('query')}'")
            st.metric("Hits Found", last_search['details'].get('hits'))
        else:
            st.write("No recent searches.")

    with tab3:
        st.caption("Long-term memory bank content")
        if os.path.exists("core/memory_bank.json"):
            with open("core/memory_bank.json", "r") as f:
                memory_data = json.load(f)
            st.json(memory_data)
        else:
            st.write("Memory empty.")

# Auto-refresh for logs (simple polling)
if st.session_state.messages:
    time.sleep(2)
    st.rerun()
