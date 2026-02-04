from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ai_engine import get_sharma_reply, SYSTEM_PROMPT

app = FastAPI()

# Allow frontend (if hosted elsewhere)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversations by session_id
conversations = {}

@app.post("/api/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        session_id = data.get("session_id")

        if not session_id:
            return JSONResponse({"error": "session_id required"}, status_code=400)
        if not message:
            return JSONResponse({"error": "message required"}, status_code=400)

        # Create new conversation if first time
        if session_id not in conversations:
            conversations[session_id] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]

        conversation = conversations[session_id]

        # Get Mr. Sharma's reply from AI engine
        reply = get_sharma_reply(message, conversation)

        # (Optional) you can also run your info extractor here
        detected_info = {
            "upi_ids": [], 
            "bank_accounts": [], 
            "links": [], 
            "phone_numbers": []
        }

        return JSONResponse({
            "reply": reply,
            "detected_info": detected_info
        })

    except Exception as e:
        print("Error in /api/chat:", e)
        return JSONResponse({"reply": "Sorry beta, backend error occurred."}, status_code=500)

# Run with: uvicorn main:app --reload
