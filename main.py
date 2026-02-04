from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    conversation.append({
        "role": "user",
        "content": user_message
    })

    # TEMP natural replies (no AI yet)
    reply = generate_natural_reply(user_message)

    conversation.append({
        "role": "assistant",
        "content": reply
    })

    return {"reply": reply}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Simple in-memory conversation (per session)
conversation = [
    {
        "role": "system",
        "content": (
            "You are Mr Sharma, a polite elderly Indian man. "
            "You are chatting with a scammer. "
            "Your goal is to sound natural, ask innocent questions, "
            "never reveal personal or financial details, "
            "and keep the conversation going realistically."
        )
    }
]




def generate_natural_reply(msg: str) -> str:
    msg = msg.lower()

    # Accident / emergency scam
    if any(word in msg for word in ["accident", "hospital", "not well", "emergency", "injured"]):
        return (
            "Oh my god… what happened? Which hospital is this? "
            "I spoke to my son this morning, he was fine. Please explain properly."
        )

    # Family relation scare
    if any(word in msg for word in ["son", "daughter", "wife", "brother"]):
        return (
            "You are saying about my family? This is very shocking for me. "
            "How did you get my number? Please tell me clearly what has happened."
        )

    # Money pressure
    if any(word in msg for word in ["send money", "send amount", "transfer", "payment", "pay now"]):
        return (
            "Sir, I am an old man, I don’t understand these things quickly. "
            "Why money is needed immediately? Can you please explain slowly?"
        )

    # Asking for bank details
    if any(word in msg for word in ["account number", "ifsc", "bank details"]):
        return (
            "I am not comfortable sharing bank details on phone. "
            "My bank manager told me never to share such information. "
            "Is there any other way?"
        )

    # Asking for UPI
    if "upi" in msg:
        return (
            "I have heard many frauds are happening through UPI. "
            "Is this really safe? Can you confirm from your office?"
        )

    # OTP scam
    if "otp" in msg:
        return (
            "I just received an OTP message. "
            "Why is OTP required now? Earlier nobody asked like this."
        )

    # Threat / urgency
    if any(word in msg for word in ["urgent", "immediately", "now", "last warning"]):
        return (
            "Please don’t shout at me. I am trying to understand. "
            "Give me some time, my hands are shaking."
        )

    # Default fallback
    return (
        "I am getting confused. Please explain once again slowly. "
        "I am not very educated in these matters."
    )