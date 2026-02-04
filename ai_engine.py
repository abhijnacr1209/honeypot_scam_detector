from openai import OpenAI

client = OpenAI()

def get_sharma_reply(scammer_message: str, conversation: list) -> str:
    # Add scammer message
    conversation.append({
        "role": "user",
        "content": scammer_message
    })

    # 🔥 ADD THIS BLOCK RIGHT HERE
    MAX_MESSAGES = 20
    if len(conversation) > MAX_MESSAGES:
        # keep system prompt + last 18 messages
        conversation[:] = [conversation[0]] + conversation[-18:]
 

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation,
        temperature=0.9,
        presence_penalty=0.6,
        frequency_penalty=0.5
    )

    reply = response.choices[0].message.content

    # Save Mr. Sharma reply
    conversation.append({
        "role": "assistant",
        "content": reply
    })

    return reply
