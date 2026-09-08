"""
prompts.py
-----------
Builds the three different prompt styles (Zero-Shot, Few-Shot, Structured
Reasoning) that are sent to the Gemini API for the AI Travel Planner.

Each function takes the traveler's details and returns a single prompt
string ready to be sent to the model.
"""


def _traveler_block(name, destination, days, budget, interests, travel_style):
    """Small helper so we don't repeat the same formatting 3 times."""
    interests_str = ", ".join(interests) if isinstance(interests, list) else interests
    return (
        f"- Name: {name}\n"
        f"- Destination: {destination}\n"
        f"- Number of Days: {days}\n"
        f"- Budget: ${budget}\n"
        f"- Interests: {interests_str}\n"
        f"- Travel Style: {travel_style}\n"
    )


# ---------------------------------------------------------------------------
# PART 1: ZERO-SHOT PROMPTING
# ---------------------------------------------------------------------------
def build_zero_shot_prompt(name, destination, days, budget, interests, travel_style):
    """
    No examples are given. We simply describe the task and hand over the
    traveler's info, and let Gemini figure out the itinerary on its own.
    """
    traveler = _traveler_block(name, destination, days, budget, interests, travel_style)

    prompt = f"""You are an AI travel planning assistant.

A traveler has given you the following details:
{traveler}

Based only on this information, please:
1. Analyze the traveler's preferences.
2. Suggest suitable places to visit in {destination}.
3. Create a day-by-day itinerary for {days} day(s).
4. Recommend activities that fit within the ${budget} budget.

Format your answer with a short summary, then a clear "Day 1", "Day 2", etc.
breakdown, each with morning/afternoon/evening activities and an
approximate cost where relevant.
"""
    return prompt


# ---------------------------------------------------------------------------
# PART 2: FEW-SHOT PROMPTING
# ---------------------------------------------------------------------------
def build_few_shot_prompt(name, destination, days, budget, interests, travel_style):
    """
    We show Gemini 2-3 example travelers with sample itineraries first,
    so it learns the pattern/format we want, then we ask it to generate
    a plan for the new traveler in the same style.
    """
    traveler = _traveler_block(name, destination, days, budget, interests, travel_style)

    examples = """Here are examples of previous travelers and the itineraries that were created for them:

Example 1:
Traveler: Sara, Destination: Paris, Days: 3, Budget: $600, Interests: Art, Food, Travel Style: Solo
Itinerary:
Day 1: Visit the Louvre Museum (art), lunch at a local bistro, evening walk along the Seine.
Day 2: Musee d'Orsay in the morning, food market tour in the afternoon, cooking class in the evening.
Day 3: Montmartre and Sacre-Coeur, café hopping, farewell dinner at a budget-friendly bistro.
Total estimated cost: ~$580, staying within the $600 budget.

Example 2:
Traveler: Ahmed, Destination: Istanbul, Days: 2, Budget: $300, Interests: History, Shopping, Travel Style: Friends
Itinerary:
Day 1: Hagia Sophia and Topkapi Palace (history), lunch near Sultanahmet, Grand Bazaar shopping in the evening.
Day 2: Bosphorus ferry ride, Spice Bazaar, casual dinner with friends at a rooftop restaurant.
Total estimated cost: ~$280, staying within the $300 budget.

Example 3:
Traveler: The Khan Family, Destination: Bali, Days: 3, Budget: $700, Interests: Nature, Beaches, Travel Style: Family
Itinerary:
Day 1: Kuta Beach relaxation, family-friendly seafood lunch, sunset at Tanah Lot.
Day 2: Ubud rice terraces and monkey forest, local lunch, evening cultural dance show.
Day 3: Water sports at Nusa Dua (budget-friendly options), souvenir shopping, farewell dinner.
Total estimated cost: ~$670, staying within the $700 budget.
"""

    prompt = f"""You are an AI travel planning assistant.

{examples}

Now generate a personalized travel plan in the SAME style and format as the
examples above, for this new traveler:
{traveler}

Your itinerary should:
1. Suggest suitable places to visit in {destination}.
2. Give a day-by-day breakdown for {days} day(s).
3. Recommend activities that fit the ${budget} budget.
4. End with a total estimated cost line, like the examples.
"""
    return prompt


# ---------------------------------------------------------------------------
# PART 3: STRUCTURED REASONING PROMPTING
# ---------------------------------------------------------------------------
def build_structured_reasoning_prompt(name, destination, days, budget, interests, travel_style):
    """
    We explicitly ask Gemini to work through a set of steps, but we tell it
    NOT to reveal its internal step-by-step reasoning — only to give brief
    justifications for each recommendation in the final itinerary.
    """
    traveler = _traveler_block(name, destination, days, budget, interests, travel_style)

    prompt = f"""You are an AI travel planning assistant that plans carefully before answering.

Traveler details:
{traveler}

Work through the planning using the following steps, but do NOT show your
internal step-by-step reasoning or thought process in the answer. Only use
these steps to guide your thinking:
1. Analyze the traveler's preferences.
2. Consider the available budget of ${budget}.
3. Consider the number of travel days ({days}).
4. Select suitable attractions and activities in {destination} that match
   the interests and travel style.
5. Create a day-by-day itinerary.
6. For each recommendation, note a brief (one sentence) justification for
   why it was chosen.

Now output ONLY the final result in this format:
- A short 2-3 sentence summary of the overall plan.
- "Day 1", "Day 2", ... sections with activities and a short justification
  next to each activity (e.g. "Visit X — chosen because it matches your
  interest in Food and fits the budget").
- A final estimated total cost line.

Do not include any headings like "Step 1" or "Reasoning" — only the final
itinerary with brief justifications.
"""
    return prompt


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------
PROMPT_BUILDERS = {
    "zero_shot": build_zero_shot_prompt,
    "few_shot": build_few_shot_prompt,
    "structured_reasoning": build_structured_reasoning_prompt,
}


def build_prompt(technique, name, destination, days, budget, interests, travel_style):
    if technique not in PROMPT_BUILDERS:
        raise ValueError(f"Unknown technique: {technique}")
    return PROMPT_BUILDERS[technique](name, destination, days, budget, interests, travel_style)
