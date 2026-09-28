"""
gemini_generator.py
Generates the structured 7-day workout plan using Gemini 1.5 Pro.
"""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)
MODEL_NAME= "gemini-3.6-flash"

def generate_workout_gemini(user_input: dict) -> str:
    """
    user_input: {"goal": str, "intensity": str}
    Returns the model's raw text response (markdown-ish, day-by-day plan).
    """
    prompt = f"""
You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for someone with the goal of **{user_input['goal']}**,
and prefers **{user_input['intensity']} intensity** workouts.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)
"""
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
