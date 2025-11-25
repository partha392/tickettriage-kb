import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="ADK CLI Wrapper")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Web Command
    web_parser = subparsers.add_parser("web", help="Launch the Web UI")
    web_parser.add_argument("--port", type=str, default="8501", help="Port to run the web server on")
    
    args = parser.parse_args()
    
    if args.command == "web":
        print(f"🚀 Launching TicketTriage Mission Control on port {args.port}...")
        try:
            subprocess.run(
                [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", args.port],
                check=True
            )
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Web UI.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
