import os
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

from google import genai

from prompts import build_prompt


# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")


# Create Gemini client
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None


# FastAPI app
app = FastAPI(
    title="AI Travel Planner - Gemini Prompting Techniques"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# Templates
templates = Jinja2Templates(
    directory="templates"
)


# Request model
class TravelRequest(BaseModel):
    name: str
    destination: str
    days: int
    budget: float
    interests: List[str]
    travel_style: str
    technique: str


# Gemini function
def call_gemini(prompt: str) -> str:

    if not GEMINI_API_KEY or client is None:
        return (
            "[No GEMINI_API_KEY found]\n\n"
            "Please set your Gemini API key in the .env file.\n\n"
            "Prompt that would have been sent:\n\n"
            + prompt
        )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text

    except Exception as exc:
        return f"Error calling Gemini API: {exc}"


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# Generate itinerary
@app.post("/generate")
async def generate_itinerary(payload: TravelRequest):

    prompt = build_prompt(
        payload.technique,
        payload.name,
        payload.destination,
        payload.days,
        payload.budget,
        payload.interests,
        payload.travel_style,
    )

    result_text = call_gemini(prompt)

    return JSONResponse(
        {
            "technique": payload.technique,
            "prompt_used": prompt,
            "itinerary": result_text,
        }
    )


# Generate all techniques
@app.post("/generate-all")
async def generate_all(payload: TravelRequest):

    results = {}

    techniques = [
        "zero_shot",
        "few_shot",
        "structured_reasoning"
    ]

    for technique in techniques:

        prompt = build_prompt(
            technique,
            payload.name,
            payload.destination,
            payload.days,
            payload.budget,
            payload.interests,
            payload.travel_style,
        )

        results[technique] = call_gemini(prompt)

    return JSONResponse(
        {
            "results": results
        }
    )


# Run application
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )