from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI()

with open("prompts/system_prompt.txt", "r") as file:
    SYSTEM_PROMPT = file.read()


class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=SYSTEM_PROMPT + data.message
        )
        return {"reply": response.text}
    except genai_errors.ServerError as e:
        if e.status_code == 503:
            return JSONResponse(status_code=503, content={"reply": "The AI is currently busy due to high demand. Please try again in a moment."})
        return JSONResponse(status_code=500, content={"reply": "AI service error. Please try again."})
    except Exception:
        return JSONResponse(status_code=500, content={"reply": "Something went wrong. Please try again."})
