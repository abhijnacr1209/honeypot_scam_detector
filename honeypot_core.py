import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

history = []

def get_honeypot_reply(user_input: str) -> str:
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        context = "\n".join(
            [f"{m['sender']}: {m['text']}" for m in history]
        )

        system_instruction = (
            "You are a scam baiting AI. "
            "Waste the scammer's time with clever, innocent replies."
        )

        full_prompt = (
            f"{system_instruction}\n\n"
            f"Chat History:\n{context}\n\n"
            f"Scammer: {user_input}\n"
            f"You:"
        )

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=full_prompt
        )

        reply = response.text.strip()

        history.append({"sender": "scammer", "text": user_input})
        history.append({"sender": "bot", "text": reply})

        return reply

    except Exception as e:
        print(f"Error: {e}")
        return "Beta, hold on… my internet is acting up."