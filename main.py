from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Frontend --------------------
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# -------------------- Conversation Memory --------------------
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

# -------------------- Pydantic Model --------------------
class ChatRequest(BaseModel):
    message: str

# -------------------- Chat API --------------------
@app.post("/api/chat")
async def chat(req: ChatRequest):
    user_message = req.message

    conversation.append({
        "role": "user",
        "content": user_message
    })

    reply = generate_natural_reply(user_message)

    conversation.append({
        "role": "assistant",
        "content": reply
    })

    return {"reply": reply}

# -------------------- Natural Reply Engine (UNCHANGED) --------------------
def generate_natural_reply(msg: str) -> str:
    msg = msg.lower()

    # Accident / emergency scam
    if any(word in msg for word in ["accident", "hospital", "not well", "emergency", "injured"]):
        return (
            "Oh my god... what happened? Which hospital is this? "
            "I spoke to my son this morning, he was fine. Please explain properly."
        )

    # Family relation scare
    if any(word in msg for word in ["son", "daughter", "wife", "brother"]):
        return (
            "You are saying about my family? This is very shocking for me. "
            "How did you get my number? Please tell me clearly what has happened."
        )

    # Money pressure
    if any(word in msg for word in ["send money", "send amount", "transfer", "payment", "pay"]):
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