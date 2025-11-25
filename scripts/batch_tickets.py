"""
Batch ticket processing script for stress testing the system.
Simulates high-volume ticket processing to verify robustness.
"""
import argparse
import time
import json
from agents.triage_agent import triage_agent
from colorama import Fore, Style

# Diverse test tickets covering all categories and severity levels
TEST_TICKETS = [
    # KB hits
    {"description": "How do I enable dark mode?", "expected": "drafted"},
    {"description": "My app crashes when I open it on Android", "expected": "drafted"},
    
    # Escalations - Billing
    {"description": "I was charged twice for my subscription!", "expected": "escalated"},
    {"description": "Double charge on my credit card", "expected": "escalated"},
    {"description": "Refund request for duplicate payment", "expected": "escalated"},
    
    # Escalations - Account Access
    {"description": "I cannot login to my account", "expected": "escalated"},
    {"description": "Password reset not working", "expected": "escalated"},
    {"description": "Account locked out", "expected": "escalated"},
    
    # Escalations - Technical High Severity
    {"description": "Video player is not working", "expected": "escalated"},
    {"description": "App crashes on startup", "expected": "escalated"},
    
    # General Support
    {"description": "I want to cancel my subscription", "expected": "drafted"},
    {"description": "How do I change my email address?", "expected": "drafted"},
    {"description": "Where can I find my invoice?", "expected": "drafted"},
    
    # Edge Cases
    {"description": "What is the capital of France?", "expected": "drafted"},
    {"description": "😡😡😡😡😡", "expected": "escalated"},
    {"description": "", "expected": "drafted"},
    
    # Noisy Input
    {"description": "hEy I CnNt lgIn 2 MY AccOunt plz fixxx ???!!", "expected": "escalated"},
    {"description": "video player not wrking maybe my device sucks idk", "expected": "escalated"},
    
    # With API Keys (sanitization test)
    {"description": "My API key AIzaSyDbX3FakeFakeFakeFakeFakeFakeKey is not working", "expected": "escalated"},
    
    # Long tickets
    {"description": "I have been trying to access my account for the past 3 days but every time I enter my password it says incorrect even though I know it's right. I tried resetting it multiple times but the email never arrives. This is very frustrating and I need access urgently for work. Please help!", "expected": "escalated"},
]

def run_batch(count=30, delay=0.1):
    """Run batch processing of tickets."""
    print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Batch Ticket Processing - {count} tickets{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}\n")
    
    results = {
        "total": 0,
        "drafted": 0,
        "escalated": 0,
        "errors": 0,
        "tickets": []
    }
    
    # Cycle through test tickets to reach desired count
    tickets_to_process = []
    for i in range(count):
        ticket_template = TEST_TICKETS[i % len(TEST_TICKETS)]
        tickets_to_process.append({
            "id": f"batch_{i+1:03d}",
            "description": ticket_template["description"],
            "user_id": f"user_{(i % 10) + 1}",
            "expected": ticket_template["expected"]
        })
    
    start_time = time.time()
    
    for i, ticket in enumerate(tickets_to_process, 1):
        print(f"{Fore.CYAN}[{i}/{count}]{Style.RESET_ALL} Processing: {ticket['description'][:50]}...")
        
        try:
            result = triage_agent.process_ticket(ticket)
            status = result.get("status", "unknown")
            
            results["total"] += 1
            if status == "drafted":
                results["drafted"] += 1
                icon = f"{Fore.GREEN}✓{Style.RESET_ALL}"
            elif status == "escalated":
                results["escalated"] += 1
                icon = f"{Fore.YELLOW}⚠{Style.RESET_ALL}"
            else:
                results["errors"] += 1
                icon = f"{Fore.RED}✗{Style.RESET_ALL}"
            
            results["tickets"].append({
                "id": ticket["id"],
                "description": ticket["description"][:50],
                "status": status,
                "expected": ticket["expected"],
                "match": status == ticket["expected"]
            })
            
            print(f"  {icon} Status: {status}")
            
        except Exception as e:
            results["errors"] += 1
            results["tickets"].append({
                "id": ticket["id"],
                "description": ticket["description"][:50],
                "status": "error",
                "error": str(e)
            })
            print(f"  {Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        
        time.sleep(delay)
    
    elapsed = time.time() - start_time
    
    # Print summary
    print(f"\n{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Batch Processing Summary{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
    print(f"Total Tickets:    {results['total']}")
    print(f"{Fore.GREEN}Drafted:          {results['drafted']}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Escalated:        {results['escalated']}{Style.RESET_ALL}")
    print(f"{Fore.RED}Errors:           {results['errors']}{Style.RESET_ALL}")
    print(f"Time Elapsed:     {elapsed:.2f}s")
    print(f"Avg Time/Ticket:  {elapsed/count:.2f}s")
    
    # Check accuracy
    matches = sum(1 for t in results["tickets"] if t.get("match", False))
    accuracy = (matches / count) * 100
    print(f"Accuracy:         {accuracy:.1f}%")
    
    # Save results
    with open("batch_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n{Fore.GREEN}Results saved to batch_results.json{Style.RESET_ALL}")
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch ticket processing stress test")
    parser.add_argument("--count", type=int, default=30, help="Number of tickets to process")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between tickets (seconds)")
    
    args = parser.parse_args()
    
    run_batch(count=args.count, delay=args.delay)
