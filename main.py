import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from ai_engine import get_sharma_reply

app = FastAPI()

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# API endpoint used by frontend
@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    scammer_message = data.get("message")

    reply = get_sharma_reply(scammer_message)

    return JSONResponse({"reply": reply})