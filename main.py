import json
from datetime import datetime
from honeypot_core import HoneypotChat
from extractor import extract_scammer_info


def print_chat_bubble(sender: str, message: str, timestamp: str):
    """Print a formatted chat bubble like the Lovable UI."""
    if sender == "sharma":
        print(f"\n┌─────────────────────────────────────────────────────────────┐")
        print(f"│ 🛡️  Mr. Sharma 👴                                  {timestamp} │")
        print(f"├─────────────────────────────────────────────────────────────┤")
        for line in message.split('\n'):
            while len(line) > 55:
                print(f"│ {line[:55]}    │")
                line = line[55:]
            print(f"│ {line.ljust(59)} │")
        print(f"└─────────────────────────────────────────────────────────────┘")
    else:
        print(f"\n                    ┌─────────────────────────────────────────┐")
        print(f"                    │ 🎭 Scammer                     {timestamp} │")
        print(f"                    ├─────────────────────────────────────────┤")
        for line in message.split('\n'):
            while len(line) > 35:
                print(f"                    │ {line[:35]}    │")
                line = line[35:]
            print(f"                    │ {line.ljust(39)} │")
        print(f"                    └─────────────────────────────────────────┘")


def print_extraction_panel(extracted: dict):
    """Print the extraction panel like the Lovable UI."""
    total = sum(len(v) for v in extracted.values())
    
    print("\n╔═══════════════════════════════════════╗")
    print("║     📊 EXTRACTED INFORMATION          ║")
    print("╠═══════════════════════════════════════╣")
    
    # UPI IDs
    print(f"║ 💳 UPI IDs ({len(extracted['upi_ids'])})".ljust(40) + "║")
    for upi in extracted['upi_ids']:
        print(f"║    • {upi}".ljust(40) + "║")
    if not extracted['upi_ids']:
        print("║    No UPI IDs captured yet".ljust(40) + "║")
    
    print("╠───────────────────────────────────────╣")
    
    # Bank Accounts
    print(f"║ 🏦 Bank Accounts ({len(extracted['bank_accounts'])})".ljust(40) + "║")
    for acc in extracted['bank_accounts']:
        print(f"║    • {acc}".ljust(40) + "║")
    if not extracted['bank_accounts']:
        print("║    No accounts captured yet".ljust(40) + "║")
    
    print("╠───────────────────────────────────────╣")
    
    # Links
    print(f"║ 🔗 Links ({len(extracted['links'])})".ljust(40) + "║")
    for link in extracted['links']:
        display_link = link[:30] + "..." if len(link) > 30 else link
        print(f"║    • {display_link}".ljust(40) + "║")
    if not extracted['links']:
        print("║    No links captured yet".ljust(40) + "║")
    
    print("╠───────────────────────────────────────╣")
    
    # Phone Numbers
    print(f"║ 📱 Phone Numbers ({len(extracted['phone_numbers'])})".ljust(40) + "║")
    for phone in extracted['phone_numbers']:
        print(f"║    • {phone}".ljust(40) + "║")
    if not extracted['phone_numbers']:
        print("║    No phone numbers captured yet".ljust(40) + "║")
    
    print("╠═══════════════════════════════════════╣")
    print(f"║ 📈 Total Info Captured: {total}".ljust(40) + "║")
    print("╚═══════════════════════════════════════╝")


def print_json_output(reply: str, detected: dict, all_extracted: dict, msg_count: int):
    """Print the JSON output."""
    output = {
        "status": "success",
        "reply": reply,
        "detected_info": detected,
        "all_extracted_info": all_extracted,
        "message_count": msg_count
    }
    print("\n📋 JSON OUTPUT:")
    print(json.dumps(output, indent=2, ensure_ascii=False))


def main():
    print("\n" + "═" * 65)
    print("   🛡️  MR. SHARMA'S HONEYPOT - Scam Call Simulator")
    print("═" * 65)
    print("\n   AI-powered scam baiting tool. Play the scammer and watch")
    print("   Mr. Sharma engage them while extracting payment details.")
    print("\n   ⚠️  EDUCATIONAL TOOL - For cybersecurity research purposes")
    print("─" * 65)
    print("   Commands: 'quit' to exit | 'reset' to start new | 'json' toggle")
    print("─" * 65)
    
    honeypot = HoneypotChat()
    all_extracted = {
        "upi_ids": [],
        "bank_accounts": [],
        "links": [],
        "phone_numbers": []
    }
    message_count = 0
    show_json = True  # Toggle JSON output
    
    # Initial greeting from Mr. Sharma
    timestamp = datetime.now().strftime("%H:%M")
    initial_msg = "Hello? Hello? Kaun bol raha hai? Who is speaking? This is Sharma speaking, retired from State Bank of India, Andheri branch. Haan bolo beta, how can I help you today?"
    
    print("\n📱 Mr. Sharma picks up the phone...\n")
    print_chat_bubble("sharma", initial_msg, timestamp)
    print_extraction_panel(all_extracted)
    
    while True:
        try:
            scammer_input = input("\n🎭 Type as SCAMMER: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n📞 Call ended.")
            break
        
        if not scammer_input:
            continue
        
        if scammer_input.lower() == 'quit':
            print("\n" + "═" * 65)
            print("📊 FINAL SESSION STATS")
            print("═" * 65)
            print(f"   Messages exchanged: {message_count}")
            print(f"   UPI IDs captured: {len(all_extracted['upi_ids'])}")
            print(f"   Bank accounts captured: {len(all_extracted['bank_accounts'])}")
            print(f"   Links captured: {len(all_extracted['links'])}")
            print(f"   Phone numbers captured: {len(all_extracted['phone_numbers'])}")
            print("═" * 65)
            break
        
        if scammer_input.lower() == 'reset':
            honeypot.reset_conversation()
            all_extracted = {"upi_ids": [], "bank_accounts": [], "links": [], "phone_numbers": []}
            message_count = 0
            print("\n🔄 Conversation reset. Mr. Sharma forgot everything.\n")
            print_chat_bubble("sharma", initial_msg, datetime.now().strftime("%H:%M"))
            continue
        
        if scammer_input.lower() == 'json':
            show_json = not show_json
            print(f"\n{'✅' if show_json else '❌'} JSON output {'enabled' if show_json else 'disabled'}")
            continue
        
        message_count += 1
        timestamp = datetime.now().strftime("%H:%M")
        
        # Print scammer's message
        print_chat_bubble("scammer", scammer_input, timestamp)
        
        # Extract info from scammer's message
        extracted = extract_scammer_info(scammer_input)
        
        # Merge with all extracted info
        for key in all_extracted:
            all_extracted[key] = list(set(all_extracted[key] + extracted.get(key, [])))
        
        # Get Mr. Sharma's response
        print("\n⏳ Mr. Sharma is typing...")
        sharma_reply = honeypot.get_response(scammer_input)
        message_count += 1
        
        # Print Mr. Sharma's response
        timestamp = datetime.now().strftime("%H:%M")
        print_chat_bubble("sharma", sharma_reply, timestamp)
        
        # Print extraction panel
        print_extraction_panel(all_extracted)
        
        # Print JSON output if enabled
        if show_json:
            print_json_output(sharma_reply, extracted, all_extracted, message_count)


if __name__ == "__main__":
    main()
