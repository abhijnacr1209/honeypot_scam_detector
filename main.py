import os
from openai import OpenAI
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load local .env file if it exists
load_dotenv()

# Initialize OpenAI Client (Key is pulled from Render Environment Variables)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="Mr. Sharma Scambaiter")

# 1. CORS MIDDLEWARE
# Essential for allowing your frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PERSONALITY DEFINITION
SYSTEM_PROMPT = (
    "You are Mr. Sharma, a polite, talkative 70-year-old retired Indian man. "
    "You are chatting with a scammer. Your goal is to keep them on the line as long as possible. "
    "Talk about your tea, your noisy neighbor, or your knee pain. Be circular and confusing. "
    "REPLY RULE: Use at least 4-5 sentences. Use 'Hinglish' (e.g., Beta, Ji, Teek hai). "
    "Never give real bank details; pretend you're looking for your spectacles or diary."
)

# 2. API ENDPOINT: CHAT
@app.post("/api/chat")
async def chat(request: Request, response: Response):
    # Prevent browser from caching old/failed responses
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    data = await request.json()
    user_message = data.get("message", "")

    try:
        api_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.85,       # High creativity
            frequency_penalty=0.7, # Prevents repeating the same words
            presence_penalty=0.6,  # Encourages talking about new topics
            max_tokens=400
        )
        return {"reply": api_response.choices[0].message.content}
    except Exception as e:
        return {"reply": "Beta, my internet is acting up. Can you repeat that? I'm not very fast with these gadgets."}

# 3. INNOVATION: COMPLAINT GENERATOR
@app.post("/api/report")
async def report_scammer(request: Request):
    data = await request.json()
    chat_history = data.get("history", "")

    try:
        report_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a Cybercrime Investigative Assistant. Summarize the chat transcript into a formal complaint for the National Cyber Crime Reporting Portal. Identify the scam type, the tactics used, and any sensitive info requested."},
                {"role": "user", "content": f"Generate a formal report from this chat: {chat_history}"}
            ]
        )
        return {
            "status": "Success",
            "report": report_response.choices[0].message.content,
            "ref_id": "I4C-SHARMA-99"
        }
    except Exception as e:
        return {"status": "Error", "message": "Could not generate report."}

# 4. STATIC FILE MOUNT (MUST BE LAST)
# Serves everything in your 'frontend' folder at the root URL (/)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")