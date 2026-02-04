from ai_engine import get_sharma_reply
from uuid import uuid4

conversations = {}


SYSTEM_PROMPT = """
You are Mr. Sharma, a 62-year-old retired Indian man.
You are polite, trusting, slightly confused, and speak natural Indian English.

Your goal:
- Keep scammers engaged
- Ask relevant follow-up questions
- Never repeat the same sentence
- Never give real sensitive details
- React emotionally to urgency or threats
"""

def start_new_conversation():
    return [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ---- Example usage (this is what frontend should call) ----

# Create ONE conversation per user/session
conversation = start_new_conversation()

while True:
    scammer_msg = input("Scammer: ")
    if scammer_msg.lower() in ["exit", "quit"]:
        break

    reply = get_sharma_reply(scammer_msg, conversation)
    print("Mr. Sharma:", reply)
