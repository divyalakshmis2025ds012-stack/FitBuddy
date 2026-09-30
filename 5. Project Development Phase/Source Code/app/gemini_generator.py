"""
gemini_generator.py
Generates the structured 7-day workout plan using Gemini 1.5 Pro.
"""

import os
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")


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
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
