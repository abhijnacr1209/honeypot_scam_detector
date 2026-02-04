from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from ai_engine import get_sharma_reply, SYSTEM_PROMPT

app = FastAPI()

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Store conversations per session
conversations = {}

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    scammer_message = data.get("message")
    session_id = data.get("session_id")

    if not session_id:
        return JSONResponse({"error": "session_id required"}, status_code=400)

    # conversations is a global dictionary storing sessions
    if session_id not in conversations:
        conversations[session_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    conversation = conversations[session_id]

    reply = get_sharma_reply(scammer_message, conversation)

    return JSONResponse({"reply": reply})


    # Create new conversation
    if session_id not in conversations:
        conversations[session_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    conversation = conversations[session_id]
    reply = get_sharma_reply(scammer_message, conversation)

    return JSONResponse({"reply": reply})
