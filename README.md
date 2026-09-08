# AI Travel Planner — Gemini Prompting Techniques

A Python (FastAPI) + Gemini API application that generates a personalized
travel itinerary while comparing three prompting techniques:

1. **Zero-Shot Prompting**
2. **Few-Shot Prompting**
3. **Structured Reasoning Prompting**

## Project structure

```
ai-travel-planner/
├── main.py              # FastAPI app + Gemini API calls
├── prompts.py            # Builds the 3 different prompt styles
├── requirements.txt
├── .env.example           # Copy to .env and add your Gemini API key
├── templates/
│   └── index.html         # Web UI (form + results)
└── static/
    ├── style.css
    └── app.js
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get a free Gemini API key from https://aistudio.google.com/app/apikey

3. Copy `.env.example` to `.env` and paste in your key:
   ```
   GEMINI_API_KEY=your_real_key_here
   ```

4. Run the app:
   ```bash
   uvicorn main:app --reload
   ```

5. Open your browser at: http://127.0.0.1:8000

> If no API key is set, the app still runs and shows you the exact prompt
> that would have been sent to Gemini, so you can test the UI without a key.

## How it works

### Part 1 — Zero-Shot Prompting (`prompts.py → build_zero_shot_prompt`)
Sends the traveler's details straight to Gemini with no examples, and asks
it to analyze preferences, suggest places, build a day-by-day itinerary,
and recommend activities within budget.

### Part 2 — Few-Shot Prompting (`prompts.py → build_few_shot_prompt`)
Includes 3 example travelers (different destinations, budgets, interests,
and travel styles) with sample itineraries, then asks Gemini to generate
a new plan in the same style/format for the current traveler.

### Part 3 — Structured Reasoning Prompting (`prompts.py → build_structured_reasoning_prompt`)
Instructs Gemini to work through 6 steps (analyze preferences → consider
budget → consider days → select attractions → build itinerary → justify
choices), but explicitly tells it **not** to reveal its internal reasoning
— only to output the final itinerary with a short one-line justification
next to each recommendation.

### App requirements
- The web form collects: Name, Destination, Number of Days, Budget,
  Interests (multi-select chips), and Travel Style.
- The user picks one of the 3 techniques (or clicks "Compare All 3" to
  run all three at once and see them side-by-side).
- `main.py` exposes:
  - `POST /generate` — runs one selected technique
  - `POST /generate-all` — runs all three techniques for comparison
- The generated itinerary from Gemini is displayed in the browser.

## Example input (from the assignment)

- Name: Alex
- Destination: Dubai
- Days: 4
- Budget: $800
- Interests: Food, Beaches, Shopping
- Travel Style: Family

## Notes for the report / submission

- Because Gemini's output can vary between the three techniques even for
  the same input, it's a good idea to run all three (using "Compare All 3")
  and take screenshots for your assignment report showing how the
  itineraries differ in structure, specificity, and reasoning depth.
- Zero-shot answers tend to be more generic since the model has no example
  to follow.
- Few-shot answers usually match the format/tone of the given examples
  more closely.
- Structured reasoning answers tend to include clearer justifications for
  each choice, since the model is guided through explicit steps.
