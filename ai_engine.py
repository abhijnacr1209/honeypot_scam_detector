from openai import OpenAI

client = OpenAI()

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

# Conversation memory (IMPORTANT)
conversation = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def get_sharma_reply(scammer_message: str) -> str:
    # Add scammer message
    conversation.append({
        "role": "user",
        "content": scammer_message
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )

    reply = response.choices[0].message.content

    # Save Mr. Sharma reply
    conversation.append({
        "role": "assistant",
        "content": reply
    })

    return reply