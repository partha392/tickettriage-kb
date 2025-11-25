import argparse
import sys
import os
from agents.triage_agent import triage_agent
from utils.observability import logger
from colorama import Fore, Style

def main():
    parser = argparse.ArgumentParser(description="TicketTriage+KB System")
    parser.add_argument("--ticket", type=str, help="Description of the support ticket")
    parser.add_argument("--id", type=str, default="ticket_001", help="Ticket ID")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--offline", action="store_true", help="Run in offline/Kaggle-safe mode (no external APIs)")
    parser.add_argument("--kaggle", action="store_true", help="Alias for --offline")
    
    args = parser.parse_args()
    
    # Set offline mode if requested or if running in Kaggle environment
    if args.offline or args.kaggle or os.getenv("RUN_MODE", "").lower() == "kaggle":
        os.environ["OFFLINE_MODE"] = "1"
        print(f"{Fore.YELLOW}Running in OFFLINE mode (Kaggle-safe){Style.RESET_ALL}")

    print(f"{Fore.BLUE}{Style.BRIGHT}=== TicketTriage+KB System Initialized ==={Style.RESET_ALL}")
    
    if args.interactive:
        run_interactive()
    elif args.ticket:
        process_single_ticket(args.id, args.ticket)
    else:
        print("Please provide a ticket description using --ticket or run with --interactive")
        parser.print_help()

def process_single_ticket(ticket_id, description):
    print(f"\n{Fore.YELLOW}Processing Ticket [{ticket_id}]:{Style.RESET_ALL} {description}")
    
    ticket = {
        "id": ticket_id,
        "description": description,
        "user_id": "user_123" # Mock user ID
    }
    
    try:
        result = triage_agent.process_ticket(ticket)
        
        print(f"\n{Fore.GREEN}=== Result ==={Style.RESET_ALL}")
        print(f"Status: {result.get('status')}")
        print(f"Reply/Action: {result.get('reply')}")
        
    except Exception as e:
        print(f"{Fore.RED}Error processing ticket: {e}{Style.RESET_ALL}")
        logger.log_event("main.error", {"error": str(e)})

def run_interactive():
    print("Enter ticket description (or 'exit' to quit):")
    ticket_counter = 1
    while True:
        user_input = input(f"\n{Fore.CYAN}Ticket #{ticket_counter}> {Style.RESET_ALL}")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        if not user_input.strip():
            continue
            
        process_single_ticket(f"ticket_{ticket_counter:03d}", user_input)
        ticket_counter += 1

if __name__ == "__main__":
    main()
